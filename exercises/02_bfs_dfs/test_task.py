"""Tests for unit 2 (BFS and DFS).

By default these tests check ``task.py``. Use ``pytest --impl=demo`` to check
``demo_solution.py`` instead.
"""

import pytest

from lib.generators import complete_graph, cycle_graph, grid_graph, path_graph, random_graph
from lib.graph import Graph
from lib.testing import assert_valid_path, load_implementation, skip_if_not_implemented

impl = load_implementation(__file__)


@pytest.fixture
def example() -> Graph:
    """The example from README.md: a 'diamond' A-B-D, A-C-D, then D-E, and isolated Z."""
    graph = Graph.from_edges([("A", "B"), ("A", "C"), ("B", "D"), ("C", "D"), ("D", "E")])
    graph.add_vertex("Z")
    return graph


@pytest.fixture
def directed() -> Graph:
    return Graph.from_edges([("a", "b"), ("b", "c"), ("c", "a"), ("c", "d"), ("e", "a")], directed=True)


def check_bfs_tree(graph: Graph, start, distance, parent) -> None:  # type: ignore[no-untyped-def]
    """Every non-start vertex has a parent one step closer to the start."""
    assert set(distance) == set(parent)
    assert distance[start] == 0
    assert parent[start] is None
    for v, p in parent.items():
        if v != start:
            assert graph.has_edge(p, v)
            assert distance[v] == distance[p] + 1


# ----------------------------------------------------------------------
# BFS
# ----------------------------------------------------------------------
def test_bfs_example(example: Graph) -> None:
    distance, parent = impl.bfs(example, "A")
    assert distance == {"A": 0, "B": 1, "C": 1, "D": 2, "E": 3}
    check_bfs_tree(example, "A", distance, parent)


def test_bfs_single_vertex() -> None:
    graph = Graph()
    graph.add_vertex("allein")
    assert impl.bfs(graph, "allein") == ({"allein": 0}, {"allein": None})


def test_bfs_path_graph() -> None:
    distance, _ = impl.bfs(path_graph(10), 0)
    assert distance == {i: i for i in range(10)}


def test_bfs_cycle_distances() -> None:
    distance, _ = impl.bfs(cycle_graph(8), 0)
    assert distance == {0: 0, 1: 1, 7: 1, 2: 2, 6: 2, 3: 3, 5: 3, 4: 4}


def test_bfs_grid_distances() -> None:
    graph = grid_graph(4, 5)
    distance, parent = impl.bfs(graph, (0, 0))
    for (r, c), d in distance.items():
        assert d == r + c  # Manhattan distance
    check_bfs_tree(graph, (0, 0), distance, parent)


def test_bfs_respects_direction(directed: Graph) -> None:
    distance, parent = impl.bfs(directed, "a")
    assert distance == {"a": 0, "b": 1, "c": 2, "d": 3}
    assert "e" not in distance  # e -> a, but not a -> e
    check_bfs_tree(directed, "a", distance, parent)


def test_bfs_unknown_start(example: Graph) -> None:
    with pytest.raises(KeyError):
        impl.bfs(example, "Stockholm")


def test_bfs_does_not_modify_graph(example: Graph) -> None:
    before = example.copy()
    impl.bfs(example, "A")
    assert example == before


@pytest.mark.parametrize("seed", range(5))
def test_bfs_random_graphs(seed: int) -> None:
    graph = random_graph(30, 0.1, seed=seed)
    distance, parent = impl.bfs(graph, 0)
    check_bfs_tree(graph, 0, distance, parent)
    # Optimality: no edge may skip a layer (|d(u) - d(v)| <= 1),
    # and no reached vertex may have an unreached neighbour.
    for u, v, _ in graph.edges():
        if u in distance or v in distance:
            assert u in distance and v in distance
            assert abs(distance[u] - distance[v]) <= 1


# ----------------------------------------------------------------------
# Shortest paths
# ----------------------------------------------------------------------
def test_shortest_path_example(example: Graph) -> None:
    path = impl.shortest_path(example, "A", "E")
    assert len(path) == 4
    assert_valid_path(example, path, start="A", end="E")


def test_shortest_path_to_start(example: Graph) -> None:
    assert impl.shortest_path(example, "D", "D") == ["D"]


def test_shortest_path_unreachable(example: Graph, directed: Graph) -> None:
    assert impl.shortest_path(example, "A", "Z") is None
    assert impl.shortest_path(directed, "a", "e") is None


def test_shortest_path_directed(directed: Graph) -> None:
    assert impl.shortest_path(directed, "e", "d") == ["e", "a", "b", "c", "d"]


def test_shortest_path_unknown_vertices(example: Graph) -> None:
    with pytest.raises(KeyError):
        impl.shortest_path(example, "A", "Stockholm")
    with pytest.raises(KeyError):
        impl.shortest_path(example, "Stockholm", "A")


def test_shortest_path_grid() -> None:
    graph = grid_graph(5, 5)
    path = impl.shortest_path(graph, (0, 0), (4, 3))
    assert len(path) == 8
    assert_valid_path(graph, path, start=(0, 0), end=(4, 3))


# ----------------------------------------------------------------------
# DFS
# ----------------------------------------------------------------------
def check_search_order(graph: Graph, start, order) -> None:  # type: ignore[no-untyped-def]
    """``order`` starts at ``start``, has no repetitions, and every later vertex
    is a neighbour of some vertex visited before it."""
    assert order[0] == start
    assert len(order) == len(set(order))
    for i in range(1, len(order)):
        assert any(graph.has_edge(order[j], order[i]) for j in range(i))


def test_dfs_example(example: Graph) -> None:
    order = impl.dfs(example, "A")
    assert set(order) == {"A", "B", "C", "D", "E"}
    check_search_order(example, "A", order)


def test_dfs_isolated_vertex(example: Graph) -> None:
    assert impl.dfs(example, "Z") == ["Z"]


def test_dfs_path_graph_goes_deep() -> None:
    assert impl.dfs(path_graph(6), 0) == [0, 1, 2, 3, 4, 5]
    assert impl.dfs(path_graph(6), 3) in ([3, 2, 1, 0, 4, 5], [3, 4, 5, 2, 1, 0])


def test_dfs_is_depth_first() -> None:
    # In a star of two long arms, DFS must finish one arm before the other.
    graph = Graph.from_edges([("s", "a1"), ("a1", "a2"), ("a2", "a3"), ("s", "b1"), ("b1", "b2"), ("b2", "b3")])
    order = impl.dfs(graph, "s")
    assert order in (["s", "a1", "a2", "a3", "b1", "b2", "b3"], ["s", "b1", "b2", "b3", "a1", "a2", "a3"])


def test_dfs_directed(directed: Graph) -> None:
    order = impl.dfs(directed, "a")
    assert set(order) == {"a", "b", "c", "d"}
    check_search_order(directed, "a", order)


def test_dfs_long_path_no_recursion_limit() -> None:
    graph = path_graph(5000)
    assert len(impl.dfs(graph, 0)) == 5000


def test_dfs_unknown_start(example: Graph) -> None:
    with pytest.raises(KeyError):
        impl.dfs(example, "Stockholm")


@pytest.mark.parametrize("seed", range(5))
def test_dfs_and_bfs_find_same_vertices(seed: int) -> None:
    graph = random_graph(25, 0.08, seed=seed)
    distance, _ = impl.bfs(graph, 0)
    order = impl.dfs(graph, 0)
    assert set(order) == set(distance)
    check_search_order(graph, 0, order)


# ----------------------------------------------------------------------
# Connected components
# ----------------------------------------------------------------------
def as_frozensets(components):  # type: ignore[no-untyped-def]
    return {frozenset(c) for c in components}


def test_components_example(example: Graph) -> None:
    components = impl.connected_components(example)
    assert len(components) == 2
    assert as_frozensets(components) == {frozenset("ABCDE"), frozenset("Z")}


def test_components_empty_graph() -> None:
    assert impl.connected_components(Graph()) == []


def test_components_without_edges() -> None:
    graph = Graph()
    graph.add_vertices([1, 2, 3])
    assert as_frozensets(impl.connected_components(graph)) == {frozenset([1]), frozenset([2]), frozenset([3])}


def test_components_three_parts() -> None:
    graph = Graph.from_edges([(1, 2), (2, 3), (4, 5), (6, 7), (7, 8), (8, 6)])
    assert as_frozensets(impl.connected_components(graph)) == {
        frozenset([1, 2, 3]),
        frozenset([4, 5]),
        frozenset([6, 7, 8]),
    }


@pytest.mark.parametrize("seed", range(5))
def test_components_partition_vertices(seed: int) -> None:
    graph = random_graph(40, 0.04, seed=seed)
    components = impl.connected_components(graph)
    all_vertices = [v for c in components for v in c]
    assert sorted(all_vertices) == sorted(graph.vertices())
    lookup = {v: i for i, c in enumerate(components) for v in c}
    for u, v, _ in graph.edges():
        assert lookup[u] == lookup[v]  # edges never connect two components


def test_components_reject_directed(directed: Graph) -> None:
    with pytest.raises(ValueError):
        impl.connected_components(directed)


def test_is_connected(example: Graph) -> None:
    assert impl.is_connected(example) is False
    assert impl.is_connected(complete_graph(5)) is True
    assert impl.is_connected(path_graph(1)) is True
    assert impl.is_connected(Graph()) is True
    with pytest.raises(ValueError):
        impl.is_connected(Graph(directed=True))


# ----------------------------------------------------------------------
# Optional tasks
# ----------------------------------------------------------------------
@skip_if_not_implemented
def test_dfs_recursive(example: Graph) -> None:
    order = impl.dfs_recursive(example, "A")
    assert set(order) == {"A", "B", "C", "D", "E"}
    check_search_order(example, "A", order)
    assert impl.dfs_recursive(path_graph(5), 0) == [0, 1, 2, 3, 4]


@skip_if_not_implemented
def test_bfs_layers(example: Graph) -> None:
    layers = impl.bfs_layers(example, "A")
    assert [set(layer) for layer in layers] == [{"A"}, {"B", "C"}, {"D"}, {"E"}]
