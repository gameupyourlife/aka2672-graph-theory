"""Tests for unit 6 (graph colouring).

By default these tests check ``task.py``. Use ``pytest --impl=demo`` to check
``demo_solution.py`` instead.
"""

import itertools
import random

import pytest

from lib.generators import (
    complete_bipartite_graph,
    complete_graph,
    cycle_graph,
    grid_graph,
    path_graph,
    petersen_graph,
    random_bipartite_graph,
    random_graph,
    random_tree,
    star_graph,
)
from lib.graph import Graph
from lib.testing import assert_valid_coloring, load_implementation, skip_if_not_implemented

impl = load_implementation(__file__)


# ----------------------------------------------------------------------
# Example graphs and helpers
# ----------------------------------------------------------------------
def crown_graph(n: int) -> Graph:
    """Vertices ("a", i) and ("b", i); ("a", i) -- ("b", j) exactly if i != j."""
    graph = Graph()
    graph.add_vertices([("a", i) for i in range(n)] + [("b", i) for i in range(n)])
    for i in range(n):
        for j in range(n):
            if i != j:
                graph.add_edge(("a", i), ("b", j))
    return graph


def party_graph() -> Graph:
    """Pippi's party from README.md: guests who quarrel are adjacent."""
    graph = Graph()
    graph.add_vertices(
        ["Pippi", "Tommy", "Annika", "Herr Nilsson", "Kleiner Onkel",
         "Prusseliese", "Kling", "Klang", "Donner-Karlsson", "Blom"]
    )
    graph.add_edges(
        [
            ("Kling", "Donner-Karlsson"),
            ("Kling", "Blom"),
            ("Klang", "Donner-Karlsson"),
            ("Klang", "Blom"),
            ("Donner-Karlsson", "Blom"),
            ("Pippi", "Prusseliese"),
            ("Herr Nilsson", "Prusseliese"),
        ]
    )
    return graph


def only_vertices(*names: object) -> Graph:
    graph = Graph()
    graph.add_vertices(names)
    return graph


def disjoint_union(first: Graph, second: Graph) -> Graph:
    """Put two graphs side by side; vertices become (1, v) and (2, v)."""
    graph = Graph()
    for tag, part in ((1, first), (2, second)):
        graph.add_vertices((tag, v) for v in part.vertices())
        graph.add_edges(((tag, u), (tag, v)) for u, v, _ in part.edges())
    return graph


def max_degree(graph: Graph) -> int:
    return max((graph.degree(v) for v in graph.vertices()), default=0)


def check_greedy_rule(graph: Graph, order, coloring) -> None:  # type: ignore[no-untyped-def]
    """Every vertex has the smallest colour not used by earlier neighbours."""
    assert set(coloring) == set(graph.vertices())
    position = {v: i for i, v in enumerate(order)}
    for v in order:
        earlier = {coloring[w] for w in graph.neighbors(v) if position[w] < position[v]}
        smallest_free = min(c for c in range(len(earlier) + 1) if c not in earlier)
        assert coloring[v] == smallest_free, f"vertex {v!r} should get colour {smallest_free}"


def bipartite_by_brute_force(graph: Graph) -> bool:
    """Try all 2^n ways to split the vertices into two sides."""
    vertices = graph.vertices()
    for sides in itertools.product((0, 1), repeat=len(vertices)):
        side = dict(zip(vertices, sides))
        if all(side[u] != side[v] for u, v, _ in graph.edges()):
            return True
    return False


def check_odd_cycle(graph: Graph, cycle) -> None:  # type: ignore[no-untyped-def]
    assert cycle is not None, "Expected an odd cycle, got None"
    assert cycle[0] == cycle[-1], "The cycle must end where it starts"
    inner = cycle[:-1]
    assert len(inner) >= 3, "A cycle needs at least 3 vertices"
    assert len(set(inner)) == len(inner), f"The cycle repeats a vertex: {cycle}"
    assert (len(cycle) - 1) % 2 == 1, f"The cycle has an even number of edges: {cycle}"
    for u, v in zip(cycle, cycle[1:]):
        assert graph.has_edge(u, v), f"There is no edge {u!r} - {v!r}"


# ----------------------------------------------------------------------
# greedy_coloring
# ----------------------------------------------------------------------
def test_greedy_path_default_order() -> None:
    assert impl.greedy_coloring(path_graph(4)) == {0: 0, 1: 1, 2: 0, 3: 1}


def test_greedy_path_bad_order() -> None:
    # 0 and 3 both get colour 0, so vertex 2 (neighbours 1 and 3) needs colour 2.
    assert impl.greedy_coloring(path_graph(4), [0, 3, 1, 2]) == {0: 0, 3: 0, 1: 1, 2: 2}


def test_greedy_odd_cycle() -> None:
    assert impl.greedy_coloring(cycle_graph(5)) == {0: 0, 1: 1, 2: 0, 3: 1, 4: 2}


def test_greedy_complete_graph() -> None:
    assert impl.greedy_coloring(complete_graph(4)) == {0: 0, 1: 1, 2: 2, 3: 3}


def test_greedy_star_orders() -> None:
    star = star_graph(4)
    assert impl.greedy_coloring(star, [0, 1, 2, 3, 4]) == {0: 0, 1: 1, 2: 1, 3: 1, 4: 1}
    assert impl.greedy_coloring(star, (4, 3, 2, 1, 0)) == {4: 0, 3: 0, 2: 0, 1: 0, 0: 1}


@pytest.mark.parametrize("n", [2, 3, 4, 6])
def test_greedy_crown_graph(n: int) -> None:
    crown = crown_graph(n)
    alternating = [vertex for i in range(n) for vertex in (("a", i), ("b", i))]
    expected = {vertex: i for i in range(n) for vertex in (("a", i), ("b", i))}
    assert impl.greedy_coloring(crown, alternating) == expected  # n colours ...
    sides = [("a", i) for i in range(n)] + [("b", i) for i in range(n)]
    result = impl.greedy_coloring(crown, sides)
    assert result == {v: (0 if v[0] == "a" else 1) for v in sides}  # ... or only 2


def test_greedy_party() -> None:
    graph = party_graph()
    tables = impl.greedy_coloring(graph)
    assert_valid_coloring(graph, tables)
    assert tables["Blom"] == 2  # Kling, Donner-Karlsson, Blom form a triangle
    assert len(set(tables.values())) == 3


def test_greedy_without_edges() -> None:
    assert impl.greedy_coloring(Graph()) == {}
    assert impl.greedy_coloring(only_vertices("Ida", "Lina")) == {"Ida": 0, "Lina": 0}


def test_greedy_default_order_is_vertex_order() -> None:
    graph = random_graph(15, 0.3, seed=3)
    assert impl.greedy_coloring(graph) == impl.greedy_coloring(graph, graph.vertices())


@pytest.mark.parametrize("seed", range(10))
def test_greedy_random_graphs(seed: int) -> None:
    graph = random_graph(25, 0.25, seed=seed)
    order = graph.vertices()
    random.Random(seed).shuffle(order)
    before = graph.copy()
    coloring = impl.greedy_coloring(graph, order)
    assert graph == before  # the input is not modified
    assert_valid_coloring(graph, coloring, max_colors=max_degree(graph) + 1)
    assert set(coloring.values()) == set(range(len(set(coloring.values()))))  # colours 0..k-1
    check_greedy_rule(graph, order, coloring)


def test_greedy_petersen_bound() -> None:
    graph = petersen_graph()
    assert_valid_coloring(graph, impl.greedy_coloring(graph), max_colors=4)


@pytest.mark.parametrize(
    "order",
    [[0, 1, 2], [0, 1, 2, 3, 3], [0, 1, 2, 2], [0, 1, 2, 3, 99], [0, 1, 2, 99]],
)
def test_greedy_invalid_order(order: list[int]) -> None:
    with pytest.raises(ValueError):
        impl.greedy_coloring(path_graph(4), order)


def test_greedy_rejects_directed() -> None:
    with pytest.raises(ValueError):
        impl.greedy_coloring(Graph.from_edges([(1, 2)], directed=True))


# ----------------------------------------------------------------------
# is_valid_coloring and number_of_colors
# ----------------------------------------------------------------------
def test_is_valid_coloring_examples() -> None:
    path = path_graph(3)
    assert impl.is_valid_coloring(path, {0: 0, 1: 1, 2: 0}) is True
    assert impl.is_valid_coloring(path, {0: 5, 1: 7, 2: 9}) is True
    assert impl.is_valid_coloring(path, {0: 0, 1: 0, 2: 1}) is False  # edge 0 - 1
    assert impl.is_valid_coloring(path, {0: 0, 1: 1}) is False  # vertex 2 missing
    assert impl.is_valid_coloring(path, {0: 0, 1: 1, 2: 0, 3: 1}) is False  # 3 is no vertex


def test_is_valid_coloring_edge_cases() -> None:
    assert impl.is_valid_coloring(Graph(), {}) is True
    assert impl.is_valid_coloring(only_vertices("a", "b"), {"a": 0, "b": 0}) is True
    assert impl.is_valid_coloring(only_vertices("a"), {}) is False


@pytest.mark.parametrize("seed", range(10))
def test_is_valid_coloring_random(seed: int) -> None:
    graph = random_graph(8, 0.3, seed=seed)
    rng = random.Random(seed)
    coloring = {v: rng.randrange(3) for v in graph.vertices()}
    expected = all(coloring[u] != coloring[v] for u, v, _ in graph.edges())
    assert impl.is_valid_coloring(graph, coloring) is expected


def test_is_valid_coloring_rejects_directed() -> None:
    with pytest.raises(ValueError):
        impl.is_valid_coloring(Graph.from_edges([(1, 2)], directed=True), {1: 0, 2: 1})


def test_number_of_colors() -> None:
    assert impl.number_of_colors({}) == 0
    assert impl.number_of_colors({"a": 0, "b": 0}) == 1
    assert impl.number_of_colors({"a": 0, "b": 2, "c": 5, "d": 2}) == 3


# ----------------------------------------------------------------------
# is_bipartite
# ----------------------------------------------------------------------
@pytest.mark.parametrize(
    ("graph", "expected"),
    [
        (Graph(), True),
        (only_vertices(1), True),
        (only_vertices(1, 2, 3), True),
        (path_graph(2), True),
        (path_graph(7), True),
        (cycle_graph(4), True),
        (cycle_graph(10), True),
        (cycle_graph(3), False),
        (cycle_graph(9), False),
        (complete_graph(3), False),
        (star_graph(5), True),
        (grid_graph(4, 5), True),
        (complete_bipartite_graph(3, 4), True),
        (petersen_graph(), False),
        (crown_graph(4), True),
        (party_graph(), False),
        (disjoint_union(cycle_graph(4), cycle_graph(6)), True),
        (disjoint_union(cycle_graph(4), cycle_graph(5)), False),
        (disjoint_union(path_graph(3), complete_graph(3)), False),
    ],
)
def test_is_bipartite_examples(graph: Graph, expected: bool) -> None:
    assert impl.is_bipartite(graph) is expected


@pytest.mark.parametrize("seed", range(5))
def test_is_bipartite_trees(seed: int) -> None:
    assert impl.is_bipartite(random_tree(30, seed=seed)) is True


@pytest.mark.parametrize("seed", range(5))
def test_is_bipartite_random_bipartite(seed: int) -> None:
    assert impl.is_bipartite(random_bipartite_graph(8, 9, 0.4, seed=seed)) is True


@pytest.mark.parametrize("seed", range(15))
def test_is_bipartite_matches_brute_force(seed: int) -> None:
    graph = random_graph(9, 0.2, seed=seed)
    assert impl.is_bipartite(graph) is bipartite_by_brute_force(graph)


def test_is_bipartite_rejects_directed() -> None:
    with pytest.raises(ValueError):
        impl.is_bipartite(Graph.from_edges([(1, 2), (2, 3)], directed=True))


# ----------------------------------------------------------------------
# Optional: welsh_powell_order
# ----------------------------------------------------------------------
@skip_if_not_implemented
def test_welsh_powell_examples() -> None:
    assert impl.welsh_powell_order(star_graph(3)) == [0, 1, 2, 3]
    assert impl.welsh_powell_order(path_graph(4)) == [1, 2, 0, 3]
    graph = Graph.from_edges([("a", "b"), ("b", "c"), ("c", "d"), ("b", "d")])
    assert impl.welsh_powell_order(graph) == ["b", "c", "d", "a"]
    assert impl.welsh_powell_order(Graph()) == []


@skip_if_not_implemented
@pytest.mark.parametrize("seed", range(5))
def test_welsh_powell_random(seed: int) -> None:
    graph = random_graph(20, 0.2, seed=seed)
    order = impl.welsh_powell_order(graph)
    assert sorted(order) == sorted(graph.vertices())  # a permutation
    position = {v: i for i, v in enumerate(graph.vertices())}
    for v, w in zip(order, order[1:]):
        assert graph.degree(v) >= graph.degree(w)  # descending degree
        if graph.degree(v) == graph.degree(w):
            assert position[v] < position[w]  # ties keep the vertex order


@skip_if_not_implemented
def test_welsh_powell_rejects_directed() -> None:
    with pytest.raises(ValueError):
        impl.welsh_powell_order(Graph.from_edges([(1, 2)], directed=True))


# ----------------------------------------------------------------------
# Optional: find_odd_cycle
# ----------------------------------------------------------------------
@skip_if_not_implemented
@pytest.mark.parametrize(
    "graph",
    [
        cycle_graph(3),
        cycle_graph(5),
        cycle_graph(11),
        complete_graph(4),
        petersen_graph(),
        party_graph(),
        disjoint_union(cycle_graph(4), cycle_graph(5)),
        disjoint_union(grid_graph(3, 3), cycle_graph(7)),
    ],
)
def test_find_odd_cycle(graph: Graph) -> None:
    before = graph.copy()
    check_odd_cycle(graph, impl.find_odd_cycle(graph))
    assert graph == before  # the input is not modified


@skip_if_not_implemented
@pytest.mark.parametrize(
    "graph",
    [
        Graph(),
        only_vertices("x", "y"),
        path_graph(5),
        cycle_graph(8),
        grid_graph(3, 4),
        complete_bipartite_graph(2, 5),
        random_tree(20, seed=1),
        disjoint_union(cycle_graph(4), cycle_graph(6)),
    ],
)
def test_find_odd_cycle_none(graph: Graph) -> None:
    assert impl.find_odd_cycle(graph) is None


@skip_if_not_implemented
@pytest.mark.parametrize("seed", range(10))
def test_find_odd_cycle_random(seed: int) -> None:
    graph = random_graph(9, 0.2, seed=seed)
    cycle = impl.find_odd_cycle(graph)
    if bipartite_by_brute_force(graph):
        assert cycle is None
    else:
        check_odd_cycle(graph, cycle)


@skip_if_not_implemented
def test_find_odd_cycle_rejects_directed() -> None:
    with pytest.raises(ValueError):
        impl.find_odd_cycle(Graph.from_edges([(1, 2), (2, 3), (3, 1)], directed=True))
