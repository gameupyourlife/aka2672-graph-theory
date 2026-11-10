"""Unit 6 - Graph colouring.

Follow the TODOs in each function. Replace each
``raise NotImplementedError(...)`` with your implementation.

The example at the end of this file also calls optional functions.
Use pytest to check the required functions while those TODOs are unfinished.

Run the tests from the project root.

    python -m pytest exercises/06_graph_coloring
"""

import sys
from collections import deque  # you will need deque in is_bipartite()
from collections.abc import Mapping, Sequence
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))  # find ``lib``

from lib.generators import cycle_graph, petersen_graph
from lib.graph import Graph, Vertex

# Pippi's party in Villa Kunterbunt: all guests, and the
# pairs of guests who must not sit at the same table.
PARTY_GUESTS = [
    "Pippi",
    "Tommy",
    "Annika",
    "Herr Nilsson",
    "Kleiner Onkel",
    "Prusseliese",
    "Kling",
    "Klang",
    "Donner-Karlsson",
    "Blom",
]

PARTY_CONFLICTS = [
    ("Kling", "Donner-Karlsson"),
    ("Kling", "Blom"),
    ("Klang", "Donner-Karlsson"),
    ("Klang", "Blom"),
    ("Donner-Karlsson", "Blom"),
    ("Pippi", "Prusseliese"),
    ("Herr Nilsson", "Prusseliese"),
]


def greedy_coloring(graph: Graph, order: Sequence[Vertex] | None = None) -> dict[Vertex, int]:
    """Colour the vertices greedily in the given order.

    The colours are the numbers 0, 1, 2, ... The vertices are coloured one
    after the other in the order ``order``; every vertex gets the smallest
    colour that none of its *already coloured* neighbours has.
    ``order=None`` means the order of ``graph.vertices()``. Use O(|V| + |E|)
    time and leave the graph unchanged.

    Returns:
        A dictionary ``vertex -> colour`` containing every vertex.

    Raises:
        ValueError: If the graph is directed, or if ``order`` is not a
            permutation of the vertices (a vertex missing, repeated, or not
            in the graph).
    """
    # TODO: Step 1 - raise a ValueError for directed graphs.
    # TODO: Step 2 - use graph.vertices() if order is None; otherwise check
    #                that order contains every vertex exactly once.
    # TODO: Step 3 - for every vertex v in order: collect the colours of the
    #                neighbours that already have a colour in a set, then
    #                find the smallest number 0, 1, 2, ... not in this set.
    raise NotImplementedError("TODO: greedy_coloring")


def is_valid_coloring(graph: Graph, coloring: Mapping[Vertex, int]) -> bool:
    """Return ``True`` if ``coloring`` is a proper colouring of ``graph``.

    Proper means:

    * every vertex of the graph has a colour,
    * every key of ``coloring`` is a vertex of the graph,
    * the two end vertices of every edge have different colours.

    Write this check yourself (do not call ``lib.testing``).

    Raises:
        ValueError: If the graph is directed.
    """
    # TODO: Check the three conditions one after the other.
    raise NotImplementedError("TODO: is_valid_coloring")


def number_of_colors(coloring: Mapping[Vertex, int]) -> int:
    """Return the number of different colours used in ``coloring``.

    An empty colouring uses 0 colours.
    """
    # TODO: Count the *different* values (a set helps).
    raise NotImplementedError("TODO: number_of_colors")


def is_bipartite(graph: Graph) -> bool:
    """Return ``True`` if the undirected graph is bipartite (2-colourable).

    Use your own breadth-first search: in every connected component, give
    the start vertex side 0 and every newly discovered vertex the opposite
    side of the vertex it was discovered from. The graph is bipartite
    exactly if no edge joins two vertices of the same side. Graphs without
    edges (including the empty graph) are bipartite.

    Raises:
        ValueError: If the graph is directed.
    """
    # TODO: Step 1 - raise a ValueError for directed graphs.
    # TODO: Step 2 - side = {}. For every vertex s that has no side yet,
    #                set side[s] = 0 and start a BFS from s.
    # TODO: Step 3 - in the BFS, look at every neighbour w of u: if w has no
    #                side, give it 1 - side[u] and append it to the queue;
    #                if w has the same side as u, return False.
    # TODO: Step 4 - no conflict found: return True.
    raise NotImplementedError("TODO: is_bipartite")


def welsh_powell_order(graph: Graph) -> list[Vertex]:
    """OPTIONAL: Return the vertices sorted by descending degree.

    Vertices with equal degree keep their order from ``graph.vertices()``.
    Use the result as ``order`` for :func:`greedy_coloring`.

    Raises:
        ValueError: If the graph is directed.
    """
    # TODO (optional): use sorted() with graph.degree as the key and reverse=True.
    raise NotImplementedError("TODO (optional): welsh_powell_order")


def find_odd_cycle(graph: Graph) -> list[Vertex] | None:
    """OPTIONAL: Return an odd cycle ``[v0, v1, ..., v0]`` or ``None``.

    If the graph is not bipartite, return a cycle with an odd number of
    edges: consecutive vertices are adjacent, the first vertex is repeated
    at the end, and no other vertex appears twice. If the graph is
    bipartite, return ``None``.

    Raises:
        ValueError: If the graph is directed.
    """
    # TODO (optional): Run the BFS from is_bipartite, but also remember
    #                  parent[v] and the BFS depth of every vertex. When you
    #                  find an edge u - w with equal depth, walk up the BFS
    #                  tree from u and from w until the two paths meet.
    raise NotImplementedError("TODO (optional): find_odd_cycle")


if __name__ == "__main__":
    party = Graph()
    party.add_vertices(PARTY_GUESTS)
    party.add_edges(PARTY_CONFLICTS)
    tables = greedy_coloring(party)
    print("Tables:", tables)
    print("Number of tables:", number_of_colors(tables))
    print("Valid seating plan:", is_valid_coloring(party, tables))
    print("Two tables enough (bipartite)?", is_bipartite(party))

    path = Graph.from_edges([(0, 1), (1, 2), (2, 3)])
    print("Path, order 0,1,2,3:", greedy_coloring(path))
    print("Path, order 0,3,1,2:", greedy_coloring(path, [0, 3, 1, 2]))

    # Optional tasks:
    petersen = petersen_graph()
    print("Petersen graph, Welsh-Powell order:", welsh_powell_order(petersen))
    print("Odd cycle in C_7:", find_odd_cycle(cycle_graph(7)))
