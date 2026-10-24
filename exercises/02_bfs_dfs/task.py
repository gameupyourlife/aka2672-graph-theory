"""Unit 2: Breadth-first search and depth-first search - YOUR SOLUTION.

Read README.md in this folder first. Replace every
``raise NotImplementedError(...)`` by your own code.

Run the tests from the project root with::

    python -m pytest exercises/02_bfs_dfs
"""

import sys
from collections import deque  # you will need deque in bfs()
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))  # find ``lib``

from lib.graph import Graph, Vertex
from lib.utils import format_path


def bfs(graph: Graph, start: Vertex) -> tuple[dict[Vertex, int], dict[Vertex, Vertex | None]]:
    """Run a breadth-first search from ``start``.

    Returns:
        A pair ``(distance, parent)``:

        * ``distance[v]`` - number of edges on a shortest path from
          ``start`` to ``v``,
        * ``parent[v]`` - the vertex from which ``v`` was discovered
          (``None`` for ``start``).

        Both dictionaries contain exactly the vertices reachable from
        ``start``.

    Raises:
        KeyError: If ``start`` is not a vertex of the graph.
    """
    # TODO: Step 1 - check that start is in the graph (raise KeyError otherwise).
    # TODO: Step 2 - initialise distance, parent and a deque containing start.
    # TODO: Step 3 - while the queue is not empty: take the first vertex u,
    #                look at all neighbours w; if w was not discovered yet,
    #                set distance[w], parent[w] and append w to the queue.
    raise NotImplementedError("TODO: bfs")


def shortest_path(graph: Graph, start: Vertex, target: Vertex) -> list[Vertex] | None:
    """Return a shortest path ``[start, ..., target]`` (fewest edges).

    Returns ``None`` if ``target`` cannot be reached from ``start``.

    Raises:
        KeyError: If ``start`` or ``target`` is not a vertex of the graph.
    """
    # TODO: Use bfs() and follow the parent pointers backwards from target.
    raise NotImplementedError("TODO: shortest_path")


def dfs(graph: Graph, start: Vertex) -> list[Vertex]:
    """Run an iterative depth-first search from ``start`` using a stack.

    Returns:
        All vertices reachable from ``start`` in the order in which they
        are visited (``start`` first, every vertex exactly once).

    Raises:
        KeyError: If ``start`` is not a vertex of the graph.
    """
    # TODO: Step 1 - check start, create an empty set "visited", a list
    #                "order" and a stack (a list) containing start.
    # TODO: Step 2 - while the stack is not empty: pop a vertex; skip it if
    #                already visited; otherwise mark it, append it to order
    #                and push all its neighbours that are not yet visited.
    raise NotImplementedError("TODO: dfs")


def connected_components(graph: Graph) -> list[set[Vertex]]:
    """Return the connected components of an undirected graph.

    Every vertex belongs to exactly one of the returned sets.

    Raises:
        ValueError: If the graph is directed.
    """
    # TODO: For every vertex that is not yet in a component, start a search
    #       (bfs or dfs) and store everything it finds as a new component.
    raise NotImplementedError("TODO: connected_components")


def is_connected(graph: Graph) -> bool:
    """Return ``True`` if the undirected graph is connected.

    The empty graph counts as connected.

    Raises:
        ValueError: If the graph is directed.
    """
    # TODO
    raise NotImplementedError("TODO: is_connected")


def dfs_recursive(graph: Graph, start: Vertex) -> list[Vertex]:
    """OPTIONAL: Depth-first search written as a recursive function.

    Same result format as :func:`dfs`.
    """
    # TODO (optional): define an inner function visit(v) that calls itself.
    raise NotImplementedError("TODO (optional): dfs_recursive")


def bfs_layers(graph: Graph, start: Vertex) -> list[list[Vertex]]:
    """OPTIONAL: Return the BFS layers ``[[start], [distance 1], [distance 2], ...]``."""
    # TODO (optional)
    raise NotImplementedError("TODO (optional): bfs_layers")


if __name__ == "__main__":
    example = Graph.from_edges([("A", "B"), ("A", "C"), ("B", "D"), ("C", "D"), ("D", "E")])
    example.add_vertex("Z")
    print("BFS:", bfs(example, "A"))
    print("Shortest path A -> E:", format_path(shortest_path(example, "A", "E")))
    print("DFS:", dfs(example, "A"))
    print("Components:", connected_components(example))
