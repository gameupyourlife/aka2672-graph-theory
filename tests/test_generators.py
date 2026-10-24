"""Tests for the graph generators (lib/generators.py)."""

import pytest

from lib import generators
from lib.testing import count_components


def test_path_graph() -> None:
    graph = generators.path_graph(5)
    assert graph.vertices() == [0, 1, 2, 3, 4]
    assert graph.num_edges() == 4
    assert graph.degree(0) == 1
    assert graph.degree(2) == 2
    assert generators.path_graph(0).num_vertices() == 0
    assert generators.path_graph(1).num_edges() == 0


def test_directed_path_graph() -> None:
    graph = generators.path_graph(3, directed=True)
    assert graph.has_edge(0, 1)
    assert not graph.has_edge(1, 0)


def test_cycle_graph() -> None:
    graph = generators.cycle_graph(6)
    assert graph.num_edges() == 6
    assert all(graph.degree(v) == 2 for v in graph)
    with pytest.raises(ValueError):
        generators.cycle_graph(2)


@pytest.mark.parametrize("n", [0, 1, 2, 5, 7])
def test_complete_graph(n: int) -> None:
    graph = generators.complete_graph(n)
    assert graph.num_vertices() == n
    assert graph.num_edges() == n * (n - 1) // 2
    assert all(graph.degree(v) == n - 1 for v in graph)


def test_complete_bipartite_graph() -> None:
    graph = generators.complete_bipartite_graph(3, 2)
    assert graph.num_vertices() == 5
    assert graph.num_edges() == 6
    assert graph.has_edge("L0", "R1")
    assert not graph.has_edge("L0", "L1")


def test_star_and_grid() -> None:
    star = generators.star_graph(4)
    assert star.degree(0) == 4
    grid = generators.grid_graph(3, 4)
    assert grid.num_vertices() == 12
    assert grid.num_edges() == 3 * 3 + 2 * 4
    assert grid.degree((1, 1)) == 4


def test_petersen_graph() -> None:
    graph = generators.petersen_graph()
    assert graph.num_vertices() == 10
    assert graph.num_edges() == 15
    assert all(graph.degree(v) == 3 for v in graph)


def test_random_graph_is_reproducible() -> None:
    a = generators.random_graph(20, 0.3, seed=42)
    b = generators.random_graph(20, 0.3, seed=42)
    c = generators.random_graph(20, 0.3, seed=43)
    assert a == b
    assert a != c
    a.check_consistency()


def test_random_graph_extremes() -> None:
    assert generators.random_graph(6, 0.0, seed=1).num_edges() == 0
    assert generators.random_graph(6, 1.0, seed=1).num_edges() == 15
    assert generators.random_graph(4, 1.0, seed=1, directed=True).num_edges() == 12
    with pytest.raises(ValueError):
        generators.random_graph(4, 1.5)


@pytest.mark.parametrize("seed", range(5))
def test_random_tree(seed: int) -> None:
    tree = generators.random_tree(15, seed=seed)
    assert tree.num_vertices() == 15
    assert tree.num_edges() == 14
    assert count_components(tree) == 1


@pytest.mark.parametrize("seed", range(5))
def test_random_connected_graph(seed: int) -> None:
    graph = generators.random_connected_graph(12, 5, seed=seed, min_weight=1, max_weight=9)
    assert count_components(graph) == 1
    assert graph.num_edges() == 11 + 5
    assert all(1 <= w <= 9 for _, _, w in graph.edges())
    assert graph == generators.random_connected_graph(12, 5, seed=seed, min_weight=1, max_weight=9)


def test_random_connected_graph_cannot_exceed_complete() -> None:
    graph = generators.random_connected_graph(4, 100, seed=0)
    assert graph.num_edges() == 6


def test_random_bipartite_graph() -> None:
    graph = generators.random_bipartite_graph(4, 5, 0.5, seed=3)
    for u, v, _ in graph.edges():
        assert {u[0], v[0]} == {"L", "R"}
    assert graph == generators.random_bipartite_graph(4, 5, 0.5, seed=3)


def test_random_weighted_graph() -> None:
    graph = generators.random_weighted_graph(15, 0.4, 2, 8, seed=7)
    assert graph.num_edges() > 0
    assert all(2 <= w <= 8 for _, _, w in graph.edges())
    assert graph == generators.random_weighted_graph(15, 0.4, 2, 8, seed=7)
    directed = generators.random_weighted_graph(6, 0.5, seed=1, directed=True)
    assert directed.directed


def test_small_weighted_graph() -> None:
    graph = generators.small_weighted_graph()
    assert graph.num_vertices() == 6
    assert graph.num_edges() == 8
    assert graph.weight("Kirche", "Markt") == 2
    assert count_components(graph) == 1


def test_negative_sizes_are_rejected() -> None:
    with pytest.raises(ValueError):
        generators.path_graph(-1)
    with pytest.raises(ValueError):
        generators.complete_bipartite_graph(2, -1)
