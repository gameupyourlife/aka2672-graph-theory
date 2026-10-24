"""Tests for unit 1 (graph basics).

By default these tests check ``task.py``. Use ``pytest --impl=demo`` to check
``demo_solution.py`` instead.
"""

import pytest

from lib.generators import complete_graph, cycle_graph, path_graph, random_graph
from lib.graph import Graph
from lib.testing import load_implementation, skip_if_not_implemented

impl = load_implementation(__file__)

EXPECTED_FOOTPATHS = {
    frozenset(pair)
    for pair in [
        ("Nordhof", "Mittelhof"),
        ("Mittelhof", "Südhof"),
        ("Nordhof", "Südhof"),
        ("Mittelhof", "Schule"),
        ("Schule", "Kaufladen"),
        ("Kaufladen", "Badestelle"),
        ("Südhof", "Badestelle"),
        ("Badestelle", "Erdbeerstelle"),
        ("Nordhof", "Erdbeerstelle"),
    ]
}

EXPECTED_LETTERS = {
    ("Lisa", "Britta"),
    ("Lisa", "Inga"),
    ("Britta", "Lisa"),
    ("Inga", "Britta"),
    ("Lasse", "Ole"),
    ("Bosse", "Lasse"),
    ("Ole", "Bosse"),
    ("Lasse", "Lisa"),
}


@pytest.fixture
def small() -> Graph:
    """A - B - C plus the isolated vertex D."""
    return Graph.from_edges([("A", "B"), ("B", "C")], vertices=["D"])


# ----------------------------------------------------------------------
# Modelling
# ----------------------------------------------------------------------
def test_bullerby_graph() -> None:
    graph = impl.build_bullerby_graph()
    assert isinstance(graph, Graph)
    assert not graph.directed
    assert graph.num_vertices() == 7
    assert {frozenset((u, v)) for u, v, _ in graph.edges()} == EXPECTED_FOOTPATHS


def test_letter_graph() -> None:
    graph = impl.build_letter_graph()
    assert graph.directed
    assert {(u, v) for u, v, _ in graph.edges()} == EXPECTED_LETTERS
    assert set(graph.vertices()) == {"Lisa", "Britta", "Inga", "Lasse", "Ole", "Bosse"}


# ----------------------------------------------------------------------
# Degrees
# ----------------------------------------------------------------------
def test_degrees_small(small: Graph) -> None:
    assert impl.degrees(small) == {"A": 1, "B": 2, "C": 1, "D": 0}


def test_degrees_empty_graph() -> None:
    assert impl.degrees(Graph()) == {}


@pytest.mark.parametrize("seed", range(5))
def test_degrees_match_library(seed: int) -> None:
    graph = random_graph(15, 0.3, seed=seed)
    expected = {v: graph.degree(v) for v in graph}
    assert impl.degrees(graph) == expected


def test_degrees_directed_are_in_plus_out() -> None:
    graph = Graph.from_edges([("x", "y"), ("y", "x"), ("x", "z")], directed=True)
    assert impl.degrees(graph) == {"x": 3, "y": 2, "z": 1}


def test_degrees_of_bullerby() -> None:
    graph = impl.build_bullerby_graph()
    assert impl.degrees(graph) == {v: graph.degree(v) for v in graph}


def test_degree_sequence(small: Graph) -> None:
    assert impl.degree_sequence(small) == [2, 1, 1, 0]
    assert impl.degree_sequence(complete_graph(4)) == [3, 3, 3, 3]
    assert impl.degree_sequence(Graph()) == []


def test_odd_degree_vertices(small: Graph) -> None:
    assert impl.odd_degree_vertices(small) == ["A", "C"]
    assert impl.odd_degree_vertices(cycle_graph(5)) == []


@pytest.mark.parametrize("seed", range(10))
def test_number_of_odd_vertices_is_even(seed: int) -> None:
    graph = random_graph(12, 0.4, seed=seed)
    assert len(impl.odd_degree_vertices(graph)) % 2 == 0


# ----------------------------------------------------------------------
# Handshake lemma
# ----------------------------------------------------------------------
@pytest.mark.parametrize(
    "graph",
    [Graph(), path_graph(1), path_graph(6), cycle_graph(7), complete_graph(6), random_graph(20, 0.2, seed=1)],
)
def test_handshake_lemma_holds(graph: Graph) -> None:
    assert impl.check_handshake_lemma(graph) is True


def test_handshake_lemma_rejects_directed_graph() -> None:
    with pytest.raises(ValueError):
        impl.check_handshake_lemma(Graph(directed=True))


# ----------------------------------------------------------------------
# Directed degrees
# ----------------------------------------------------------------------
def test_in_and_out_degrees_example() -> None:
    graph = Graph.from_edges([("x", "y"), ("y", "z"), ("x", "z")], directed=True)
    assert impl.in_and_out_degrees(graph) == {"x": (0, 2), "y": (1, 1), "z": (2, 0)}


def test_in_and_out_degrees_letters() -> None:
    graph = impl.build_letter_graph()
    result = impl.in_and_out_degrees(graph)
    assert result == {v: (graph.in_degree(v), graph.out_degree(v)) for v in graph}
    assert sum(i for i, _ in result.values()) == graph.num_edges()
    assert sum(o for _, o in result.values()) == graph.num_edges()


def test_in_and_out_degrees_rejects_undirected_graph(small: Graph) -> None:
    with pytest.raises(ValueError):
        impl.in_and_out_degrees(small)


# ----------------------------------------------------------------------
# Adjacency matrix
# ----------------------------------------------------------------------
def test_adjacency_matrix_example(small: Graph) -> None:
    assert impl.adjacency_matrix(small, order=["A", "B", "C", "D"]) == [
        [0, 1, 0, 0],
        [1, 0, 1, 0],
        [0, 1, 0, 0],
        [0, 0, 0, 0],
    ]


def test_adjacency_matrix_default_order() -> None:
    graph = path_graph(3)
    assert impl.adjacency_matrix(graph) == [[0, 1, 0], [1, 0, 1], [0, 1, 0]]


def test_adjacency_matrix_directed() -> None:
    graph = Graph.from_edges([("a", "b"), ("b", "c")], directed=True)
    assert impl.adjacency_matrix(graph, ["c", "b", "a"]) == [[0, 0, 0], [1, 0, 0], [0, 1, 0]]


def test_adjacency_matrix_rows_are_independent() -> None:
    matrix = impl.adjacency_matrix(path_graph(3))
    matrix[0][0] = 99
    assert matrix[1][0] == 1 and matrix[2][0] == 0


def test_adjacency_matrix_empty_graph() -> None:
    assert impl.adjacency_matrix(Graph()) == []


@pytest.mark.parametrize("order", [["A", "B", "C"], ["A", "B", "C", "D", "E"], ["A", "A", "B", "C"]])
def test_adjacency_matrix_invalid_order(small: Graph, order: list[str]) -> None:
    with pytest.raises(ValueError):
        impl.adjacency_matrix(small, order)


# ----------------------------------------------------------------------
# Optional: complement
# ----------------------------------------------------------------------
@skip_if_not_implemented
def test_complement() -> None:
    graph = path_graph(4)
    result = impl.complement(graph)
    assert set(result.vertices()) == {0, 1, 2, 3}
    assert {frozenset((u, v)) for u, v, _ in result.edges()} == {
        frozenset((0, 2)),
        frozenset((0, 3)),
        frozenset((1, 3)),
    }
    assert graph.num_edges() == 3  # the input is not modified


@skip_if_not_implemented
def test_complement_edge_count() -> None:
    graph = random_graph(10, 0.3, seed=5)
    result = impl.complement(graph)
    assert graph.num_edges() + result.num_edges() == 10 * 9 // 2
