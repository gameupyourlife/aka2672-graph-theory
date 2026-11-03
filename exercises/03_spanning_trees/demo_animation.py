"""Unit 3: Spanning trees, Union-Find and Kruskal's algorithm - STEP-BY-STEP ANIMATION.

The functions below are the algorithms of ``demo_solution.py`` with
additional calls of a :class:`~lib.trace.Trace`. Every ``trace.step(...)``
records one picture; the browser player then lets you step forwards and
backwards through the run or play it automatically.

Run it with ``python exercises/03_spanning_trees/demo_animation.py``.

How to animate your own algorithm: see docs/visualisierung.md.
"""

import heapq
import itertools
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))  # find ``lib``

from lib.generators import random_connected_graph, small_weighted_graph
from lib.graph import Graph, Vertex
from lib.trace import Trace
from lib.utils import load_module_from_path
from lib.viewer import show

# The Union-Find data structure is a building block of demo_solution.py.
UnionFind = load_module_from_path(Path(__file__).with_name("demo_solution.py")).UnionFind

KRUSKAL_PSEUDOCODE = [
    "F = [];  every vertex is a set of its own",
    "for each edge (u, v) from light to heavy:",
    "    if find(u) == find(v):",
    "        skip (u, v): it would close a cycle",
    "    else:",
    "        union(u, v);  F.append((u, v))",
    "return F",
]

PRIM_PSEUDOCODE = [
    "T = {s};  push every edge (s, w) into H",
    "while H is not empty:",
    "    (weight, u, v) = H.pop()       # lightest edge",
    "    if v in T: continue            # outdated entry",
    "    T.add(v);  take the edge (u, v)",
    "    for each neighbour w of v not in T:",
    "        H.push((weight(v, w), v, w))",
]


def _sets(components: "UnionFind", vertices: list[Vertex]) -> list[set[Vertex]]:
    """Return the sets of the Union-Find partition, the largest set first."""
    groups: dict[Vertex, set[Vertex]] = {}
    for v in vertices:
        groups.setdefault(components.find(v), set()).add(v)
    return sorted(groups.values(), key=len, reverse=True)


def _show_partition(trace: Trace, components: "UnionFind", vertices: list[Vertex]) -> None:
    """Colour every vertex of a set with >= 2 elements by its representative."""
    sets = _sets(components, vertices)
    for group in sets:
        representative = components.find(next(iter(group)))
        for v in group:
            trace.color(v, representative if len(group) > 1 else None)
    trace.variable("sets", sets)


def trace_kruskal(graph: Graph, **options: object) -> Trace:
    """Run Kruskal's algorithm and record every step.

    Flags: ``current`` = edge being examined, ``tree`` = accepted edge,
    ``rejected`` = edge that would close a cycle. Vertices of the same
    Union-Find set (with at least two elements) share a colour; the colour
    class is the representative ``find(v)``. ``options`` are passed to
    :class:`Trace` (e.g. ``layout``).
    """
    trace = Trace(
        graph,
        f"Kruskal ({graph.num_vertices()} vertices, {graph.num_edges()} edges)",
        description="Kruskal looks at the edges from light to heavy and keeps an edge "
        "whenever it joins two different components (Union-Find sets). An edge inside "
        "one component would close a cycle.",
        pseudocode=KRUSKAL_PSEUDOCODE,
        **options,  # type: ignore[arg-type]
    )
    vertices = graph.vertices()
    components = UnionFind(vertices)
    forest = []
    total: float = 0
    edges = sorted(graph.edges(), key=lambda e: e.weight)
    trace.variable("edges left", [f"{e.u}-{e.v} ({e.weight})" for e in edges])
    _show_partition(trace, components, vertices)
    trace.variable("total weight", total)
    trace.step(f"Start: {len(vertices)} single vertices, {len(edges)} edges sorted by weight.", line=1)

    for i, edge in enumerate(edges):
        u, v, weight = edge
        name = f"{u} - {v} ({weight})"
        trace.current_edge(u, v)
        trace.variable("edges left", [f"{e.u}-{e.v} ({e.weight})" for e in edges[i + 1 :]])
        roots = f"find({u}) = {components.find(u)}, find({v}) = {components.find(v)}"
        trace.step(f"Next lightest edge: {name}; {roots}.", line=3)
        if components.union(u, v):
            forest.append(edge)
            total += weight
            trace.flag_edge(u, v, "tree")
            _show_partition(trace, components, vertices)
            trace.variable("total weight", total)
            trace.step(f"Edge {name} joins two components: take it.", line=6)
        else:
            trace.flag_edge(u, v, "rejected")
            trace.step(f"{u} and {v} are in the same component: {name} closes a cycle, skip it.", line=4)
        trace.current_edge(None)

    kind = "spanning tree" if len(forest) == len(vertices) - 1 else "spanning forest"
    trace.step(f"Done: the green edges form a minimum {kind} ({len(forest)} edges, weight {total}).", line=7)
    return trace


def _heap_view(heap: list[tuple[float, int, Vertex, Vertex]]) -> list[tuple[float, str]]:
    """Return the heap as a sorted list of (weight, edge)."""
    return [(weight, f"{u}-{v}") for weight, _, u, v in sorted(heap)]


def trace_prim(graph: Graph, start: Vertex, **options: object) -> Trace:
    """OPTIONAL: Run Prim's algorithm from ``start`` and record every step.

    Flags: ``start``, ``visited`` = in the tree T, ``queued`` = outside T but
    with a candidate edge in the heap, ``current`` = vertex that just joined
    T / edge just taken from the heap, ``tree`` = edge of the tree,
    ``rejected`` = outdated heap entry (its edge would close a cycle).
    """
    trace = Trace(
        graph,
        f"Prim from {start}",
        description="Prim grows ONE tree: it always takes the lightest edge that leaves "
        "the tree. The heap H holds the candidate edges (weight, u-v).",
        pseudocode=PRIM_PSEUDOCODE,
        **options,  # type: ignore[arg-type]
    )
    in_tree: set[Vertex] = {start}
    total: float = 0
    tie = itertools.count()
    heap: list[tuple[float, int, Vertex, Vertex]] = []
    for v in graph.neighbors(start):
        heapq.heappush(heap, (graph.weight(start, v), next(tie), start, v))
        trace.flag(v, "queued")
    trace.flag(start, "start", "visited")
    trace.current(start)
    trace.variable("H", _heap_view(heap))
    trace.variable("total weight", total)
    trace.step(f"Start: T = {{{start}}}. All edges at {start} go into the heap.", line=1)

    while heap:
        weight, _, u, v = heapq.heappop(heap)
        trace.current(None)
        trace.current_edge(u, v)
        trace.variable("H", _heap_view(heap))
        if v in in_tree:
            trace.flag_edge(u, v, "rejected")
            trace.step(f"Edge {u} - {v} ({weight}) is outdated: {v} is in T already (it closes a cycle).", line=4)
            trace.current_edge(None)
            continue
        in_tree.add(v)
        total += weight
        trace.flag_edge(u, v, "tree")
        trace.unflag(v, "queued")
        trace.flag(v, "visited")
        trace.current(v)
        trace.variable("total weight", total)
        trace.step(f"Lightest edge leaving T: {u} - {v} ({weight}). {v} joins the tree.", line=5)
        trace.current_edge(None)
        new = [w for w in graph.neighbors(v) if w not in in_tree]
        for w in new:
            heapq.heappush(heap, (graph.weight(v, w), next(tie), v, w))
            trace.flag(w, "queued")
        if new:
            trace.variable("H", _heap_view(heap))
            trace.step(f"Push the edges from {v} to {', '.join(map(str, new))} into the heap.", line=7)

    trace.current(None)
    trace.step(f"The heap is empty: minimum spanning tree with {len(in_tree) - 1} edges, total weight {total}.")
    return trace


def main() -> None:
    """Show all animations of this unit on one page."""
    lonneberga = small_weighted_graph()
    example = random_connected_graph(10, 8, seed=7, min_weight=1, max_weight=20)
    show(
        trace_kruskal(lonneberga),
        trace_kruskal(example),
        trace_prim(lonneberga, "Markt"),
        title="Unit 3: Spanning trees",
    )


if __name__ == "__main__":
    main()
