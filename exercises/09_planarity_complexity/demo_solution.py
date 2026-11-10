"""Unit 9: Planarity and complexity - DEMO SOLUTION.

This file solves all programming tasks of README.md. It is written as
teaching material: the comments explain the mathematical idea behind each
step.

Two big ideas meet in this unit:

* **Planarity.** Euler's formula ``n - m + f = 1 + c`` for plane graphs gives
  simple *necessary* conditions for planarity (``m <= 3n - 6``, and
  ``m <= 2n - 4`` without triangles). If a graph violates them, it is
  certainly not planar. If it satisfies them, we know nothing - the Petersen
  graph is the classic example.
* **Complexity.** Some problems (Euler circuit, 2-colourability, shortest
  paths) have polynomial-time algorithms. For others (Hamiltonian cycle,
  3-colourability, TSP) nobody knows such an algorithm. The naive search for
  a Hamiltonian cycle tries ``(n-1)!`` vertex orders - and ``(n-1)!`` explodes.

Solutions of the pen-and-paper exercises (README.md, "Auf Papier")
-----------------------------------------------------------------------

C1. Euler's formula on drawings (n - m + f = 2 for connected graphs):
    * K4 drawn as a triangle with a centre vertex: n = 4, m = 6, f = 4
      (three inner triangles + outer face); 4 - 6 + 4 = 2.
    * Cube graph: n = 8, m = 12, f = 6 (the six sides of the cube; when
      drawn flat, one side becomes the outer face); 8 - 12 + 6 = 2.
    * 2 x 3 grid: n = 6, m = 7, f = 3 (two squares + outer face);
      6 - 7 + 3 = 2.
    * Two disjoint triangles: n = 6, m = 6, c = 2, f = 3 (two inner faces,
      ONE common outer face); 6 - 6 + 3 = 3 = 1 + c.

C2. K5: n = 5, m = 10 > 9 = 3n - 6, so K5 is not planar.
    K3,3: n = 6, m = 9 <= 12 = 3n - 6, so the first bound does NOT decide.
    But K3,3 is bipartite, hence has no odd cycle and in particular no
    triangle. Then m <= 2n - 4 = 8 must hold for a planar graph, and
    9 > 8. So K3,3 is not planar ("three houses, three utilities" cannot be
    connected without crossings).

C3. Petersen graph: n = 10, m = 15, no triangle (shortest cycle has length
    5). 15 <= 24 = 3n - 6 and 15 <= 16 = 2n - 4: both bounds are satisfied,
    yet the graph is not planar. Proof with Wagner's theorem: contract the
    five spokes {i, i+5}; the result is K5 (every outer vertex i becomes
    adjacent to i +- 1 via the outer cycle and to i +- 2 via the pentagram).
    Alternatively one finds a subdivision of K3,3 (Kuratowski). The bounds
    are only necessary conditions.
    Optional sharper bound: if every cycle has length >= g (girth g), then
    g * f <= 2m and Euler give m <= g (n - 2) / (g - 2). For Petersen
    (g = 5): m <= 5 * 8 / 3 = 13.3 < 15 - this bound DOES show
    non-planarity.

C4. Brute force for n = 20: (n-1)! = 19! = 121 645 100 408 832 000
    (about 1.2 * 10^17) permutations. At 10^9 permutations per second:
    about 1.2 * 10^8 seconds, i.e. about 3.9 years. For n = 25:
    24! / 10^9 s, about 6.2 * 10^14 s or roughly 20 million years.
    In one day (8.64 * 10^13 permutations) we get up to n = 17
    (16! = 2.1 * 10^13), but not n = 18 (17! = 3.6 * 10^14, about 4 days).
    Every additional vertex multiplies the work by (n-1): a 1000 times
    faster computer only gains about 3 to 4 vertices.

C5. Certificate for "a Hamiltonian cycle exists": the cycle itself (a list of
    n + 1 vertices). A verifier checks in O(n) (with an adjacency matrix,
    or O(n * maximum degree) with adjacency lists) that every vertex appears
    exactly once and that consecutive vertices are adjacent. Hence the
    problem is in NP. For "there is NO Hamiltonian cycle" no short
    certificate is known - this problem lies in co-NP, and whether it is
    in NP is open.

C6. Euler circuit versus Hamiltonian cycle: a connected graph has an Euler
    circuit exactly if every vertex has even degree (Euler/Hierholzer), and
    degrees plus connectivity can be checked in O(n + m). For Hamiltonian
    cycles no such simple criterion is known; the problem is NP-complete,
    so (unless P = NP) there is no polynomial-time test at all.
"""

import itertools
import math
import sys
from collections.abc import Iterable
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))  # find ``lib``

from lib.generators import (
    complete_bipartite_graph,
    complete_graph,
    cycle_graph,
    grid_graph,
    petersen_graph,
    random_tree,
)
from lib.graph import Graph, Vertex
from lib.utils import format_path, measure_time
from lib.visualization import show, snapshot

# ----------------------------------------------------------------------
# Part A: planarity
# ----------------------------------------------------------------------


def faces_by_euler_formula(num_vertices: int, num_edges: int, num_components: int = 1) -> int:
    """Return the number of faces of a plane embedding: ``f = m - n + 1 + c``.

    Raises:
        ValueError: If ``num_vertices < 1``, ``num_edges < 0``,
            ``num_components < 1``, ``num_components > num_vertices`` or
            ``num_edges < num_vertices - num_components`` (no graph with
            these numbers exists).
    """
    n, m, c = num_vertices, num_edges, num_components
    if n < 1:
        raise ValueError("A graph for Euler's formula needs at least one vertex")
    if m < 0:
        raise ValueError("The number of edges must not be negative")
    if c < 1 or c > n:
        raise ValueError("The number of components must be between 1 and the number of vertices")
    # Every component with n_i vertices needs at least n_i - 1 edges (a tree),
    # so a graph with c components has at least n - c edges.
    if m < n - c:
        raise ValueError(f"A graph with {n} vertices and {c} components has at least {n - c} edges")
    # Euler: n - m + f = 1 + c  <=>  f = m - n + 1 + c.
    return m - n + 1 + c


def max_planar_edges(num_vertices: int) -> int:
    """Return the maximum number of edges of a simple planar graph with ``num_vertices`` vertices.

    Raises:
        ValueError: If ``num_vertices`` is negative.
    """
    n = num_vertices
    if n < 0:
        raise ValueError("The number of vertices must not be negative")
    if n <= 2:
        # Small cases: no edge with 0 or 1 vertices, one edge with 2 vertices.
        # (The formula 3n - 6 would give -6, -3 and 0 - it needs n >= 3.)
        return n * (n - 1) // 2
    # For n >= 3 every face is bounded by at least 3 edges, which gives
    # 3f <= 2m; together with Euler's formula this yields m <= 3n - 6.
    # The bound is attained by triangulations (e.g. K3, K4, the octahedron).
    return 3 * n - 6


def _require_undirected(graph: Graph, name: str) -> None:
    """Raise a ValueError if ``graph`` is directed."""
    if graph.directed:
        raise ValueError(f"{name}() expects an undirected graph")


def has_triangle(graph: Graph) -> bool:
    """Return ``True`` if the undirected graph contains a triangle (a cycle of length 3).

    Raises:
        ValueError: If the graph is directed.
    """
    _require_undirected(graph, "has_triangle")
    # A triangle u - v - w exists exactly if some edge {u, v} has a common
    # neighbour w. We look at every edge and intersect the neighbourhoods.
    for u, v, _weight in graph.edges():
        if set(graph.neighbors(u)) & set(graph.neighbors(v)):
            return True
    return False


def is_certainly_nonplanar(graph: Graph) -> bool:
    """Return ``True`` if the edge bounds from Euler's formula prove that the graph is not planar.

    ``False`` does NOT mean "planar" - it only means that the bounds cannot
    decide (example: the Petersen graph).

    Raises:
        ValueError: If the graph is directed.
    """
    _require_undirected(graph, "is_certainly_nonplanar")
    n = graph.num_vertices()
    m = graph.num_edges()
    if n < 3:
        # Graphs with at most 2 vertices are always planar; the bounds
        # are only stated for n >= 3.
        return False
    # Bound 1: every simple planar graph with n >= 3 has m <= 3n - 6.
    if m > 3 * n - 6:
        return True
    # Bound 2: a triangle-free planar graph with n >= 3 has m <= 2n - 4
    # (every face is then bounded by at least 4 edges: 4f <= 2m).
    if not has_triangle(graph) and m > 2 * n - 4:
        return True
    # Both necessary conditions hold - the graph may or may not be planar.
    return False


# ----------------------------------------------------------------------
# Part B: complexity
# ----------------------------------------------------------------------


def hamiltonian_cycle_bruteforce(graph: Graph) -> tuple[list[Vertex] | None, int]:
    """Search a Hamiltonian cycle by trying all vertex orders.

    Returns:
        ``(cycle, checked)``: the first Hamiltonian cycle found as
        ``[v0, v1, ..., v0]`` (or ``None``) and the number of permutations
        that were checked.

    Raises:
        ValueError: If the graph is directed.
    """
    _require_undirected(graph, "hamiltonian_cycle_bruteforce")
    vertices = graph.vertices()
    if len(vertices) < 3:
        # A simple graph needs at least 3 vertices for a cycle.
        return None, 0

    # Every cycle passes through every vertex, so we may fix the start v0.
    # The remaining n - 1 vertices can be arranged in (n-1)! orders.
    first, rest = vertices[0], vertices[1:]
    checked = 0
    for order in itertools.permutations(rest):
        checked += 1
        cycle = [first, *order, first]
        # Check whether all consecutive pairs are edges. all() stops at the
        # first missing edge - this only makes the check of ONE permutation
        # faster, the number of permutations stays (n-1)! in the worst case.
        if all(graph.has_edge(cycle[i], cycle[i + 1]) for i in range(len(cycle) - 1)):
            return cycle, checked
    return None, checked


def number_of_hamiltonian_cycles_complete(n: int) -> int:
    """Return the number of distinct Hamiltonian cycles in ``K_n``.

    Raises:
        ValueError: If ``n`` is negative.
    """
    if n < 0:
        raise ValueError("n must not be negative")
    if n < 3:
        return 0
    # Fix the start vertex: (n-1)! orders of the others. Every cycle is
    # counted twice (once in each direction), hence the division by 2.
    return math.factorial(n - 1) // 2


# Convention: the most precise class known today, assuming P != NP.
# "P" is also used for optimisation problems that can be solved in
# polynomial time; "NP-schwer" for problems that are NP-hard but are not
# decision problems in NP (e.g. the optimisation version of TSP).
COMPLEXITY_CLASSES: dict[str, str] = {
    "Eulerkreis: Besitzt der Graph einen Eulerkreis?": "P",
    "Hamiltonkreis: Besitzt der Graph einen Hamiltonkreis?": "NP-vollständig",
    "Kürzester Weg zwischen zwei Knoten (nichtnegative Gewichte) finden": "P",
    "Minimalen Spannbaum finden": "P",
    "2-Färbbarkeit: Ist der Graph mit 2 Farben färbbar?": "P",
    "3-Färbbarkeit: Ist der Graph mit 3 Farben färbbar?": "NP-vollständig",
    "Maximales Matching in einem bipartiten Graphen finden": "P",
    "Maximalen Fluss in einem Netzwerk finden": "P",
    "Clique: Gibt es eine Clique mit k Knoten (k ist Teil der Eingabe)?": "NP-vollständig",
    "Planarität: Ist der Graph planar?": "P",
    "TSP-Entscheidung: Gibt es eine Rundreise mit Länge höchstens L?": "NP-vollständig",
    "TSP-Optimierung: Kürzeste Rundreise finden": "NP-schwer",
}


def runtime_experiment(sizes: Iterable[int], seed: int = 0) -> list[tuple[int, float]]:
    """OPTIONAL: Measure ``hamiltonian_cycle_bruteforce`` on graphs without Hamiltonian cycle.

    For every ``n`` in ``sizes`` a random tree with ``n`` vertices is built
    (a tree has no cycle at all, so the search must try every permutation).

    Returns:
        A list of pairs ``(n, seconds)`` in the order of ``sizes``.
    """
    results: list[tuple[int, float]] = []
    for n in sizes:
        # Different seed per size, but reproducible.
        tree = random_tree(n, seed=seed + n)
        # repeat=1: the large sizes take long enough already.
        seconds = measure_time(hamiltonian_cycle_bruteforce, tree, repeat=1)
        results.append((n, seconds))
    return results


# ----------------------------------------------------------------------
# Demonstration
# ----------------------------------------------------------------------
if __name__ == "__main__":
    print("=== Euler's formula: f = m - n + 1 + c ===")
    examples = [
        ("K4", 4, 6, 1),
        ("cube", 8, 12, 1),
        ("3 x 3 grid", 9, 12, 1),
        ("tree with 5 vertices", 5, 4, 1),
        ("two disjoint triangles", 6, 6, 2),
    ]
    for name, n, m, c in examples:
        print(f"  {name:<24} n={n:>2}, m={m:>2}, c={c}  ->  f = {faces_by_euler_formula(n, m, c)}")

    print("\n=== Maximum number of edges of a simple planar graph ===")
    print("  " + ", ".join(f"n={n}: {max_planar_edges(n)}" for n in range(0, 9)))

    print("\n=== Edge bounds as a planarity filter ===")
    candidates = [
        ("K4", complete_graph(4)),
        ("K5", complete_graph(5)),
        ("K3,3", complete_bipartite_graph(3, 3)),
        ("K2,5", complete_bipartite_graph(2, 5)),
        ("Petersen", petersen_graph()),
        ("4 x 4 grid", grid_graph(4, 4)),
        ("C7", cycle_graph(7)),
    ]
    for name, graph in candidates:
        n, m = graph.num_vertices(), graph.num_edges()
        verdict = "certainly NOT planar" if is_certainly_nonplanar(graph) else "bounds cannot decide"
        print(
            f"  {name:<11} n={n:>2}, m={m:>2}, 3n-6={3 * n - 6:>2}, "
            f"triangle={str(has_triangle(graph)):<5} -> {verdict}"
        )
    print("  (Petersen: bounds cannot decide, but it is NOT planar - Kuratowski/Wagner!)")

    print("\n=== Brute-force search for Hamiltonian cycles ===")
    for name, graph in [("K5", complete_graph(5)), ("C6", cycle_graph(6)), ("K2,3", complete_bipartite_graph(2, 3))]:
        cycle, checked = hamiltonian_cycle_bruteforce(graph)
        shown = format_path(cycle) if cycle is not None else "(kein Hamiltonkreis)"
        print(f"  {name:<5} cycle: {shown:<32} permutations checked: {checked}")
    cycle, checked = hamiltonian_cycle_bruteforce(petersen_graph())
    print(f"  Petersen: cycle {cycle}, permutations checked: {checked} = 9!")

    print("\n=== Factorials explode: (n-1)! orders, (n-1)!/2 cycles in K_n ===")
    print(f"  {'n':>3} {'(n-1)!/2 cycles':>28} {'time at 10^9 perm/s':>22}")
    for n in [5, 10, 15, 20, 25]:
        seconds = math.factorial(n - 1) / 1e9
        years = seconds / (365.25 * 24 * 3600)
        when = f"{seconds:.3g} s" if years < 1 else f"{years:.3g} years"
        print(f"  {n:>3} {number_of_hamiltonian_cycles_complete(n):>28,} {when:>22}")

    print("\n=== Runtime experiment (random trees: no Hamiltonian cycle) ===")
    previous = None
    for n, seconds in runtime_experiment(range(5, 10)):
        factor = f"x{seconds / previous:5.1f}" if previous else ""
        print(f"  n={n}: {seconds:9.5f} s  {factor}")
        previous = seconds

    print("\n=== Complexity classes (assuming P != NP) ===")
    width = max(len(problem) for problem in COMPLEXITY_CLASSES)
    for problem, label in COMPLEXITY_CLASSES.items():
        print(f"  {problem:<{width}}  {label}")

    # Pictures in the browser (no extra packages needed).
    pictures = []
    for name, graph, options in [
        ("K5", complete_graph(5), {"layout": "circular"}),
        ("K3,3", complete_bipartite_graph(3, 3), {"left": ["L0", "L1", "L2"]}),
        ("Petersen graph", petersen_graph(), {"shells": [range(5), range(5, 10)]}),
    ]:
        n, m = graph.num_vertices(), graph.num_edges()
        if is_certainly_nonplanar(graph):
            bound = 3 * n - 6 if has_triangle(graph) else 2 * n - 4
            verdict = f"m = {m} > {bound}: certainly not planar"
        else:
            verdict = f"m = {m}: the bounds cannot decide"
        pictures.append(snapshot(graph, f"{name}: {verdict}", **options))
    show(*pictures, title="Unit 9: results")
    print("Step by step: python exercises/09_planarity_complexity/demo_animation.py")
