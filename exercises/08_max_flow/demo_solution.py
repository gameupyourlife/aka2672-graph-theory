"""Unit 8: Maximum flows - DEMO SOLUTION.

Representation used throughout:

* the network is a directed ``Graph``; the capacity of ``u -> v`` is the
  edge weight,
* a flow is a dictionary ``(u, v) -> value`` keyed by the ORIGINAL edges
  (a missing key means flow 0).

The residual capacity of an ordered pair (u, v) is

    c_f(u, v) = (c(u, v) - f(u, v)) + f(v, u)

"free capacity forwards" plus "flow on the opposite edge that we may take
back". Non-existing edges have capacity 0 and flow 0, so the formula also
works when u -> v and v -> u both exist (antiparallel edges).

Edmonds-Karp = Ford-Fulkerson with shortest augmenting paths (BFS):
repeat "build residual network, find shortest s-t path, push the
bottleneck" until the sink is unreachable. By the max-flow min-cut theorem
the flow is then maximum. Runtime O(|V| * |E|^2).

Run it with ``python exercises/08_max_flow/demo_solution.py``.
"""

import sys
from collections import deque
from collections.abc import Mapping
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))  # find ``lib``

from lib.graph import Graph, Vertex
from lib.utils import format_path
from lib.visualization import show, snapshot

Flow = dict[tuple[Vertex, Vertex], float]


def _capacity(graph: Graph, u: Vertex, v: Vertex) -> float:
    """c(u, v): the edge weight, or 0 if there is no edge u -> v."""
    return graph.weight(u, v) if graph.has_edge(u, v) else 0


def residual_graph(graph: Graph, flow: Mapping[tuple[Vertex, Vertex], float]) -> Graph:
    """Return the residual network: an edge u -> v for every c_f(u, v) > 0."""
    residual = Graph(directed=True)
    residual.add_vertices(graph.vertices())

    # Every edge u -> v gives two candidate pairs: (u, v) (forwards) and
    # (v, u) (backwards). If v -> u is also an edge, the pairs coincide,
    # so we remember which pairs we have already handled.
    pairs: list[tuple[Vertex, Vertex]] = []
    seen: set[tuple[Vertex, Vertex]] = set()
    for u, v, _ in graph.edges():
        for pair in ((u, v), (v, u)):
            if pair not in seen:
                seen.add(pair)
                pairs.append(pair)

    for u, v in pairs:
        forward = _capacity(graph, u, v) - flow.get((u, v), 0)  # unused capacity
        backward = flow.get((v, u), 0)  # flow on v -> u that we can take back
        capacity = forward + backward
        if capacity > 0:
            residual.add_edge(u, v, capacity)
    return residual


def _bfs_parents(graph: Graph, source: Vertex) -> dict[Vertex, Vertex | None]:
    """Breadth-first search: parent pointers of all vertices reachable from source."""
    parent: dict[Vertex, Vertex | None] = {source: None}
    queue = deque([source])
    while queue:
        u = queue.popleft()
        for w in graph.neighbors(u):
            if w not in parent:
                parent[w] = u
                queue.append(w)
    return parent


def find_augmenting_path(residual: Graph, source: Vertex, sink: Vertex) -> list[Vertex] | None:
    """Return a shortest path ``[source, ..., sink]`` in ``residual`` or ``None``.

    Raises:
        KeyError: If ``source`` or ``sink`` is not a vertex of ``residual``.
    """
    if source not in residual:
        raise KeyError(f"Source {source!r} is not in the graph")
    if sink not in residual:
        raise KeyError(f"Sink {sink!r} is not in the graph")
    parent = _bfs_parents(residual, source)
    if sink not in parent:
        return None  # the sink is not reachable: no augmenting path

    # BFS tree paths are shortest paths (fewest edges), see unit 2.
    path = []
    v: Vertex | None = sink
    while v is not None:
        path.append(v)
        v = parent[v]
    path.reverse()
    return path


def _push(flow: Flow, u: Vertex, v: Vertex, delta: float) -> None:
    """Send ``delta`` units along the residual pair (u, v)."""
    # First take back flow from the opposite edge v -> u (if it exists) ...
    back = min(delta, flow.get((v, u), 0))
    if back > 0:
        flow[(v, u)] -= back
    # ... and only put the rest on u -> v. If u -> v is not an edge, the
    # rest is 0, because then c_f(u, v) = f(v, u) >= delta.
    rest = delta - back
    if rest > 0:
        flow[(u, v)] += rest


def _check_network(graph: Graph, source: Vertex, sink: Vertex) -> None:
    if not graph.directed:
        raise ValueError("A flow network must be a directed graph")
    if source not in graph:
        raise KeyError(f"Source {source!r} is not in the graph")
    if sink not in graph:
        raise KeyError(f"Sink {sink!r} is not in the graph")
    if source == sink:
        raise ValueError("Source and sink must be different")
    for u, v, capacity in graph.edges():
        if capacity < 0:
            raise ValueError(f"Negative capacity {capacity} on {u!r} -> {v!r}")


def edmonds_karp(graph: Graph, source: Vertex, sink: Vertex) -> tuple[float, dict[tuple[Vertex, Vertex], float]]:
    """Return ``(value, flow)`` of a maximum flow from ``source`` to ``sink``.

    Raises:
        ValueError: Undirected graph, ``source == sink`` or negative capacity.
        KeyError: If ``source`` or ``sink`` is not a vertex of the graph.
    """
    _check_network(graph, source, sink)
    flow: Flow = {(u, v): 0 for u, v, _ in graph.edges()}  # start with the zero flow
    value: float = 0

    while True:
        residual = residual_graph(graph, flow)
        path = find_augmenting_path(residual, source, sink)
        if path is None:
            # No augmenting path: by the max-flow min-cut theorem the flow
            # is maximum.
            return value, flow
        # The bottleneck is the smallest residual capacity along the path.
        delta = min(residual.weight(path[i], path[i + 1]) for i in range(len(path) - 1))
        for i in range(len(path) - 1):
            _push(flow, path[i], path[i + 1], delta)
        value += delta


def min_cut(graph: Graph, source: Vertex, sink: Vertex) -> set[Vertex]:
    """OPTIONAL: Return the source side S of a minimum cut."""
    _value, flow = edmonds_karp(graph, source, sink)
    # S = everything still reachable from the source in the final residual
    # network. Edges S -> T are saturated, edges T -> S carry no flow, so
    # the cut capacity equals the flow value (proof of max-flow min-cut).
    return set(_bfs_parents(residual_graph(graph, flow), source))


if __name__ == "__main__":
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
    first = find_augmenting_path(residual_graph(clrs, {}), "s", "t")
    print("First augmenting path:", format_path(first))
    value, flow = edmonds_karp(clrs, "s", "t")
    print("Maximum flow value:", value)
    for (u, v), f in flow.items():
        print(f"  {u:>2} -> {v:<2}: {f:>2} / {clrs.weight(u, v)}")
    cut = min_cut(clrs, "s", "t")
    print("Minimum cut S =", sorted(cut))
    print()

    # The small network from README.md: the first unit of flow goes
    # s -> a -> b -> t, the second one needs the backward edge b -> a.
    small = Graph.from_edges(
        [("s", "a", 1), ("s", "b", 1), ("a", "b", 1), ("a", "t", 1), ("b", "t", 1)], directed=True
    )
    bad_flow = {("s", "a"): 1, ("a", "b"): 1, ("b", "t"): 1}
    residual = residual_graph(small, bad_flow)
    print("Residual edges:", residual.edges())
    print("Augmenting path:", format_path(find_augmenting_path(residual, "s", "t")))
    print("Edmonds-Karp:", edmonds_karp(small, "s", "t"))

    # Pictures in the browser (no extra packages needed).
    network = {"s": (0, 0), "v1": (1, 1), "v2": (1, -1), "v3": (2, 1), "v4": (2, -1), "t": (3, 0)}
    cut_edges = [(u, v) for u, v, _ in clrs.edges() if u in cut and v not in cut]
    show(
        snapshot(
            clrs,
            f"Maximum flow {value} = capacity of the minimum cut (red edges)",
            layout=network,
            edge_labels={(u, v): f"{flow[(u, v)]}/{c}" for u, v, c in clrs.edges()},
            edge_flags={edge: ["cut"] for edge in cut_edges},
            vertex_colors={v: "S" if v in cut else "T" for v in clrs.vertices()},
            vertex_flags={"s": ["start"], "t": ["target"]},
        ),
        snapshot(
            residual,
            "Residual network of the flow s -> a -> b -> t",
            layout={"s": (0, 0), "a": (1, 1), "b": (1, -1), "t": (2, 0)},
            show_weights=True,
            vertex_flags={"s": ["start"], "t": ["target"]},
        ),
        title="Unit 8: results",
    )
    print("Step by step: python exercises/08_max_flow/demo_animation.py")
