"""Tests for unit 10 (final project "Das Netzwerk von Nangijala").

By default these tests check ``task.py``. Use ``pytest --impl=demo`` to check
``demo_solution.py`` instead.

The expected values were computed independently (Floyd-Warshall, Prim,
brute-force cuts) and are hard-coded here.
"""

from pathlib import Path

import pytest

from lib.graph import Graph
from lib.testing import (
    assert_valid_coloring,
    assert_valid_flow,
    assert_valid_matching,
    assert_valid_path,
    assert_valid_spanning_tree,
    flow_value,
    load_implementation,
    skip_if_not_implemented,
)
from lib.utils import load_module_from_path, path_weight

impl = load_implementation(__file__)
data = load_module_from_path(Path(__file__).with_name("nangijala_data.py"))

ALL_PLACES = {
    "Reiterhof", "Goldener Hahn", "Sofias Hof", "Mühle", "Kirschtalbrücke", "Westwald",
    "Wolfsschlucht", "Bärenpass", "Adlerhorst", "Waldsee", "Karmafall", "Katlas Höhle",
    "Stadttor", "Marktplatz", "Mattiashof", "Rebellenhöhle", "Fischerhütte",
    "Grenzwache", "Tengils Burg", "Karmanjaka",
}  # fmt: skip


@pytest.fixture
def nangijala() -> Graph:
    return impl.build_network(data.ROADS)


# ----------------------------------------------------------------------
# Module A
# ----------------------------------------------------------------------
def test_build_network(nangijala: Graph) -> None:
    assert not nangijala.directed
    assert set(nangijala.vertices()) == ALL_PLACES
    assert nangijala.num_edges() == 28
    assert nangijala.weight("Reiterhof", "Goldener Hahn") == 20
    assert nangijala.weight("Karmanjaka", "Tengils Burg") == 18


def test_build_network_small() -> None:
    graph = impl.build_network([("a", "b", 3)])
    assert graph.weight("b", "a") == 3
    assert impl.build_network([]).num_vertices() == 0


def test_without_places(nangijala: Graph) -> None:
    smaller = impl.without_places(nangijala, ["Bärenpass", "Waldsee"])
    assert set(smaller.vertices()) == ALL_PLACES - {"Bärenpass", "Waldsee"}
    # Bärenpass has 4 roads, Waldsee 3, and they share one road.
    assert smaller.num_edges() == 28 - (4 + 3 - 1)
    assert nangijala.num_vertices() == 20  # original unchanged
    with pytest.raises(KeyError):
        impl.without_places(nangijala, ["Stockholm"])


# ----------------------------------------------------------------------
# Module B
# ----------------------------------------------------------------------
def test_everything_reachable(nangijala: Graph) -> None:
    assert impl.reachable_places(nangijala, "Reiterhof") == ALL_PLACES


def test_reachable_with_closed_passes(nangijala: Graph) -> None:
    reachable = impl.reachable_places(nangijala, "Reiterhof", ["Bärenpass", "Adlerhorst"])
    assert reachable == set(data.KIRSCHTAL) | {"Wolfsschlucht"}


def test_reachable_with_closed_border(nangijala: Graph) -> None:
    reachable = impl.reachable_places(nangijala, "Marktplatz", ["Grenzwache"])
    assert reachable == ALL_PLACES - {"Grenzwache", "Tengils Burg", "Karmanjaka"}
    assert impl.reachable_places(nangijala, "Karmanjaka", ["Grenzwache"]) == {"Karmanjaka", "Tengils Burg"}


def test_reachable_invalid(nangijala: Graph) -> None:
    with pytest.raises(ValueError):
        impl.reachable_places(nangijala, "Reiterhof", ["Reiterhof"])
    with pytest.raises(KeyError):
        impl.reachable_places(nangijala, "Stockholm")
    with pytest.raises(KeyError):
        impl.reachable_places(nangijala, "Reiterhof", ["Stockholm"])


def test_critical_places(nangijala: Graph) -> None:
    assert set(impl.critical_places(nangijala)) == {"Karmafall", "Grenzwache", "Tengils Burg"}


def test_critical_places_small_graphs() -> None:
    path = Graph.from_edges([("a", "b"), ("b", "c"), ("c", "d")])
    assert impl.critical_places(path) == ["b", "c"]
    triangle = Graph.from_edges([("a", "b"), ("b", "c"), ("c", "a")])
    assert impl.critical_places(triangle) == []
    two_parts = Graph.from_edges([("a", "b"), ("b", "c"), ("x", "y")])
    assert impl.critical_places(two_parts) == ["b"]


# ----------------------------------------------------------------------
# Module C
# ----------------------------------------------------------------------
MST_EDGES = {
    frozenset(pair)
    for pair in [
        ("Stadttor", "Marktplatz"), ("Tengils Burg", "Karmanjaka"), ("Reiterhof", "Goldener Hahn"),
        ("Marktplatz", "Mattiashof"), ("Goldener Hahn", "Sofias Hof"), ("Mühle", "Kirschtalbrücke"),
        ("Marktplatz", "Fischerhütte"), ("Goldener Hahn", "Mühle"), ("Fischerhütte", "Rebellenhöhle"),
        ("Westwald", "Kirschtalbrücke"), ("Wolfsschlucht", "Bärenpass"), ("Adlerhorst", "Waldsee"),
        ("Kirschtalbrücke", "Wolfsschlucht"), ("Bärenpass", "Waldsee"), ("Karmafall", "Katlas Höhle"),
        ("Waldsee", "Stadttor"), ("Rebellenhöhle", "Karmafall"), ("Fischerhütte", "Grenzwache"),
        ("Grenzwache", "Tengils Burg"),
    ]
}  # fmt: skip


def test_winter_roads(nangijala: Graph) -> None:
    edges, total = impl.winter_roads(nangijala)
    assert total == 1070
    assert len(edges) == 19
    assert_valid_spanning_tree(nangijala, edges)
    # All travel times differ, so the minimum spanning tree is unique.
    assert {frozenset((e[0], e[1])) for e in edges} == MST_EDGES


# ----------------------------------------------------------------------
# Module D
# ----------------------------------------------------------------------
@pytest.mark.parametrize(
    ("target", "blocked", "minutes"),
    [
        ("Tengils Burg", [], 435),
        ("Marktplatz", [], 360),
        ("Katlas Höhle", [], 395),
        ("Marktplatz", ["Bärenpass", "Waldsee"], 495),
        ("Goldener Hahn", [], 20),
    ],
)
def test_fastest_route(nangijala: Graph, target: str, blocked: list[str], minutes: int) -> None:
    result = impl.fastest_route(nangijala, "Reiterhof", target, blocked)
    assert result is not None
    path, length = result
    assert length == minutes
    assert_valid_path(nangijala, path, start="Reiterhof", end=target)
    assert path_weight(nangijala, path) == minutes
    assert not set(path) & set(blocked)


def test_fastest_route_to_itself(nangijala: Graph) -> None:
    assert impl.fastest_route(nangijala, "Mühle", "Mühle") == (["Mühle"], 0)


def test_fastest_route_unreachable(nangijala: Graph) -> None:
    assert impl.fastest_route(nangijala, "Reiterhof", "Karmanjaka", ["Grenzwache"]) is None


def test_fastest_route_invalid(nangijala: Graph) -> None:
    with pytest.raises(ValueError):
        impl.fastest_route(nangijala, "Reiterhof", "Waldsee", ["Waldsee"])
    with pytest.raises(KeyError):
        impl.fastest_route(nangijala, "Reiterhof", "Stockholm")


# ----------------------------------------------------------------------
# Module E
# ----------------------------------------------------------------------
def test_lantern_colors(nangijala: Graph) -> None:
    colors = impl.lantern_colors(nangijala)
    assert_valid_coloring(nangijala, colors)
    # Reiterhof, Goldener Hahn and Sofias Hof form a triangle: at least 3 colours.
    # The network can be coloured with 3 colours; we accept up to 4.
    assert 3 <= len(set(colors.values())) <= 4


def test_lantern_colors_small() -> None:
    graph = Graph.from_edges([("a", "b"), ("b", "c"), ("c", "d")])
    colors = impl.lantern_colors(graph)
    assert_valid_coloring(graph, colors, max_colors=2)
    assert impl.lantern_colors(Graph()) == {}


# ----------------------------------------------------------------------
# Module F
# ----------------------------------------------------------------------
def qualification_graph(qualifications: dict[str, list[str]]) -> Graph:
    graph = Graph()
    graph.add_vertices(qualifications)
    for person, tasks in qualifications.items():
        for task in tasks:
            graph.add_edge(person, task)
    return graph


def test_assign_tasks(nangijala: Graph) -> None:
    assignment = impl.assign_tasks(data.QUALIFICATIONS)
    graph = qualification_graph(data.QUALIFICATIONS)
    assert_valid_matching(graph, assignment, left=data.QUALIFICATIONS)
    # Hubert and Elias both can only do "Botengang": at most 6 of 7 people.
    assert len(assignment) == 6
    assert ("Hubert" in assignment) != ("Elias" in assignment)


def test_assign_tasks_small() -> None:
    qualifications = {"Pippi": ["Pferd", "Affe"], "Tommy": ["Pferd"], "Annika": ["Pferd", "Garten"]}
    assignment = impl.assign_tasks(qualifications)
    assert assignment["Tommy"] == "Pferd"
    assert len(assignment) == 3
    assert impl.assign_tasks({}) == {}
    assert impl.assign_tasks({"Ida": []}) == {}


def test_assign_tasks_name_clash() -> None:
    with pytest.raises(ValueError):
        impl.assign_tasks({"Michel": ["Alfred"], "Alfred": ["Michel"]})


# ----------------------------------------------------------------------
# Module G (optional)
# ----------------------------------------------------------------------
@skip_if_not_implemented
def test_max_supply() -> None:
    value, flow = impl.max_supply(data.SUPPLY_ROUTES, "Kirschtal", "Heckenrosental")
    assert value == 15
    network = Graph.from_edges(data.SUPPLY_ROUTES, directed=True)
    assert_valid_flow(network, flow, "Kirschtal", "Heckenrosental")
    assert flow_value(network, flow, "Kirschtal") == 15


@skip_if_not_implemented
def test_max_supply_small() -> None:
    value, _flow = impl.max_supply([("s", "a", 3), ("a", "t", 2)], "s", "t")
    assert value == 2
