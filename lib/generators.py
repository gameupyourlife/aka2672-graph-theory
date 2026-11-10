"""Functions that create example graphs.

All generators return a :class:`~lib.graph.Graph`. Random generators accept
an optional ``seed``: with the same seed you always get the same graph, which
makes experiments and tests reproducible.

Unless stated otherwise the vertices are the integers ``0, 1, ..., n - 1``.
"""

from __future__ import annotations

import random

from lib.graph import Graph


def path_graph(n: int, directed: bool = False) -> Graph:
    """Return the path ``P_n`` with the vertices ``0 - 1 - ... - (n-1)``.

    Args:
        n: Number of vertices (``n >= 0``).
        directed: If ``True``, the edges point from ``i`` to ``i + 1``.
    """
    _require_non_negative(n, "n")
    graph = Graph(directed=directed)
    graph.add_vertices(range(n))
    for i in range(n - 1):
        graph.add_edge(i, i + 1)
    return graph


def cycle_graph(n: int, directed: bool = False) -> Graph:
    """Return the cycle ``C_n``: ``0 - 1 - ... - (n-1) - 0``.

    Args:
        n: Number of vertices, at least 3 (a simple graph has no shorter
            cycles).
        directed: If ``True``, the edges point from ``i`` to ``i + 1``.
    """
    if n < 3:
        raise ValueError("A cycle needs at least 3 vertices")
    graph = path_graph(n, directed=directed)
    graph.add_edge(n - 1, 0)
    return graph


def complete_graph(n: int) -> Graph:
    """Return the complete graph ``K_n`` (every pair of vertices is adjacent)."""
    _require_non_negative(n, "n")
    graph = Graph()
    graph.add_vertices(range(n))
    for i in range(n):
        for j in range(i + 1, n):
            graph.add_edge(i, j)
    return graph


def complete_bipartite_graph(m: int, n: int) -> Graph:
    """Return the complete bipartite graph ``K_{m,n}``.

    The left vertices are called ``"L0", ..., "L{m-1}"``, the right vertices
    ``"R0", ..., "R{n-1}"``. Every left vertex is adjacent to every right
    vertex.
    """
    _require_non_negative(m, "m")
    _require_non_negative(n, "n")
    graph = Graph()
    graph.add_vertices(f"L{i}" for i in range(m))
    graph.add_vertices(f"R{j}" for j in range(n))
    for i in range(m):
        for j in range(n):
            graph.add_edge(f"L{i}", f"R{j}")
    return graph


def star_graph(n: int) -> Graph:
    """Return the star ``K_{1,n}``: centre ``0`` joined to ``1, ..., n``."""
    _require_non_negative(n, "n")
    graph = Graph()
    graph.add_vertex(0)
    for i in range(1, n + 1):
        graph.add_edge(0, i)
    return graph


def grid_graph(rows: int, cols: int) -> Graph:
    """Return a ``rows x cols`` grid.

    The vertices are tuples ``(row, col)``; neighbours differ by one step to
    the left/right or up/down.
    """
    _require_non_negative(rows, "rows")
    _require_non_negative(cols, "cols")
    graph = Graph()
    for r in range(rows):
        for c in range(cols):
            graph.add_vertex((r, c))
            if r > 0:
                graph.add_edge((r - 1, c), (r, c))
            if c > 0:
                graph.add_edge((r, c - 1), (r, c))
    return graph


def petersen_graph() -> Graph:
    """Return the Petersen graph (10 vertices, 15 edges, 3-regular).

    A famous counterexample: it is not planar and has no Hamiltonian cycle.
    Outer vertices ``0..4`` form a 5-cycle, inner vertices ``5..9`` form a
    pentagram, and ``i`` is joined to ``i + 5``.
    """
    graph = Graph()
    for i in range(5):
        graph.add_edge(i, (i + 1) % 5)  # outer cycle
        graph.add_edge(5 + i, 5 + (i + 2) % 5)  # inner pentagram
        graph.add_edge(i, i + 5)  # spokes
    return graph


def random_graph(
    n: int, p: float, seed: int | None = None, directed: bool = False
) -> Graph:
    """Return a random graph ``G(n, p)`` (Erdős-Rényi model).

    Every possible edge is inserted independently with probability ``p``.

    Args:
        n: Number of vertices.
        p: Edge probability between 0 and 1.
        seed: Optional seed for reproducible results.
        directed: If ``True``, both directions are decided independently.
    """
    _require_non_negative(n, "n")
    _require_probability(p)
    rng = random.Random(seed)
    graph = Graph(directed=directed)
    graph.add_vertices(range(n))
    for u in range(n):
        for v in range(n):
            if u == v or (not directed and v < u):
                continue
            if rng.random() < p:
                graph.add_edge(u, v)
    return graph


def random_tree(n: int, seed: int | None = None) -> Graph:
    """Return a random tree with ``n`` vertices.

    Vertex ``i`` (for ``i >= 1``) is attached to a randomly chosen vertex
    ``j < i``. The result is connected and has exactly ``n - 1`` edges.
    """
    _require_non_negative(n, "n")
    rng = random.Random(seed)
    graph = Graph()
    graph.add_vertices(range(n))
    for i in range(1, n):
        graph.add_edge(rng.randrange(i), i)
    return graph


def random_connected_graph(
    n: int,
    extra_edges: int,
    seed: int | None = None,
    min_weight: int = 1,
    max_weight: int = 1,
) -> Graph:
    """Return a random connected undirected graph.

    The graph consists of a random tree plus ``extra_edges`` further random
    edges (fewer if the graph becomes complete). Weights are random integers
    between ``min_weight`` and ``max_weight`` (default: all weights 1).
    """
    _require_non_negative(n, "n")
    _require_non_negative(extra_edges, "extra_edges")
    if min_weight > max_weight:
        raise ValueError("min_weight must not be larger than max_weight")
    rng = random.Random(seed)
    graph = Graph()
    graph.add_vertices(range(n))
    for i in range(1, n):
        graph.add_edge(rng.randrange(i), i, rng.randint(min_weight, max_weight))
    missing = [
        (u, v)
        for u in range(n)
        for v in range(u + 1, n)
        if not graph.has_edge(u, v)
    ]
    rng.shuffle(missing)
    for u, v in missing[:extra_edges]:
        graph.add_edge(u, v, rng.randint(min_weight, max_weight))
    return graph


def random_bipartite_graph(
    m: int, n: int, p: float, seed: int | None = None
) -> Graph:
    """Return a random bipartite graph.

    Left vertices ``"L0", ..., "L{m-1}"``, right vertices ``"R0", ...,
    "R{n-1}"``. Each of the ``m * n`` possible edges exists with
    probability ``p``.
    """
    _require_non_negative(m, "m")
    _require_non_negative(n, "n")
    _require_probability(p)
    rng = random.Random(seed)
    graph = Graph()
    graph.add_vertices(f"L{i}" for i in range(m))
    graph.add_vertices(f"R{j}" for j in range(n))
    for i in range(m):
        for j in range(n):
            if rng.random() < p:
                graph.add_edge(f"L{i}", f"R{j}")
    return graph


def random_weighted_graph(
    n: int,
    p: float,
    min_weight: int = 1,
    max_weight: int = 10,
    seed: int | None = None,
    directed: bool = False,
) -> Graph:
    """Return a random graph ``G(n, p)`` with random integer weights.

    Args:
        n: Number of vertices.
        p: Edge probability.
        min_weight: Smallest possible weight (inclusive).
        max_weight: Largest possible weight (inclusive).
        seed: Optional seed for reproducible results.
        directed: Whether the graph is directed.
    """
    if min_weight > max_weight:
        raise ValueError("min_weight must not be larger than max_weight")
    rng = random.Random(seed)
    unweighted = random_graph(n, p, seed=rng.randrange(2**32), directed=directed)
    graph = Graph(directed=directed)
    graph.add_vertices(unweighted.vertices())
    for u, v, _ in unweighted.edges():
        graph.add_edge(u, v, rng.randint(min_weight, max_weight))
    return graph


def small_weighted_graph() -> Graph:
    """Return a small fixed weighted graph (paths around Lönneberga).

    Useful for first experiments with spanning trees and shortest paths.
    The weights are walking times in minutes::

        Katthult --4-- Lönneberga --3-- Backhorva
           |  \\            |              |
           2    7          5              6
           |      \\        |              |
        Gibberyd --3-- Kirche ----2---- Markt
    """
    return Graph.from_edges(
        [
            ("Katthult", "Lönneberga", 4),
            ("Katthult", "Gibberyd", 2),
            ("Katthult", "Kirche", 7),
            ("Lönneberga", "Backhorva", 3),
            ("Lönneberga", "Kirche", 5),
            ("Backhorva", "Markt", 6),
            ("Gibberyd", "Kirche", 3),
            ("Kirche", "Markt", 2),
        ]
    )


def _require_non_negative(value: int, name: str) -> None:
    if value < 0:
        raise ValueError(f"{name} must not be negative, got {value}")


def _require_probability(p: float) -> None:
    if not 0 <= p <= 1:
        raise ValueError(f"p must be between 0 and 1, got {p}")
