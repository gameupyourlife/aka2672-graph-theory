"""Tests for unit 8 (maximum flows).

By default these tests check ``task.py``. Use ``pytest --impl=demo`` to check
``demo_solution.py`` instead.
"""

import itertools

import pytest

from lib.generators import path_graph, random_weighted_graph
from lib.graph import Graph
from lib.testing import (
    assert_valid_flow,
    assert_valid_path,
    cut_capacity,
    flow_value,
    load_implementation,
    skip_if_not_implemented,
)

impl = load_implementation(__file__)


@pytest.fixture
def clrs() -> Graph:
    """The example network from Cormen et al. (maximum flow 23)."""
    return Graph.from_edges(
        [
            ("s", "v1", 16),
            ("s", "v2", 13),
            ("v1", "v3", 12),
            ("v2", "v1", 4),
            ("v2", "v4", 14),
            ("v3", "v2", 9),
            ("v3", "t", 20),
            ("v4", "v3", 7),
            ("v4", "t", 4),
        ],
        directed=True,
    )


@pytest.fixture
def diamond() -> Graph:
    """s -> a, s -> b, a -> b, a -> t, b -> t, all with capacity 1 (README)."""
    return Graph.from_edges([("s", "a", 1), ("s", "b", 1), ("a", "b", 1), ("a", "t", 1), ("b", "t", 1)], directed=True)


@pytest.fixture
def detour() -> Graph:
    """The unique shortest path s-a-d-t must be undone via the backward edge d -> a.

    Maximum flow 2: s-a-x-y-t and s-c-e-d-t. In every maximum flow a -> d
    carries no flow.
    """
    return Graph.from_edges(
        [
            ("s", "a", 1),
            ("a", "d", 1),
            ("d", "t", 1),
            ("a", "x", 1),
            ("x", "y", 1),
            ("y", "t", 1),
            ("s", "c", 1),
            ("c", "e", 1),
            ("e", "d", 1),
        ],
        directed=True,
    )


@pytest.fixture
def antiparallel() -> Graph:
    """Antiparallel edges a -> b (capacity 1) and b -> a (capacity 2).

    Edmonds-Karp first sends 2 units along s-b-a-t (the only shortest path),
    then 3 units along s-c-d-a-b-e-f-t. Pushing 3 units along (a, b) is only
    possible by first cancelling the 2 units on b -> a. The maximum flow
    (value 5) is unique.
    """
    return Graph.from_edges(
        [
            ("s", "b", 2),
            ("b", "a", 2),
            ("a", "t", 2),
            ("s", "c", 3),
            ("c", "d", 3),
            ("d", "a", 3),
            ("a", "b", 1),
            ("b", "e", 3),
            ("e", "f", 3),
            ("f", "t", 3),
        ],
        directed=True,
    )


def edge_set(graph: Graph) -> set:  # type: ignore[type-arg]
    return {(u, v) for u, v, _ in graph.edges()}


def weighted_edges(graph: Graph) -> dict:  # type: ignore[type-arg]
    return {(u, v): w for u, v, w in graph.edges()}


def brute_force_min_cut(graph: Graph, source, sink) -> float:  # type: ignore[no-untyped-def]
    """Minimum cut capacity by trying all sets S with source in S, sink not in S."""
    others = [v for v in graph.vertices() if v not in (source, sink)]
    best = float("inf")
    for k in range(len(others) + 1):
        for chosen in itertools.combinations(others, k):
            best = min(best, cut_capacity(graph, {source, *chosen}))
    return best


def check_max_flow(graph: Graph, source, sink, result, expected) -> None:  # type: ignore[no-untyped-def]
    value, flow = result
    assert set(flow) == edge_set(graph), "The flow needs an entry for every edge (and only for edges)"
    assert_valid_flow(graph, flow, source, sink)
    assert value == pytest.approx(expected)
    assert flow_value(graph, flow, source) == pytest.approx(expected)


# ----------------------------------------------------------------------
# residual_graph
# ----------------------------------------------------------------------
def test_residual_of_zero_flow(clrs: Graph) -> None:
    residual = impl.residual_graph(clrs, {})
    assert residual.directed
    assert set(residual.vertices()) == set(clrs.vertices())
    assert weighted_edges(residual) == weighted_edges(clrs)


def test_residual_zero_flow_explicit_entries(clrs: Graph) -> None:
    zero = {(u, v): 0 for u, v, _ in clrs.edges()}
    assert weighted_edges(impl.residual_graph(clrs, zero)) == weighted_edges(clrs)


def test_residual_backward_edges(diamond: Graph) -> None:
    flow = {("s", "a"): 1, ("a", "b"): 1, ("b", "t"): 1}
    residual = impl.residual_graph(diamond, flow)
    assert weighted_edges(residual) == {
        ("a", "s"): 1,
        ("s", "b"): 1,
        ("b", "a"): 1,
        ("a", "t"): 1,
        ("t", "b"): 1,
    }


def test_residual_partial_flow() -> None:
    graph = Graph.from_edges([("s", "a", 5), ("a", "t", 3)], directed=True)
    residual = impl.residual_graph(graph, {("s", "a"): 2, ("a", "t"): 2})
    assert weighted_edges(residual) == {("s", "a"): 3, ("a", "s"): 2, ("a", "t"): 1, ("t", "a"): 2}


def test_residual_antiparallel_edges() -> None:
    graph = Graph.from_edges([("a", "b", 3), ("b", "a", 2)], directed=True)
    # c_f(a, b) = (3 - 1) + 0 = 2,  c_f(b, a) = (2 - 0) + 1 = 3
    assert weighted_edges(impl.residual_graph(graph, {("a", "b"): 1})) == {("a", "b"): 2, ("b", "a"): 3}
    # c_f(a, b) = (3 - 1) + 1 = 3,  c_f(b, a) = (2 - 1) + 1 = 2
    both = {("a", "b"): 1, ("b", "a"): 1}
    assert weighted_edges(impl.residual_graph(graph, both)) == {("a", "b"): 3, ("b", "a"): 2}
    # c_f(a, b) = (3 - 3) + 2 = 2,  c_f(b, a) = (2 - 2) + 3 = 3
    full = {("a", "b"): 3, ("b", "a"): 2}
    assert weighted_edges(impl.residual_graph(graph, full)) == {("a", "b"): 2, ("b", "a"): 3}


def test_residual_keeps_isolated_vertices_and_skips_zero_capacity() -> None:
    graph = Graph.from_edges([("s", "t", 0), ("s", "a", 2)], directed=True, vertices=["z"])
    residual = impl.residual_graph(graph, {})
    assert set(residual.vertices()) == {"s", "t", "a", "z"}
    assert weighted_edges(residual) == {("s", "a"): 2}


def test_residual_does_not_modify_input(diamond: Graph) -> None:
    before = diamond.copy()
    flow = {("s", "a"): 1, ("a", "t"): 1}
    flow_before = dict(flow)
    residual = impl.residual_graph(diamond, flow)
    assert diamond == before
    assert flow == flow_before
    assert residual is not diamond


# ----------------------------------------------------------------------
# find_augmenting_path
# ----------------------------------------------------------------------
def test_find_path_shortest(clrs: Graph) -> None:
    path = impl.find_augmenting_path(clrs, "s", "t")
    assert len(path) == 4  # e.g. s -> v1 -> v3 -> t; there is no shorter path
    assert_valid_path(clrs, path, start="s", end="t")


def test_find_path_uses_backward_edge() -> None:
    # The residual network of the diamond with flow along s -> a -> b -> t.
    residual = Graph.from_edges(
        [("a", "s", 1), ("s", "b", 1), ("b", "a", 1), ("a", "t", 1), ("t", "b", 1)], directed=True
    )
    assert impl.find_augmenting_path(residual, "s", "t") == ["s", "b", "a", "t"]


def test_find_path_prefers_fewest_edges() -> None:
    graph = path_graph(6, directed=True)
    graph.add_edge(1, 4)
    assert impl.find_augmenting_path(graph, 0, 5) == [0, 1, 4, 5]


def test_find_path_unreachable() -> None:
    graph = Graph.from_edges([("s", "a"), ("t", "a")], directed=True)
    assert impl.find_augmenting_path(graph, "s", "t") is None


def test_find_path_trivial_and_unknown() -> None:
    graph = Graph.from_edges([("s", "t")], directed=True)
    assert impl.find_augmenting_path(graph, "s", "s") == ["s"]
    with pytest.raises(KeyError):
        impl.find_augmenting_path(graph, "s", "Vimmerby")
    with pytest.raises(KeyError):
        impl.find_augmenting_path(graph, "Vimmerby", "t")


# ----------------------------------------------------------------------
# edmonds_karp
# ----------------------------------------------------------------------
def test_edmonds_karp_clrs(clrs: Graph) -> None:
    check_max_flow(clrs, "s", "t", impl.edmonds_karp(clrs, "s", "t"), 23)


def test_edmonds_karp_clrs_with_antiparallel_edge(clrs: Graph) -> None:
    # Older editions of the book also have v1 -> v2 (10); the value stays 23.
    clrs.add_edge("v1", "v2", 10)
    check_max_flow(clrs, "s", "t", impl.edmonds_karp(clrs, "s", "t"), 23)


def test_edmonds_karp_diamond(diamond: Graph) -> None:
    check_max_flow(diamond, "s", "t", impl.edmonds_karp(diamond, "s", "t"), 2)


def test_edmonds_karp_backward_edge(detour: Graph) -> None:
    result = impl.edmonds_karp(detour, "s", "t")
    check_max_flow(detour, "s", "t", result, 2)
    assert result[1][("a", "d")] == 0  # the first (greedy) path had to be undone


def test_edmonds_karp_antiparallel(antiparallel: Graph) -> None:
    result = impl.edmonds_karp(antiparallel, "s", "t")
    check_max_flow(antiparallel, "s", "t", result, 5)
    assert result[1] == {
        ("s", "b"): 2,
        ("b", "a"): 0,
        ("a", "t"): 2,
        ("s", "c"): 3,
        ("c", "d"): 3,
        ("d", "a"): 3,
        ("a", "b"): 1,
        ("b", "e"): 3,
        ("e", "f"): 3,
        ("f", "t"): 3,
    }


def test_edmonds_karp_single_edge() -> None:
    graph = Graph.from_edges([("s", "t", 5)], directed=True)
    assert impl.edmonds_karp(graph, "s", "t") == (5, {("s", "t"): 5})


def test_edmonds_karp_sink_unreachable() -> None:
    graph = Graph.from_edges([("s", "a", 3), ("t", "a", 2), ("t", "s", 4)], directed=True)
    value, flow = impl.edmonds_karp(graph, "s", "t")
    assert value == 0
    assert flow == {("s", "a"): 0, ("t", "a"): 0, ("t", "s"): 0}


def test_edmonds_karp_without_edges() -> None:
    graph = Graph(directed=True)
    graph.add_vertices(["s", "t"])
    assert impl.edmonds_karp(graph, "s", "t") == (0, {})


def test_edmonds_karp_zero_capacity() -> None:
    graph = Graph.from_edges([("s", "a", 0), ("a", "t", 7), ("s", "t", 1)], directed=True)
    check_max_flow(graph, "s", "t", impl.edmonds_karp(graph, "s", "t"), 1)


def test_edmonds_karp_float_capacities() -> None:
    graph = Graph.from_edges(
        [("s", "a", 1.5), ("s", "b", 2.25), ("a", "b", 0.5), ("a", "t", 0.75), ("b", "t", 2.5)], directed=True
    )
    # Minimum cut: S = {s, a, b} with 0.75 + 2.5 = 3.25.
    check_max_flow(graph, "s", "t", impl.edmonds_karp(graph, "s", "t"), 3.25)


def test_edmonds_karp_parallel_paths() -> None:
    # Three disjoint paths with bottlenecks 2, 5 and 1.
    graph = Graph.from_edges(
        [("s", "a", 2), ("a", "t", 9), ("s", "b", 6), ("b", "t", 5), ("s", "c", 1), ("c", "t", 1)], directed=True
    )
    check_max_flow(graph, "s", "t", impl.edmonds_karp(graph, "s", "t"), 8)


def test_edmonds_karp_source_with_incoming_edges() -> None:
    # Edges into the source and out of the sink are allowed but useless.
    graph = Graph.from_edges([("s", "a", 4), ("a", "s", 2), ("a", "t", 3), ("t", "a", 5)], directed=True)
    check_max_flow(graph, "s", "t", impl.edmonds_karp(graph, "s", "t"), 3)


def test_edmonds_karp_integrality(clrs: Graph) -> None:
    _value, flow = impl.edmonds_karp(clrs, "s", "t")
    for value in flow.values():
        assert value == int(value)


def test_edmonds_karp_does_not_modify_graph(clrs: Graph) -> None:
    before = clrs.copy()
    impl.edmonds_karp(clrs, "s", "t")
    assert clrs == before


@pytest.mark.parametrize("seed", range(12))
def test_edmonds_karp_random_against_min_cut(seed: int) -> None:
    n = 5 + seed % 3
    graph = random_weighted_graph(n, 0.45, min_weight=1, max_weight=9, seed=seed, directed=True)
    source, sink = 0, n - 1
    expected = brute_force_min_cut(graph, source, sink)
    check_max_flow(graph, source, sink, impl.edmonds_karp(graph, source, sink), expected)


@pytest.mark.parametrize("seed", range(3))
def test_edmonds_karp_larger_random(seed: int) -> None:
    graph = random_weighted_graph(14, 0.3, min_weight=1, max_weight=20, seed=100 + seed, directed=True)
    value, flow = impl.edmonds_karp(graph, 0, 13)
    assert set(flow) == edge_set(graph)
    assert_valid_flow(graph, flow, 0, 13)
    assert flow_value(graph, flow, 0) == pytest.approx(value)
    assert value == pytest.approx(brute_force_min_cut(graph, 0, 13))


def test_edmonds_karp_rejects_undirected() -> None:
    with pytest.raises(ValueError):
        impl.edmonds_karp(Graph.from_edges([("s", "t", 1)]), "s", "t")


def test_edmonds_karp_rejects_same_source_and_sink(clrs: Graph) -> None:
    with pytest.raises(ValueError):
        impl.edmonds_karp(clrs, "s", "s")


def test_edmonds_karp_rejects_negative_capacity() -> None:
    graph = Graph.from_edges([("s", "a", 2), ("a", "t", -1)], directed=True)
    with pytest.raises(ValueError):
        impl.edmonds_karp(graph, "s", "t")


def test_edmonds_karp_unknown_vertices(clrs: Graph) -> None:
    with pytest.raises(KeyError):
        impl.edmonds_karp(clrs, "s", "Vimmerby")
    with pytest.raises(KeyError):
        impl.edmonds_karp(clrs, "Katthult", "t")


# ----------------------------------------------------------------------
# Optional: min_cut
# ----------------------------------------------------------------------
def check_min_cut(graph: Graph, source, sink, cut, expected) -> None:  # type: ignore[no-untyped-def]
    cut = set(cut)
    assert source in cut and sink not in cut
    assert cut <= set(graph.vertices())
    assert cut_capacity(graph, cut) == pytest.approx(expected)


@skip_if_not_implemented
def test_min_cut_clrs(clrs: Graph) -> None:
    cut = impl.min_cut(clrs, "s", "t")
    check_min_cut(clrs, "s", "t", cut, 23)
    assert cut == {"s", "v1", "v2", "v4"}  # the only minimum cut


@skip_if_not_implemented
def test_min_cut_examples(diamond: Graph, detour: Graph, antiparallel: Graph) -> None:
    check_min_cut(diamond, "s", "t", impl.min_cut(diamond, "s", "t"), 2)
    check_min_cut(detour, "s", "t", impl.min_cut(detour, "s", "t"), 2)
    check_min_cut(antiparallel, "s", "t", impl.min_cut(antiparallel, "s", "t"), 5)


@skip_if_not_implemented
def test_min_cut_unreachable_sink() -> None:
    graph = Graph.from_edges([("s", "a", 3), ("t", "a", 2), ("t", "s", 4)], directed=True)
    assert impl.min_cut(graph, "s", "t") == {"s", "a"}


@skip_if_not_implemented
@pytest.mark.parametrize("seed", range(6))
def test_min_cut_random(seed: int) -> None:
    graph = random_weighted_graph(6, 0.45, min_weight=1, max_weight=9, seed=50 + seed, directed=True)
    check_min_cut(graph, 0, 5, impl.min_cut(graph, 0, 5), brute_force_min_cut(graph, 0, 5))


@skip_if_not_implemented
def test_min_cut_invalid_input() -> None:
    with pytest.raises(ValueError):
        impl.min_cut(Graph.from_edges([("s", "t", 1)]), "s", "t")
    with pytest.raises(KeyError):
        impl.min_cut(Graph.from_edges([("s", "t", 1)], directed=True), "s", "x")
