"""Unit 1: Modelling graphs - DEMO SOLUTION.

This file solves all tasks of README.md. It is written as teaching material:
the comments explain *why* each step is done.

Run it with ``python exercises/01_graph_basics/demo_solution.py``.
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))  # find ``lib``

from lib.graph import Graph, Vertex
from lib.visualization import can_draw, draw, print_graph

# The data from README.md, written as lists of pairs. Keeping data separate
# from code makes it easy to check against the table.
FOOTPATHS = [
    ("Nordhof", "Mittelhof"),
    ("Mittelhof", "Südhof"),
    ("Nordhof", "Südhof"),
    ("Mittelhof", "Schule"),
    ("Schule", "Kaufladen"),
    ("Kaufladen", "Badestelle"),
    ("Südhof", "Badestelle"),
    ("Badestelle", "Erdbeerstelle"),
    ("Nordhof", "Erdbeerstelle"),
]

LETTERS = [
    ("Lisa", "Britta"),
    ("Lisa", "Inga"),
    ("Britta", "Lisa"),
    ("Inga", "Britta"),
    ("Lasse", "Ole"),
    ("Bosse", "Lasse"),
    ("Ole", "Bosse"),
    ("Lasse", "Lisa"),
]


def build_bullerby_graph() -> Graph:
    """Return the undirected graph of footpaths in Bullerbü."""
    graph = Graph(directed=False)
    for u, v in FOOTPATHS:
        # add_edge creates missing vertices automatically.
        graph.add_edge(u, v)
    return graph


def build_letter_graph() -> Graph:
    """Return the directed graph "who writes letters to whom"."""
    graph = Graph(directed=True)
    for sender, receiver in LETTERS:
        # The order matters: the edge points from sender to receiver.
        graph.add_edge(sender, receiver)
    return graph


def degrees(graph: Graph) -> dict[Vertex, int]:
    """Return a dictionary ``vertex -> degree`` for every vertex.

    Idea (this is exactly the proof of the handshake lemma): every edge
    {u, v} contributes 1 to the degree of u and 1 to the degree of v.
    """
    # Start with 0 for *every* vertex, so isolated vertices are included.
    result = {v: 0 for v in graph.vertices()}
    for u, v, _weight in graph.edges():
        result[u] += 1
        result[v] += 1
    return result


def degree_sequence(graph: Graph) -> list[int]:
    """Return the degree sequence: all degrees sorted in descending order."""
    return sorted(degrees(graph).values(), reverse=True)


def odd_degree_vertices(graph: Graph) -> list[Vertex]:
    """Return all vertices with odd degree (in the order of ``graph.vertices()``)."""
    degree_of = degrees(graph)
    return [v for v in graph.vertices() if degree_of[v] % 2 == 1]


def check_handshake_lemma(graph: Graph) -> bool:
    """Return ``True`` if the sum of all degrees equals ``2 * |E|``.

    Raises:
        ValueError: If the graph is directed.
    """
    if graph.directed:
        raise ValueError("The handshake lemma is stated for undirected graphs")
    return sum(degrees(graph).values()) == 2 * graph.num_edges()


def in_and_out_degrees(graph: Graph) -> dict[Vertex, tuple[int, int]]:
    """Return ``vertex -> (in_degree, out_degree)`` for a directed graph.

    Raises:
        ValueError: If the graph is undirected.
    """
    if not graph.directed:
        raise ValueError("In- and out-degrees are defined for directed graphs")
    in_degree = {v: 0 for v in graph.vertices()}
    out_degree = {v: 0 for v in graph.vertices()}
    for u, v, _weight in graph.edges():
        out_degree[u] += 1  # the edge leaves u ...
        in_degree[v] += 1  # ... and enters v
    return {v: (in_degree[v], out_degree[v]) for v in graph.vertices()}


def adjacency_matrix(graph: Graph, order: list[Vertex] | None = None) -> list[list[int]]:
    """Return the adjacency matrix of ``graph`` as a list of rows.

    Raises:
        ValueError: If ``order`` does not contain every vertex exactly once.
    """
    if order is None:
        order = graph.vertices()
    # The order must be a permutation of the vertex set.
    if len(order) != graph.num_vertices() or set(order) != set(graph.vertices()):
        raise ValueError("order must contain every vertex exactly once")

    n = len(order)
    # Translate vertex names into row/column numbers.
    index = {v: i for i, v in enumerate(order)}
    # One new list per row! ([[0] * n] * n would share a single row.)
    matrix = [[0] * n for _ in range(n)]
    for u, v, _weight in graph.edges():
        matrix[index[u]][index[v]] = 1
        if not graph.directed:
            # Undirected edges work in both directions: the matrix is symmetric.
            matrix[index[v]][index[u]] = 1
    return matrix


def complement(graph: Graph) -> Graph:
    """OPTIONAL: Return the complement of the undirected ``graph``."""
    if graph.directed:
        raise ValueError("complement() expects an undirected graph")
    result = Graph(directed=False)
    vertices = graph.vertices()
    result.add_vertices(vertices)
    # Look at every unordered pair {u, v} exactly once (i < j).
    for i in range(len(vertices)):
        for j in range(i + 1, len(vertices)):
            u, v = vertices[i], vertices[j]
            if not graph.has_edge(u, v):
                result.add_edge(u, v)
    return result


if __name__ == "__main__":
    bullerby = build_bullerby_graph()
    print_graph(bullerby)
    print("Degrees:", degrees(bullerby))
    print("Degree sequence:", degree_sequence(bullerby))
    odd = odd_degree_vertices(bullerby)
    print(f"Odd degree ({len(odd)} vertices - an even number!):", odd)
    print("Handshake lemma holds:", check_handshake_lemma(bullerby))
    print()
    letters = build_letter_graph()
    print_graph(letters)
    print("(in, out):", in_and_out_degrees(letters))
    print()
    for row in adjacency_matrix(bullerby):
        print(row)

    # Drawings (only if matplotlib is installed). The windows do not block:
    # the program continues, and they stay open until you close them.
    if can_draw():
        draw(
            bullerby,
            title=f"Bullerbü: {len(odd)} vertices with odd degree (red)",
            highlight_vertices=odd,
            vertex_labels={v: f"deg {d}" for v, d in degrees(bullerby).items()},
        )
        draw(
            letters,
            title="Who writes letters to whom?",
            vertex_labels={v: f"in {i} / out {o}" for v, (i, o) in in_and_out_degrees(letters).items()},
        )
