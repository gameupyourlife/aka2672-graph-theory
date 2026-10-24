"""Unit 1: Modelling graphs - YOUR SOLUTION.

Read README.md in this folder first. Replace every
``raise NotImplementedError(...)`` by your own code.

Run the tests from the project root with::

    python -m pytest exercises/01_graph_basics
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))  # find ``lib``

from lib.graph import Graph, Vertex
from lib.visualization import print_graph


def build_bullerby_graph() -> Graph:
    """Return the undirected graph of footpaths in Bullerbü.

    The vertices are the place names from the first table in README.md,
    every footpath is an (unweighted) edge.
    """
    # TODO: Create an undirected Graph and add one edge per footpath.
    raise NotImplementedError("TODO: build_bullerby_graph")


def build_letter_graph() -> Graph:
    """Return the directed graph "who writes letters to whom".

    An edge ``u -> v`` means: child ``u`` writes letters to child ``v``.
    """
    # TODO: Create a *directed* Graph and add one edge per row of the table.
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
    # TODO
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
    ``graph``.
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
