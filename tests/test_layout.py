"""Tests for the vertex layouts (lib/layout.py)."""

import math

import pytest

from lib import generators, layout
from lib.graph import Graph


def assert_in_unit_box(positions: dict) -> None:  # type: ignore[type-arg]
    for x, y in positions.values():
        assert -1e-9 <= x <= 1 + 1e-9
        assert -1e-9 <= y <= 1 + 1e-9


def min_distance(positions: dict) -> float:  # type: ignore[type-arg]
    points = list(positions.values())
    return min(
        math.dist(points[i], points[j]) for i in range(len(points)) for j in range(i + 1, len(points))
    )


def test_normalize_keeps_aspect_ratio() -> None:
    result = layout.normalize({"a": (0, 0), "b": (4, 0), "c": (4, 2)})
    assert result["a"] == pytest.approx((0, 0.25))
    assert result["b"] == pytest.approx((1, 0.25))
    assert result["c"] == pytest.approx((1, 0.75))
    assert layout.normalize({}) == {}
    assert layout.normalize({"x": (3, 3)}) == {"x": (0.5, 0.5)}


def test_circular_layout() -> None:
    positions = layout.circular_layout(range(6))
    assert len(positions) == 6
    assert_in_unit_box(positions)
    assert positions[0] == pytest.approx((0.5, 1.0))  # first vertex on top
    centre = (0.5, 0.5)
    radii = {round(math.dist(p, centre), 9) for p in positions.values()}
    assert len(radii) == 1


def test_shell_layout_petersen() -> None:
    positions = layout.shell_layout([range(5), range(5, 10)])
    assert_in_unit_box(positions)
    centre = (sum(positions[i][0] for i in range(5)) / 5, sum(positions[i][1] for i in range(5)) / 5)
    outer = math.dist(positions[0], centre)
    inner = math.dist(positions[5], centre)
    assert inner == pytest.approx(outer / 2)


def test_bipartite_layout() -> None:
    graph = generators.complete_bipartite_graph(2, 3)
    positions = layout.bipartite_layout(graph, ["L0", "L1"])
    left_x = {positions[v][0] for v in ["L0", "L1"]}
    right_x = {positions[v][0] for v in ["R0", "R1", "R2"]}
    assert len(left_x) == 1 and len(right_x) == 1
    assert left_x.pop() < right_x.pop()


def test_layered_layout() -> None:
    positions = layout.layered_layout([["s"], ["a", "b"], ["t"]])
    assert positions["s"][0] < positions["a"][0] == positions["b"][0] < positions["t"][0]
    assert positions["a"][1] > positions["b"][1]  # first vertex of a layer on top


def test_grid_layout() -> None:
    graph = generators.grid_graph(2, 3)
    positions = layout.grid_layout(graph)
    assert positions[(0, 0)][1] > positions[(1, 0)][1]  # row 0 on top
    assert positions[(0, 0)][0] < positions[(0, 2)][0]


@pytest.mark.parametrize("seed", range(3))
def test_spring_layout_is_reproducible_and_spread_out(seed: int) -> None:
    graph = generators.random_connected_graph(15, 8, seed=seed)
    first = layout.spring_layout(graph, seed=seed)
    second = layout.spring_layout(graph, seed=seed)
    assert first == second
    assert_in_unit_box(first)
    assert min_distance(first) > 0.03  # no two vertices on top of each other


def test_spring_layout_pulls_neighbours_together() -> None:
    graph = generators.path_graph(8)
    positions = layout.spring_layout(graph)
    neighbour = sum(math.dist(positions[i], positions[i + 1]) for i in range(7)) / 7
    assert math.dist(positions[0], positions[7]) > 2 * neighbour


def test_spring_layout_small_graphs() -> None:
    assert layout.spring_layout(Graph()) == {}
    single = Graph()
    single.add_vertex("a")
    assert layout.spring_layout(single) == {"a": (0.5, 0.5)}
    assert len(layout.spring_layout(generators.path_graph(2))) == 2


def test_auto_layout_choices() -> None:
    assert layout.auto_layout(generators.grid_graph(2, 2)) == layout.grid_layout(generators.grid_graph(2, 2))
    assert layout.auto_layout(generators.complete_graph(5)) == layout.circular_layout(range(5))
    assert layout.auto_layout(generators.cycle_graph(6)) == layout.circular_layout(range(6))
    tree = generators.random_tree(10, seed=1)
    assert layout.auto_layout(tree) == layout.spring_layout(tree)
