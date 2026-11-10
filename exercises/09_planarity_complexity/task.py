"""Einheit 9 – Planarität und Komplexität.

Bearbeite die TODOs direkt an den Funktionen. Ersetze dort jeweils
``raise NotImplementedError(...)`` durch deinen Code.

Ordne außerdem jedem Problem in `COMPLEXITY_CLASSES` ein Label zu.

Starte die Tests im Projektordner mit diesem Befehl.

    python -m pytest exercises/09_planarity_complexity
"""

import itertools  # you will need itertools.permutations
import math  # you will need math.factorial
import sys
from collections.abc import Iterable
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))  # find ``lib``

from lib.generators import complete_bipartite_graph, complete_graph, petersen_graph, random_tree
from lib.graph import Graph, Vertex
from lib.utils import format_path, measure_time

# ----------------------------------------------------------------------
# Part A: planarity
# ----------------------------------------------------------------------


def faces_by_euler_formula(num_vertices: int, num_edges: int, num_components: int = 1) -> int:
    """Return the number of faces ``f`` of a plane embedding of a graph.

    Euler's formula for a plane graph with ``n`` vertices, ``m`` edges,
    ``f`` faces and ``c`` connected components reads ``n - m + f = 1 + c``.
    Hence ``f = m - n + 1 + c``.

    Raises:
        ValueError: If ``num_vertices < 1``, ``num_edges < 0``,
            ``num_components < 1``, ``num_components > num_vertices`` or
            ``num_edges < num_vertices - num_components`` (no graph with
            these numbers exists).
    """
    # TODO: Step 1 - check the arguments in the order listed above.
    # TODO: Step 2 - solve Euler's formula for f.
    raise NotImplementedError("TODO: faces_by_euler_formula")


def max_planar_edges(num_vertices: int) -> int:
    """Return the maximum number of edges of a simple planar graph with ``num_vertices`` vertices.

    This is ``3n - 6`` for ``n >= 3``, ``0`` for ``n = 0`` or ``n = 1`` and
    ``1`` for ``n = 2``.

    Raises:
        ValueError: If ``num_vertices`` is negative.
    """
    # TODO: Treat the small cases n <= 2 separately.
    raise NotImplementedError("TODO: max_planar_edges")


def has_triangle(graph: Graph) -> bool:
    """Return ``True`` if the undirected graph contains a triangle (a cycle of length 3).

    Raises:
        ValueError: If the graph is directed.
    """
    # TODO: Step 1 - raise a ValueError for directed graphs.
    # TODO: Step 2 - for every edge {u, v}: do u and v have a common neighbour?
    raise NotImplementedError("TODO: has_triangle")


def is_certainly_nonplanar(graph: Graph) -> bool:
    """Return ``True`` if the edge bounds from Euler's formula prove that the graph is not planar.

    With ``n`` vertices and ``m`` edges (and ``n >= 3``) the function returns
    ``True`` if

    * ``m > 3n - 6``, or
    * the graph has no triangle and ``m > 2n - 4``.

    In all other cases (including ``n < 3``) it returns ``False``.

    Important: ``False`` does NOT mean "the graph is planar". It only means
    that these necessary conditions cannot decide the question (example:
    the Petersen graph satisfies both bounds but is not planar).

    Raises:
        ValueError: If the graph is directed.
    """
    # TODO: Step 1 - raise a ValueError for directed graphs.
    # TODO: Step 2 - graphs with fewer than 3 vertices: return False.
    # TODO: Step 3 - check the bound m <= 3n - 6.
    # TODO: Step 4 - if there is no triangle, check the bound m <= 2n - 4.
    raise NotImplementedError("TODO: is_certainly_nonplanar")


# ----------------------------------------------------------------------
# Part B: complexity
# ----------------------------------------------------------------------


def hamiltonian_cycle_bruteforce(graph: Graph) -> tuple[list[Vertex] | None, int]:
    """Search a Hamiltonian cycle by trying all vertex orders (brute force).

    The first vertex ``v0`` of ``graph.vertices()`` is fixed as start. All
    permutations of the other ``n - 1`` vertices are tried one after the
    other (e.g. with ``itertools.permutations``) until one of them forms a
    cycle ``v0, ..., v0`` in the graph. Leave the input graph unchanged and
    try the function only on small graphs (around 10 vertices or fewer).

    Returns:
        A pair ``(cycle, checked)``:

        * ``cycle`` - the first Hamiltonian cycle found as a list
          ``[v0, v1, ..., v_{n-1}, v0]``, or ``None`` if there is none,
        * ``checked`` - the number of permutations that were checked
          (including the successful one). For a graph without Hamiltonian
          cycle this is exactly ``(n-1)!``.

        For graphs with fewer than 3 vertices the result is ``(None, 0)``.

    Raises:
        ValueError: If the graph is directed.
    """
    # TODO: Step 1 - raise a ValueError for directed graphs; handle n < 3.
    # TODO: Step 2 - fix the first vertex, loop over all permutations of the rest.
    # TODO: Step 3 - count every permutation; build [first, *order, first]
    #                and check whether all consecutive pairs are edges.
    raise NotImplementedError("TODO: hamiltonian_cycle_bruteforce")


def number_of_hamiltonian_cycles_complete(n: int) -> int:
    """Return the number of distinct Hamiltonian cycles in the complete graph ``K_n``.

    Two cycles are the same if they use the same edges (start vertex and
    direction do not matter). The result is ``(n-1)! / 2`` for ``n >= 3``
    and ``0`` for ``n < 3``.

    Raises:
        ValueError: If ``n`` is negative.
    """
    # TODO: Use math.factorial and integer division //.
    raise NotImplementedError("TODO: number_of_hamiltonian_cycles_complete")


# Ersetze jedes "TODO" durch "P", "NP-vollständig" oder "NP-schwer".
# Lass die Schlüssel unverändert und wähle unter der Annahme P != NP
# das präziseste Label. Verwende "P" auch für Optimierungsprobleme,
# die du in Polynomialzeit lösen kannst, und "NP-schwer" für NP-schwere
# Probleme, die keine Entscheidungsprobleme in NP sind.
COMPLEXITY_CLASSES: dict[str, str] = {
    "Eulerkreis: Besitzt der Graph einen Eulerkreis?": "TODO",
    "Hamiltonkreis: Besitzt der Graph einen Hamiltonkreis?": "TODO",
    "Kürzester Weg zwischen zwei Knoten (nichtnegative Gewichte) finden": "TODO",
    "Minimalen Spannbaum finden": "TODO",
    "2-Färbbarkeit: Ist der Graph mit 2 Farben färbbar?": "TODO",
    "3-Färbbarkeit: Ist der Graph mit 3 Farben färbbar?": "TODO",
    "Maximales Matching in einem bipartiten Graphen finden": "TODO",
    "Maximalen Fluss in einem Netzwerk finden": "TODO",
    "Clique: Gibt es eine Clique mit k Knoten (k ist Teil der Eingabe)?": "TODO",
    "Planarität: Ist der Graph planar?": "TODO",
    "TSP-Entscheidung: Gibt es eine Rundreise mit Länge höchstens L?": "TODO",
    "TSP-Optimierung: Kürzeste Rundreise finden": "TODO",
}


def runtime_experiment(sizes: Iterable[int], seed: int = 0) -> list[tuple[int, float]]:
    """OPTIONAL: Measure ``hamiltonian_cycle_bruteforce`` on graphs without Hamiltonian cycle.

    For every ``n`` in ``sizes`` build a graph with ``n`` vertices that has
    no Hamiltonian cycle (e.g. ``random_tree(n, seed=seed + n)`` - a tree
    has no cycle at all), so the search has to try all ``(n-1)!``
    permutations. Measure the time with ``measure_time`` from ``lib.utils``.

    Returns:
        A list of pairs ``(n, seconds)`` in the order of ``sizes``.
    """
    # TODO (optional): measure_time(hamiltonian_cycle_bruteforce, graph, repeat=1)
    raise NotImplementedError("TODO (optional): runtime_experiment")


if __name__ == "__main__":
    print("Faces of K4:", faces_by_euler_formula(4, 6))
    print("Max. edges of a planar graph with 5 vertices:", max_planar_edges(5))
    for name, graph in [("K4", complete_graph(4)), ("K5", complete_graph(5)),
                        ("K3,3", complete_bipartite_graph(3, 3)), ("Petersen", petersen_graph())]:
        print(f"{name}: triangle={has_triangle(graph)}, certainly non-planar={is_certainly_nonplanar(graph)}")
    cycle, checked = hamiltonian_cycle_bruteforce(complete_graph(5))
    print("Hamiltonian cycle in K5:", format_path(cycle), "- permutations checked:", checked)
    print("Hamiltonian cycle in a tree:", hamiltonian_cycle_bruteforce(random_tree(6, seed=1)))
    for n in range(3, 11):
        print(f"K_{n} has {number_of_hamiltonian_cycles_complete(n)} Hamiltonian cycles")
    for problem, label in COMPLEXITY_CLASSES.items():
        print(f"{problem}: {label}")
