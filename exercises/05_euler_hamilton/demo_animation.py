"""Unit 5: Euler and Hamilton problems - STEP-BY-STEP ANIMATION.

The functions below are the algorithms of ``demo_solution.py`` with
additional calls of a :class:`~lib.trace.Trace`. Every ``trace.step(...)``
records one picture; the browser player then lets you step forwards and
backwards through the run or play it automatically.

Run it with ``python exercises/05_euler_hamilton/demo_animation.py``.

How to animate your own algorithm: see docs/visualisierung.md.
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))  # find ``lib``

from lib.generators import complete_bipartite_graph, complete_graph
from lib.graph import Graph, Vertex
from lib.trace import Trace
from lib.utils import load_module_from_path
from lib.viewer import show

# The data (bridges, Nikolaus house) and the precondition checks come from the demo solution.
solution = load_module_from_path(Path(__file__).with_name("demo_solution.py"))

# Königsberg like on a map: land masses and bridges (as extra vertices).
CITY_MAP = {
    "Nord": (0.5, 2.2), "Insel": (0, 0), "Süd": (0.5, -2.2), "Ost": (3.2, 0),
    "b1": (-0.6, 1.1), "b2": (0.6, 1.1), "b3": (-0.6, -1.1), "b4": (0.6, -1.1),
    "b5": (1.6, 0), "b6": (2.1, 1.3), "b7": (2.1, -1.3),
}

# The Nikolaus house: a square with a roof.
HOUSE = {1: (0, 0), 2: (2, 0), 3: (0, 2), 4: (2, 2), 5: (1, 3.3)}

EULER_CHECK_PSEUDOCODE = [
    "odd = []",
    "for each vertex v:",
    "    if deg(v) is odd: odd.append(v)",
    "S = [a vertex with an edge];  mark it",
    "while S is not empty:",
    "    u = S.pop();  mark and push every unmarked neighbour",
    "if a vertex with an edge is unmarked: no Euler trail",
    "if |odd| == 0: Euler circuit",
    "if |odd| == 2: Euler trail from odd[0] to odd[1]",
    "otherwise: no Euler trail",
]

HIERHOLZER_PSEUDOCODE = [
    "S = [start];  T = []",
    "while S is not empty:",
    "    v = top of S",
    "    if v has an unused edge v - w:",
    "        mark v - w as used;  push w onto S",
    "    else:",
    "        pop v from S;  put v in front of T",
    "return T",
]

HAMILTON_PSEUDOCODE = [
    "path = [s]",
    "extend():",
    "    if all n vertices are on the path:",
    "        return (last vertex - s is an edge)",
    "    for each neighbour w of the last vertex:",
    "        if w is on the path: skip w",
    "        path.append(w)",
    "        if extend(): return True",
    "        path.pop()   (dead end: go back)",
    "    return False",
]


def koenigsberg_graph() -> Graph:
    """Return Königsberg as a simple graph: every bridge is a vertex of degree 2."""
    graph = Graph()
    for bridge, bank1, bank2 in solution.KOENIGSBERG_BRIDGES:
        graph.add_edge(bank1, bridge)
        graph.add_edge(bridge, bank2)
    return graph


def trace_euler_check(graph: Graph, title: str = "Euler check", **options: object) -> Trace:
    """Check Euler's conditions (degrees and connectivity) and record every step.

    Flags: ``current`` = vertex being looked at, ``conflict`` = odd degree,
    ``visited`` = reached by the connectivity search, ``queued`` = on the
    stack of the search, ``rejected`` = vertex with an edge that was not
    reached. The label below a vertex is its degree. ``title`` names the
    scene; ``options`` are passed to :class:`Trace` (e.g. ``layout``).
    """
    trace = Trace(
        graph,
        title,
        description="An Euler trail exists exactly if all edges lie in one connected piece and "
        "0 (closed trail = circuit) or 2 (open trail) vertices have odd degree.",
        pseudocode=EULER_CHECK_PSEUDOCODE,
        **options,  # type: ignore[arg-type]
    )
    odd: list[Vertex] = []
    trace.variable("odd", odd)
    trace.step("First condition: count the degree of every vertex.", line=1)

    for v in graph.vertices():
        degree = graph.degree(v)
        trace.current(v)
        trace.label(v, f"deg {degree}")
        if degree % 2 == 1:
            odd.append(v)
            trace.flag(v, "conflict")
            trace.variable("odd", odd)
            trace.step(f"{v} has degree {degree}: odd. A walk cannot enter and leave it equally often.", line=3)
        else:
            trace.step(f"{v} has degree {degree}: even, fine.", line=3)
    trace.current(None)

    # Second condition: all vertices with an edge in one component (as in edges_connected).
    active = [v for v in graph.vertices() if graph.degree(v) > 0]
    connected = True
    if active:
        seen = {active[0]}
        stack = [active[0]]
        trace.flag(active[0], "queued")
        trace.variable("S", stack)
        trace.step(f"Second condition: search from {active[0]} and see whether it reaches every edge.", line=4)
        while stack:
            u = stack.pop()
            trace.unflag(u, "queued")
            trace.flag(u, "visited")
            trace.current(u)
            new = []
            for w in graph.neighbors(u):
                if w not in seen:
                    seen.add(w)
                    stack.append(w)
                    new.append(w)
                    trace.flag(w, "queued")
            trace.variable("S", stack)
            if new:
                trace.step(f"Take {u} from the stack and mark its new neighbours {', '.join(map(str, new))}.", line=6)
            else:
                trace.step(f"Take {u} from the stack: no new neighbours.", line=6)
        trace.current(None)
        trace.remove_variable("S")
        missing = [v for v in active if v not in seen]
        for v in missing:
            trace.flag(v, "rejected")
        connected = not missing
        if missing:
            trace.step(f"{len(missing)} vertices with edges were not reached: the edges are not connected.", line=7)
        else:
            trace.step("The search reached every vertex with an edge: the edges are connected.", line=7)

    if not connected:
        trace.step("Result: no Euler trail, because the edges do not lie in one piece.", line=7)
    elif not odd:
        trace.step("Result: connected and all degrees even - there is an Euler circuit.", line=8)
    elif len(odd) == 2:
        trace.flag(odd[0], "start")
        trace.flag(odd[1], "target")
        trace.step(f"Result: exactly 2 odd vertices - an Euler trail from {odd[0]} to {odd[1]}, "
                   "but no circuit.", line=9)
    else:
        trace.step(f"Result: {len(odd)} odd vertices - no Euler trail, and no Euler circuit.", line=10)
    return trace


def trace_hierholzer(graph: Graph, start: Vertex | None = None, **options: object) -> Trace:
    """Run Hierholzer's algorithm and record every step.

    ``start=None`` chooses the start like ``find_euler_trail``: an odd vertex
    if there is one, otherwise the first vertex with an edge.

    Flags: ``current`` = top of the stack, ``start`` = start vertex,
    ``path`` = used edges of the walk that is still on the stack,
    ``final`` = edges whose place in the trail is fixed (the edge label is
    their position). The label below a vertex counts its unused edges.

    Raises:
        ValueError: If the graph has no Euler trail starting at ``start``.
    """
    if not solution.has_euler_trail(graph) or graph.num_edges() == 0:
        raise ValueError("The graph has no Euler trail")
    odd = [v for v in graph.vertices() if graph.degree(v) % 2 == 1]
    if start is None:
        start = odd[0] if odd else next(v for v in graph.vertices() if graph.degree(v) > 0)
    if odd and start not in odd:
        raise ValueError(f"An Euler trail must start at an odd vertex {odd}, not at {start!r}")

    kind = "trail" if odd else "circuit"
    trace = Trace(
        graph,
        f"Hierholzer from {start}",
        description="Walk along unused edges until you get stuck. A vertex without unused edges is "
        "final: it moves from the stack to the front of the result T. If a vertex below on the stack "
        "still has unused edges, a detour starts there and is spliced into the result.",
        pseudocode=HIERHOLZER_PSEUDOCODE,
        **options,  # type: ignore[arg-type]
    )
    trace.style("path", description="used edge, walk still on the stack")
    trace.style("final", color="#15803d", width=4.5, priority=56, description="final edge (label = position)")

    total = graph.num_edges()
    remaining = graph.copy()  # we delete used edges - never in the input!
    stack = [start]
    walk: list[Vertex] = []
    for v in graph.vertices():
        trace.label(v, f"{remaining.degree(v)} left")
    trace.flag(start, "start")
    trace.current(start)
    trace.variable("S", stack)
    trace.variable("T", [])
    reason = "it has odd degree" if odd else "all degrees are even, any vertex works"
    trace.step(f"Start at {start} ({reason}).", line=1)

    while stack:
        v = stack[-1]
        trace.current(v)
        neighbours = remaining.neighbors(v)
        if neighbours:
            # Walk on along an unused edge and delete it.
            w = neighbours[0]
            remaining.remove_edge(v, w)
            stack.append(w)
            trace.flag_edge(v, w, "path")
            trace.current_edge(v, w)
            trace.label(v, f"{remaining.degree(v)} left")
            trace.label(w, f"{remaining.degree(w)} left")
            trace.current(w)
            trace.variable("S", stack)
            trace.step(f"{v} has an unused edge: walk {v} - {w} and push {w}.", line=5)
        else:
            # Stuck at v: v is the next vertex of the result (from the end).
            walk.append(stack.pop())
            trace.variable("S", stack)
            trace.variable("T", walk[::-1])
            if stack:
                # The edge stack[-1] - v gets its final place in the trail.
                position = total - len(walk) + 1
                trace.unflag_edge(stack[-1], v, "path")
                trace.flag_edge(stack[-1], v, "final")
                trace.edge_label(stack[-1], v, position)
                trace.current_edge(stack[-1], v)
                trace.step(f"{v} has no unused edge: move it to T. Edge {stack[-1]} - {v} becomes edge "
                           f"number {position}.", line=7)
            else:
                trace.current_edge(None)
                trace.step(f"{v} has no unused edge: move it to T. The stack is empty.", line=7)

    trace.current(None)
    trace.current_edge(None)
    walk.reverse()
    trace.step(f"Euler {kind} with {total} edges: {' - '.join(map(str, walk))}.", line=8)
    return trace


def trace_hamilton_backtracking(graph: Graph, title: str = "Hamilton backtracking", **options: object) -> Trace:
    """Search a Hamiltonian cycle by naive backtracking and record every step.

    Flags: ``start`` = fixed start vertex, ``path`` = the current partial
    path, ``current`` = its last vertex, ``rejected`` = the vertex and edge
    just given up (dead end). The label below a vertex is its place on the path.
    ``title`` names the scene; ``options`` are passed to :class:`Trace`.
    """
    trace = Trace(
        graph,
        title,
        description="Extend a path vertex by vertex in every possible way. At a dead end, go back one "
        "step and try the next neighbour. In the worst case this tries all orders: O(n!).",
        pseudocode=HAMILTON_PSEUDOCODE,
        **options,  # type: ignore[arg-type]
    )
    trace.style("rejected", description="dead end, given up")
    vertices = graph.vertices()
    n = len(vertices)
    start = vertices[0]
    path = [start]
    on_path = {start}
    tries = 0

    def show_path() -> None:
        trace.clear("path")
        trace.flag_path(path)
        trace.current(path[-1])
        for i, v in enumerate(path):
            trace.label(v, f"#{i + 1}")
        trace.variable("path", path)

    def extend() -> bool:
        """Try to complete ``path``; return True on success."""
        nonlocal tries
        u = path[-1]
        if len(path) == n:
            # All vertices used: we only have to get back to the start.
            return graph.has_edge(u, start)
        for w in graph.neighbors(u):
            if w not in on_path:
                path.append(w)
                on_path.add(w)
                tries += 1
                trace.clear("rejected")
                show_path()
                trace.current_edge(u, w)
                trace.variable("extensions", tries)
                if len(path) == n:
                    if graph.has_edge(w, start):
                        trace.step(f"Extend to {w}: all {n} vertices are on the path, and {w} - {start} "
                                   "is an edge.", line=4)
                    else:
                        trace.step(f"Extend to {w}: all {n} vertices are on the path, but {w} - {start} "
                                   "is no edge.", line=4)
                    stuck = True
                else:
                    stuck = all(x in on_path for x in graph.neighbors(w))
                    if stuck:
                        trace.step(f"Extend the path from {u} to {w} - but every neighbour of {w} is "
                                   "already on the path.", line=7)
                    else:
                        trace.step(f"Extend the path from {u} to {w}.", line=7)
                if extend():
                    return True
                # Dead end: undo the last step and try the next neighbour.
                path.pop()
                on_path.remove(w)
                trace.clear("rejected")
                show_path()
                trace.label(w, None)
                trace.flag(w, "rejected")
                trace.flag_edge(u, w, "rejected")
                trace.current_edge(None)
                if stuck:
                    trace.step(f"Dead end at {w}: remove it and go back to {u}.", line=9)
                else:
                    trace.step(f"Every way on from {w} failed: remove it and go back to {u}.", line=9)
        return False

    trace.flag(start, "start")
    show_path()
    trace.variable("n", n)
    trace.variable("extensions", tries)
    trace.step(f"Every Hamiltonian cycle passes {start}, so the path may start there.", line=1)

    if n >= 3 and extend():
        trace.flag_edge(path[-1], start, "path")
        trace.current(None)
        trace.current_edge(None)
        trace.clear("rejected")
        cycle = path + [start]
        trace.step(f"Hamiltonian cycle found after {tries} extensions: {' - '.join(map(str, cycle))}.", line=4)
    else:
        trace.current(None)
        trace.clear("rejected")
        trace.step(f"All possibilities tried ({tries} extensions): there is no Hamiltonian cycle.", line=10)
    return trace


def main() -> None:
    """Show all animations of this unit on one page."""
    nikolaus = Graph.from_edges(solution.NIKOLAUS_EDGES)
    k23 = complete_bipartite_graph(2, 3)
    show(
        trace_euler_check(koenigsberg_graph(), "Euler check: Königsberg", layout=CITY_MAP),
        trace_euler_check(nikolaus, "Euler check: Nikolaus house", layout=HOUSE),
        trace_hierholzer(nikolaus, layout=HOUSE),
        trace_hierholzer(complete_graph(5), layout="circular"),
        trace_hamilton_backtracking(nikolaus, "Hamilton: Nikolaus house", layout=HOUSE),
        trace_hamilton_backtracking(k23, "Hamilton: K_{2,3}", left=["L0", "L1"]),
        title="Unit 5: Euler and Hamilton",
    )


if __name__ == "__main__":
    main()
