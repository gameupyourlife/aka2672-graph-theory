"""Unit 1 - Modelling graphs.

Follow the TODOs in each function. Replace each
``raise NotImplementedError(...)`` with your implementation.

Use ``Graph`` from ``lib.graph``. ``Graph(directed=True)`` creates a directed
graph. ``add_edge(u, v)`` adds any missing vertices, ``vertices()`` returns
the vertices, and ``edges()`` returns the edges with their weights.
Handle empty graphs too.

Run the tests from the project root.

    python -m pytest exercises/01_graph_basics
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))  # find ``lib``

from lib.graph import Graph, Vertex
from lib.visualization import print_graph


def build_bullerby_graph() -> Graph:
    """Build an undirected graph with one edge per footpath.

    Use the place names exactly as shown. Each edge has weight 1.

    Nordhof - Mittelhof
    Mittelhof - Südhof
    Nordhof - Südhof
    Mittelhof - Schule
    Schule - Kaufladen
    Kaufladen - Badestelle
    Südhof - Badestelle
    Badestelle - Erdbeerstelle
    Nordhof - Erdbeerstelle
    """
    # TODO: Add an undirected edge for each footpath.
    raise NotImplementedError("TODO: build_bullerby_graph")


def build_letter_graph() -> Graph:
    """Build a directed graph with one edge per sender-recipient pair.

    Each arrow points from the sender to the recipient.

    Lisa -> Britta
    Lisa -> Inga
    Britta -> Lisa
    Inga -> Britta
    Lasse -> Ole
    Bosse -> Lasse
    Ole -> Bosse
    Lasse -> Lisa
    """
    # TODO: Add the directed edges listed above.
    raise NotImplementedError("TODO: build_letter_graph")


def degrees(graph: Graph) -> dict[Vertex, int]:
    """Return a dictionary ``vertex -> degree`` for every vertex.

    The degrees must be computed by counting the end vertices of the edges
    in ``graph.edges()`` (do not use ``graph.degree``). Isolated vertices
    have degree 0. For a directed graph the result is in-degree plus
    out-degree.
    """
    # TODO: Step 1 - start with degree 0 for every vertex.
    # TODO: Step 2 - for every edge (u, v, weight), increase the count of u and v.
    raise NotImplementedError("TODO: degrees")


def degree_sequence(graph: Graph) -> list[int]:
    """Return the degree sequence: all degrees sorted in descending order."""
    # TODO: Use your function degrees().
    raise NotImplementedError("TODO: degree_sequence")


def odd_degree_vertices(graph: Graph) -> list[Vertex]:
    """Return all vertices with odd degree (in the order of ``graph.vertices()``)."""
    # TODO: Filter graph.vertices() using the values from degrees().
    raise NotImplementedError("TODO: odd_degree_vertices")


def check_handshake_lemma(graph: Graph) -> bool:
    """Return ``True`` if the sum of all degrees equals ``2 * |E|``.

    Raises:
        ValueError: If the graph is directed.
    """
    # TODO: Raise a ValueError for directed graphs.
    # TODO: Compare the sum of your degrees() with 2 * graph.num_edges().
    raise NotImplementedError("TODO: check_handshake_lemma")


def in_and_out_degrees(graph: Graph) -> dict[Vertex, tuple[int, int]]:
    """Return ``vertex -> (in_degree, out_degree)`` for a directed graph.

    Compute the values by counting edges (do not use ``graph.in_degree`` or
    ``graph.out_degree``).

    Raises:
        ValueError: If the graph is undirected.
    """
    # TODO: An edge u -> v increases the out-degree of u and the in-degree of v.
    raise NotImplementedError("TODO: in_and_out_degrees")


def adjacency_matrix(graph: Graph, order: list[Vertex] | None = None) -> list[list[int]]:
    """Return the adjacency matrix of ``graph`` as a list of rows.

    Entry ``[i][j]`` is 1 if there is an edge from ``order[i]`` to
    ``order[j]``, otherwise 0. Without ``order`` the order of
    ``graph.vertices()`` is used.

    Raises:
        ValueError: If ``order`` does not contain every vertex exactly once.
    """
    # TODO: Step 1 - choose the order and check it.
    # TODO: Step 2 - create an n x n matrix of zeros.
    # TODO: Step 3 - set the entries for all edges (both directions if undirected).
    raise NotImplementedError("TODO: adjacency_matrix")


def complement(graph: Graph) -> Graph:
    """OPTIONAL: Return the complement of the undirected ``graph``.

    The complement has the same vertices; two different vertices are
    adjacent in the complement exactly if they are *not* adjacent in
    ``graph``. Return a new graph with unweighted edges.

    Raises:
        ValueError: If the graph is directed.
    """
    # TODO (optional)
    raise NotImplementedError("TODO (optional): complement")


if __name__ == "__main__":
    bullerby = build_bullerby_graph()
    print_graph(bullerby)
    print("Degrees:", degrees(bullerby))
    print("Degree sequence:", degree_sequence(bullerby))
    print("Odd degree:", odd_degree_vertices(bullerby))
    print("Handshake lemma holds:", check_handshake_lemma(bullerby))
    letters = build_letter_graph()
    print_graph(letters)
    print("(in, out):", in_and_out_degrees(letters))
