"""Tests for unit 9 (planarity and complexity).

By default these tests check ``task.py``. Use ``pytest --impl=demo`` to check
``demo_solution.py`` instead.
"""

import itertools
import math

import pytest

from lib.generators import (
    complete_bipartite_graph,
    complete_graph,
    cycle_graph,
    grid_graph,
    path_graph,
    petersen_graph,
    random_graph,
    random_tree,
    star_graph,
)
from lib.graph import Graph
from lib.testing import assert_valid_hamiltonian_cycle, load_implementation, skip_if_not_implemented

impl = load_implementation(__file__)


def two_triangles() -> Graph:
    """Two disjoint triangles: 6 vertices, 6 edges, 2 components."""
    return Graph.from_edges([(1, 2), (2, 3), (3, 1), (4, 5), (5, 6), (6, 4)])


# ----------------------------------------------------------------------
# Euler's formula
# ----------------------------------------------------------------------
@pytest.mark.parametrize(
    ("n", "m", "c", "faces"),
    [
        (4, 6, 1, 4),  # K4: three inner triangles + outer face
        (8, 12, 1, 6),  # cube
        (9, 12, 1, 5),  # 3 x 3 grid: four squares + outer face
        (5, 4, 1, 1),  # tree: only the outer face
        (1, 0, 1, 1),  # a single vertex
        (3, 3, 1, 2),  # triangle
        (6, 6, 2, 3),  # two disjoint triangles: two inner faces + ONE outer face
        (6, 4, 2, 1),  # forest with two trees
        (5, 0, 5, 1),  # five isolated vertices
    ],
)
def test_faces_by_euler_formula(n: int, m: int, c: int, faces: int) -> None:
    assert impl.faces_by_euler_formula(n, m, c) == faces


def test_faces_default_is_connected() -> None:
    assert impl.faces_by_euler_formula(4, 6) == 4
    assert impl.faces_by_euler_formula(10, 9) == 1


@pytest.mark.parametrize(
    ("n", "m", "c"),
    [
        (0, 0, 1),  # no vertex
        (-1, 0, 1),
        (3, -1, 1),  # negative number of edges
        (3, 3, 0),  # no component
        (2, 0, 3),  # more components than vertices
        (4, 1, 1),  # 4 vertices, 1 edge cannot be connected
    ],
)
def test_faces_invalid_input(n: int, m: int, c: int) -> None:
    with pytest.raises(ValueError):
        impl.faces_by_euler_formula(n, m, c)


# ----------------------------------------------------------------------
# Edge bound
# ----------------------------------------------------------------------
@pytest.mark.parametrize(
    ("n", "expected"),
    [(0, 0), (1, 0), (2, 1), (3, 3), (4, 6), (5, 9), (6, 12), (10, 24), (100, 294)],
)
def test_max_planar_edges(n: int, expected: int) -> None:
    assert impl.max_planar_edges(n) == expected


def test_max_planar_edges_negative() -> None:
    with pytest.raises(ValueError):
        impl.max_planar_edges(-1)


# ----------------------------------------------------------------------
# Triangles
# ----------------------------------------------------------------------
@pytest.mark.parametrize(
    ("graph", "expected"),
    [
        (complete_graph(3), True),
        (complete_graph(4), True),
        (cycle_graph(4), False),
        (cycle_graph(5), False),
        (petersen_graph(), False),
        (complete_bipartite_graph(3, 3), False),
        (grid_graph(3, 4), False),
        (path_graph(6), False),
        (star_graph(5), False),
        (Graph(), False),
        (path_graph(1), False),
        (two_triangles(), True),
    ],
)
def test_has_triangle(graph: Graph, expected: bool) -> None:
    assert impl.has_triangle(graph) is expected


def test_has_triangle_in_second_component() -> None:
    graph = Graph.from_edges([("a", "b"), ("b", "c"), ("x", "y"), ("y", "z"), ("z", "x")])
    assert impl.has_triangle(graph) is True


@pytest.mark.parametrize("seed", range(8))
def test_has_triangle_random(seed: int) -> None:
    graph = random_graph(9, 0.25, seed=seed)
    # Obviously correct reference: try all triples of vertices.
    expected = any(
        graph.has_edge(a, b) and graph.has_edge(b, c) and graph.has_edge(a, c)
        for a, b, c in itertools.combinations(graph.vertices(), 3)
    )
    assert impl.has_triangle(graph) is expected


def test_has_triangle_rejects_directed() -> None:
    with pytest.raises(ValueError):
        impl.has_triangle(Graph.from_edges([(1, 2), (2, 3), (3, 1)], directed=True))


# ----------------------------------------------------------------------
# Planarity filter
# ----------------------------------------------------------------------
@pytest.mark.parametrize("n", [5, 6, 7, 8, 10])
def test_complete_graphs_from_5_are_nonplanar(n: int) -> None:
    assert impl.is_certainly_nonplanar(complete_graph(n)) is True


@pytest.mark.parametrize(("a", "b"), [(3, 3), (3, 4), (4, 4), (3, 5)])
def test_complete_bipartite_nonplanar(a: int, b: int) -> None:
    assert impl.is_certainly_nonplanar(complete_bipartite_graph(a, b)) is True


@pytest.mark.parametrize(
    "graph",
    [
        Graph(),
        path_graph(1),
        path_graph(2),
        complete_graph(3),
        complete_graph(4),  # planar, attains m = 3n - 6
        complete_bipartite_graph(2, 5),  # planar, attains m = 2n - 4
        cycle_graph(3),
        cycle_graph(4),
        cycle_graph(9),
        grid_graph(2, 2),
        grid_graph(4, 5),
        path_graph(7),
        star_graph(6),
        random_tree(12, seed=3),
        random_tree(30, seed=7),
    ],
)
def test_planar_graphs_are_not_flagged(graph: Graph) -> None:
    assert impl.is_certainly_nonplanar(graph) is False


def test_petersen_bounds_cannot_decide() -> None:
    # Not planar, but both edge bounds hold: False means "cannot decide".
    assert impl.is_certainly_nonplanar(petersen_graph()) is False


def test_isolated_vertices_hide_k5() -> None:
    # K5 plus two isolated vertices: n = 7, m = 10 <= 15. The bound alone
    # cannot see the K5 any more - another example of "False != planar".
    graph = complete_graph(5)
    graph.add_vertices(["Pippi", "Annika"])
    assert impl.is_certainly_nonplanar(graph) is False


def test_nonplanar_rejects_directed() -> None:
    with pytest.raises(ValueError):
        impl.is_certainly_nonplanar(Graph(directed=True))


def test_nonplanar_does_not_modify_graph() -> None:
    graph = complete_bipartite_graph(3, 3)
    before = graph.copy()
    impl.is_certainly_nonplanar(graph)
    assert graph == before


# ----------------------------------------------------------------------
# Brute-force Hamiltonian cycles
# ----------------------------------------------------------------------
@pytest.mark.parametrize(
    "graph",
    [
        complete_graph(3),
        complete_graph(5),
        cycle_graph(6),
        complete_bipartite_graph(3, 3),
        grid_graph(2, 3),
        Graph.from_edges([("A", "B"), ("B", "C"), ("C", "D"), ("D", "A"), ("A", "C")]),
    ],
)
def test_hamiltonian_cycle_found(graph: Graph) -> None:
    cycle, checked = impl.hamiltonian_cycle_bruteforce(graph)
    assert_valid_hamiltonian_cycle(graph, cycle)
    assert cycle[0] == graph.vertices()[0]
    assert 1 <= checked <= math.factorial(graph.num_vertices() - 1)


@pytest.mark.parametrize(
    ("graph", "expected_count"),
    [
        (path_graph(3), 2),  # 2! permutations
        (path_graph(5), 24),  # 4!
        (star_graph(4), 24),  # 5 vertices
        (complete_bipartite_graph(2, 3), 24),  # unbalanced bipartite graph
        (grid_graph(3, 3), 40320),  # 9 vertices, bipartite 5 + 4: 8!
        (two_triangles(), 120),  # disconnected: 5!
        (random_tree(7, seed=2), 720),  # trees have no cycles: 6!
        (
            Graph.from_edges([("Tommy", "Annika"), ("Annika", "Pippi"), ("Pippi", "Tommy"), ("Pippi", "Herr Nilsson")]),
            6,
        ),
    ],
)
def test_no_hamiltonian_cycle_checks_all_permutations(graph: Graph, expected_count: int) -> None:
    assert impl.hamiltonian_cycle_bruteforce(graph) == (None, expected_count)


def test_petersen_has_no_hamiltonian_cycle() -> None:
    assert impl.hamiltonian_cycle_bruteforce(petersen_graph()) == (None, 362880)  # 9!


@pytest.mark.parametrize("graph", [Graph(), path_graph(1), path_graph(2)])
def test_hamiltonian_small_graphs(graph: Graph) -> None:
    assert impl.hamiltonian_cycle_bruteforce(graph) == (None, 0)


def test_hamiltonian_rejects_directed() -> None:
    with pytest.raises(ValueError):
        impl.hamiltonian_cycle_bruteforce(cycle_graph(4, directed=True))


def test_hamiltonian_does_not_modify_graph() -> None:
    graph = complete_graph(5)
    before = graph.copy()
    impl.hamiltonian_cycle_bruteforce(graph)
    assert graph == before


# ----------------------------------------------------------------------
# Counting Hamiltonian cycles of K_n
# ----------------------------------------------------------------------
@pytest.mark.parametrize(
    ("n", "expected"),
    [(0, 0), (1, 0), (2, 0), (3, 1), (4, 3), (5, 12), (6, 60), (10, 181440), (20, 60822550204416000)],
)
def test_number_of_hamiltonian_cycles_complete(n: int, expected: int) -> None:
    assert impl.number_of_hamiltonian_cycles_complete(n) == expected


@pytest.mark.parametrize("n", [3, 4, 5, 6])
def test_number_of_hamiltonian_cycles_by_enumeration(n: int) -> None:
    # Obviously correct reference: list every cycle of K_n as its edge set.
    cycles = set()
    for order in itertools.permutations(range(1, n)):
        cycle = [0, *order, 0]
        cycles.add(frozenset(frozenset(cycle[i : i + 2]) for i in range(n)))
    assert impl.number_of_hamiltonian_cycles_complete(n) == len(cycles)


def test_number_of_hamiltonian_cycles_negative() -> None:
    with pytest.raises(ValueError):
        impl.number_of_hamiltonian_cycles_complete(-3)


# ----------------------------------------------------------------------
# Complexity classes
# ----------------------------------------------------------------------
EXPECTED_CLASSES = {
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

VALID_LABELS = {"P", "NP-vollständig", "NP-schwer"}


def filled_complexity_classes() -> dict[str, str]:
    """Return ``impl.COMPLEXITY_CLASSES``; treat remaining "TODO" entries as not implemented."""
    classes = impl.COMPLEXITY_CLASSES
    if any(label == "TODO" for label in classes.values()):
        raise NotImplementedError("TODO: fill in COMPLEXITY_CLASSES")
    return classes


def test_complexity_classes_keys_unchanged() -> None:
    classes = filled_complexity_classes()
    assert set(classes) == set(EXPECTED_CLASSES), "Do not change, add or remove the problem descriptions"


def test_complexity_classes_valid_labels() -> None:
    classes = filled_complexity_classes()
    for problem, label in classes.items():
        assert label in VALID_LABELS, f"{problem!r}: {label!r} is not one of {sorted(VALID_LABELS)}"


@pytest.mark.parametrize("problem", list(EXPECTED_CLASSES))
def test_complexity_class(problem: str) -> None:
    classes = filled_complexity_classes()
    assert classes[problem] == EXPECTED_CLASSES[problem], problem


# ----------------------------------------------------------------------
# Optional: runtime experiment
# ----------------------------------------------------------------------
@skip_if_not_implemented
def test_runtime_experiment_format() -> None:
    result = impl.runtime_experiment([3, 4, 5, 6, 7], seed=1)
    assert [n for n, _ in result] == [3, 4, 5, 6, 7]
    for _n, seconds in result:
        assert isinstance(seconds, float)
        assert seconds >= 0


@skip_if_not_implemented
def test_runtime_experiment_empty() -> None:
    assert impl.runtime_experiment([]) == []
