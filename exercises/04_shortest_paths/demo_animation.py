"""Unit 4: Shortest paths with Dijkstra (and Bellman-Ford) - STEP-BY-STEP ANIMATION.

The functions below are the algorithms of ``demo_solution.py`` with
additional calls of a :class:`~lib.trace.Trace`. Every ``trace.step(...)``
records one picture; the browser player then lets you step forwards and
backwards through the run or play it automatically.

Run it with ``python exercises/04_shortest_paths/demo_animation.py``.

How to animate your own algorithm: see docs/visualisierung.md.
"""

import heapq
import itertools
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))  # find ``lib``

from lib.generators import random_weighted_graph, small_weighted_graph
from lib.graph import Graph, Vertex
from lib.trace import Trace
from lib.utils import format_path
from lib.viewer import show

DIJKSTRA_PSEUDOCODE = [
    "d[s] = 0;  H = [(0, s)]",
    "while H is not empty:",
    "    (d, u) = H.pop()               # closest vertex",
    "    if u is finished: continue     # outdated entry",
    "    u is finished: d[u] is final",
    "    for each neighbour v of u:",
    "        if d + w(u, v) < d[v]:",
    "            d[v] = d + w(u, v);  parent[v] = u;  H.push((d[v], v))",
]

BELLMAN_FORD_PSEUDOCODE = [
    "d[s] = 0",
    "repeat |V| - 1 times:",
    "    for each edge (u, v) with weight w:",
    "        if d[u] + w < d[v]:",
    "            d[v] = d[u] + w;  parent[v] = u",
    "    if nothing changed: stop",
    "if one more round still improves: negative cycle",
]


def _heap_view(heap: list[tuple[float, int, Vertex]]) -> list[tuple[float, Vertex]]:
    """Return the heap as a sorted list of (distance, vertex)."""
    return [(d, v) for d, _, v in sorted(heap)]


def _set_parent(trace: Trace, parent: dict[Vertex, Vertex | None], v: Vertex, u: Vertex) -> None:
    """Make ``u`` the parent of ``v`` and move the ``tree`` flag accordingly."""
    old = parent.get(v)
    if old is not None:
        trace.unflag_edge(old, v, "tree")
    parent[v] = u
    trace.flag_edge(u, v, "tree")


def _path_to(parent: dict[Vertex, Vertex | None], target: Vertex) -> list[Vertex]:
    """Return the path ``[start, ..., target]`` encoded by ``parent``."""
    path = []
    v: Vertex | None = target
    while v is not None:
        path.append(v)
        v = parent[v]
    return path[::-1]


def trace_dijkstra(graph: Graph, start: Vertex, target: Vertex | None = None, **options: object) -> Trace:
    """Run Dijkstra's algorithm from ``start`` and record every step.

    Flags: ``start``, ``queued`` = discovered, in the heap, ``current`` =
    vertex taken from the heap / edge being relaxed, ``visited`` = finished
    (distance final), ``tree`` = edge (parent[v], v) of the current
    shortest-path tree. Labels show the tentative distances. If ``target``
    is given, a last step marks a shortest path to it with ``path`` and
    ``target``. ``options`` are passed to :class:`Trace` (e.g. ``layout``).
    """
    trace = Trace(
        graph,
        f"Dijkstra from {start}",
        description="Dijkstra always continues with the unfinished vertex that is closest "
        "to the start (the top of the heap H). With non-negative weights its distance "
        "is final. Then it relaxes the edges leaving this vertex.",
        pseudocode=DIJKSTRA_PSEUDOCODE,
        **options,  # type: ignore[arg-type]
    )
    dist: dict[Vertex, float] = {start: 0}
    parent: dict[Vertex, Vertex | None] = {start: None}
    finished: set[Vertex] = set()
    tie = itertools.count()
    heap: list[tuple[float, int, Vertex]] = [(0, next(tie), start)]
    trace.flag(start, "start", "queued")
    trace.label(start, "d = 0")
    trace.variable("H", _heap_view(heap))
    trace.step(f"Start: d[{start}] = 0, and (0, {start}) goes into the heap.", line=1)

    while heap:
        d, _, u = heapq.heappop(heap)
        trace.current(u)
        trace.current_edge(None)
        trace.variable("H", _heap_view(heap))
        trace.variable("u", u)
        if u in finished:
            trace.step(f"Entry ({d}, {u}) is outdated: {u} is finished already. Skip it.", line=4)
            continue
        finished.add(u)
        trace.unflag(u, "queued")
        trace.flag(u, "visited")
        trace.step(f"Take ({d}, {u}) from the heap: the closest unfinished vertex, d[{u}] = {d} is final.", line=5)
        for v in graph.neighbors(u):
            weight = graph.weight(u, v)
            new_distance = d + weight
            trace.current_edge(u, v)
            if v not in dist:
                dist[v] = new_distance
                _set_parent(trace, parent, v, u)
                heapq.heappush(heap, (new_distance, next(tie), v))
                trace.flag(v, "queued")
                trace.label(v, f"d = {new_distance}")
                trace.variable("H", _heap_view(heap))
                trace.step(f"{v} is new: d[{v}] = {d} + {weight} = {new_distance}, parent {u}.", line=8)
            elif new_distance < dist[v]:
                old = dist[v]
                dist[v] = new_distance
                _set_parent(trace, parent, v, u)
                heapq.heappush(heap, (new_distance, next(tie), v))
                trace.label(v, f"d = {new_distance}")
                trace.variable("H", _heap_view(heap))
                trace.step(f"d[{v}] = {old} > {d} + {weight}: improve to {new_distance}, new parent {u}.", line=8)
            else:
                note = f" ({v} is final)" if v in finished else ""
                trace.step(f"d[{v}] = {dist[v]} ≤ {d} + {weight} = {new_distance}: no improvement{note}.", line=7)
        trace.current_edge(None)

    trace.current(None)
    trace.remove_variable("u")
    trace.step(f"The heap is empty: all {len(dist)} vertices reachable from {start} have their final distance.")

    if target is not None and target in dist:
        path = _path_to(parent, target)
        trace.flag_path(path)
        trace.flag(target, "target")
        trace.step(
            f"Shortest path {format_path(path, directed=graph.directed)} of length {dist[target]}: "
            f"follow the parents back from {target}."
        )
    return trace


def _plus(a: float, b: float) -> str:
    """Return ``"a + b"``, or ``"a - |b|"`` if ``b`` is negative."""
    return f"{a} - {-b}" if b < 0 else f"{a} + {b}"


def trace_bellman_ford(graph: Graph, start: Vertex, title: str | None = None, **options: object) -> Trace:
    """OPTIONAL: Run Bellman-Ford from ``start`` and record every step.

    Flags: ``start``, ``visited`` = reached (has a distance), ``current`` =
    edge being relaxed, ``tree`` = edge (parent[v], v), ``conflict`` =
    vertex whose distance still improves in the extra round (negative cycle).
    """
    trace = Trace(
        graph,
        title or f"Bellman-Ford from {start}",
        description="Bellman-Ford relaxes ALL edges in every round. After round k, d[v] is at "
        "most the length of a shortest path with at most k edges. It works with negative "
        "weights and detects negative cycles.",
        pseudocode=BELLMAN_FORD_PSEUDOCODE,
        **options,  # type: ignore[arg-type]
    )
    arcs = [(u, v, graph.weight(u, v)) for u in graph.vertices() for v in graph.neighbors(u)]
    dist: dict[Vertex, float] = {start: 0}
    parent: dict[Vertex, Vertex | None] = {start: None}
    rounds = graph.num_vertices() - 1
    trace.flag(start, "start", "visited")
    trace.label(start, "d = 0")
    trace.step(f"Start: d[{start}] = 0. At most |V| - 1 = {rounds} rounds are needed.", line=1)

    for round_number in range(1, rounds + 2):
        check = round_number > rounds  # the extra round that looks for negative cycles
        changed = False
        trace.variable("round", f"{round_number} (check)" if check else round_number)
        trace.variable("changed", changed)
        for u, v, weight in arcs:
            trace.current_edge(u, v)
            arrow = f"{u} -> {v}" if graph.directed else f"{u} - {v}"
            if u not in dist:
                trace.step(f"Edge {arrow}: {u} has no distance yet, skip it.", line=4)
            elif v not in dist or dist[u] + weight < dist[v]:
                old, old_u = dist.get(v), dist[u]
                dist[v] = dist[u] + weight
                _set_parent(trace, parent, v, u)
                changed = True
                trace.flag(v, "conflict" if check else "visited")
                trace.label(v, f"d = {dist[v]}")
                trace.variable("changed", changed)
                before = "∞" if old is None else old
                relaxed = _plus(old_u, weight)
                trace.step(f"Edge {arrow} ({weight}): d[{v}] = {before} > {relaxed}: improve to {dist[v]}.", line=5)
            else:
                relaxed = _plus(dist[u], weight)
                trace.step(f"Edge {arrow} ({weight}): d[{v}] = {dist[v]} ≤ {relaxed}: no improvement.", line=4)
        trace.current_edge(None)
        if not changed:
            trace.step(f"Round {round_number} changed nothing: the distances are final.", line=6)
            break
        if check:
            trace.step(f"Round {round_number} still improves: a negative cycle is reachable from {start}.", line=7)
            break
        trace.step(f"End of round {round_number}: some distance improved, so do another round.", line=2)

    distances = ", ".join(f"d[{v}] = {d}" for v, d in dist.items())
    if not changed:
        trace.step(f"Done: {distances}. The green edges form the shortest-path tree.")
    return trace


def main() -> None:
    """Show all animations of this unit on one page."""
    lonneberga = small_weighted_graph()
    directed = random_weighted_graph(8, 0.3, 1, 15, seed=94, directed=True)
    negative = Graph.from_edges([("s", "a", 2), ("s", "b", 3), ("b", "a", -2)], directed=True)
    negative_cycle = Graph.from_edges([("s", "a", 1), ("a", "b", -3), ("b", "a", 1)], directed=True)
    show(
        trace_dijkstra(lonneberga, "Katthult", target="Backhorva"),
        trace_dijkstra(directed, 0, target=5),
        trace_bellman_ford(negative, "s"),
        trace_bellman_ford(negative_cycle, "s", title="Bellman-Ford: negative cycle"),
        title="Unit 4: Shortest paths",
    )


if __name__ == "__main__":
    main()
