"""Unit 8: Maximum flows - STEP-BY-STEP ANIMATION.

The function below is the Edmonds-Karp algorithm of ``demo_solution.py``
with additional calls of a :class:`~lib.trace.Trace`. Every
``trace.step(...)`` records one picture; the browser player then lets you
step forwards and backwards through the run or play it automatically.

The residual network is not drawn as a graph of its own: a residual edge
u -> v that takes back flow is shown on the original edge v -> u.

Run it with ``python exercises/08_max_flow/demo_animation.py``.

How to animate your own algorithm: see docs/visualisierung.md.
"""

import sys
from collections import deque
from collections.abc import Mapping
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))  # find ``lib``

from lib.graph import Graph, Vertex
from lib.trace import Trace, format_value
from lib.utils import format_path, load_module_from_path
from lib.viewer import show

# Building blocks of the demo solution: residual network and pushing flow.
_demo = load_module_from_path(Path(__file__).with_name("demo_solution.py"))
residual_graph = _demo.residual_graph
_push = _demo._push

Flow = dict[tuple[Vertex, Vertex], float]

EDMONDS_KARP_PSEUDOCODE = [
    "f = 0 on every edge",
    "repeat:",
    "    build the residual network G_f",
    "    BFS from s in G_f",
    "    if t is not reached: stop, f is maximum",
    "    P = shortest s-t path,  δ = min c_f on P",
    "    push δ along P (backward edge: take back flow);  |f| += δ",
    "S = vertices reached by the last BFS: minimum cut",
]

CLRS_POSITIONS = {"s": (0, 0), "v1": (1, 1), "v2": (1, -1), "v3": (2, 1), "v4": (2, -1), "t": (3, 0)}
SMALL_POSITIONS = {"s": (0, 0), "a": (1, 1), "b": (1, -1), "t": (2, 0)}


def trace_edmonds_karp(
    graph: Graph,
    source: Vertex,
    sink: Vertex,
    title: str = "Edmonds-Karp",
    initial_flow: Mapping[tuple[Vertex, Vertex], float] | None = None,
    **options: object,
) -> Trace:
    """Run Edmonds-Karp from ``source`` to ``sink`` and record every step.

    Every edge shows ``flow/capacity``. Flags: ``start`` / ``target`` =
    source / sink, ``flow`` = edge carries flow, ``saturated`` = flow equals
    capacity, ``queued`` / ``current`` / ``visited`` = vertices of the BFS
    in the residual network, ``tree`` = edge over which the BFS reached a
    vertex (backward residual edges on the original reverse edge), ``path``
    = the shortest augmenting path, ``cut`` = edges of the minimum cut; the
    colour classes ``S`` / ``T`` are the two sides of the cut.

    ``initial_flow`` (optional) is a valid flow to start with instead of
    the zero flow. ``options`` are passed to :class:`Trace` (e.g. ``layout``).
    """
    trace = Trace(
        graph,
        title,
        description="Ford-Fulkerson with shortest augmenting paths: search the residual network "
        "with BFS, push the bottleneck along the path, repeat. A residual edge u -> v either uses "
        "free capacity of u -> v or takes back flow from v -> u.",
        pseudocode=EDMONDS_KARP_PSEUDOCODE,
        **options,  # type: ignore[arg-type]
    )
    flow: Flow = {(u, v): 0 for u, v, _ in graph.edges()}
    for edge, value in (initial_flow or {}).items():
        flow[edge] = value
    value = sum(flow[(u, v)] for u, v in flow if u == source) - sum(flow[(u, v)] for u, v in flow if v == source)

    def show_flow() -> None:
        """Label every edge with flow/capacity and flag edges with flow."""
        for u, v, capacity in graph.edges():
            trace.edge_label(u, v, f"{format_value(flow[(u, v)])}/{format_value(capacity)}")
        trace.flag_only_edges("saturated", [e for e in flow if flow[e] == graph.weight(*e) and flow[e] > 0])
        trace.flag_only_edges("flow", [e for e in flow if 0 < flow[e] < graph.weight(*e)])
        trace.variable("|f|", value)

    trace.flag(source, "start")
    trace.flag(sink, "target")
    show_flow()
    if initial_flow:
        trace.step(f"Start with the given flow of value {format_value(value)} (labels: flow/capacity).", line=1)
    else:
        trace.step("Start with the zero flow (labels: flow/capacity).", line=1)

    round_number = 0
    while True:
        round_number += 1
        residual = residual_graph(graph, flow)
        trace.clear("path", "visited", "queued", "tree")
        trace.remove_variable("δ")
        trace.remove_variable("P")

        # Breadth-first search in the residual network (as _bfs_parents).
        parent: dict[Vertex, Vertex | None] = {source: None}
        queue = deque([source])
        trace.flag(source, "queued")
        trace.variable("Q", queue)
        trace.step(
            f"Round {round_number}: build the residual network and search it breadth-first from {source}.",
            line=3,
        )
        while queue:
            u = queue.popleft()
            trace.current(u)
            trace.unflag(u, "queued")
            trace.variable("Q", queue)
            discovered = []
            for w in residual.neighbors(u):
                if w in parent:
                    continue
                parent[w] = u
                queue.append(w)
                discovered.append(w)
                trace.flag(w, "queued")
                trace.flag_edge(*_drawn_edge(graph, flow, u, w), "tree")
            trace.variable("Q", queue)
            if discovered:
                kinds = [f"{w}{' (backward edge)' if _is_backward(flow, u, w) else ''}" for w in discovered]
                trace.step(f"From {u} the residual network leads to new vertices: {', '.join(kinds)}.", line=4)
            else:
                trace.step(f"From {u} no new vertex is reachable in the residual network.", line=4)
            trace.flag(u, "visited")
        trace.current(None)
        trace.remove_variable("Q")

        if sink not in parent:
            trace.step(
                f"{sink} is not reachable in the residual network: no augmenting path, the flow is maximum.",
                line=5,
            )
            break

        # Shortest augmenting path and its bottleneck.
        path = [sink]
        while parent[path[-1]] is not None:
            path.append(parent[path[-1]])  # type: ignore[arg-type]
        path.reverse()
        pairs = list(zip(path, path[1:]))
        capacities = [residual.weight(u, v) for u, v in pairs]
        delta = min(capacities)
        trace.clear("visited", "queued", "tree")
        for u, v in pairs:
            trace.flag_edge(*_drawn_edge(graph, flow, u, v), "path")
        for v in path:
            trace.flag(v, "path")
        trace.variable("P", format_path(path))
        trace.variable("δ", delta)
        backward = [(u, v) for u, v in pairs if _is_backward(flow, u, v)]
        message = (
            f"Shortest augmenting path {format_path(path)}, bottleneck "
            f"δ = min({', '.join(format_value(c) for c in capacities)}) = {format_value(delta)}."
        )
        for u, v in backward:
            message += f" It uses the backward edge {u} -> {v}: takes back flow from {v} -> {u}."
        trace.step(message, line=6)

        # Push the bottleneck along the path.
        for u, v in pairs:
            _push(flow, u, v, delta)
        value += delta
        show_flow()
        trace.step(
            f"Push δ = {format_value(delta)} along the path: the flow value is now {format_value(value)}.", line=7
        )

    # Minimum cut: S = everything the last BFS reached.
    side = set(parent)
    trace.clear("visited", "queued", "tree", "path")
    cut_edges = [(u, v) for u, v, _ in graph.edges() if u in side and v not in side]
    for v in graph.vertices():
        trace.color(v, "S" if v in side else "T")
    trace.flag_only_edges("cut", cut_edges)
    cut_capacity = sum(graph.weight(u, v) for u, v in cut_edges)
    trace.variable("S", sorted(side, key=graph.vertices().index))
    trace.variable("cut capacity", cut_capacity)
    terms = " + ".join(format_value(graph.weight(u, v)) for u, v in cut_edges)
    trace.step(
        f"Minimum cut: S = vertices reached by the last BFS. The cut edges S -> T are saturated: "
        f"max flow = {format_value(value)} = {terms} = cut capacity.",
        line=8,
    )
    return trace


def trace_residual_graph(
    graph: Graph, flow: Mapping[tuple[Vertex, Vertex], float], title: str = "Residual network", **options: object
) -> Trace:
    """Return a one-step trace: the residual network of ``flow`` in ``graph``.

    Edge labels are residual capacities. Flags: ``backward`` = residual edge
    that only takes back flow, ``start`` / ``target`` for the vertices
    ``"s"`` / ``"t"`` if they exist. ``options`` are passed to :class:`Trace`.
    """
    residual = residual_graph(graph, flow)
    trace = Trace(
        residual,
        title,
        description="c_f(u, v) = (c(u, v) - f(u, v)) + f(v, u): free capacity forwards "
        "plus flow on the opposite edge that may be taken back.",
        show_weights=True,
        **options,  # type: ignore[arg-type]
    )
    trace.style("backward", color="#ea580c", dash=True, width=3, description="backward edge (takes back flow)")
    backward = []
    for u, v, _ in residual.edges():
        free = (graph.weight(u, v) if graph.has_edge(u, v) else 0) - flow.get((u, v), 0)
        if free <= 0:
            trace.flag_edge(u, v, "backward")
            backward.append(f"{u} -> {v}")
    for v, name in (("s", "start"), ("t", "target")):
        if v in residual:
            trace.flag(v, name)
    trace.step(
        f"Residual network: {residual.num_edges()} edges (labels: residual capacity), "
        f"backward edges: {', '.join(backward) or 'none'}."
    )
    return trace


def _is_backward(flow: Flow, u: Vertex, v: Vertex) -> bool:
    """True if pushing along the residual pair (u, v) takes back flow from v -> u."""
    return flow.get((v, u), 0) > 0


def _drawn_edge(graph: Graph, flow: Flow, u: Vertex, v: Vertex) -> tuple[Vertex, Vertex]:
    """The original edge on which the residual pair (u, v) is drawn."""
    if _is_backward(flow, u, v) or not graph.has_edge(u, v):
        return (v, u)
    return (u, v)


def main() -> None:
    """Show all animations of this unit on one page."""
    clrs = Graph.from_edges(
        [
            ("s", "v1", 16),
            ("s", "v2", 13),
            ("v1", "v3", 12),
            ("v2", "v1", 4),
            ("v2", "v4", 14),
            ("v3", "v2", 9),
            ("v3", "t", 20),
            ("v4", "v3", 7),
            ("v4", "t", 4),
        ],
        directed=True,
    )
    # The small network from README.md: the first unit of flow went
    # s -> a -> b -> t, the second one needs the backward edge b -> a.
    small = Graph.from_edges(
        [("s", "a", 1), ("s", "b", 1), ("a", "b", 1), ("a", "t", 1), ("b", "t", 1)], directed=True
    )
    bad_flow = {("s", "a"): 1, ("a", "b"): 1, ("b", "t"): 1}
    show(
        trace_edmonds_karp(clrs, "s", "t", "Edmonds-Karp (CLRS network)", layout=CLRS_POSITIONS),
        trace_edmonds_karp(small, "s", "t", "Backward edge", initial_flow=bad_flow, layout=SMALL_POSITIONS),
        trace_residual_graph(small, bad_flow, "Residual network of s -> a -> b -> t", layout=SMALL_POSITIONS),
        title="Unit 8: Maximum flows",
    )


if __name__ == "__main__":
    main()
