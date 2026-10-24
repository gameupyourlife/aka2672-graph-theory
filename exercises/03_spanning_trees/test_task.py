"""Tests for unit 3 (spanning trees, Union-Find, Kruskal).

By default these tests check ``task.py``. Use ``pytest --impl=demo`` to check
``demo_solution.py`` instead.
"""

import itertools
import random

import pytest

from lib.generators import (
    complete_graph,
    cycle_graph,
    grid_graph,
    path_graph,
    random_connected_graph,
    random_weighted_graph,
    small_weighted_graph,
)
from lib.graph import Edge, Graph
from lib.testing import (
    assert_valid_spanning_forest,
    assert_valid_spanning_tree,
    count_components,
    load_implementation,
    skip_if_not_implemented,
)

impl = load_implementation(__file__)

# The unique minimum spanning tree of small_weighted_graph() (weight 14),
# computed by hand: 2 + 2 + 3 + 3 + 4.
LONNEBERGA_MST = {
    frozenset(("Katthult", "Gibberyd")),
    frozenset(("Kirche", "Markt")),
    frozenset(("Lönneberga", "Backhorva")),
    frozenset(("Gibberyd", "Kirche")),
    frozenset(("Katthult", "Lönneberga")),
}


@pytest.fixture
def two_triangles() -> Graph:
    """Two weighted triangles and the isolated vertex Q (3 components).

    Minimum spanning forest: A-B (1), B-C (2), Y-Z (4), X-Y (5) -> weight 12.
    """
    return Graph.from_edges(
        [("A", "B", 1), ("B", "C", 2), ("A", "C", 3), ("X", "Y", 5), ("Y", "Z", 4), ("X", "Z", 6)],
        vertices=["Q"],
    )


def edge_set(edges) -> set[frozenset]:  # type: ignore[no-untyped-def]
    return {frozenset((e[0], e[1])) for e in edges}


def assert_edges_from_graph(graph: Graph, edges) -> None:  # type: ignore[no-untyped-def]
    """Every result entry is an ``Edge`` of the graph with the correct weight."""
    for edge in edges:
        assert isinstance(edge, Edge), f"Expected Edge objects, got {edge!r}"
        assert graph.has_edge(edge.u, edge.v), f"{edge!r} is not an edge of the graph"
        assert edge.weight == graph.weight(edge.u, edge.v), f"Wrong weight in {edge!r}"


def assert_minimum_forest(graph: Graph, edges) -> None:  # type: ignore[no-untyped-def]
    """Check that ``edges`` is a *minimum* spanning forest of ``graph``.

    Optimality criterion (cycle property): a spanning forest F is minimal
    iff every edge {u, v} outside F is at least as heavy as every edge on
    the path from u to v in F.
    """
    edges = list(edges)
    assert_edges_from_graph(graph, edges)
    assert_valid_spanning_forest(graph, edges)
    adjacency: dict = {v: [] for v in graph.vertices()}
    for u, v, w in edges:
        adjacency[u].append((v, w))
        adjacency[v].append((u, w))
    chosen = edge_set(edges)
    for u, v, w in graph.edges():
        if frozenset((u, v)) in chosen:
            continue
        # Simple stack search in the forest, remembering the heaviest edge.
        heaviest = {u: float("-inf")}
        stack = [u]
        while stack:
            x = stack.pop()
            for y, wy in adjacency[x]:
                if y not in heaviest:
                    heaviest[y] = max(heaviest[x], wy)
                    stack.append(y)
        assert v in heaviest, f"{u!r} and {v!r} are not connected by the forest"
        assert heaviest[v] <= w, (
            f"Not minimal: edge {u!r} - {v!r} (weight {w}) could replace an edge "
            f"of weight {heaviest[v]} on the forest path"
        )


def brute_force_forest_weight(graph: Graph) -> float:
    """Minimum weight over *all* edge subsets of size n - c that form a spanning forest."""
    n = graph.num_vertices()
    c = count_components(graph)
    best = float("inf")
    for subset in itertools.combinations(graph.edges(), n - c):
        candidate = Graph.from_edges(subset, vertices=graph.vertices())
        if count_components(candidate) == c:  # n - c edges and c components: a forest
            best = min(best, sum(e.weight for e in subset))
    return best


# ----------------------------------------------------------------------
# Union-Find
# ----------------------------------------------------------------------
def test_union_find_singletons() -> None:
    uf = impl.UnionFind(["Michel", "Ida", "Alfred"])
    for x in ["Michel", "Ida", "Alfred"]:
        assert uf.find(x) == x  # a singleton set is represented by its element
    assert uf.connected("Michel", "Michel") is True
    assert uf.connected("Michel", "Ida") is False


def test_union_find_union_return_values() -> None:
    uf = impl.UnionFind(["Michel", "Ida", "Alfred", "Lina"])
    assert uf.union("Michel", "Ida") is True
    assert uf.union("Ida", "Michel") is False
    assert uf.union("Michel", "Michel") is False
    assert uf.union("Alfred", "Lina") is True
    assert uf.union("Ida", "Lina") is True
    assert uf.union("Michel", "Alfred") is False  # already joined via Ida - Lina


def test_union_find_connected_is_transitive() -> None:
    uf = impl.UnionFind(range(6))
    uf.union(0, 1)
    uf.union(2, 3)
    uf.union(1, 2)
    assert uf.connected(0, 3) and uf.connected(3, 0)
    assert not uf.connected(0, 4)
    assert not uf.connected(4, 5)
    assert uf.find(0) == uf.find(1) == uf.find(2) == uf.find(3)
    assert uf.find(0) in {0, 1, 2, 3}  # the representative is a member of the set
    assert uf.find(4) == 4 and uf.find(5) == 5


def test_union_find_empty_and_add() -> None:
    uf = impl.UnionFind()
    with pytest.raises(KeyError):
        uf.find("Katthult")
    uf.add("Katthult")
    uf.add("Lönneberga")
    assert uf.find("Katthult") == "Katthult"
    assert uf.union("Katthult", "Lönneberga") is True


def test_union_find_add_existing_is_noop() -> None:
    uf = impl.UnionFind(["a", "b"])
    uf.union("a", "b")
    uf.add("a")
    uf.add("b")
    assert uf.connected("a", "b")


def test_union_find_unknown_elements() -> None:
    uf = impl.UnionFind(["a", "b"])
    with pytest.raises(KeyError):
        uf.find("z")
    with pytest.raises(KeyError):
        uf.union("a", "z")
    with pytest.raises(KeyError):
        uf.union("z", "a")
    with pytest.raises(KeyError):
        uf.connected("z", "b")


def test_union_find_tuple_elements() -> None:
    uf = impl.UnionFind([(0, 0), (0, 1), (1, 1)])
    uf.union((0, 0), (1, 1))
    assert uf.connected((1, 1), (0, 0))
    assert not uf.connected((0, 1), (0, 0))


@pytest.mark.parametrize("seed", range(5))
def test_union_find_against_explicit_sets(seed: int) -> None:
    """Compare with a naive partition stored as a list of Python sets."""
    rng = random.Random(seed)
    n = 300
    uf = impl.UnionFind(range(n))
    sets = [{i} for i in range(n)]
    where = list(range(n))  # where[x] = index of the set containing x
    for _ in range(400):
        x, y = rng.randrange(n), rng.randrange(n)
        different = where[x] != where[y]
        assert uf.union(x, y) is different
        if different:
            old = where[y]
            for z in sets[old]:
                where[z] = where[x]
            sets[where[x]] |= sets[old]
            sets[old] = set()
    for _ in range(400):
        x, y = rng.randrange(n), rng.randrange(n)
        assert uf.connected(x, y) is (where[x] == where[y])


# ----------------------------------------------------------------------
# Kruskal
# ----------------------------------------------------------------------
def test_kruskal_lonneberga() -> None:
    graph = small_weighted_graph()
    tree = impl.kruskal(graph)
    assert_valid_spanning_tree(graph, tree)
    assert_edges_from_graph(graph, tree)
    assert impl.spanning_tree_weight(tree) == 14
    assert edge_set(tree) == LONNEBERGA_MST  # the MST of this graph is unique


def test_kruskal_disconnected(two_triangles: Graph) -> None:
    forest = impl.kruskal(two_triangles)
    assert len(forest) == 7 - 3  # n - c edges
    assert_minimum_forest(two_triangles, forest)
    assert edge_set(forest) == {
        frozenset("AB"),
        frozenset("BC"),
        frozenset("YZ"),
        frozenset("XY"),
    }
    assert impl.spanning_tree_weight(forest) == 12


def test_kruskal_empty_and_edgeless() -> None:
    assert impl.kruskal(Graph()) == []
    assert impl.kruskal(path_graph(1)) == []
    graph = Graph()
    graph.add_vertices(["Pippi", "Tommy", "Annika"])
    assert impl.kruskal(graph) == []


def test_kruskal_single_edge() -> None:
    graph = Graph.from_edges([("Katthult", "Lönneberga", 4)])
    tree = impl.kruskal(graph)
    assert edge_set(tree) == {frozenset(("Katthult", "Lönneberga"))}
    assert impl.spanning_tree_weight(tree) == 4


def test_kruskal_tree_is_its_own_mst() -> None:
    graph = Graph.from_edges([(0, 1, 5), (1, 2, 1), (1, 3, 7), (3, 4, 2)])
    assert edge_set(impl.kruskal(graph)) == edge_set(graph.edges())


def test_kruskal_cycle_drops_heaviest_edge() -> None:
    graph = cycle_graph(6)
    graph.set_weight(2, 3, 10)
    tree = impl.kruskal(graph)
    assert_valid_spanning_tree(graph, tree)
    assert frozenset((2, 3)) not in edge_set(tree)
    assert impl.spanning_tree_weight(tree) == 5


def test_kruskal_all_weights_equal() -> None:
    # Every spanning tree of K_6 is minimal; any one is accepted.
    graph = complete_graph(6)
    tree = impl.kruskal(graph)
    assert_valid_spanning_tree(graph, tree)
    assert impl.spanning_tree_weight(tree) == 5


def test_kruskal_grid() -> None:
    graph = grid_graph(5, 5)
    tree = impl.kruskal(graph)
    assert_valid_spanning_tree(graph, tree)
    assert impl.spanning_tree_weight(tree) == 24


def test_kruskal_float_weights() -> None:
    graph = Graph.from_edges(
        [("a", "b", 0.5), ("b", "c", 1.25), ("a", "c", 1.5), ("c", "d", 0.25), ("b", "d", 2.75)]
    )
    tree = impl.kruskal(graph)
    assert_minimum_forest(graph, tree)
    assert impl.spanning_tree_weight(tree) == pytest.approx(2.0)


def test_kruskal_negative_weights() -> None:
    # Unlike shortest paths, minimum spanning trees allow negative weights.
    graph = Graph.from_edges([("a", "b", -3), ("b", "c", 2), ("c", "d", -1), ("d", "a", 4), ("a", "c", 0)])
    tree = impl.kruskal(graph)
    assert_minimum_forest(graph, tree)
    assert impl.spanning_tree_weight(tree) == -4  # a-b, c-d, a-c


def test_kruskal_rejects_directed() -> None:
    graph = Graph.from_edges([("a", "b", 1), ("b", "c", 2)], directed=True)
    with pytest.raises(ValueError):
        impl.kruskal(graph)


def test_kruskal_does_not_modify_graph() -> None:
    graph = small_weighted_graph()
    before = graph.copy()
    impl.kruskal(graph)
    assert graph == before


@pytest.mark.parametrize("seed", range(10))
def test_kruskal_matches_brute_force(seed: int) -> None:
    # Small random graphs, some of them disconnected, with many equal weights.
    graph = random_weighted_graph(6, 0.3 + 0.05 * seed, min_weight=1, max_weight=4, seed=seed)
    forest = impl.kruskal(graph)
    assert_valid_spanning_forest(graph, forest)
    assert impl.spanning_tree_weight(forest) == brute_force_forest_weight(graph)


@pytest.mark.parametrize("seed", range(5))
def test_kruskal_random_connected(seed: int) -> None:
    graph = random_connected_graph(60, 120, seed=seed, min_weight=1, max_weight=20)
    tree = impl.kruskal(graph)
    assert_valid_spanning_tree(graph, tree)
    assert_minimum_forest(graph, tree)


@pytest.mark.parametrize("seed", range(5))
def test_kruskal_random_disconnected(seed: int) -> None:
    graph = random_weighted_graph(40, 0.04, min_weight=1, max_weight=9, seed=seed)
    assert_minimum_forest(graph, impl.kruskal(graph))


# ----------------------------------------------------------------------
# spanning_tree_weight
# ----------------------------------------------------------------------
def test_spanning_tree_weight() -> None:
    assert impl.spanning_tree_weight([]) == 0
    assert impl.spanning_tree_weight([Edge("a", "b", 3), Edge("b", "c", 4)]) == 7
    assert impl.spanning_tree_weight([Edge("a", "b", 0.1), Edge("b", "c", 0.2)]) == pytest.approx(0.3)
    assert impl.spanning_tree_weight([Edge("a", "b", -2), Edge("b", "c")]) == -1
    assert impl.spanning_tree_weight(small_weighted_graph().edges()) == 32


# ----------------------------------------------------------------------
# Optional: Prim
# ----------------------------------------------------------------------
@skip_if_not_implemented
@pytest.mark.parametrize("start", ["Katthult", "Markt", "Backhorva"])
def test_prim_lonneberga(start: str) -> None:
    graph = small_weighted_graph()
    tree = impl.prim(graph, start)
    assert_valid_spanning_tree(graph, tree)
    assert_edges_from_graph(graph, tree)
    assert edge_set(tree) == LONNEBERGA_MST


@skip_if_not_implemented
def test_prim_only_component_of_start(two_triangles: Graph) -> None:
    tree = impl.prim(two_triangles, "Z")
    assert edge_set(tree) == {frozenset("YZ"), frozenset("XY")}
    assert impl.prim(two_triangles, "Q") == []


@skip_if_not_implemented
@pytest.mark.parametrize("seed", range(5))
def test_prim_random_connected(seed: int) -> None:
    graph = random_connected_graph(50, 100, seed=seed, min_weight=-5, max_weight=15)
    tree = impl.prim(graph, 0)
    assert_valid_spanning_tree(graph, tree)
    assert_minimum_forest(graph, tree)


@skip_if_not_implemented
def test_prim_invalid_input() -> None:
    with pytest.raises(KeyError):
        impl.prim(small_weighted_graph(), "Stockholm")
    with pytest.raises(ValueError):
        impl.prim(Graph.from_edges([("a", "b", 1)], directed=True), "a")


# ----------------------------------------------------------------------
# Optional: counting components with Union-Find
# ----------------------------------------------------------------------
@skip_if_not_implemented
def test_count_components_examples(two_triangles: Graph) -> None:
    assert impl.count_components(Graph()) == 0
    assert impl.count_components(path_graph(1)) == 1
    assert impl.count_components(small_weighted_graph()) == 1
    assert impl.count_components(two_triangles) == 3
    edgeless = Graph()
    edgeless.add_vertices(range(5))
    assert impl.count_components(edgeless) == 5


@skip_if_not_implemented
@pytest.mark.parametrize("seed", range(5))
def test_count_components_random(seed: int) -> None:
    graph = random_weighted_graph(50, 0.03, seed=seed)
    assert impl.count_components(graph) == count_components(graph)


@skip_if_not_implemented
def test_count_components_rejects_directed() -> None:
    with pytest.raises(ValueError):
        impl.count_components(Graph.from_edges([("a", "b")], directed=True))
