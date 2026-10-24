"""Unit 4: Shortest paths with Dijkstra (and Bellman-Ford) - DEMO SOLUTION.

Dijkstra's algorithm is a "weighted BFS": instead of a queue it uses a
priority queue and always continues with the unfinished vertex that is
closest to the start. With non-negative weights the distance of this vertex
cannot improve any more - it is final.

Runtime with a binary heap and lazy deletion: every edge is relaxed at most
once and creates at most one heap entry, so there are O(|V| + |E|) heap
operations of cost O(log |V|) each: O((|V| + |E|) log |V|).

Bellman-Ford (optional task) also handles negative weights, at the price of
O(|V| * |E|) time.
"""

import heapq
import itertools
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))  # find ``lib``

from lib.generators import small_weighted_graph
from lib.graph import Graph, Vertex
from lib.utils import format_path
from lib.visualization import can_draw, draw


def dijkstra(graph: Graph, start: Vertex) -> tuple[dict[Vertex, float], dict[Vertex, Vertex | None]]:
    """Compute shortest paths from ``start`` with Dijkstra's algorithm.

    Returns:
        ``(dist, parent)`` for all vertices reachable from ``start``.

    Raises:
        KeyError: If ``start`` is not a vertex of the graph.
        ValueError: If ANY edge of the graph has a negative weight.
    """
    if start not in graph:
        raise KeyError(f"Start vertex {start!r} is not in the graph")
    # The correctness proof needs non-negative weights (README, section 2).
    # We check *all* edges up front, so the result never depends on luck.
    for u, v, weight in graph.edges():
        if weight < 0:
            raise ValueError(
                f"Dijkstra needs non-negative weights, but {u!r} - {v!r} has weight {weight}"
            )

    dist: dict[Vertex, float] = {start: 0}  # best distances found so far
    parent: dict[Vertex, Vertex | None] = {start: None}
    finished: set[Vertex] = set()  # vertices whose distance is final
    # Heap entries are (distance, tie, vertex). The running number "tie"
    # decides between equal distances, so Python never has to compare two
    # vertices with each other (they might be of incomparable types).
    tie = itertools.count()
    heap: list[tuple[float, int, Vertex]] = [(0, next(tie), start)]

    while heap:
        d, _, u = heapq.heappop(heap)  # the closest unfinished vertex ...
        if u in finished:
            # ... unless this entry is outdated: u was pushed again with a
            # smaller distance and has been finished already (lazy deletion).
            continue
        finished.add(u)  # d == dist[u] is now final
        for v in graph.neighbors(u):
            new_distance = d + graph.weight(u, v)
            # Relaxation: is the way via u shorter than everything known?
            if v not in dist or new_distance < dist[v]:
                dist[v] = new_distance
                parent[v] = u
                heapq.heappush(heap, (new_distance, next(tie), v))
    return dist, parent


def reconstruct_path(parent: dict[Vertex, Vertex | None], target: Vertex) -> list[Vertex] | None:
    """Return the path ``[start, ..., target]`` encoded by ``parent`` (or ``None``)."""
    if target not in parent:
        return None  # target was never reached
    path = []
    v: Vertex | None = target
    while v is not None:  # parent[start] is None, so we stop after start
        path.append(v)
        v = parent[v]
    path.reverse()  # we walked from the target back to the start
    return path


def shortest_route(graph: Graph, start: Vertex, target: Vertex) -> tuple[list[Vertex], float] | None:
    """Return ``(path, length)`` of a shortest path, or ``None`` if unreachable.

    Raises:
        KeyError: If ``start`` or ``target`` is not a vertex of the graph.
        ValueError: If some edge has a negative weight.
    """
    if target not in graph:
        raise KeyError(f"Target vertex {target!r} is not in the graph")
    dist, parent = dijkstra(graph, start)
    path = reconstruct_path(parent, target)
    if path is None:
        return None
    return path, dist[target]


def bellman_ford(graph: Graph, start: Vertex) -> tuple[dict[Vertex, float], dict[Vertex, Vertex | None]]:
    """OPTIONAL: Shortest paths with the Bellman-Ford algorithm.

    Raises:
        KeyError: If ``start`` is not a vertex of the graph.
        ValueError: If a negative cycle is reachable from ``start``, or if the
            graph is undirected and has a negative edge.
    """
    if start not in graph:
        raise KeyError(f"Start vertex {start!r} is not in the graph")
    if not graph.directed:
        for u, v, weight in graph.edges():
            if weight < 0:
                # u -> v -> u is a closed walk of length 2 * weight < 0.
                raise ValueError(
                    f"Undirected edge {u!r} - {v!r} has negative weight {weight}: "
                    "walking it back and forth is a negative cycle"
                )

    # All edges as (u, v, weight); undirected edges in both directions.
    arcs = [(u, v, graph.weight(u, v)) for u in graph.vertices() for v in graph.neighbors(u)]

    dist: dict[Vertex, float] = {start: 0}
    parent: dict[Vertex, Vertex | None] = {start: None}

    def relax_all() -> bool:
        """Relax every edge once; return True if some distance improved."""
        changed = False
        for u, v, weight in arcs:
            if u in dist and (v not in dist or dist[u] + weight < dist[v]):
                dist[v] = dist[u] + weight
                parent[v] = u
                changed = True
        return changed

    # After round k, dist[v] is at most the length of a shortest path with
    # at most k edges. Without negative cycles, shortest paths have at most
    # |V| - 1 edges, so |V| - 1 rounds are enough.
    for _ in range(graph.num_vertices() - 1):
        if not relax_all():
            break  # nothing changed: nothing will ever change again
    else:
        # All |V| - 1 rounds changed something. If one more round still
        # improves a distance, there is a negative cycle reachable from start.
        if relax_all():
            raise ValueError("The graph contains a negative cycle reachable from the start")
    return dist, parent


if __name__ == "__main__":
    graph = small_weighted_graph()
    dist, parent = dijkstra(graph, "Katthult")
    print("Walking times from Katthult (minutes):")
    for place in sorted(dist, key=dist.get):
        path = reconstruct_path(parent, place)
        print(f"  {place:<11} {dist[place]:>2}   {format_path(path, directed=False)}")
    print("Katthult -> Backhorva:", shortest_route(graph, "Katthult", "Backhorva"))

    unreachable = graph.copy()
    unreachable.add_vertex("Vimmerby")
    print("Katthult -> Vimmerby (isolated):", shortest_route(unreachable, "Katthult", "Vimmerby"))
    print()

    # The counterexample from README.md: Dijkstra must refuse it ...
    bad = Graph.from_edges([("s", "a", 2), ("s", "b", 3), ("b", "a", -2)], directed=True)
    try:
        dijkstra(bad, "s")
    except ValueError as error:
        print("Dijkstra refuses:", error)
    # ... while Bellman-Ford handles it correctly: d(s, a) = 3 - 2 = 1.
    print("Bellman-Ford:", bellman_ford(bad, "s"))

    cycle = Graph.from_edges([("s", "a", 1), ("a", "b", -3), ("b", "a", 1)], directed=True)
    try:
        bellman_ford(cycle, "s")
    except ValueError as error:
        print("Bellman-Ford refuses:", error)

    # Drawings (only if matplotlib is installed; the windows do not block).
    if can_draw():
        # The shortest-path tree: the edges (parent[v], v) in red.
        draw(
            graph,
            title="Dijkstra from Katthult: distances and shortest-path tree",
            highlight_edges=[(p, v) for v, p in parent.items() if p is not None],
            highlight_vertices=["Katthult"],
            vertex_labels={v: f"d = {d}" for v, d in dist.items()},
        )
        route = shortest_route(graph, "Katthult", "Backhorva")
        if route is not None:
            path, length = route
            draw(
                graph,
                title=f"Fastest way Katthult -> Backhorva: {length} minutes",
                highlight_edges=list(zip(path, path[1:])),
                highlight_vertices=[path[0], path[-1]],
            )
        bf_dist, _ = bellman_ford(bad, "s")
        draw(
            bad,
            title="Negative weight: Dijkstra refuses, Bellman-Ford finds d(a) = 1",
            vertex_labels={v: f"d = {d}" for v, d in bf_dist.items()},
        )
