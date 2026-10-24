"""Tests for unit 7 (bipartite matching).

By default these tests check ``task.py``. Use ``pytest --impl=demo`` to check
``demo_solution.py`` instead.
"""

import itertools

import pytest

from lib.generators import (
    complete_bipartite_graph,
    cycle_graph,
    grid_graph,
    path_graph,
    random_bipartite_graph,
    star_graph,
)
from lib.graph import Graph
from lib.testing import assert_valid_matching, load_implementation, skip_if_not_implemented

impl = load_implementation(__file__)

PEOPLE = ["Pippi", "Tommy", "Annika", "Kling"]


@pytest.fixture
def villa() -> Graph:
    """The example from README.md. It has exactly one perfect matching."""
    return Graph.from_edges(
        [
            ("Pippi", "Pferd"),
            ("Pippi", "Pfannkuchen"),
            ("Tommy", "Pfannkuchen"),
            ("Tommy", "Garten"),
            ("Annika", "Garten"),
            ("Annika", "Einkauf"),
            ("Kling", "Pferd"),
        ]
    )


@pytest.fixture
def horses() -> Graph:
    """Tommy and Annika both only want the horse: at most 2 people get a task."""
    return Graph.from_edges([("Pippi", "Pferd"), ("Pippi", "Garten"), ("Tommy", "Pferd"), ("Annika", "Pferd")])


def left_of(graph: Graph) -> list:  # type: ignore[type-arg]
    """Left vertices of the generator graphs: names starting with 'L'."""
    return [v for v in graph.vertices() if str(v).startswith("L")]


def brute_force_matching_size(graph: Graph) -> int:
    """Size of a maximum matching by trying all edge subsets (tiny graphs only)."""
    edges = [(u, v) for u, v, _ in graph.edges()]
    for k in range(len(edges), 0, -1):
        for subset in itertools.combinations(edges, k):
            ends = [x for edge in subset for x in edge]
            if len(ends) == len(set(ends)):  # no common end vertices
                return k
    return 0


def check_augmenting_path(graph: Graph, left, matching, path) -> None:  # type: ignore[no-untyped-def]
    """Check the structure [l0, r0, l1, r1, ..., lk, rk] of an augmenting path."""
    left = set(left)
    matched_right = set(matching.values())
    assert path is not None, "Expected an augmenting path, got None"
    assert len(path) >= 2 and len(path) % 2 == 0, f"Wrong length: {path}"
    assert len(set(path)) == len(path), f"A vertex appears twice: {path}"
    assert path[0] in left and path[0] not in matching, "The path must start at an unmatched left vertex"
    assert path[-1] not in left and path[-1] not in matched_right, "The path must end at an unmatched right vertex"
    for i in range(0, len(path), 2):
        l, r = path[i], path[i + 1]
        assert l in left and r not in left, f"{l!r} must be left, {r!r} right"
        assert graph.has_edge(l, r), f"There is no edge {l!r} - {r!r}"
        assert matching.get(l) != r, f"{l!r} - {r!r} must not be a matching edge"
        if i + 2 < len(path):
            assert matching.get(path[i + 2]) == r, f"{r!r} - {path[i + 2]!r} must be a matching edge"


def symmetric_difference(matching, path):  # type: ignore[no-untyped-def]
    """Reference augmentation for the tests (independent of the implementation)."""
    new = dict(matching)
    for i in range(0, len(path), 2):
        new[path[i]] = path[i + 1]
    return new


# ----------------------------------------------------------------------
# augment
# ----------------------------------------------------------------------
def test_augment_villa() -> None:
    greedy = {"Pippi": "Pferd", "Tommy": "Pfannkuchen", "Annika": "Garten"}
    path = ["Kling", "Pferd", "Pippi", "Pfannkuchen", "Tommy", "Garten", "Annika", "Einkauf"]
    result = impl.augment(greedy, path)
    assert result == {"Kling": "Pferd", "Pippi": "Pfannkuchen", "Tommy": "Garten", "Annika": "Einkauf"}
    assert greedy == {"Pippi": "Pferd", "Tommy": "Pfannkuchen", "Annika": "Garten"}  # unchanged


def test_augment_single_edge() -> None:
    matching: dict = {}  # type: ignore[type-arg]
    assert impl.augment(matching, ["a", "x"]) == {"a": "x"}
    assert matching == {}
    assert impl.augment({"b": "y"}, ["a", "x"]) == {"a": "x", "b": "y"}


def test_augment_returns_new_dict() -> None:
    matching = {"Pippi": "Pfannkuchen"}
    result = impl.augment(matching, ["Tommy", "Pfannkuchen", "Pippi", "Pferd"])
    assert result == {"Pippi": "Pferd", "Tommy": "Pfannkuchen"}
    assert result is not matching
    assert matching == {"Pippi": "Pfannkuchen"}


def test_augment_invalid_path() -> None:
    with pytest.raises(ValueError):
        impl.augment({}, [])
    with pytest.raises(ValueError):
        impl.augment({}, ["a", "x", "b"])


# ----------------------------------------------------------------------
# find_augmenting_path
# ----------------------------------------------------------------------
def test_find_path_villa(villa: Graph) -> None:
    greedy = {"Pippi": "Pferd", "Tommy": "Pfannkuchen", "Annika": "Garten"}
    path = impl.find_augmenting_path(villa, PEOPLE, greedy)
    # Only Kling and Einkauf are free, and there is only one alternating path.
    assert path == ["Kling", "Pferd", "Pippi", "Pfannkuchen", "Tommy", "Garten", "Annika", "Einkauf"]
    assert greedy == {"Pippi": "Pferd", "Tommy": "Pfannkuchen", "Annika": "Garten"}  # unchanged


def test_find_path_small_example() -> None:
    graph = Graph.from_edges([("Pippi", "Pfannkuchen"), ("Pippi", "Pferd"), ("Tommy", "Pfannkuchen")])
    left = ["Pippi", "Tommy"]
    assert impl.find_augmenting_path(graph, left, {"Pippi": "Pfannkuchen"}) == ["Tommy", "Pfannkuchen", "Pippi", "Pferd"]
    assert impl.find_augmenting_path(graph, left, {"Pippi": "Pferd", "Tommy": "Pfannkuchen"}) is None


def test_find_path_empty_matching(villa: Graph) -> None:
    path = impl.find_augmenting_path(villa, PEOPLE, {})
    check_augmenting_path(villa, PEOPLE, {}, path)
    assert len(path) == 2  # with an empty matching every edge is augmenting


def test_find_path_none_for_maximum_matching() -> None:
    graph = complete_bipartite_graph(2, 3)
    assert impl.find_augmenting_path(graph, ["L0", "L1"], {"L0": "R0", "L1": "R1"}) is None


def test_find_path_none_without_edges() -> None:
    graph = Graph()
    graph.add_vertices(["a", "b", "x"])
    assert impl.find_augmenting_path(graph, ["a", "b"], {}) is None
    assert impl.find_augmenting_path(Graph(), [], {}) is None


def test_find_path_in_path_graph() -> None:
    # 0 - 1 - 2 - 3 - 4 - 5 with the maximal (not maximum) matching {1-2, 3-4}.
    graph = path_graph(6)
    left = [0, 2, 4]
    matching = {2: 1, 4: 3}
    path = impl.find_augmenting_path(graph, left, matching)
    assert path == [0, 1, 2, 3, 4, 5]


def test_find_path_maximal_but_not_maximum(villa: Graph) -> None:
    # Inclusion-maximal: no edge can be added, but it is not maximum.
    matching = {"Pippi": "Pferd", "Tommy": "Pfannkuchen", "Annika": "Garten"}
    for _ in range(2):  # calling twice gives a valid answer twice
        check_augmenting_path(villa, PEOPLE, matching, impl.find_augmenting_path(villa, PEOPLE, matching))


@pytest.mark.parametrize("seed", range(8))
def test_find_path_berge_random(seed: int) -> None:
    # Repeatedly augment from the empty matching. By Berge's theorem a path
    # exists exactly as long as the matching is smaller than the maximum.
    graph = random_bipartite_graph(4, 4, 0.45, seed=seed)
    left = left_of(graph)
    optimum = brute_force_matching_size(graph)
    matching: dict = {}  # type: ignore[type-arg]
    for _ in range(optimum):
        before = dict(matching)
        path = impl.find_augmenting_path(graph, left, matching)
        assert matching == before  # not modified
        check_augmenting_path(graph, left, matching, path)
        matching = symmetric_difference(matching, path)
        assert_valid_matching(graph, matching, left=left)
    assert len(matching) == optimum
    assert impl.find_augmenting_path(graph, left, matching) is None


# ----------------------------------------------------------------------
# maximum_bipartite_matching
# ----------------------------------------------------------------------
def test_maximum_matching_villa(villa: Graph) -> None:
    matching = impl.maximum_bipartite_matching(villa, PEOPLE)
    assert_valid_matching(villa, matching, left=PEOPLE)
    # The perfect matching of the villa is unique.
    assert matching == {"Pippi": "Pfannkuchen", "Tommy": "Garten", "Annika": "Einkauf", "Kling": "Pferd"}


def test_maximum_matching_horses(horses: Graph) -> None:
    matching = impl.maximum_bipartite_matching(horses, ["Pippi", "Tommy", "Annika"])
    assert_valid_matching(horses, matching, left=["Pippi", "Tommy", "Annika"])
    assert len(matching) == 2


@pytest.mark.parametrize(("m", "n", "expected"), [(3, 3, 3), (2, 5, 2), (5, 2, 2), (1, 1, 1), (0, 3, 0), (4, 0, 0)])
def test_maximum_matching_complete_bipartite(m: int, n: int, expected: int) -> None:
    graph = complete_bipartite_graph(m, n)
    left = [f"L{i}" for i in range(m)]
    matching = impl.maximum_bipartite_matching(graph, left)
    assert_valid_matching(graph, matching, left=left)
    assert len(matching) == expected


def test_maximum_matching_empty_graph() -> None:
    assert impl.maximum_bipartite_matching(Graph(), []) == {}


def test_maximum_matching_no_edges() -> None:
    graph = Graph()
    graph.add_vertices(["a", "b", "x", "y"])
    assert impl.maximum_bipartite_matching(graph, ["a", "b"]) == {}


def test_maximum_matching_empty_left_side() -> None:
    graph = Graph()
    graph.add_vertices(["x", "y"])
    assert impl.maximum_bipartite_matching(graph, []) == {}


def test_maximum_matching_accepts_any_iterable(villa: Graph) -> None:
    matching = impl.maximum_bipartite_matching(villa, (p for p in PEOPLE))  # a generator
    assert_valid_matching(villa, matching, left=PEOPLE)
    assert len(matching) == 4


@pytest.mark.parametrize(
    ("graph", "left", "expected"),
    [
        (path_graph(6), [0, 2, 4], 3),
        (path_graph(5), [0, 2, 4], 2),
        (path_graph(5), [1, 3], 2),
        (cycle_graph(8), [0, 2, 4, 6], 4),
        (star_graph(5), [0], 1),
        (star_graph(5), [1, 2, 3, 4, 5], 1),
        (grid_graph(3, 3), [(r, c) for r in range(3) for c in range(3) if (r + c) % 2 == 0], 4),
        (grid_graph(4, 4), [(r, c) for r in range(4) for c in range(4) if (r + c) % 2 == 0], 8),
    ],
)
def test_maximum_matching_known_sizes(graph: Graph, left: list, expected: int) -> None:  # type: ignore[type-arg]
    matching = impl.maximum_bipartite_matching(graph, left)
    assert_valid_matching(graph, matching, left=left)
    assert len(matching) == expected


def test_maximum_matching_ladder() -> None:
    # A "ladder": a_i - x_i and a_i - x_{i-1}. The only perfect matching is
    # a_0 - x_0, ..., a_4 - x_4 (a_0 must take x_0, then a_1 must take x_1, ...).
    graph = Graph()
    for i in range(5):
        if i > 0:
            graph.add_edge(f"a{i}", f"x{i - 1}")
        graph.add_edge(f"a{i}", f"x{i}")
    left = [f"a{i}" for i in range(5)]
    matching = impl.maximum_bipartite_matching(graph, left)
    assert matching == {f"a{i}": f"x{i}" for i in range(5)}


@pytest.mark.parametrize("seed", range(10))
def test_maximum_matching_random_brute_force(seed: int) -> None:
    graph = random_bipartite_graph(3 + seed % 3, 4, 0.4, seed=seed)
    left = left_of(graph)
    matching = impl.maximum_bipartite_matching(graph, left)
    assert_valid_matching(graph, matching, left=left)
    assert len(matching) == brute_force_matching_size(graph)


@pytest.mark.parametrize("seed", range(3))
def test_maximum_matching_larger_random(seed: int) -> None:
    graph = random_bipartite_graph(40, 30, 0.1, seed=seed)
    left = left_of(graph)
    matching = impl.maximum_bipartite_matching(graph, left)
    assert_valid_matching(graph, matching, left=left)
    # Berge: a maximum matching has no augmenting path. We check this with
    # a simple search over alternating paths written here in the test.
    matched_right = {r: l for l, r in matching.items()}
    reached = {l for l in left if l not in matching}
    changed = True
    while changed:
        changed = False
        for l in list(reached):
            for r in graph.neighbors(l):
                assert r in matched_right, "There is still an augmenting path"
                if matched_right[r] not in reached:
                    reached.add(matched_right[r])
                    changed = True


def test_maximum_matching_does_not_modify_graph(villa: Graph) -> None:
    before = villa.copy()
    impl.maximum_bipartite_matching(villa, PEOPLE)
    assert villa == before


def test_maximum_matching_rejects_directed() -> None:
    graph = Graph.from_edges([("a", "x")], directed=True)
    with pytest.raises(ValueError):
        impl.maximum_bipartite_matching(graph, ["a"])


def test_maximum_matching_unknown_left_vertex(villa: Graph) -> None:
    with pytest.raises(KeyError):
        impl.maximum_bipartite_matching(villa, ["Pippi", "Michel"])


def test_maximum_matching_edge_inside_one_side() -> None:
    # The triangle 0 - 1 - 2 is not bipartite: 1 - 2 are both on the right.
    with pytest.raises(ValueError):
        impl.maximum_bipartite_matching(cycle_graph(3), [0])
    # An edge between two left vertices.
    graph = Graph.from_edges([("a", "b"), ("a", "x")])
    with pytest.raises(ValueError):
        impl.maximum_bipartite_matching(graph, ["a", "b"])


# ----------------------------------------------------------------------
# Optional tasks
# ----------------------------------------------------------------------
def check_vertex_cover(graph: Graph, cover) -> None:  # type: ignore[no-untyped-def]
    for v in cover:
        assert v in graph, f"{v!r} is not a vertex of the graph"
    for u, v, _ in graph.edges():
        assert u in cover or v in cover, f"The edge {u!r} - {v!r} is not covered"


@skip_if_not_implemented
def test_minimum_vertex_cover_villa(villa: Graph, horses: Graph) -> None:
    cover = impl.minimum_vertex_cover(villa, PEOPLE)
    check_vertex_cover(villa, cover)
    assert len(cover) == 4
    cover = impl.minimum_vertex_cover(horses, ["Pippi", "Tommy", "Annika"])
    check_vertex_cover(horses, cover)
    assert len(cover) == 2  # e.g. {"Pippi", "Pferd"} or {"Garten", "Pferd"}


@skip_if_not_implemented
def test_minimum_vertex_cover_small_cases() -> None:
    assert impl.minimum_vertex_cover(Graph(), []) == set()
    star = star_graph(4)
    assert impl.minimum_vertex_cover(star, [1, 2, 3, 4]) == {0}
    graph = complete_bipartite_graph(2, 5)
    cover = impl.minimum_vertex_cover(graph, ["L0", "L1"])
    assert cover == {"L0", "L1"}


@skip_if_not_implemented
@pytest.mark.parametrize("seed", range(8))
def test_minimum_vertex_cover_koenig(seed: int) -> None:
    graph = random_bipartite_graph(4, 4, 0.4, seed=seed)
    cover = impl.minimum_vertex_cover(graph, left_of(graph))
    check_vertex_cover(graph, cover)
    # König: minimum cover size = maximum matching size.
    assert len(cover) == brute_force_matching_size(graph)


@skip_if_not_implemented
def test_minimum_vertex_cover_invalid_input() -> None:
    with pytest.raises(ValueError):
        impl.minimum_vertex_cover(cycle_graph(3), [0])
    with pytest.raises(KeyError):
        impl.minimum_vertex_cover(path_graph(2), [7])


def check_hall_violator(graph: Graph, left, s) -> None:  # type: ignore[no-untyped-def]
    assert s is not None, "Expected a set S with |N(S)| < |S|, got None"
    assert len(s) > 0
    assert set(s) <= set(left), "S must contain only left vertices"
    neighbours = {w for v in s for w in graph.neighbors(v)}
    assert len(neighbours) < len(s), f"|N(S)| = {len(neighbours)} is not smaller than |S| = {len(s)}"


@skip_if_not_implemented
def test_hall_violator_horses(horses: Graph) -> None:
    left = ["Pippi", "Tommy", "Annika"]
    check_hall_violator(horses, left, impl.hall_violator(horses, left))


@skip_if_not_implemented
def test_hall_violator_none_if_left_side_can_be_matched(villa: Graph) -> None:
    assert impl.hall_violator(villa, PEOPLE) is None
    assert impl.hall_violator(complete_bipartite_graph(2, 5), ["L0", "L1"]) is None
    assert impl.hall_violator(Graph(), []) is None


@skip_if_not_implemented
def test_hall_violator_cases() -> None:
    graph = complete_bipartite_graph(5, 2)
    left = [f"L{i}" for i in range(5)]
    check_hall_violator(graph, left, impl.hall_violator(graph, left))
    isolated = Graph()
    isolated.add_vertices(["a", "x"])
    assert impl.hall_violator(isolated, ["a"]) == {"a"}  # N({a}) is empty


@skip_if_not_implemented
@pytest.mark.parametrize("seed", range(8))
def test_hall_violator_random(seed: int) -> None:
    graph = random_bipartite_graph(4, 4, 0.35, seed=seed)
    left = left_of(graph)
    s = impl.hall_violator(graph, left)
    if brute_force_matching_size(graph) == len(left):
        assert s is None
    else:
        check_hall_violator(graph, left, s)
