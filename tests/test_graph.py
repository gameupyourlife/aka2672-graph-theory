"""Tests for the shared Graph class (lib/graph.py)."""

import pytest

from lib.graph import Edge, Graph


@pytest.fixture
def bullerby() -> Graph:
    graph = Graph()
    graph.add_edge("Nordhof", "Mittelhof", 1)
    graph.add_edge("Mittelhof", "Südhof", 1)
    graph.add_edge("Nordhof", "Schule", 3)
    return graph


def test_empty_graph() -> None:
    graph = Graph()
    assert graph.num_vertices() == 0
    assert graph.num_edges() == 0
    assert graph.vertices() == []
    assert graph.edges() == []
    assert len(graph) == 0
    assert not graph.directed


def test_constructor_accepts_vertices_and_edges() -> None:
    graph = Graph(
        vertices=iter(["isolated", "A"]),
        edges=iter([("A", "B"), Edge("B", "C", 5)]),
        directed=False,
    )

    assert graph.vertices() == ["isolated", "A", "B", "C"]
    assert graph.edges() == [Edge("A", "B"), Edge("B", "C", 5)]
    assert graph.degree("isolated") == 0
    assert graph.weight("C", "B") == 5


def test_constructor_keeps_directed_as_a_positional_argument() -> None:
    graph = Graph(True, edges=[("A", "B")])

    assert graph.has_edge("A", "B")
    assert not graph.has_edge("B", "A")


def test_example_from_documentation() -> None:
    graph = Graph(directed=False)
    graph.add_edge("Bullerby", "Lonneberga")
    graph.add_edge("Bullerby", "Sevedstorp")
    assert graph.neighbors("Bullerby") == ["Lonneberga", "Sevedstorp"]
    assert graph.neighbors("Lonneberga") == ["Bullerby"]


def test_add_vertex_is_idempotent() -> None:
    graph = Graph()
    graph.add_vertex("A")
    graph.add_vertex("A")
    assert graph.vertices() == ["A"]


def test_add_edge_adds_vertices(bullerby: Graph) -> None:
    assert set(bullerby.vertices()) == {"Nordhof", "Mittelhof", "Südhof", "Schule"}
    assert bullerby.num_vertices() == 4
    assert bullerby.num_edges() == 3


def test_undirected_edges_are_symmetric(bullerby: Graph) -> None:
    assert bullerby.has_edge("Nordhof", "Schule")
    assert bullerby.has_edge("Schule", "Nordhof")
    assert bullerby.weight("Schule", "Nordhof") == 3
    assert not bullerby.has_edge("Schule", "Südhof")


def test_edges_listed_once(bullerby: Graph) -> None:
    edges = bullerby.edges()
    assert len(edges) == 3
    assert all(isinstance(e, Edge) for e in edges)
    assert {frozenset((e.u, e.v)) for e in edges} == {
        frozenset(("Nordhof", "Mittelhof")),
        frozenset(("Mittelhof", "Südhof")),
        frozenset(("Nordhof", "Schule")),
    }


def test_unweighted_edges_have_weight_one() -> None:
    graph = Graph()
    graph.add_edge(1, 2)
    assert graph.weight(1, 2) == 1
    assert graph.edges() == [Edge(1, 2, 1)]


def test_degree_undirected(bullerby: Graph) -> None:
    assert bullerby.degree("Nordhof") == 2
    assert bullerby.degree("Südhof") == 1
    assert sum(bullerby.degree(v) for v in bullerby) == 2 * bullerby.num_edges()


def test_directed_graph() -> None:
    graph = Graph(directed=True)
    graph.add_edge("a", "b", 2)
    graph.add_edge("b", "a", 5)
    graph.add_edge("a", "c")
    assert graph.directed
    assert graph.num_edges() == 3
    assert graph.neighbors("a") == ["b", "c"]
    assert graph.predecessors("a") == ["b"]
    assert graph.out_degree("a") == 2
    assert graph.in_degree("a") == 1
    assert graph.degree("a") == 3
    assert graph.weight("a", "b") == 2
    assert graph.weight("b", "a") == 5
    assert not graph.has_edge("c", "a")


def test_predecessors_undirected_equal_neighbors(bullerby: Graph) -> None:
    assert bullerby.predecessors("Nordhof") == bullerby.neighbors("Nordhof")


def test_loops_are_rejected() -> None:
    with pytest.raises(ValueError):
        Graph().add_edge("A", "A")


def test_parallel_edges_are_rejected() -> None:
    graph = Graph()
    graph.add_edge("A", "B")
    with pytest.raises(ValueError):
        graph.add_edge("B", "A")


@pytest.mark.parametrize("weight", ["3", None, float("inf"), float("nan"), True])
def test_invalid_weights_are_rejected(weight: object) -> None:
    with pytest.raises(ValueError):
        Graph().add_edge("A", "B", weight)  # type: ignore[arg-type]


def test_negative_weights_are_allowed() -> None:
    graph = Graph(directed=True)
    graph.add_edge("A", "B", -2.5)
    assert graph.weight("A", "B") == -2.5


def test_missing_vertex_raises_key_error() -> None:
    graph = Graph()
    with pytest.raises(KeyError):
        graph.neighbors("X")
    with pytest.raises(KeyError):
        graph.degree("X")
    with pytest.raises(KeyError):
        graph.weight("X", "Y")


def test_set_weight(bullerby: Graph) -> None:
    bullerby.set_weight("Schule", "Nordhof", 7)
    assert bullerby.weight("Nordhof", "Schule") == 7
    with pytest.raises(KeyError):
        bullerby.set_weight("Schule", "Südhof", 1)


def test_remove_edge_and_vertex(bullerby: Graph) -> None:
    bullerby.remove_edge("Mittelhof", "Nordhof")
    assert not bullerby.has_edge("Nordhof", "Mittelhof")
    assert bullerby.num_edges() == 2
    bullerby.remove_vertex("Nordhof")
    assert "Nordhof" not in bullerby
    assert bullerby.neighbors("Schule") == []
    assert bullerby.num_edges() == 1
    bullerby.check_consistency()
    with pytest.raises(KeyError):
        bullerby.remove_edge("Nordhof", "Schule")


def test_remove_vertex_directed() -> None:
    graph = Graph.from_edges([("a", "b"), ("b", "c"), ("c", "a")], directed=True)
    graph.remove_vertex("b")
    assert graph.vertices() == ["a", "c"]
    assert graph.edges() == [Edge("c", "a", 1)]
    graph.check_consistency()


def test_copy_is_independent(bullerby: Graph) -> None:
    copy = bullerby.copy()
    assert copy == bullerby
    copy.add_edge("Südhof", "Schule")
    assert not bullerby.has_edge("Südhof", "Schule")
    assert copy != bullerby


def test_copy_keeps_isolated_vertices_and_direction() -> None:
    graph = Graph(directed=True)
    graph.add_vertex("einsam")
    graph.add_edge("a", "b", 4)
    copy = graph.copy()
    assert copy.directed
    assert copy.vertices() == ["einsam", "a", "b"]
    assert copy.weight("a", "b") == 4


def test_from_edges() -> None:
    graph = Graph.from_edges([("A", "B"), ("B", "C", 5)], vertices=["Z"])
    assert graph.vertices() == ["Z", "A", "B", "C"]
    assert graph.weight("A", "B") == 1
    assert graph.weight("C", "B") == 5
    with pytest.raises(ValueError):
        Graph.from_edges([("A",)])  # type: ignore[list-item]


def test_contains_iter_len(bullerby: Graph) -> None:
    assert "Schule" in bullerby
    assert "Stockholm" not in bullerby
    assert list(bullerby) == bullerby.vertices()
    assert len(bullerby) == 4


def test_check_consistency_detects_broken_graph(bullerby: Graph) -> None:
    bullerby.check_consistency()
    # Deliberately break the internal structure.
    bullerby._succ["Nordhof"]["Südhof"] = 1  # only one direction stored
    with pytest.raises(ValueError):
        bullerby.check_consistency()


def test_check_consistency_detects_unknown_neighbour() -> None:
    graph = Graph(directed=True)
    graph.add_edge("a", "b")
    graph._succ["a"]["ghost"] = 1
    with pytest.raises(ValueError):
        graph.check_consistency()


def test_repr() -> None:
    assert repr(Graph(directed=True)) == "Graph(directed, 0 vertices, 0 edges)"


# ----------------------------------------------------------------------
# Attributes
# ----------------------------------------------------------------------
def test_vertex_attributes() -> None:
    graph = Graph()
    graph.add_vertex("Katthult", pos=(0, 1))
    assert graph.vertex_attributes("Katthult") == {"pos": (0, 1)}
    graph.add_vertex("Katthult", label="Hof")  # merges, keeps pos
    assert graph.vertex_attributes("Katthult") == {"pos": (0, 1), "label": "Hof"}
    graph.vertex_attributes("Katthult")["pos"] = (2, 2)  # live dictionary
    assert graph.vertex_attributes("Katthult")["pos"] == (2, 2)
    graph.add_edge("Katthult", "Lönneberga")
    assert graph.vertex_attributes("Lönneberga") == {}
    with pytest.raises(KeyError):
        graph.vertex_attributes("Stockholm")


def test_edge_attributes_undirected_are_shared() -> None:
    graph = Graph()
    graph.add_edge("a", "b", 3, name="Brücke")
    assert graph.edge_attributes("b", "a") == {"name": "Brücke"}
    graph.edge_attributes("a", "b")["color"] = "rot"
    assert graph.edge_attributes("b", "a")["color"] == "rot"
    with pytest.raises(KeyError):
        graph.edge_attributes("a", "c")


def test_edge_attributes_directed_are_separate() -> None:
    graph = Graph(directed=True)
    graph.add_edge("a", "b", name="hin")
    graph.add_edge("b", "a", name="zurück")
    assert graph.edge_attributes("a", "b") == {"name": "hin"}
    assert graph.edge_attributes("b", "a") == {"name": "zurück"}


def test_attributes_are_copied_and_removed() -> None:
    graph = Graph()
    graph.add_vertex("x", pos=(1, 2))
    graph.add_edge("x", "y", 2, kind="road")
    copy = graph.copy()
    assert copy.vertex_attributes("x") == {"pos": (1, 2)}
    assert copy.edge_attributes("y", "x") == {"kind": "road"}
    copy.vertex_attributes("x")["pos"] = (9, 9)
    assert graph.vertex_attributes("x")["pos"] == (1, 2)
    assert copy == graph  # attributes are not compared
    graph.remove_edge("x", "y")
    graph.check_consistency()
    graph.remove_vertex("x")
    graph.check_consistency()
    with pytest.raises(KeyError):
        graph.vertex_attributes("x")
