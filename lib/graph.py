"""A small, easy-to-read graph class for the course.

The class stores a graph as an *adjacency list*: for every vertex we keep a
dictionary that maps each neighbour to the weight of the connecting edge::

    {
        "Bullerby":   {"Lonneberga": 1, "Sevedstorp": 1},
        "Lonneberga": {"Bullerby": 1},
        "Sevedstorp": {"Bullerby": 1},
    }

Design decisions (important for all exercises):

* **Every edge has a weight.** Unweighted graphs simply use the default
  weight ``1``. Therefore the methods return the same data types for weighted
  and unweighted graphs - there are no surprises.
* **Simple graphs only.** Loops (edges ``v -> v``) and parallel edges are not
  allowed. In a directed graph ``u -> v`` and ``v -> u`` are two different
  edges and may both exist.
* **Vertices can be any hashable value**, e.g. strings, numbers or tuples.
* **Deterministic order.** ``vertices()``, ``neighbors()`` and ``edges()``
  return their elements in insertion order. This makes outputs reproducible.
* Accessing a vertex that does not exist raises a ``KeyError``.
* **Attributes.** Vertices and edges can carry additional data in a
  dictionary, e.g. a position for drawings or a display name::

      graph.add_vertex("Katthult", pos=(0, 1), label="Hof Katthult")
      graph.vertex_attributes("Katthult")["pos"]   # (0, 1)

  Attributes describe the *problem* (positions, names, ...). The *state of an
  algorithm* (visited, current, ...) belongs into a ``lib.trace.Trace``, so
  that algorithms never have to change their input graph.

The class deliberately contains **no** graph algorithms (no BFS, DFS,
Dijkstra, ...). These are implemented by you in the exercises.
"""

from __future__ import annotations

import math
from collections.abc import Hashable, Iterable, Iterator
from typing import Any, NamedTuple

Vertex = Hashable
"""Type alias for vertices: any hashable value (str, int, tuple, ...)."""


class Edge(NamedTuple):
    """An edge ``u -- v`` (or ``u -> v`` in a directed graph) with a weight.

    ``Edge`` is a named tuple, so you can unpack it::

        for u, v, weight in graph.edges():
            ...

    or access the fields by name: ``edge.u``, ``edge.v``, ``edge.weight``.
    """

    u: Vertex
    v: Vertex
    weight: float = 1


class Graph:
    """A directed or undirected graph stored as an adjacency list.

    Example::

        >>> graph = Graph(directed=False)
        >>> graph.add_edge("Bullerby", "Lonneberga")
        >>> graph.add_edge("Bullerby", "Sevedstorp", weight=4)
        >>> graph.neighbors("Bullerby")
        ['Lonneberga', 'Sevedstorp']
        >>> graph.degree("Bullerby")
        2
    """

    def __init__(
        self,
        directed: bool = False,
        *,
        vertices: Iterable[Vertex] | None = None,
        edges: Iterable[tuple[Vertex, Vertex] | tuple[Vertex, Vertex, float]] | None = None,
    ) -> None:
        """Create a graph with optional initial vertices and edges.

        Args:
            directed: ``True`` for a directed graph (edges have a direction),
                ``False`` (default) for an undirected graph.
            vertices: Vertices to insert before adding edges, including any
                isolated vertices.
            edges: Pairs ``(u, v)`` or triples ``(u, v, weight)``. Missing
                end vertices are added automatically.
        """
        self._directed = directed
        # _succ[u][v] = weight of the edge u -> v (or u -- v).
        self._succ: dict[Vertex, dict[Vertex, float]] = {}
        # _pred[v][u] = weight of the edge u -> v. For undirected graphs we
        # simply reuse the same dictionary, because there is no direction.
        self._pred: dict[Vertex, dict[Vertex, float]] = (
            {} if directed else self._succ
        )
        # Optional data of vertices and edges (see vertex_attributes()).
        # For an undirected edge the same dictionary is stored under
        # (u, v) and (v, u).
        self._vertex_attrs: dict[Vertex, dict[str, Any]] = {}
        self._edge_attrs: dict[tuple[Vertex, Vertex], dict[str, Any]] = {}
        if vertices is not None:
            self.add_vertices(vertices)
        if edges is not None:
            self.add_edges(edges)

    # ------------------------------------------------------------------
    # Construction
    # ------------------------------------------------------------------
    @classmethod
    def from_edges(
        cls,
        edges: Iterable[tuple[Vertex, Vertex] | tuple[Vertex, Vertex, float]],
        directed: bool = False,
        vertices: Iterable[Vertex] = (),
    ) -> Graph:
        """Create a graph from a list of edges.

        Args:
            edges: Pairs ``(u, v)`` or triples ``(u, v, weight)``.
            directed: Whether the new graph is directed.
            vertices: Additional (e.g. isolated) vertices.

        Returns:
            The new graph.

        Example::

            Graph.from_edges([("A", "B", 3), ("B", "C", 1)])
        """
        graph = cls(directed=directed)
        graph.add_vertices(vertices)
        graph.add_edges(edges)
        return graph

    @property
    def directed(self) -> bool:
        """``True`` if the graph is directed, otherwise ``False``."""
        return self._directed

    def add_vertex(self, v: Vertex, **attributes: Any) -> None:
        """Add the vertex ``v``.

        Adding an existing vertex does not change its edges; given
        attributes are added to (or overwrite) its existing attributes.

        Example::

            graph.add_vertex("Katthult", pos=(0, 1))
        """
        if v not in self._succ:
            self._succ[v] = {}
            self._vertex_attrs[v] = {}
            if self._directed:
                self._pred[v] = {}
        self._vertex_attrs[v].update(attributes)

    def add_vertices(self, vertices: Iterable[Vertex]) -> None:
        """Add several vertices at once."""
        for v in vertices:
            self.add_vertex(v)

    def add_edge(self, u: Vertex, v: Vertex, weight: float = 1, **attributes: Any) -> None:
        """Add the edge ``u -- v`` (undirected) or ``u -> v`` (directed).

        Missing end vertices are added automatically.

        Args:
            u: First end vertex (tail of a directed edge).
            v: Second end vertex (head of a directed edge).
            weight: Weight of the edge (length, cost, capacity, ...).
                Defaults to ``1`` for unweighted graphs.
            **attributes: Optional data of the edge, e.g. ``label="B1"``
                (see :meth:`edge_attributes`).

        Raises:
            ValueError: If ``u == v`` (loops are not allowed), if the edge
                already exists, or if the weight is not a finite number.
        """
        if u == v:
            raise ValueError(f"Loops are not allowed: {u!r} -- {v!r}")
        _check_weight(weight)
        if self.has_edge(u, v):
            raise ValueError(f"The edge {u!r} -- {v!r} already exists")
        self.add_vertex(u)
        self.add_vertex(v)
        self._succ[u][v] = weight
        self._pred[v][u] = weight
        data = dict(attributes)
        self._edge_attrs[(u, v)] = data
        if not self._directed:
            self._edge_attrs[(v, u)] = data  # one shared dictionary

    def add_edges(
        self,
        edges: Iterable[tuple[Vertex, Vertex] | tuple[Vertex, Vertex, float]],
    ) -> None:
        """Add several edges given as pairs ``(u, v)`` or triples ``(u, v, w)``."""
        for edge in edges:
            if len(edge) == 2:
                u, v = edge
                self.add_edge(u, v)
            elif len(edge) == 3:
                u, v, weight = edge
                self.add_edge(u, v, weight)
            else:
                raise ValueError(f"An edge needs 2 or 3 entries, got {edge!r}")

    def set_weight(self, u: Vertex, v: Vertex, weight: float) -> None:
        """Change the weight of the existing edge ``u -- v`` / ``u -> v``.

        Raises:
            KeyError: If the edge does not exist.
            ValueError: If the weight is not a finite number.
        """
        if not self.has_edge(u, v):
            raise KeyError(f"Edge {u!r} -- {v!r} does not exist")
        _check_weight(weight)
        self._succ[u][v] = weight
        self._pred[v][u] = weight

    def remove_edge(self, u: Vertex, v: Vertex) -> None:
        """Remove the edge ``u -- v`` / ``u -> v``.

        Raises:
            KeyError: If the edge does not exist.
        """
        if not self.has_edge(u, v):
            raise KeyError(f"Edge {u!r} -- {v!r} does not exist")
        del self._succ[u][v]
        del self._pred[v][u]
        del self._edge_attrs[(u, v)]
        if not self._directed:
            del self._edge_attrs[(v, u)]

    def remove_vertex(self, v: Vertex) -> None:
        """Remove the vertex ``v`` together with all incident edges.

        Raises:
            KeyError: If the vertex does not exist.
        """
        self._require_vertex(v)
        for w in list(self._succ[v]):
            self.remove_edge(v, w)
        for w in list(self._pred[v]):
            self.remove_edge(w, v)
        del self._succ[v]
        del self._vertex_attrs[v]
        if self._directed:
            del self._pred[v]

    # ------------------------------------------------------------------
    # Queries
    # ------------------------------------------------------------------
    def has_vertex(self, v: Vertex) -> bool:
        """Return ``True`` if ``v`` is a vertex of the graph."""
        return v in self._succ

    def has_edge(self, u: Vertex, v: Vertex) -> bool:
        """Return ``True`` if the edge ``u -- v`` / ``u -> v`` exists."""
        return u in self._succ and v in self._succ[u]

    def weight(self, u: Vertex, v: Vertex) -> float:
        """Return the weight of the edge ``u -- v`` / ``u -> v``.

        Raises:
            KeyError: If the edge does not exist.
        """
        if not self.has_edge(u, v):
            raise KeyError(f"Edge {u!r} -- {v!r} does not exist")
        return self._succ[u][v]

    def vertex_attributes(self, v: Vertex) -> dict[str, Any]:
        """Return the attribute dictionary of the vertex ``v``.

        The dictionary belongs to the graph: changes are stored directly::

            graph.vertex_attributes("A")["pos"] = (0, 0)

        Raises:
            KeyError: If ``v`` is not a vertex of the graph.
        """
        self._require_vertex(v)
        return self._vertex_attrs[v]

    def edge_attributes(self, u: Vertex, v: Vertex) -> dict[str, Any]:
        """Return the attribute dictionary of the edge ``u -- v`` / ``u -> v``.

        For an undirected edge, ``edge_attributes(u, v)`` and
        ``edge_attributes(v, u)`` are the same dictionary.

        Raises:
            KeyError: If the edge does not exist.
        """
        if not self.has_edge(u, v):
            raise KeyError(f"Edge {u!r} -- {v!r} does not exist")
        return self._edge_attrs[(u, v)]

    def vertices(self) -> list[Vertex]:
        """Return a list of all vertices (in insertion order)."""
        return list(self._succ)

    def edges(self) -> list[Edge]:
        """Return a list of all edges as ``Edge(u, v, weight)``.

        In an undirected graph every edge appears exactly **once**.
        """
        result: list[Edge] = []
        seen: set[Vertex] = set()
        for u, neighbours in self._succ.items():
            for v, weight in neighbours.items():
                # Undirected: the edge u -- v was already listed as v -- u
                # if we have visited v before.
                if not self._directed and v in seen:
                    continue
                result.append(Edge(u, v, weight))
            seen.add(u)
        return result

    def neighbors(self, v: Vertex) -> list[Vertex]:
        """Return the neighbours of ``v`` (in insertion order).

        For a directed graph these are the *successors*, i.e. all ``w``
        with an edge ``v -> w``.

        Raises:
            KeyError: If ``v`` is not a vertex of the graph.
        """
        self._require_vertex(v)
        return list(self._succ[v])

    def predecessors(self, v: Vertex) -> list[Vertex]:
        """Return all ``u`` with an edge ``u -> v``.

        For an undirected graph this is the same as :meth:`neighbors`.

        Raises:
            KeyError: If ``v`` is not a vertex of the graph.
        """
        self._require_vertex(v)
        return list(self._pred[v])

    def degree(self, v: Vertex) -> int:
        """Return the degree of ``v``.

        Undirected graph: number of incident edges.
        Directed graph: in-degree + out-degree.

        Raises:
            KeyError: If ``v`` is not a vertex of the graph.
        """
        if self._directed:
            return self.in_degree(v) + self.out_degree(v)
        self._require_vertex(v)
        return len(self._succ[v])

    def out_degree(self, v: Vertex) -> int:
        """Return the number of edges leaving ``v`` (``v -> w``)."""
        self._require_vertex(v)
        return len(self._succ[v])

    def in_degree(self, v: Vertex) -> int:
        """Return the number of edges entering ``v`` (``u -> v``)."""
        self._require_vertex(v)
        return len(self._pred[v])

    def num_vertices(self) -> int:
        """Return the number of vertices ``|V|``."""
        return len(self._succ)

    def num_edges(self) -> int:
        """Return the number of edges ``|E|``."""
        total = sum(len(neighbours) for neighbours in self._succ.values())
        # In an undirected graph every edge is stored twice (u->v, v->u).
        return total if self._directed else total // 2

    # ------------------------------------------------------------------
    # Copying and checking
    # ------------------------------------------------------------------
    def copy(self) -> Graph:
        """Return an independent copy of the graph (including attributes).

        Changes to the copy do not affect the original and vice versa.
        (Attribute *values* such as lists are not copied themselves.)
        """
        new = Graph(directed=self._directed)
        for v in self.vertices():
            new.add_vertex(v, **self._vertex_attrs[v])
        for u, v, weight in self.edges():
            new.add_edge(u, v, weight, **self._edge_attrs[(u, v)])
        return new

    def check_consistency(self) -> None:
        """Check the internal data structure for contradictions.

        This is mainly useful if you have modified the graph in unusual ways.
        The following properties are checked:

        * every neighbour is itself a vertex of the graph,
        * there are no loops,
        * all weights are finite numbers,
        * undirected: ``u -- v`` is stored in both directions with the same
          weight; directed: successor and predecessor lists match,
        * every vertex and every edge has exactly one attribute dictionary.

        Raises:
            ValueError: With a description of the first problem found.
        """
        for u, neighbours in self._succ.items():
            for v, weight in neighbours.items():
                if v not in self._succ:
                    raise ValueError(f"Neighbour {v!r} of {u!r} is not a vertex")
                if u == v:
                    raise ValueError(f"Loop at vertex {u!r}")
                _check_weight(weight)
                if self._pred[v].get(u) != weight:
                    raise ValueError(
                        f"Edge {u!r} -- {v!r} is not stored consistently"
                    )
        if set(self._vertex_attrs) != set(self._succ):
            raise ValueError("Vertex attributes do not match the vertices")
        stored_pairs = {(u, v) for u, neighbours in self._succ.items() for v in neighbours}
        if set(self._edge_attrs) != stored_pairs:
            raise ValueError("Edge attributes do not match the edges")
        if self._directed:
            if set(self._pred) != set(self._succ):
                raise ValueError("Successor and predecessor lists differ")
            for v, predecessors in self._pred.items():
                for u, weight in predecessors.items():
                    if self._succ.get(u, {}).get(v) != weight:
                        raise ValueError(
                            f"Predecessor entry {u!r} -> {v!r} has no edge"
                        )

    # ------------------------------------------------------------------
    # Python conveniences
    # ------------------------------------------------------------------
    def __contains__(self, v: object) -> bool:
        """Allow ``v in graph``."""
        return v in self._succ

    def __iter__(self) -> Iterator[Vertex]:
        """Allow ``for v in graph``: iterates over the vertices."""
        return iter(list(self._succ))

    def __len__(self) -> int:
        """Allow ``len(graph)``: number of vertices."""
        return len(self._succ)

    def __eq__(self, other: object) -> bool:
        """Two graphs are equal if they have the same vertices and edges.

        Attributes are not compared.
        """
        if not isinstance(other, Graph):
            return NotImplemented
        return self._directed == other._directed and self._succ == other._succ

    def __repr__(self) -> str:
        kind = "directed" if self._directed else "undirected"
        return (
            f"Graph({kind}, {self.num_vertices()} vertices, "
            f"{self.num_edges()} edges)"
        )

    def _require_vertex(self, v: Vertex) -> None:
        if v not in self._succ:
            raise KeyError(f"Vertex {v!r} is not in the graph")


def _check_weight(weight: object) -> None:
    """Raise ``ValueError`` if ``weight`` is not a finite real number."""
    if isinstance(weight, bool) or not isinstance(weight, (int, float)):
        raise ValueError(f"Weight must be a number, got {weight!r}")
    if not math.isfinite(weight):
        raise ValueError(f"Weight must be finite, got {weight!r}")
