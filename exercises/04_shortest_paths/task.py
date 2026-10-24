"""Unit 4: Shortest paths with Dijkstra (and Bellman-Ford) - YOUR SOLUTION.

Read README.md in this folder first. Replace every
``raise NotImplementedError(...)`` by your own code.

Run the tests from the project root with::

    python -m pytest exercises/04_shortest_paths
"""

import heapq  # you will need heapq.heappush and heapq.heappop in dijkstra()
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))  # find ``lib``

from lib.generators import small_weighted_graph
from lib.graph import Graph, Vertex
from lib.utils import format_path


def dijkstra(graph: Graph, start: Vertex) -> tuple[dict[Vertex, float], dict[Vertex, Vertex | None]]:
    """Compute shortest paths from ``start`` with Dijkstra's algorithm.

    Works for directed and undirected graphs with non-negative weights.

    Returns:
        A pair ``(dist, parent)``:

        * ``dist[v]`` - length (sum of weights) of a shortest path from
          ``start`` to ``v``,
        * ``parent[v]`` - the vertex before ``v`` on such a path
          (``None`` for ``start``).

        Both dictionaries contain exactly the vertices reachable from
        ``start``.

    Raises:
        KeyError: If ``start`` is not a vertex of the graph.
        ValueError: If ANY edge of the graph has a negative weight (checked
            before the search starts, even for unreachable edges).
    """
    # TODO: Step 1 - raise KeyError if start is not in the graph.
    # TODO: Step 2 - raise ValueError if some edge has a negative weight.
    # TODO: Step 3 - dist = {start: 0}, parent = {start: None},
    #                heap = [(0, start)], finished = set().
    # TODO: Step 4 - while the heap is not empty: pop the smallest (d, u);
    #                skip u if it is already finished (lazy deletion);
    #                otherwise mark u as finished and relax every edge u -> v:
    #                if v is new or d + weight < dist[v], update dist[v] and
    #                parent[v] and push (dist[v], v).
    raise NotImplementedError("TODO: dijkstra")


def reconstruct_path(parent: dict[Vertex, Vertex | None], target: Vertex) -> list[Vertex] | None:
    """Return the path ``[start, ..., target]`` encoded by ``parent``.

    ``parent`` is the second result of :func:`dijkstra` (or of a BFS): the
    start vertex has the parent ``None``.

    Returns:
        The list of vertices from the start to ``target``, or ``None`` if
        ``target`` is not a key of ``parent`` (i.e. it was not reached).
    """
    # TODO: Step 1 - return None if target is not in parent.
    # TODO: Step 2 - follow the parents from target until you reach None.
    # TODO: Step 3 - reverse the collected list.
    raise NotImplementedError("TODO: reconstruct_path")


def shortest_route(graph: Graph, start: Vertex, target: Vertex) -> tuple[list[Vertex], float] | None:
    """Return a shortest path from ``start`` to ``target`` and its length.

    Returns:
        ``(path, length)`` with ``path = [start, ..., target]``, or ``None``
        if ``target`` cannot be reached from ``start``.

    Raises:
        KeyError: If ``start`` or ``target`` is not a vertex of the graph.
        ValueError: If some edge has a negative weight (as in dijkstra()).
    """
    # TODO: Check target, then combine dijkstra() and reconstruct_path().
    raise NotImplementedError("TODO: shortest_route")


def bellman_ford(graph: Graph, start: Vertex) -> tuple[dict[Vertex, float], dict[Vertex, Vertex | None]]:
    """OPTIONAL: Shortest paths with the Bellman-Ford algorithm.

    Same result format as :func:`dijkstra`, but negative weights are
    allowed in directed graphs.

    Raises:
        KeyError: If ``start`` is not a vertex of the graph.
        ValueError: If a negative cycle is reachable from ``start``, or if
            the graph is undirected and has an edge with negative weight
            (u - v - u is then already a negative closed walk).
    """
    # TODO (optional): |V| - 1 rounds of relaxing every edge, then one more
    #                  check round to detect negative cycles.
    raise NotImplementedError("TODO (optional): bellman_ford")


if __name__ == "__main__":
    graph = small_weighted_graph()
    dist, parent = dijkstra(graph, "Katthult")
    print("dist:  ", dist)
    print("parent:", parent)
    print("Path to Markt:", format_path(reconstruct_path(parent, "Markt"), directed=False))
    print("Katthult -> Backhorva:", shortest_route(graph, "Katthult", "Backhorva"))
