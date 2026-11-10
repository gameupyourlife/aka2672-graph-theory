"""Unit 3 - Spanning trees and Kruskal's algorithm.

Follow the TODOs in each function. Replace each
``raise NotImplementedError(...)`` with your implementation.

Run the tests from the project root.

    python -m pytest exercises/03_spanning_trees
"""

import sys
from collections.abc import Iterable
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))  # find ``lib``

from lib.generators import small_weighted_graph
from lib.graph import Edge, Graph, Vertex


class UnionFind:
    """A partition of elements into disjoint sets ("disjoint-set forest").

    Every set is stored as a small internal tree: ``parent[x]`` is the
    parent of ``x``, and the root of a tree (``parent[root] == root``) is
    the *representative* of its set.

    Example::

        uf = UnionFind(["A", "B", "C"])
        uf.union("A", "B")      # True  - {A, B}, {C}
        uf.connected("A", "B")  # True
        uf.connected("A", "C")  # False
    """

    def __init__(self, elements: Iterable[Vertex] = ()) -> None:
        """Create one singleton set ``{x}`` for every ``x`` in ``elements``."""
        # TODO: Step 1 - create the dictionary self.parent (element -> parent).
        # TODO: Step 2 - call self.add(x) for every element.
        # TODO (later): for union by size, also create self.size (root -> size).
        raise NotImplementedError("TODO: UnionFind.__init__")

    def add(self, x: Vertex) -> None:
        """Add ``x`` as a new singleton set.

        If ``x`` is already present, nothing happens (it stays in its set).
        """
        # TODO: If x is new, make it its own parent (it is a root).
        raise NotImplementedError("TODO: UnionFind.add")

    def find(self, x: Vertex) -> Vertex:
        """Return the representative (root) of the set containing ``x``.

        Two elements are in the same set exactly if ``find`` returns the same
        representative for both.

        Raises:
            KeyError: If ``x`` was never added.
        """
        # TODO: Step 1 - raise KeyError if x is unknown.
        # TODO: Step 2 - follow the parent pointers until you reach a root.
        # TODO (later): path compression - let every vertex on the way point
        #               directly to the root.
        raise NotImplementedError("TODO: UnionFind.find")

    def union(self, x: Vertex, y: Vertex) -> bool:
        """Merge the sets containing ``x`` and ``y``.

        Returns:
            ``True`` if two different sets were merged, ``False`` if ``x``
            and ``y`` were already in the same set.

        Raises:
            KeyError: If ``x`` or ``y`` was never added.
        """
        # TODO: Step 1 - find both roots.
        # TODO: Step 2 - equal roots: return False.
        # TODO: Step 3 - otherwise hang one ROOT below the other, return True.
        # TODO (later): union by size - hang the smaller set below the larger.
        raise NotImplementedError("TODO: UnionFind.union")

    def connected(self, x: Vertex, y: Vertex) -> bool:
        """Return ``True`` if ``x`` and ``y`` are in the same set.

        Raises:
            KeyError: If ``x`` or ``y`` was never added.
        """
        # TODO: Compare the representatives.
        raise NotImplementedError("TODO: UnionFind.connected")


def kruskal(graph: Graph) -> list[Edge]:
    """Return a minimum spanning forest of an undirected weighted graph.

    For a connected graph this is a minimum spanning tree with
    ``|V| - 1`` edges; for a graph with ``c`` connected components it
    contains a minimum spanning tree of every component (``|V| - c``
    edges). The edges are ``Edge`` objects as returned by
    ``graph.edges()``; their order does not matter. Accept negative and
    fractional weights and leave the input graph unchanged. Use UnionFind
    for cycle checks. With path compression and union by size, aim for
    O(|V| + |E| log |E|) time.

    Raises:
        ValueError: If the graph is directed.
    """
    # TODO: Step 1 - raise ValueError for directed graphs.
    # TODO: Step 2 - create a UnionFind containing all vertices.
    # TODO: Step 3 - sort graph.edges() by weight (sorted(..., key=...)).
    # TODO: Step 4 - for every edge: if union(u, v) succeeds, keep the edge.
    raise NotImplementedError("TODO: kruskal")


def spanning_tree_weight(edges: Iterable[Edge]) -> float:
    """Return the total weight of the given edges (0 for no edges)."""
    # TODO: Add up edge.weight for all edges.
    raise NotImplementedError("TODO: spanning_tree_weight")


def prim(graph: Graph, start: Vertex) -> list[Edge]:
    """OPTIONAL: Return a minimum spanning tree of the component of ``start``.

    Prim's algorithm grows a single tree from ``start``: it always adds the
    lightest edge that joins a tree vertex ``u`` to a vertex ``v`` outside
    the tree, and returns these edges as ``Edge(u, v, weight)``.

    Raises:
        KeyError: If ``start`` is not a vertex of the graph.
        ValueError: If the graph is directed.
    """
    # TODO (optional): use heapq with (weight, unique_counter, u, v) so
    #                  equal weights do not require comparing vertex labels.
    raise NotImplementedError("TODO (optional): prim")


def count_components(graph: Graph) -> int:
    """OPTIONAL: Return the number of connected components, using only UnionFind.

    Raises:
        ValueError: If the graph is directed.
    """
    # TODO (optional): every successful union reduces the number of sets by 1.
    raise NotImplementedError("TODO (optional): count_components")


if __name__ == "__main__":
    uf = UnionFind(["Michel", "Ida", "Alfred", "Lina"])
    print("union(Michel, Ida):", uf.union("Michel", "Ida"))
    print("connected(Ida, Michel):", uf.connected("Ida", "Michel"))
    print("connected(Michel, Alfred):", uf.connected("Michel", "Alfred"))

    graph = small_weighted_graph()
    tree = kruskal(graph)
    for edge in tree:
        print(f"  {edge.u} - {edge.v} ({edge.weight})")
    print("Total weight:", spanning_tree_weight(tree))
