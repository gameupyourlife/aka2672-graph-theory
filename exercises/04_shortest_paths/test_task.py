"""Tests for unit 4 (shortest paths: Dijkstra, path reconstruction, Bellman-Ford).

By default these tests check ``task.py``. Use ``pytest --impl=demo`` to check
``demo_solution.py`` instead.
"""

import random

import pytest

from lib.generators import grid_graph, path_graph, random_connected_graph, random_weighted_graph, small_weighted_graph
from lib.graph import Graph
from lib.testing import assert_valid_path, load_implementation, skip_if_not_implemented
from lib.utils import path_weight

impl = load_implementation(__file__)

# Hand-computed distances in small_weighted_graph() from Katthult and from Markt.
FROM_KATTHULT = {"Katthult": 0, "Gibberyd": 2, "Lönneberga": 4, "Kirche": 5, "Backhorva": 7, "Markt": 7}
FROM_MARKT = {"Markt": 0, "Kirche": 2, "Gibberyd": 5, "Backhorva": 6, "Lönneberga": 7, "Katthult": 7}


@pytest.fixture
def lonneberga() -> Graph:
    return small_weighted_graph()


@pytest.fixture
def one_way() -> Graph:
    """Directed roads ("one-way streets"). Mariannelund only has a road *to* Katthult.

    From Katthult: Gibberyd 1, Lönneberga 3 (via Gibberyd), Backhorva 5,
    Vimmerby 9; Mariannelund is unreachable.
    """
    return Graph.from_edges(
        [
            ("Katthult", "Lönneberga", 4),
            ("Katthult", "Gibberyd", 1),
            ("Gibberyd", "Lönneberga", 2),
            ("Lönneberga", "Vimmerby", 6),
            ("Lönneberga", "Backhorva", 2),
            ("Vimmerby", "Katthult", 1),
            ("Mariannelund", "Katthult", 3),
        ],
        directed=True,
    )


def arcs(graph: Graph):  # type: ignore[no-untyped-def]
    """All edges as (u, v, weight); undirected edges in both directions."""
    return [(u, v, graph.weight(u, v)) for u in graph.vertices() for v in graph.neighbors(u)]


def check_shortest_path_tree(graph: Graph, start, dist, parent) -> None:  # type: ignore[no-untyped-def]
    """Certificate for correct shortest-path results (non-negative weights).

    * the parent pointers form a tree rooted at ``start`` whose edges are
      "tight": dist[v] = dist[parent[v]] + w(parent[v], v),
    * no edge can improve a distance: dist[v] <= dist[u] + w(u, v), and
      every vertex reachable via an edge is contained in ``dist``.
    """
    assert set(dist) == set(parent), "dist and parent must have the same keys"
    assert dist[start] == 0
    assert parent[start] is None
    for v in dist:
        if v == start:
            continue
        p = parent[v]
        assert p in dist, f"parent[{v!r}] = {p!r} is not a reached vertex"
        assert graph.has_edge(p, v), f"parent edge {p!r} -> {v!r} does not exist"
        assert dist[v] == pytest.approx(dist[p] + graph.weight(p, v)), f"dist[{v!r}] does not match its parent edge"
        # Following the parents must lead back to start (no cycles).
        x, steps = v, 0
        while x != start:
            x = parent[x]
            steps += 1
            assert steps <= len(dist), "The parent pointers contain a cycle"
    for u, v, weight in arcs(graph):
        if u in dist:
            assert v in dist, f"{v!r} is reachable via {u!r} but missing in dist"
            assert dist[v] <= dist[u] + weight + 1e-9, f"Edge {u!r} -> {v!r} gives a shorter way to {v!r}"


def brute_force_distances(graph: Graph, start):  # type: ignore[no-untyped-def]
    """Minimum length over *all* simple paths from ``start`` (tiny graphs only)."""
    best: dict = {}
    stack = [(start, 0, frozenset([start]))]
    while stack:
        v, length, seen = stack.pop()
        if v not in best or length < best[v]:
            best[v] = length
        for w in graph.neighbors(v):
            if w not in seen:
                stack.append((w, length + graph.weight(v, w), seen | {w}))
    return best


def assert_same_distances(actual, expected) -> None:  # type: ignore[no-untyped-def]
    assert set(actual) == set(expected)
    for v, d in expected.items():
        assert actual[v] == pytest.approx(d), f"Wrong distance for {v!r}"


# ----------------------------------------------------------------------
# Dijkstra
# ----------------------------------------------------------------------
def test_dijkstra_lonneberga(lonneberga: Graph) -> None:
    dist, parent = impl.dijkstra(lonneberga, "Katthult")
    assert dist == FROM_KATTHULT
    # All shortest paths from Katthult are unique here.
    assert parent == {
        "Katthult": None,
        "Gibberyd": "Katthult",
        "Lönneberga": "Katthult",
        "Kirche": "Gibberyd",
        "Backhorva": "Lönneberga",
        "Markt": "Kirche",
    }


def test_dijkstra_lonneberga_from_markt(lonneberga: Graph) -> None:
    dist, parent = impl.dijkstra(lonneberga, "Markt")
    assert dist == FROM_MARKT
    check_shortest_path_tree(lonneberga, "Markt", dist, parent)


def test_dijkstra_single_vertex() -> None:
    graph = Graph()
    graph.add_vertex("Katthult")
    assert impl.dijkstra(graph, "Katthult") == ({"Katthult": 0}, {"Katthult": None})


def test_dijkstra_directed(one_way: Graph) -> None:
    dist, parent = impl.dijkstra(one_way, "Katthult")
    assert dist == {"Katthult": 0, "Gibberyd": 1, "Lönneberga": 3, "Backhorva": 5, "Vimmerby": 9}
    assert parent["Lönneberga"] == "Gibberyd"
    assert "Mariannelund" not in dist and "Mariannelund" not in parent
    check_shortest_path_tree(one_way, "Katthult", dist, parent)


def test_dijkstra_directed_other_start(one_way: Graph) -> None:
    dist, _ = impl.dijkstra(one_way, "Vimmerby")
    assert dist == {"Vimmerby": 0, "Katthult": 1, "Gibberyd": 2, "Lönneberga": 4, "Backhorva": 6}
    assert impl.dijkstra(one_way, "Backhorva") == ({"Backhorva": 0}, {"Backhorva": None})


def test_dijkstra_unreachable_vertices(lonneberga: Graph) -> None:
    lonneberga.add_edge("Vimmerby", "Mariannelund", 3)  # a second component
    lonneberga.add_vertex("Sevedstorp")  # an isolated vertex
    dist, parent = impl.dijkstra(lonneberga, "Katthult")
    assert dist == FROM_KATTHULT
    assert set(parent) == set(FROM_KATTHULT)
    assert impl.dijkstra(lonneberga, "Mariannelund")[0] == {"Mariannelund": 0, "Vimmerby": 3}


def test_dijkstra_prefers_many_light_edges() -> None:
    # The direct edge is heavier than the detour over four light edges.
    graph = path_graph(5)
    graph.add_edge(0, 4, 5)
    dist, parent = impl.dijkstra(graph, 0)
    assert dist == {0: 0, 1: 1, 2: 2, 3: 3, 4: 4}
    assert parent[4] == 3


def test_dijkstra_float_weights() -> None:
    graph = Graph.from_edges([("a", "b", 0.1), ("b", "c", 0.2), ("a", "c", 0.35), ("c", "d", 1.5)])
    dist, parent = impl.dijkstra(graph, "a")
    assert_same_distances(dist, {"a": 0, "b": 0.1, "c": 0.3, "d": 1.8})
    assert parent["c"] == "b"
    check_shortest_path_tree(graph, "a", dist, parent)


def test_dijkstra_zero_weights() -> None:
    graph = Graph.from_edges([("a", "b", 0), ("b", "c", 0), ("a", "c", 1), ("c", "d", 2)], directed=True)
    dist, parent = impl.dijkstra(graph, "a")
    assert dist == {"a": 0, "b": 0, "c": 0, "d": 2}
    check_shortest_path_tree(graph, "a", dist, parent)


def test_dijkstra_ties() -> None:
    # Two shortest ways from a to d (via b or via c) - both are accepted.
    graph = Graph.from_edges([("a", "b", 1), ("b", "d", 2), ("a", "c", 2), ("c", "d", 1), ("d", "e", 1)])
    dist, parent = impl.dijkstra(graph, "a")
    assert dist == {"a": 0, "b": 1, "c": 2, "d": 3, "e": 4}
    assert parent["d"] in ("b", "c")
    check_shortest_path_tree(graph, "a", dist, parent)


def test_dijkstra_unweighted_grid_equals_bfs() -> None:
    graph = grid_graph(5, 6)
    dist, parent = impl.dijkstra(graph, (0, 0))
    assert dist == {(r, c): r + c for r in range(5) for c in range(6)}
    check_shortest_path_tree(graph, (0, 0), dist, parent)


def test_dijkstra_unknown_start(lonneberga: Graph) -> None:
    with pytest.raises(KeyError):
        impl.dijkstra(lonneberga, "Stockholm")


def test_dijkstra_rejects_negative_weights() -> None:
    counterexample = Graph.from_edges([("s", "a", 2), ("s", "b", 3), ("b", "a", -2)], directed=True)
    with pytest.raises(ValueError):
        impl.dijkstra(counterexample, "s")


def test_dijkstra_rejects_unreachable_negative_edge() -> None:
    # The negative edge cannot be reached from "a" - it is rejected anyway.
    graph = Graph.from_edges([("a", "b", 1), ("x", "y", -1)])
    with pytest.raises(ValueError):
        impl.dijkstra(graph, "a")
    directed = Graph.from_edges([("a", "b", 1), ("y", "x", -0.5)], directed=True)
    with pytest.raises(ValueError):
        impl.dijkstra(directed, "a")


def test_dijkstra_does_not_modify_graph(lonneberga: Graph) -> None:
    before = lonneberga.copy()
    impl.dijkstra(lonneberga, "Katthult")
    assert lonneberga == before


@pytest.mark.parametrize("directed", [False, True])
@pytest.mark.parametrize("seed", range(6))
def test_dijkstra_matches_brute_force(seed: int, directed: bool) -> None:
    graph = random_weighted_graph(7, 0.4, min_weight=0, max_weight=9, seed=seed, directed=directed)
    dist, parent = impl.dijkstra(graph, 0)
    assert_same_distances(dist, brute_force_distances(graph, 0))
    check_shortest_path_tree(graph, 0, dist, parent)


@pytest.mark.parametrize("seed", range(5))
def test_dijkstra_random_large(seed: int) -> None:
    graph = random_connected_graph(80, 200, seed=seed, min_weight=1, max_weight=30)
    dist, parent = impl.dijkstra(graph, 0)
    assert len(dist) == 80
    check_shortest_path_tree(graph, 0, dist, parent)


@pytest.mark.parametrize("seed", range(3))
def test_dijkstra_random_directed_large(seed: int) -> None:
    graph = random_weighted_graph(60, 0.05, min_weight=0, max_weight=20, seed=seed, directed=True)
    dist, parent = impl.dijkstra(graph, 0)
    check_shortest_path_tree(graph, 0, dist, parent)


# ----------------------------------------------------------------------
# reconstruct_path
# ----------------------------------------------------------------------
def test_reconstruct_path_by_hand() -> None:
    parent = {"Katthult": None, "Gibberyd": "Katthult", "Kirche": "Gibberyd", "Markt": "Kirche"}
    assert impl.reconstruct_path(parent, "Markt") == ["Katthult", "Gibberyd", "Kirche", "Markt"]
    assert impl.reconstruct_path(parent, "Gibberyd") == ["Katthult", "Gibberyd"]
    assert impl.reconstruct_path(parent, "Katthult") == ["Katthult"]


def test_reconstruct_path_missing_target() -> None:
    parent = {"a": None, "b": "a"}
    assert impl.reconstruct_path(parent, "z") is None
    assert impl.reconstruct_path({}, "a") is None


def test_reconstruct_path_does_not_modify_parent() -> None:
    parent = {0: None, 1: 0, 2: 1}
    impl.reconstruct_path(parent, 2)
    assert parent == {0: None, 1: 0, 2: 1}


@pytest.mark.parametrize("start", ["Katthult", "Markt", "Backhorva"])
def test_reconstruct_path_after_dijkstra(lonneberga: Graph, start: str) -> None:
    dist, parent = impl.dijkstra(lonneberga, start)
    for target in lonneberga.vertices():
        path = impl.reconstruct_path(parent, target)
        assert_valid_path(lonneberga, path, start=start, end=target)
        assert path_weight(lonneberga, path) == dist[target]


# ----------------------------------------------------------------------
# shortest_route
# ----------------------------------------------------------------------
def test_shortest_route_lonneberga(lonneberga: Graph) -> None:
    assert impl.shortest_route(lonneberga, "Katthult", "Markt") == (["Katthult", "Gibberyd", "Kirche", "Markt"], 7)
    assert impl.shortest_route(lonneberga, "Katthult", "Backhorva") == (["Katthult", "Lönneberga", "Backhorva"], 7)
    assert impl.shortest_route(lonneberga, "Markt", "Katthult") == (["Markt", "Kirche", "Gibberyd", "Katthult"], 7)


def test_shortest_route_start_equals_target(lonneberga: Graph) -> None:
    assert impl.shortest_route(lonneberga, "Kirche", "Kirche") == (["Kirche"], 0)


def test_shortest_route_unreachable(lonneberga: Graph, one_way: Graph) -> None:
    lonneberga.add_vertex("Vimmerby")
    assert impl.shortest_route(lonneberga, "Katthult", "Vimmerby") is None
    assert impl.shortest_route(one_way, "Katthult", "Mariannelund") is None
    assert impl.shortest_route(one_way, "Backhorva", "Lönneberga") is None


def test_shortest_route_directed(one_way: Graph) -> None:
    assert impl.shortest_route(one_way, "Vimmerby", "Backhorva") == (
        ["Vimmerby", "Katthult", "Gibberyd", "Lönneberga", "Backhorva"],
        6,
    )
    assert impl.shortest_route(one_way, "Mariannelund", "Vimmerby") == (
        ["Mariannelund", "Katthult", "Gibberyd", "Lönneberga", "Vimmerby"],
        12,
    )


def test_shortest_route_ties() -> None:
    graph = grid_graph(3, 3)
    path, length = impl.shortest_route(graph, (0, 0), (2, 2))
    assert length == 4
    assert_valid_path(graph, path, start=(0, 0), end=(2, 2))
    assert path_weight(graph, path) == 4


def test_shortest_route_float_weights() -> None:
    graph = Graph.from_edges([("a", "b", 1.5), ("b", "c", 1.25), ("a", "c", 3.0)])
    path, length = impl.shortest_route(graph, "a", "c")
    assert path == ["a", "b", "c"]
    assert length == pytest.approx(2.75)


def test_shortest_route_invalid_input(lonneberga: Graph) -> None:
    with pytest.raises(KeyError):
        impl.shortest_route(lonneberga, "Katthult", "Stockholm")
    with pytest.raises(KeyError):
        impl.shortest_route(lonneberga, "Stockholm", "Katthult")
    lonneberga.set_weight("Kirche", "Markt", -2)
    with pytest.raises(ValueError):
        impl.shortest_route(lonneberga, "Katthult", "Markt")


@pytest.mark.parametrize("seed", range(5))
def test_shortest_route_random(seed: int) -> None:
    graph = random_weighted_graph(7, 0.45, min_weight=1, max_weight=6, seed=seed, directed=True)
    expected = brute_force_distances(graph, 0)
    for target in graph.vertices():
        result = impl.shortest_route(graph, 0, target)
        if target not in expected:
            assert result is None
            continue
        path, length = result
        assert_valid_path(graph, path, start=0, end=target)
        assert length == expected[target]
        assert path_weight(graph, path) == expected[target]


# ----------------------------------------------------------------------
# Optional: Bellman-Ford
# ----------------------------------------------------------------------
@skip_if_not_implemented
def test_bellman_ford_counterexample() -> None:
    graph = Graph.from_edges([("s", "a", 2), ("s", "b", 3), ("b", "a", -2)], directed=True)
    dist, parent = impl.bellman_ford(graph, "s")
    assert dist == {"s": 0, "a": 1, "b": 3}
    assert parent == {"s": None, "a": "b", "b": "s"}


@skip_if_not_implemented
def test_bellman_ford_negative_edges() -> None:
    graph = Graph.from_edges(
        [
            ("s", "a", 4),
            ("s", "b", 5),
            ("b", "a", -2),
            ("a", "c", -3),
            ("c", "d", 2),
            ("b", "d", 4),
            ("d", "e", -1),
            ("x", "s", 1),  # x is not reachable from s
        ],
        directed=True,
    )
    dist, parent = impl.bellman_ford(graph, "s")
    assert dist == {"s": 0, "b": 5, "a": 3, "c": 0, "d": 2, "e": 1}
    assert impl.reconstruct_path(parent, "e") == ["s", "b", "a", "c", "d", "e"]


@skip_if_not_implemented
def test_bellman_ford_negative_cycle() -> None:
    graph = Graph.from_edges([("s", "a", 1), ("a", "b", -3), ("b", "a", 1), ("b", "t", 2)], directed=True)
    with pytest.raises(ValueError):
        impl.bellman_ford(graph, "s")


@skip_if_not_implemented
def test_bellman_ford_unreachable_negative_cycle() -> None:
    # The negative cycle x -> y -> x cannot be reached from s: no problem.
    graph = Graph.from_edges([("s", "a", 2), ("a", "b", -1), ("x", "y", -2), ("y", "x", 1), ("x", "s", 1)], directed=True)
    dist, parent = impl.bellman_ford(graph, "s")
    assert dist == {"s": 0, "a": 2, "b": 1}
    assert set(parent) == {"s", "a", "b"}


@skip_if_not_implemented
def test_bellman_ford_undirected(lonneberga: Graph) -> None:
    dist, parent = impl.bellman_ford(lonneberga, "Katthult")
    assert dist == FROM_KATTHULT
    check_shortest_path_tree(lonneberga, "Katthult", dist, parent)
    lonneberga.set_weight("Backhorva", "Markt", -1)  # u - v - u is a negative closed walk
    with pytest.raises(ValueError):
        impl.bellman_ford(lonneberga, "Katthult")


@skip_if_not_implemented
def test_bellman_ford_edge_cases(lonneberga: Graph) -> None:
    with pytest.raises(KeyError):
        impl.bellman_ford(lonneberga, "Stockholm")
    single = Graph(directed=True)
    single.add_vertex("Ida")
    assert impl.bellman_ford(single, "Ida") == ({"Ida": 0}, {"Ida": None})


@skip_if_not_implemented
@pytest.mark.parametrize("seed", range(6))
def test_bellman_ford_random_dag(seed: int) -> None:
    # Edges only go from smaller to larger numbers: no cycles at all, so
    # negative weights are fine and the brute force is the right answer.
    rng = random.Random(seed)
    graph = Graph(directed=True)
    graph.add_vertices(range(7))
    for i in range(7):
        for j in range(i + 1, 7):
            if rng.random() < 0.5:
                graph.add_edge(i, j, rng.randint(-5, 8))
    dist, parent = impl.bellman_ford(graph, 0)
    assert_same_distances(dist, brute_force_distances(graph, 0))
    for v in dist:
        path = impl.reconstruct_path(parent, v)
        assert_valid_path(graph, path, start=0, end=v)
        assert path_weight(graph, path) == dist[v]


@skip_if_not_implemented
@pytest.mark.parametrize("seed", range(4))
def test_bellman_ford_agrees_with_brute_force_non_negative(seed: int) -> None:
    graph = random_weighted_graph(7, 0.4, min_weight=0, max_weight=9, seed=seed, directed=seed % 2 == 0)
    dist, parent = impl.bellman_ford(graph, 0)
    assert_same_distances(dist, brute_force_distances(graph, 0))
    check_shortest_path_tree(graph, 0, dist, parent)
