"""Tests for unit 5 (Euler and Hamilton problems).

By default these tests check ``task.py``. Use ``pytest --impl=demo`` to check
``demo_solution.py`` instead.
"""

import itertools

import pytest

from lib.generators import (
    complete_bipartite_graph,
    complete_graph,
    cycle_graph,
    grid_graph,
    path_graph,
    petersen_graph,
    random_connected_graph,
    random_graph,
    small_weighted_graph,
    star_graph,
)
from lib.graph import Graph
from lib.testing import (
    assert_valid_euler_circuit,
    assert_valid_euler_trail,
    assert_valid_hamiltonian_cycle,
    count_components,
    load_implementation,
    skip_if_not_implemented,
)

impl = load_implementation(__file__)


# ----------------------------------------------------------------------
# Example graphs
# ----------------------------------------------------------------------
def nikolaus() -> Graph:
    """The House of St. Nicholas has odd vertices 1 and 2 (the bottom corners)."""
    return Graph.from_edges([(1, 2), (1, 3), (1, 4), (2, 3), (2, 4), (3, 4), (3, 5), (4, 5)])


def koenigsberg() -> Graph:
    """The seven bridges, every bridge subdivided by a vertex of degree 2."""
    bridges = [
        ("b1", "Insel", "Nord"),
        ("b2", "Insel", "Nord"),
        ("b3", "Insel", "Süd"),
        ("b4", "Insel", "Süd"),
        ("b5", "Insel", "Ost"),
        ("b6", "Nord", "Ost"),
        ("b7", "Süd", "Ost"),
    ]
    graph = Graph()
    for bridge, bank1, bank2 in bridges:
        graph.add_edge(bank1, bridge)
        graph.add_edge(bridge, bank2)
    return graph


def two_triangles() -> Graph:
    """All degrees even, but the edges lie in two components."""
    return Graph.from_edges([(1, 2), (2, 3), (3, 1), (4, 5), (5, 6), (6, 4)])


def triangle_and_edge() -> Graph:
    """Exactly two odd vertices (4 and 5), but the edges are not connected."""
    return Graph.from_edges([(1, 2), (2, 3), (3, 1), (4, 5)])


def triangle_with_isolated_vertices() -> Graph:
    return Graph.from_edges([("a", "b"), ("b", "c"), ("c", "a")], vertices=["x", "y"])


def figure_eight() -> Graph:
    """Two triangles sharing vertex 0: Eulerian, but 0 is a cut vertex."""
    return Graph.from_edges([(0, 1), (1, 2), (2, 0), (0, 3), (3, 4), (4, 0)])


def only_vertices(*names: object) -> Graph:
    graph = Graph()
    graph.add_vertices(names)
    return graph


def prism() -> Graph:
    """Pentagonal prism: 3-regular with 10 vertices like Petersen, but Hamiltonian."""
    graph = Graph()
    for i in range(5):
        graph.add_edge(i, (i + 1) % 5)
        graph.add_edge(5 + i, 5 + (i + 1) % 5)
        graph.add_edge(i, i + 5)
    return graph


def make_eulerian(graph: Graph) -> Graph:
    """Join a new vertex 'x' to all odd vertices of the graph.

    The number of odd vertices is even (handshake lemma), so afterwards
    every degree is even. If the graph was connected, the result is Eulerian.
    """
    result = graph.copy()
    for v in graph.vertices():
        if graph.degree(v) % 2 == 1:
            result.add_edge("x", v)
    return result


# ----------------------------------------------------------------------
# Brute-force references (exponential, only for tiny graphs)
# ----------------------------------------------------------------------
def euler_walk_exists(graph: Graph, closed: bool) -> bool:
    """Try every walk that never reuses an edge (straight from the definition)."""
    all_edges = frozenset(frozenset((u, v)) for u, v, _ in graph.edges())
    if not all_edges:
        return True

    def extend(v, start, unused) -> bool:  # type: ignore[no-untyped-def]
        if not unused:
            return v == start or not closed
        for w in graph.neighbors(v):
            edge = frozenset((v, w))
            if edge in unused and extend(w, start, unused - {edge}):
                return True
        return False

    return any(extend(s, s, all_edges) for s in graph.vertices() if graph.degree(s) > 0)


def hamiltonian_cycle_exists(graph: Graph) -> bool:
    """Try all orders of the vertices (straight from the definition)."""
    vertices = graph.vertices()
    if len(vertices) < 3:
        return False
    first, rest = vertices[0], vertices[1:]
    for order in itertools.permutations(rest):
        cycle = [first, *order, first]
        if all(graph.has_edge(u, v) for u, v in zip(cycle, cycle[1:])):
            return True
    return False


# ----------------------------------------------------------------------
# edges_connected
# ----------------------------------------------------------------------
@pytest.mark.parametrize(
    ("graph", "expected"),
    [
        (Graph(), True),
        (only_vertices("Michel"), True),
        (only_vertices(1, 2, 3), True),
        (triangle_with_isolated_vertices(), True),
        (path_graph(5), True),
        (koenigsberg(), True),
        (figure_eight(), True),
        (two_triangles(), False),
        (triangle_and_edge(), False),
        (Graph.from_edges([(1, 2), (3, 4)]), False),
    ],
)
def test_edges_connected(graph: Graph, expected: bool) -> None:
    assert impl.edges_connected(graph) is expected


@pytest.mark.parametrize("seed", range(10))
def test_edges_connected_random(seed: int) -> None:
    graph = random_graph(12, 0.12, seed=seed)
    graph.add_vertex("isolated")
    # The graph formed by the edges alone contains no isolated vertices.
    only_edges = Graph.from_edges([(u, v) for u, v, _ in graph.edges()])
    assert impl.edges_connected(graph) is (count_components(only_edges) <= 1)


def test_edges_connected_rejects_directed() -> None:
    with pytest.raises(ValueError):
        impl.edges_connected(Graph.from_edges([(1, 2)], directed=True))


# ----------------------------------------------------------------------
# has_euler_circuit / has_euler_trail
# ----------------------------------------------------------------------
@pytest.mark.parametrize("n", range(1, 8))
def test_complete_graphs(n: int) -> None:
    # K_n is (n-1)-regular: an Euler circuit exists exactly for odd n.
    assert impl.has_euler_circuit(complete_graph(n)) is (n % 2 == 1)


@pytest.mark.parametrize(
    ("graph", "circuit", "trail"),
    [
        (Graph(), True, True),
        (only_vertices("Pippi", "Annika"), True, True),
        (triangle_with_isolated_vertices(), True, True),
        (cycle_graph(3), True, True),
        (cycle_graph(8), True, True),
        (figure_eight(), True, True),
        (complete_bipartite_graph(2, 4), True, True),
        (path_graph(2), False, True),
        (path_graph(6), False, True),
        (star_graph(2), False, True),
        (nikolaus(), False, True),
        (small_weighted_graph(), False, True),
        (grid_graph(2, 3), False, True),
        (koenigsberg(), False, False),
        (complete_graph(4), False, False),
        (star_graph(3), False, False),
        (petersen_graph(), False, False),
        (complete_bipartite_graph(3, 3), False, False),
        (grid_graph(3, 3), False, False),
        (two_triangles(), False, False),
        (triangle_and_edge(), False, False),
    ],
)
def test_euler_examples(graph: Graph, circuit: bool, trail: bool) -> None:
    assert impl.has_euler_circuit(graph) is circuit
    assert impl.has_euler_trail(graph) is trail


@pytest.mark.parametrize("seed", range(25))
def test_euler_criteria_match_definition(seed: int) -> None:
    graph = random_graph(6, 0.45, seed=seed)
    assert impl.has_euler_circuit(graph) is euler_walk_exists(graph, closed=True)
    assert impl.has_euler_trail(graph) is euler_walk_exists(graph, closed=False)


@pytest.mark.parametrize("seed", range(10))
def test_euler_criteria_match_definition_even_degrees(seed: int) -> None:
    graph = make_eulerian(random_graph(6, 0.3, seed=seed))
    assert impl.has_euler_circuit(graph) is euler_walk_exists(graph, closed=True)
    assert impl.has_euler_trail(graph) is euler_walk_exists(graph, closed=False)


@pytest.mark.parametrize("seed", range(5))
def test_euler_on_constructed_eulerian_graphs(seed: int) -> None:
    graph = make_eulerian(random_connected_graph(15, 10, seed=seed))
    assert impl.has_euler_circuit(graph) is True
    assert impl.has_euler_trail(graph) is True


def test_euler_checks_reject_directed() -> None:
    directed = Graph.from_edges([(1, 2), (2, 3), (3, 1)], directed=True)
    with pytest.raises(ValueError):
        impl.has_euler_circuit(directed)
    with pytest.raises(ValueError):
        impl.has_euler_trail(directed)


# ----------------------------------------------------------------------
# Optional: find_euler_circuit
# ----------------------------------------------------------------------
@skip_if_not_implemented
@pytest.mark.parametrize(
    "graph",
    [
        cycle_graph(3),
        cycle_graph(7),
        complete_graph(5),
        complete_graph(7),
        figure_eight(),
        complete_bipartite_graph(2, 4),
        complete_bipartite_graph(4, 4),
        triangle_with_isolated_vertices(),
    ],
)
def test_find_euler_circuit(graph: Graph) -> None:
    before = graph.copy()
    walk = impl.find_euler_circuit(graph)
    assert_valid_euler_circuit(graph, walk)
    assert graph == before  # the input is not modified


@skip_if_not_implemented
@pytest.mark.parametrize("seed", range(5))
def test_find_euler_circuit_random(seed: int) -> None:
    graph = make_eulerian(random_connected_graph(20, 25, seed=seed))
    assert_valid_euler_circuit(graph, impl.find_euler_circuit(graph))


@skip_if_not_implemented
def test_find_euler_circuit_without_edges() -> None:
    assert impl.find_euler_circuit(Graph()) == []
    assert impl.find_euler_circuit(only_vertices("Ida", "Alfred")) == []


@skip_if_not_implemented
@pytest.mark.parametrize("graph", [nikolaus(), koenigsberg(), two_triangles(), path_graph(4), petersen_graph()])
def test_find_euler_circuit_none(graph: Graph) -> None:
    assert impl.find_euler_circuit(graph) is None


@skip_if_not_implemented
def test_find_euler_circuit_rejects_directed() -> None:
    with pytest.raises(ValueError):
        impl.find_euler_circuit(Graph.from_edges([(1, 2), (2, 3), (3, 1)], directed=True))


# ----------------------------------------------------------------------
# Optional: find_euler_trail
# ----------------------------------------------------------------------
@skip_if_not_implemented
@pytest.mark.parametrize(
    ("graph", "ends"),
    [
        (nikolaus(), {1, 2}),
        (small_weighted_graph(), {"Katthult", "Lönneberga"}),
        (path_graph(6), {0, 5}),
        (path_graph(2), {0, 1}),
        (grid_graph(2, 3), {(0, 1), (1, 1)}),
    ],
)
def test_find_euler_trail_open(graph: Graph, ends: set) -> None:
    before = graph.copy()
    walk = impl.find_euler_trail(graph)
    assert_valid_euler_trail(graph, walk)
    assert {walk[0], walk[-1]} == ends  # it runs from one odd vertex to the other
    assert graph == before  # the input is not modified


@skip_if_not_implemented
@pytest.mark.parametrize("seed", range(5))
def test_find_euler_trail_random(seed: int) -> None:
    # Removing one edge u - v from an Eulerian graph leaves exactly two odd
    # vertices u and v (and keeps the graph connected).
    graph = make_eulerian(random_connected_graph(15, 12, seed=seed))
    u, v, _ = graph.edges()[0]
    graph.remove_edge(u, v)
    walk = impl.find_euler_trail(graph)
    assert_valid_euler_trail(graph, walk)
    assert {walk[0], walk[-1]} == {u, v}


@skip_if_not_implemented
def test_find_euler_trail_closed() -> None:
    graph = complete_graph(5)
    assert_valid_euler_trail(graph, impl.find_euler_trail(graph))


@skip_if_not_implemented
def test_find_euler_trail_without_edges() -> None:
    assert impl.find_euler_trail(Graph()) == []
    assert impl.find_euler_trail(only_vertices(1)) == []


@skip_if_not_implemented
@pytest.mark.parametrize("graph", [koenigsberg(), complete_graph(4), triangle_and_edge(), star_graph(3)])
def test_find_euler_trail_none(graph: Graph) -> None:
    assert impl.find_euler_trail(graph) is None


@skip_if_not_implemented
def test_find_euler_trail_rejects_directed() -> None:
    with pytest.raises(ValueError):
        impl.find_euler_trail(Graph.from_edges([(1, 2)], directed=True))


# ----------------------------------------------------------------------
# Optional: find_hamiltonian_cycle
# ----------------------------------------------------------------------
@skip_if_not_implemented
@pytest.mark.parametrize(
    "graph",
    [
        complete_graph(3),
        complete_graph(5),
        cycle_graph(6),
        complete_bipartite_graph(2, 2),
        complete_bipartite_graph(3, 3),
        grid_graph(2, 3),
        grid_graph(4, 4),
        prism(),
        nikolaus(),
        small_weighted_graph(),
    ],
)
def test_find_hamiltonian_cycle(graph: Graph) -> None:
    before = graph.copy()
    cycle = impl.find_hamiltonian_cycle(graph)
    assert_valid_hamiltonian_cycle(graph, cycle)
    assert graph == before  # the input is not modified


@skip_if_not_implemented
@pytest.mark.parametrize(
    "graph",
    [
        petersen_graph(),  # 3-regular, but no Hamiltonian cycle
        complete_bipartite_graph(2, 3),  # bipartite with unequal sides
        grid_graph(3, 3),  # bipartite with 5 + 4 vertices
        figure_eight(),  # vertex 0 is a cut vertex
        path_graph(5),
        star_graph(4),
        two_triangles(),
        complete_graph(2),
        only_vertices("Lina"),
        Graph(),
    ],
)
def test_find_hamiltonian_cycle_none(graph: Graph) -> None:
    assert impl.find_hamiltonian_cycle(graph) is None


@skip_if_not_implemented
@pytest.mark.parametrize("seed", range(10))
def test_find_hamiltonian_cycle_matches_brute_force(seed: int) -> None:
    graph = random_graph(7, 0.5, seed=seed)
    cycle = impl.find_hamiltonian_cycle(graph)
    if hamiltonian_cycle_exists(graph):
        assert_valid_hamiltonian_cycle(graph, cycle)
    else:
        assert cycle is None


@skip_if_not_implemented
def test_find_hamiltonian_cycle_rejects_directed() -> None:
    with pytest.raises(ValueError):
        impl.find_hamiltonian_cycle(Graph.from_edges([(1, 2), (2, 3), (3, 1)], directed=True))
