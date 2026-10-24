"""Helpers for checking results of graph algorithms.

The ``assert_*`` functions check whether a result is *valid* (e.g. whether a
list of vertices really is a path in the graph). They raise an
``AssertionError`` with an explanation if not, and can therefore be used
directly in pytest tests::

    from lib.testing import assert_valid_path

    assert_valid_path(graph, ["A", "B", "C"], start="A", end="C")

Important: these functions only **check** results. They do not compute
them - that is your job in the exercises. Where a check needs connectivity
information, a deliberately simple (and slow) method is used that is not one
of the algorithms from the course.

In addition this module contains the test infrastructure that lets every
``test_task.py`` run against either ``task.py`` or ``demo_solution.py``
(see :func:`load_implementation`).
"""

from __future__ import annotations

import functools
import math
import os
from collections.abc import Callable, Hashable, Iterable, Mapping, Sequence
from pathlib import Path
from types import ModuleType
from typing import Any, TypeVar

from lib.graph import Graph, Vertex
from lib.utils import load_module_from_path

IMPLEMENTATION_ENV_VAR = "GRAPH_COURSE_IMPL"
"""Environment variable that selects the tested file: ``task`` or ``demo``."""

_IMPLEMENTATION_FILES = {"task": "task.py", "demo": "demo_solution.py"}

F = TypeVar("F", bound=Callable[..., Any])


# ----------------------------------------------------------------------
# Test infrastructure
# ----------------------------------------------------------------------
def selected_implementation() -> str:
    """Return ``"task"`` or ``"demo"``, depending on ``GRAPH_COURSE_IMPL``.

    The default is ``"task"``: the tests check *your* solution. Run
    ``pytest --impl=demo`` (or set ``GRAPH_COURSE_IMPL=demo``) to check the
    demo solutions instead.
    """
    choice = os.environ.get(IMPLEMENTATION_ENV_VAR, "task").strip().lower()
    if choice not in _IMPLEMENTATION_FILES:
        raise ValueError(
            f"{IMPLEMENTATION_ENV_VAR} must be 'task' or 'demo', got {choice!r}"
        )
    return choice


def load_implementation(test_file: str | Path) -> ModuleType:
    """Load ``task.py`` or ``demo_solution.py`` next to ``test_file``.

    Usage at the top of a ``test_task.py``::

        from lib.testing import load_implementation
        impl = load_implementation(__file__)

        def test_something():
            assert impl.my_function(...) == ...
    """
    folder = Path(test_file).resolve().parent
    return load_module_from_path(folder / _IMPLEMENTATION_FILES[selected_implementation()])


def skip_if_not_implemented(test: F) -> F:
    """Decorator for tests of **optional** tasks.

    If the tested function raises ``NotImplementedError`` (i.e. the optional
    task has not been solved yet), the test is *skipped* instead of failed.
    """

    @functools.wraps(test)
    def wrapper(*args: Any, **kwargs: Any) -> Any:
        import pytest  # imported here so that lib does not require pytest

        try:
            return test(*args, **kwargs)
        except NotImplementedError:
            pytest.skip("optional task not implemented yet")

    return wrapper  # type: ignore[return-value]


# ----------------------------------------------------------------------
# Paths, cycles and walks
# ----------------------------------------------------------------------
def assert_valid_path(
    graph: Graph,
    path: Sequence[Vertex],
    start: Vertex | None = None,
    end: Vertex | None = None,
) -> None:
    """Check that ``path`` is a path in ``graph``.

    A path is a non-empty sequence of vertices without repetitions in which
    consecutive vertices are joined by an edge (respecting the direction in
    directed graphs).

    Args:
        graph: The graph.
        path: List of vertices.
        start: If given, the path must begin at this vertex.
        end: If given, the path must end at this vertex.
    """
    assert path is not None, "Expected a path, got None"
    assert len(path) > 0, "The path is empty"
    for v in path:
        assert v in graph, f"{v!r} is not a vertex of the graph"
    assert len(set(path)) == len(path), f"The path repeats a vertex: {list(path)}"
    for u, v in zip(path, path[1:]):
        assert graph.has_edge(u, v), f"There is no edge {u!r} -> {v!r}"
    if start is not None:
        assert path[0] == start, f"The path starts at {path[0]!r}, not {start!r}"
    if end is not None:
        assert path[-1] == end, f"The path ends at {path[-1]!r}, not {end!r}"


def assert_valid_euler_circuit(graph: Graph, walk: Sequence[Vertex]) -> None:
    """Check that ``walk`` is an Euler circuit of the undirected ``graph``.

    The walk is a list of vertices ``[v0, v1, ..., v0]`` that uses every
    edge exactly once and ends where it starts. For a graph without edges
    the empty list or a list with one vertex is accepted.
    """
    _assert_euler_walk(graph, walk, closed=True)


def assert_valid_euler_trail(graph: Graph, walk: Sequence[Vertex]) -> None:
    """Check that ``walk`` is an Euler trail (open or closed) of ``graph``.

    The walk is a list of vertices that uses every edge exactly once.
    """
    _assert_euler_walk(graph, walk, closed=False)


def _assert_euler_walk(graph: Graph, walk: Sequence[Vertex], closed: bool) -> None:
    assert walk is not None, "Expected a walk, got None"
    if graph.num_edges() == 0:
        assert len(walk) <= 1, "A graph without edges only has trivial walks"
        if walk:
            assert walk[0] in graph, f"{walk[0]!r} is not a vertex of the graph"
        return
    assert len(walk) == graph.num_edges() + 1, (
        f"The walk has {len(walk) - 1} edges, the graph has {graph.num_edges()}"
    )
    used: set[frozenset[Hashable]] = set()
    for u, v in zip(walk, walk[1:]):
        assert graph.has_edge(u, v), f"There is no edge {u!r} - {v!r}"
        edge = frozenset((u, v))
        assert edge not in used, f"The edge {u!r} - {v!r} is used twice"
        used.add(edge)
    if closed:
        assert walk[0] == walk[-1], "An Euler circuit must end where it starts"


def assert_valid_hamiltonian_cycle(graph: Graph, cycle: Sequence[Vertex]) -> None:
    """Check that ``cycle`` is a Hamiltonian cycle of ``graph``.

    The cycle is given as ``[v0, v1, ..., v_{n-1}, v0]``: every vertex
    appears exactly once, except that the first vertex is repeated at the end.
    """
    assert cycle is not None, "Expected a cycle, got None"
    n = graph.num_vertices()
    assert n >= 3, "Hamiltonian cycles need at least 3 vertices"
    assert len(cycle) == n + 1, f"Expected {n + 1} entries, got {len(cycle)}"
    assert cycle[0] == cycle[-1], "The cycle must end where it starts"
    assert set(cycle[:-1]) == set(graph.vertices()), (
        "The cycle must visit every vertex exactly once"
    )
    assert len(set(cycle[:-1])) == n, "The cycle repeats a vertex"
    for u, v in zip(cycle, cycle[1:]):
        assert graph.has_edge(u, v), f"There is no edge {u!r} -> {v!r}"


# ----------------------------------------------------------------------
# Spanning trees
# ----------------------------------------------------------------------
def _component_labels(vertices: Iterable[Vertex], edges: Iterable[tuple[Vertex, Vertex]]) -> dict[Vertex, int]:
    """Label vertices by connected component.

    Deliberately naive fixpoint iteration (not BFS/DFS/Union-Find):
    every vertex starts with its own label, and along each edge the smaller
    label is copied until nothing changes any more. Runtime O(V * E), which
    is fine for checking small test cases.
    """
    vertex_list = list(vertices)
    edge_list = list(edges)
    label = {v: i for i, v in enumerate(vertex_list)}
    changed = True
    while changed:
        changed = False
        for u, v in edge_list:
            smaller = min(label[u], label[v])
            if label[u] != smaller or label[v] != smaller:
                label[u] = label[v] = smaller
                changed = True
    return label


def count_components(graph: Graph) -> int:
    """Return the number of connected components (direction is ignored)."""
    labels = _component_labels(graph.vertices(), [(u, v) for u, v, _ in graph.edges()])
    return len(set(labels.values()))


def assert_valid_spanning_forest(graph: Graph, edges: Iterable[tuple[Vertex, Vertex] | tuple[Vertex, Vertex, float]]) -> None:
    """Check that ``edges`` form a spanning forest of the undirected ``graph``.

    A spanning forest contains a spanning tree for every connected component
    of the graph: it uses only edges of the graph, contains no cycle and
    connects exactly the vertices that are connected in the graph.

    ``edges`` may contain pairs ``(u, v)`` or triples / ``Edge`` objects.
    """
    pairs = [(edge[0], edge[1]) for edge in edges]
    for u, v in pairs:
        assert graph.has_edge(u, v), f"{u!r} - {v!r} is not an edge of the graph"
    assert len({frozenset(p) for p in pairs}) == len(pairs), "An edge appears twice"

    graph_labels = _component_labels(graph.vertices(), [(u, v) for u, v, _ in graph.edges()])
    forest_labels = _component_labels(graph.vertices(), pairs)
    graph_components = len(set(graph_labels.values()))
    forest_components = len(set(forest_labels.values()))
    assert forest_components == graph_components, (
        f"The edges leave {forest_components} components, but the graph has "
        f"{graph_components} - some connections are missing"
    )
    # A forest with n vertices and k components has exactly n - k edges.
    expected = graph.num_vertices() - graph_components
    assert len(pairs) == expected, (
        f"Expected {expected} edges, got {len(pairs)} - the edges contain a cycle"
    )


def assert_valid_spanning_tree(graph: Graph, edges: Iterable[tuple[Vertex, Vertex] | tuple[Vertex, Vertex, float]]) -> None:
    """Check that ``edges`` form a spanning tree of the connected ``graph``."""
    assert count_components(graph) <= 1, "The graph is not connected"
    assert_valid_spanning_forest(graph, edges)


# ----------------------------------------------------------------------
# Colourings and matchings
# ----------------------------------------------------------------------
def assert_valid_coloring(
    graph: Graph, coloring: Mapping[Vertex, Hashable], max_colors: int | None = None
) -> None:
    """Check that ``coloring`` is a proper vertex colouring of ``graph``.

    Every vertex must have a colour, and adjacent vertices must have
    different colours.

    Args:
        graph: The graph.
        coloring: Dictionary vertex -> colour.
        max_colors: If given, at most this many different colours may be used.
    """
    assert coloring is not None, "Expected a colouring, got None"
    for v in graph.vertices():
        assert v in coloring, f"Vertex {v!r} has no colour"
    for v in coloring:
        assert v in graph, f"{v!r} is not a vertex of the graph"
    for u, v, _ in graph.edges():
        assert coloring[u] != coloring[v], (
            f"Adjacent vertices {u!r} and {v!r} both have colour {coloring[u]!r}"
        )
    if max_colors is not None:
        used = len(set(coloring.values()))
        assert used <= max_colors, f"{used} colours used, at most {max_colors} allowed"


def assert_valid_matching(
    graph: Graph,
    matching: Mapping[Vertex, Vertex] | Iterable[tuple[Vertex, Vertex]],
    left: Iterable[Vertex] | None = None,
) -> None:
    """Check that ``matching`` is a matching in ``graph``.

    A matching is a set of edges without common end vertices.

    Args:
        graph: The graph.
        matching: Either a dictionary ``left -> right`` or a list of pairs.
        left: If given, the first vertex of each pair must belong to this
            set and the second must not.
    """
    assert matching is not None, "Expected a matching, got None"
    pairs = list(matching.items()) if isinstance(matching, Mapping) else list(matching)
    covered: set[Vertex] = set()
    left_set = set(left) if left is not None else None
    for u, v in pairs:
        assert graph.has_edge(u, v), f"{u!r} - {v!r} is not an edge of the graph"
        assert u not in covered, f"Vertex {u!r} is matched twice"
        assert v not in covered, f"Vertex {v!r} is matched twice"
        covered.update((u, v))
        if left_set is not None:
            assert u in left_set, f"{u!r} should be a left vertex"
            assert v not in left_set, f"{v!r} should be a right vertex"


# ----------------------------------------------------------------------
# Flows
# ----------------------------------------------------------------------
def flow_value(graph: Graph, flow: Mapping[tuple[Vertex, Vertex], float], source: Vertex) -> float:
    """Return the value of a flow: outflow minus inflow at the source.

    Edges missing from ``flow`` count as flow 0.
    """
    outflow = sum(flow.get((source, v), 0) for v in graph.neighbors(source))
    inflow = sum(flow.get((u, source), 0) for u in graph.predecessors(source))
    return outflow - inflow


def assert_valid_flow(
    graph: Graph,
    flow: Mapping[tuple[Vertex, Vertex], float],
    source: Vertex,
    sink: Vertex,
    tolerance: float = 1e-9,
) -> None:
    """Check that ``flow`` is a feasible flow from ``source`` to ``sink``.

    The capacities are the edge weights of the directed ``graph``. Checked:

    * every key of ``flow`` is an edge of the graph,
    * capacity constraint: ``0 <= flow(u, v) <= capacity(u, v)``,
    * flow conservation: inflow = outflow for every vertex except
      source and sink.
    """
    assert graph.directed, "Flow networks must be directed graphs"
    for (u, v), value in flow.items():
        assert graph.has_edge(u, v), f"Flow on {u!r} -> {v!r}, but there is no such edge"
        capacity = graph.weight(u, v)
        assert value >= -tolerance, f"Negative flow {value} on {u!r} -> {v!r}"
        assert value <= capacity + tolerance, (
            f"Flow {value} on {u!r} -> {v!r} exceeds the capacity {capacity}"
        )
    for v in graph.vertices():
        if v in (source, sink):
            continue
        inflow = sum(flow.get((u, v), 0) for u in graph.predecessors(v))
        outflow = sum(flow.get((v, w), 0) for w in graph.neighbors(v))
        assert math.isclose(inflow, outflow, abs_tol=tolerance), (
            f"Flow conservation violated at {v!r}: inflow {inflow}, outflow {outflow}"
        )


def cut_capacity(graph: Graph, source_side: Iterable[Vertex]) -> float:
    """Return the capacity of the cut ``(S, V \\ S)`` with ``S = source_side``.

    This is the sum of the capacities of all edges ``u -> v`` with ``u`` in
    ``S`` and ``v`` not in ``S``.
    """
    s = set(source_side)
    return sum(w for u, v, w in graph.edges() if u in s and v not in s)
