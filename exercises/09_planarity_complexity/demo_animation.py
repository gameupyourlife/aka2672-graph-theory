"""Unit 9: Planarity and complexity - STEP-BY-STEP ANIMATION.

The functions below are the algorithms of ``demo_solution.py`` with
additional calls of a :class:`~lib.trace.Trace`. Every ``trace.step(...)``
records one picture; the browser player then lets you step forwards and
backwards through the run or play it automatically.

Run it with ``python exercises/09_planarity_complexity/demo_animation.py``.

How to animate your own algorithm: see docs/visualisierung.md.
"""

import itertools
import math
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))  # find ``lib``

from lib.generators import complete_bipartite_graph, complete_graph, petersen_graph
from lib.graph import Graph, Vertex
from lib.trace import Trace
from lib.viewer import show

PLANARITY_PSEUDOCODE = [
    "n = number of vertices;  m = number of edges",
    "if m > 3n - 6: certainly not planar",
    "if no triangle and m > 2n - 4: certainly not planar",
    "otherwise: the bounds cannot decide",
]

HAMILTON_PSEUDOCODE = [
    "v0 = first vertex;  checked = 0",
    "for each order of the other n - 1 vertices:",
    "    checked += 1;  cycle = [v0, *order, v0]",
    "    if two consecutive vertices are not adjacent: reject",
    "    else: return cycle",
    "return None  (no Hamiltonian cycle)",
]


def _find_triangle(graph: Graph) -> tuple[Vertex, Vertex, Vertex] | None:
    """Return one triangle ``(u, v, w)`` of ``graph`` or ``None`` (same idea as ``has_triangle``)."""
    for u, v, _weight in graph.edges():
        common = set(graph.neighbors(v))
        for w in graph.neighbors(u):
            if w in common:
                return u, v, w
    return None


def trace_planarity_bounds(graph: Graph, name: str, **options: object) -> Trace:
    """Check the edge bounds from Euler's formula for ``graph`` and record every step.

    Flags: ``highlight`` = the vertices / edges that are being counted, and
    the edges of a triangle (if there is one). The vertices and edges get
    their running numbers as labels while they are counted.
    ``options`` are passed to :class:`Trace` (e.g. ``layout``, ``left``, ``shells``).
    """
    trace = Trace(
        graph,
        f"Planarity bounds: {name}",
        description="Euler's formula gives necessary conditions for planarity: every simple planar "
        "graph with n >= 3 has m <= 3n - 6, a triangle-free one even m <= 2n - 4. "
        "If a bound is violated, the graph is certainly not planar; otherwise the bounds cannot decide "
        "(classic example: the Petersen graph satisfies both bounds but is not planar).",
        pseudocode=PLANARITY_PSEUDOCODE,
        **options,  # type: ignore[arg-type]
    )
    vertices = graph.vertices()
    edges = [(u, v) for u, v, _weight in graph.edges()]
    trace.step(f"The graph {name}. Can the edge bounds show that it is not planar?")

    # Count the vertices ...
    n = len(vertices)
    for number, v in enumerate(vertices, start=1):
        trace.label(v, number)
    trace.flag_only("highlight", vertices)
    trace.variable("n", n)
    trace.step(f"Count the vertices: n = {n}.", line=1)
    trace.clear("highlight")
    for v in vertices:
        trace.label(v, None)

    # ... and the edges.
    m = len(edges)
    for number, (u, v) in enumerate(edges, start=1):
        trace.edge_label(u, v, number)
    trace.flag_only_edges("highlight", edges)
    trace.variable("m", m)
    trace.step(f"Count the edges: m = {m}.", line=1)
    trace.clear("highlight")
    for u, v in edges:
        trace.edge_label(u, v, None)

    if n < 3:
        trace.step(f"Only n = {n} vertices: such a graph is always planar (the bounds need n >= 3).", line=4)
        return trace

    # Bound 1: m <= 3n - 6 for every simple planar graph.
    bound = 3 * n - 6
    trace.variable("3n - 6", bound)
    if m > bound:
        trace.step(f"m = {m} > {bound} = 3n - 6: too many edges for a planar graph.", line=2)
        trace.step(f"Result for {name}: m > 3n - 6, so {name} is certainly not planar.", line=2)
        return trace
    trace.step(f"m = {m} <= {bound} = 3n - 6: the first bound is satisfied.", line=2)

    # Bound 2: m <= 2n - 4, but only for triangle-free graphs.
    triangle = _find_triangle(graph)
    trace.variable("triangle", "none" if triangle is None else " - ".join(map(str, triangle)))
    if triangle is not None:
        u, v, w = triangle
        trace.flag_only_edges("highlight", [(u, v), (v, w), (w, u)])
        trace.step(
            f"Triangle {u} - {v} - {w}: faces may have only 3 edges, so only m <= 3n - 6 applies.",
            line=3,
        )
        trace.clear("highlight")
        trace.step(f"Result for {name}: m <= 3n - 6, the bounds cannot decide (they are only necessary).", line=4)
        return trace

    bound2 = 2 * n - 4
    trace.variable("2n - 4", bound2)
    if m > bound2:
        trace.step(
            f"No triangle: every face has at least 4 edges, so m <= 2n - 4 = {bound2} must hold - but m = {m}.",
            line=3,
        )
        trace.step(f"Result for {name}: m > 2n - 4 without triangle, so {name} is certainly not planar.", line=3)
        return trace
    trace.step(f"No triangle, and m = {m} <= {bound2} = 2n - 4: the second bound is satisfied too.", line=3)
    trace.step(f"Result for {name}: both bounds hold, the bounds cannot decide (they are only necessary).", line=4)
    return trace


def trace_bruteforce_hamilton(graph: Graph, **options: object) -> Trace:
    """Search a Hamiltonian cycle by trying all vertex orders and record every permutation.

    Flags: ``start`` = the fixed first vertex, ``path`` = the edges of the
    tried cycle that exist (up to the first missing one), ``rejected`` = the
    two vertices of the first consecutive pair that is not adjacent. The
    label below a vertex is its position in the tried order.
    ``options`` are passed to :class:`Trace` (e.g. ``layout``, ``left``).
    """
    vertices = graph.vertices()
    n = len(vertices)
    total = math.factorial(n - 1) if n >= 1 else 0
    trace = Trace(
        graph,
        f"Brute-force Hamiltonian cycle (n = {n})",
        description="Fix the first vertex and try every order of the other n - 1 vertices: "
        f"(n-1)! permutations, here {n - 1}! = {total}. Each further vertex multiplies the work "
        "by n - 1 - for n = 20 there are already about 1.2 * 10^17 orders.",
        pseudocode=HAMILTON_PSEUDOCODE,
        **options,  # type: ignore[arg-type]
    )
    if n < 3:
        trace.step("A simple graph needs at least 3 vertices for a cycle: nothing to search.", line=6)
        return trace

    # Every cycle passes through every vertex, so we may fix the start v0.
    first, rest = vertices[0], vertices[1:]
    checked = 0
    trace.flag(first, "start")
    trace.variable("(n-1)!", total)
    trace.variable("checked", checked)
    trace.step(f"Fix the start vertex {first}; the other {n - 1} vertices can be ordered in {n - 1}! = {total} ways.", line=1)

    for order in itertools.permutations(rest):
        checked += 1
        cycle = [first, *order, first]
        trace.clear("path", "rejected")
        for position, v in enumerate(cycle[:-1], start=1):
            trace.label(v, f"#{position}")
        trace.variable("checked", checked)
        trace.variable("cycle", cycle)
        shown = " - ".join(map(str, cycle))
        # Walk along the cycle until the first pair that is not adjacent.
        missing = None
        for i in range(len(cycle) - 1):
            u, v = cycle[i], cycle[i + 1]
            if not graph.has_edge(u, v):
                missing = (u, v)
                break
            trace.flag_edge(u, v, "path")
        if missing is not None:
            u, v = missing
            trace.flag(u, "rejected")
            trace.flag(v, "rejected")
            trace.step(f"Permutation #{checked}: {shown}: no edge {u} - {v}. Reject.", line=4)
            continue
        trace.flag_path(cycle)
        trace.step(f"Permutation #{checked}: {shown}: all {n} edges exist - a Hamiltonian cycle!", line=5)
        trace.step(f"Found after {checked} of {total} permutations: {shown}.", line=5)
        return trace

    trace.clear("path", "rejected")
    for v in vertices:
        trace.label(v, None)
    trace.remove_variable("cycle")
    trace.step(f"All {checked} = {n - 1}! permutations failed: the graph has no Hamiltonian cycle.", line=6)
    return trace


def main() -> None:
    """Show all animations of this unit on one page."""
    k23 = complete_bipartite_graph(2, 3)
    # A 6-cycle A - E - C - B - D - F - A with two chords. Its Hamiltonian
    # cycle starts with A - E, so the search finds it only after 79 of 120 orders.
    hamiltonian = Graph()
    hamiltonian.add_vertices("ABCDEF")
    for u, v in [("A", "E"), ("E", "C"), ("C", "B"), ("B", "D"), ("D", "F"), ("F", "A"), ("C", "D"), ("B", "F")]:
        hamiltonian.add_edge(u, v)
    show(
        trace_planarity_bounds(complete_graph(5), "K5", layout="circular"),
        trace_planarity_bounds(complete_bipartite_graph(3, 3), "K3,3", left=["L0", "L1", "L2"]),
        trace_planarity_bounds(petersen_graph(), "Petersen graph", shells=[range(5), range(5, 10)]),
        # K4 drawn without crossings: a triangle with a centre vertex.
        trace_planarity_bounds(complete_graph(4), "K4", shells=[[1, 2, 3], [0]]),
        trace_bruteforce_hamilton(k23, left=["L0", "L1"]),
        trace_bruteforce_hamilton(hamiltonian, layout="circular"),
        title="Unit 9: Planarity and complexity",
    )


if __name__ == "__main__":
    main()
