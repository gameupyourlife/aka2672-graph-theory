"""Tests for the validation helpers, the visualisation and the utilities."""

import pytest

from lib import testing, utils, visualization
from lib.generators import complete_graph, cycle_graph, path_graph, petersen_graph
from lib.graph import Graph


# ----------------------------------------------------------------------
# lib.testing
# ----------------------------------------------------------------------
def test_assert_valid_path() -> None:
    graph = path_graph(4)
    testing.assert_valid_path(graph, [0, 1, 2], start=0, end=2)
    testing.assert_valid_path(graph, [3])
    with pytest.raises(AssertionError):
        testing.assert_valid_path(graph, [0, 2])  # no edge
    with pytest.raises(AssertionError):
        testing.assert_valid_path(graph, [0, 1, 0])  # repeated vertex
    with pytest.raises(AssertionError):
        testing.assert_valid_path(graph, [])
    with pytest.raises(AssertionError):
        testing.assert_valid_path(graph, [1, 2], start=0)


def test_assert_valid_path_respects_direction() -> None:
    graph = path_graph(3, directed=True)
    testing.assert_valid_path(graph, [0, 1, 2])
    with pytest.raises(AssertionError):
        testing.assert_valid_path(graph, [2, 1, 0])


def test_euler_circuit_check() -> None:
    graph = cycle_graph(4)
    testing.assert_valid_euler_circuit(graph, [0, 1, 2, 3, 0])
    with pytest.raises(AssertionError):
        testing.assert_valid_euler_circuit(graph, [0, 1, 2, 3])
    with pytest.raises(AssertionError):
        testing.assert_valid_euler_circuit(graph, [0, 1, 0, 1, 0])
    testing.assert_valid_euler_trail(path_graph(3), [0, 1, 2])
    testing.assert_valid_euler_circuit(Graph(), [])


def test_hamiltonian_cycle_check() -> None:
    graph = complete_graph(4)
    testing.assert_valid_hamiltonian_cycle(graph, [0, 2, 1, 3, 0])
    with pytest.raises(AssertionError):
        testing.assert_valid_hamiltonian_cycle(graph, [0, 1, 2, 0])
    with pytest.raises(AssertionError):
        testing.assert_valid_hamiltonian_cycle(path_graph(4), [0, 1, 2, 3, 0])


def test_spanning_forest_check() -> None:
    graph = cycle_graph(4)
    graph.add_edge("x", "y")
    testing.assert_valid_spanning_forest(graph, [(0, 1), (1, 2), (2, 3), ("x", "y")])
    with pytest.raises(AssertionError):  # missing x - y
        testing.assert_valid_spanning_forest(graph, [(0, 1), (1, 2), (2, 3)])
    with pytest.raises(AssertionError):  # contains a cycle, misses x - y
        testing.assert_valid_spanning_forest(graph, [(0, 1), (1, 2), (2, 3), (3, 0)])
    with pytest.raises(AssertionError):  # not an edge
        testing.assert_valid_spanning_forest(graph, [(0, 2), (1, 2), (2, 3), ("x", "y")])
    with pytest.raises(AssertionError):  # graph not connected
        testing.assert_valid_spanning_tree(graph, [(0, 1), (1, 2), (2, 3), ("x", "y")])
    testing.assert_valid_spanning_tree(cycle_graph(3), [(0, 1), (1, 2)])


def test_coloring_check() -> None:
    graph = cycle_graph(4)
    testing.assert_valid_coloring(graph, {0: "a", 1: "b", 2: "a", 3: "b"}, max_colors=2)
    with pytest.raises(AssertionError):
        testing.assert_valid_coloring(graph, {0: 1, 1: 1, 2: 2, 3: 2})
    with pytest.raises(AssertionError):
        testing.assert_valid_coloring(graph, {0: 1, 1: 2, 2: 1})
    with pytest.raises(AssertionError):
        testing.assert_valid_coloring(graph, {0: 1, 1: 2, 2: 3, 3: 4}, max_colors=3)


def test_matching_check() -> None:
    graph = Graph.from_edges([("a", 1), ("a", 2), ("b", 2)])
    testing.assert_valid_matching(graph, {"a": 1, "b": 2}, left=["a", "b"])
    testing.assert_valid_matching(graph, [("a", 1), ("b", 2)])
    with pytest.raises(AssertionError):
        testing.assert_valid_matching(graph, [("a", 2), ("b", 2)])
    with pytest.raises(AssertionError):
        testing.assert_valid_matching(graph, {"b": 1})
    with pytest.raises(AssertionError):
        testing.assert_valid_matching(graph, {1: "a"}, left=["a", "b"])


def test_flow_check() -> None:
    graph = Graph.from_edges([("s", "a", 3), ("a", "t", 2), ("s", "t", 1)], directed=True)
    flow = {("s", "a"): 2, ("a", "t"): 2, ("s", "t"): 1}
    testing.assert_valid_flow(graph, flow, "s", "t")
    assert testing.flow_value(graph, flow, "s") == 3
    with pytest.raises(AssertionError):  # capacity violated
        testing.assert_valid_flow(graph, {("s", "a"): 3, ("a", "t"): 3}, "s", "t")
    with pytest.raises(AssertionError):  # conservation violated
        testing.assert_valid_flow(graph, {("s", "a"): 2, ("a", "t"): 1}, "s", "t")
    with pytest.raises(AssertionError):  # not an edge
        testing.assert_valid_flow(graph, {("t", "s"): 1}, "s", "t")
    assert testing.cut_capacity(graph, {"s"}) == 4
    assert testing.cut_capacity(graph, {"s", "a"}) == 3


def test_count_components() -> None:
    graph = path_graph(3)
    graph.add_vertex("isolated")
    assert testing.count_components(graph) == 2
    assert testing.count_components(Graph()) == 0


def test_skip_if_not_implemented() -> None:
    @testing.skip_if_not_implemented
    def optional_test() -> None:
        raise NotImplementedError

    with pytest.raises(pytest.skip.Exception):
        optional_test()


def test_selected_implementation(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv(testing.IMPLEMENTATION_ENV_VAR, "demo")
    assert testing.selected_implementation() == "demo"
    monkeypatch.setenv(testing.IMPLEMENTATION_ENV_VAR, "nonsense")
    with pytest.raises(ValueError):
        testing.selected_implementation()


# ----------------------------------------------------------------------
# lib.visualization
# ----------------------------------------------------------------------
def test_to_text() -> None:
    graph = Graph.from_edges([("A", "B", 4), ("A", "C", 2)])
    graph.add_vertex("D")
    text = visualization.to_text(graph)
    assert "Undirected graph with 4 vertices and 2 edges" in text
    assert "B (4), C (2)" in text
    assert "D : -" in text
    assert "(4)" not in visualization.to_text(graph, show_weights=False)


def test_to_dot() -> None:
    graph = Graph.from_edges([("A", "B", 4), ("B", "C", 2)], directed=True)
    dot = visualization.to_dot(
        graph, highlight_edges=[("A", "B")], vertex_colors={"A": 0}, edge_labels={("B", "C"): "1/2"}
    )
    assert dot.startswith('digraph "G" {')
    assert '"A" -> "B" [label="4", color=red, penwidth=3];' in dot
    assert '"B" -> "C" [label="1/2"];' in dot
    assert "fillcolor=tomato" in dot


def test_save_dot(tmp_path) -> None:  # type: ignore[no-untyped-def]
    path = visualization.save_dot(petersen_graph(), tmp_path / "petersen.dot", name="Petersen")
    content = path.read_text(encoding="utf-8")
    assert content.startswith('graph "Petersen" {')
    assert content.count(" -- ") == 15


# ----------------------------------------------------------------------
# lib.utils
# ----------------------------------------------------------------------
def test_path_weight_and_format() -> None:
    graph = Graph.from_edges([("A", "B", 4), ("B", "C", 2)])
    assert utils.path_weight(graph, ["A", "B", "C"]) == 6
    assert utils.path_weight(graph, ["A"]) == 0
    with pytest.raises(KeyError):
        utils.path_weight(graph, ["A", "C"])
    assert utils.format_path(["A", "B"]) == "A -> B"
    assert utils.format_path(None) == "(kein Weg)"


def test_measure_time() -> None:
    assert utils.measure_time(sum, [1, 2, 3], repeat=2) >= 0


def test_load_exercise() -> None:
    module = utils.load_exercise("01_graph_basics", "task")
    assert module is utils.load_exercise("01_graph_basics", "task")
    assert hasattr(module, "build_bullerby_graph")
    with pytest.raises(FileNotFoundError):
        utils.load_exercise("99_does_not_exist")
