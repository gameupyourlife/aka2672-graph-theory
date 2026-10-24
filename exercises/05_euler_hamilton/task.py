"""Unit 5: Euler and Hamilton problems - YOUR SOLUTION.

Read README.md in this folder first. Replace every
``raise NotImplementedError(...)`` by your own code.

Run the tests from the project root with::

    python -m pytest exercises/05_euler_hamilton
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))  # find ``lib``

from lib.generators import complete_graph, petersen_graph, small_weighted_graph
from lib.graph import Graph, Vertex
from lib.utils import format_path

# The seven bridges of Königsberg: (bridge, bank, bank). There are two
# bridges between the island and the north bank and two between the island
# and the south bank - parallel edges, which our Graph class does not allow.
# The __main__ block below therefore turns every bridge into a vertex.
KOENIGSBERG_BRIDGES = [
    ("b1", "Insel", "Nord"),
    ("b2", "Insel", "Nord"),
    ("b3", "Insel", "Süd"),
    ("b4", "Insel", "Süd"),
    ("b5", "Insel", "Ost"),
    ("b6", "Nord", "Ost"),
    ("b7", "Süd", "Ost"),
]

# "Das ist das Haus vom Ni-ko-laus": 5 corners, 8 lines (see README.md).
NIKOLAUS_EDGES = [(1, 2), (1, 3), (1, 4), (2, 3), (2, 4), (3, 4), (3, 5), (4, 5)]


def edges_connected(graph: Graph) -> bool:
    """Return ``True`` if all vertices with positive degree lie in one component.

    Isolated vertices (degree 0) are ignored. A graph without edges
    (including the empty graph) gives ``True``.

    Write your own small search here (do not import other exercises).

    Raises:
        ValueError: If the graph is directed.
    """
    # TODO: Step 1 - raise a ValueError for directed graphs.
    # TODO: Step 2 - collect all vertices with degree > 0; if there are none,
    #                return True.
    # TODO: Step 3 - start a search (stack or queue) at the first of them and
    #                remember every vertex you reach in a set.
    # TODO: Step 4 - return True if every vertex with degree > 0 was reached.
    raise NotImplementedError("TODO: edges_connected")


def has_euler_circuit(graph: Graph) -> bool:
    """Return ``True`` if the undirected graph has an Euler circuit.

    An Euler circuit is a closed walk that uses every edge exactly once.
    Conventions: isolated vertices are ignored, and a graph without edges
    (including the empty graph) has a trivial Euler circuit (``True``).

    Raises:
        ValueError: If the graph is directed.
    """
    # TODO: Raise a ValueError for directed graphs.
    # TODO: Use Euler's theorem: edges_connected(graph) and every degree even.
    raise NotImplementedError("TODO: has_euler_circuit")


def has_euler_trail(graph: Graph) -> bool:
    """Return ``True`` if the undirected graph has an Euler trail.

    An Euler trail is a walk that uses every edge exactly once. It may be
    open or closed, so every graph with an Euler circuit also has an Euler
    trail. Same conventions as :func:`has_euler_circuit`.

    Raises:
        ValueError: If the graph is directed.
    """
    # TODO: Raise a ValueError for directed graphs.
    # TODO: Use Euler's theorem: edges_connected(graph) and exactly 0 or 2
    #       vertices of odd degree.
    raise NotImplementedError("TODO: has_euler_trail")


def find_euler_circuit(graph: Graph) -> list[Vertex] | None:
    """OPTIONAL: Return an Euler circuit as a closed walk ``[v0, ..., v0]``.

    The list has ``|E| + 1`` entries and uses every edge exactly once.
    Returns ``None`` if there is no Euler circuit and ``[]`` for a graph
    without edges. The input graph must not be modified.

    Raises:
        ValueError: If the graph is directed.
    """
    # TODO (optional): Hierholzer's algorithm, see README.md.
    #   Step 1 - handle directed graphs, graphs without edges and graphs
    #            without an Euler circuit.
    #   Step 2 - remaining = graph.copy(); choose a start vertex with an edge.
    #   Step 3 - stack = [start], walk = []. While the stack is not empty:
    #            look at the top vertex v. If v still has an edge v - w in
    #            remaining, delete that edge and push w. Otherwise pop v and
    #            append it to walk.
    #   Step 4 - return walk (reversed).
    raise NotImplementedError("TODO (optional): find_euler_circuit")


def find_euler_trail(graph: Graph) -> list[Vertex] | None:
    """OPTIONAL: Return an Euler trail (open or closed) as a list of vertices.

    The list has ``|E| + 1`` entries and uses every edge exactly once. If
    the graph has two vertices of odd degree, the trail starts at one of
    them and ends at the other. Returns ``None`` if there is no Euler trail
    and ``[]`` for a graph without edges. The input graph must not be
    modified.

    Raises:
        ValueError: If the graph is directed.
    """
    # TODO (optional): Same algorithm as find_euler_circuit - only the start
    #                  vertex is different.
    raise NotImplementedError("TODO (optional): find_euler_trail")


def find_hamiltonian_cycle(graph: Graph) -> list[Vertex] | None:
    """OPTIONAL: Return a Hamiltonian cycle ``[v0, v1, ..., v_{n-1}, v0]``.

    Every vertex appears exactly once (the first one is repeated at the
    end). Returns ``None`` if there is no Hamiltonian cycle or if the graph
    has fewer than 3 vertices. Naive backtracking is enough - this is only
    meant for small graphs. The input graph must not be modified.

    Raises:
        ValueError: If the graph is directed.
    """
    # TODO (optional): Backtracking, see README.md.
    #   Step 1 - handle directed graphs and graphs with fewer than 3 vertices.
    #   Step 2 - fix a start vertex; path = [start].
    #   Step 3 - write an inner function extend() that tries every unused
    #            neighbour of path[-1], calls itself, and undoes the step if
    #            that leads to a dead end.
    #   Step 4 - a full path is a solution if its last vertex is adjacent
    #            to the start.
    raise NotImplementedError("TODO (optional): find_hamiltonian_cycle")


if __name__ == "__main__":
    # Königsberg as a simple graph: every bridge becomes a vertex of degree 2.
    koenigsberg = Graph()
    for bridge, bank1, bank2 in KOENIGSBERG_BRIDGES:
        koenigsberg.add_edge(bank1, bridge)
        koenigsberg.add_edge(bridge, bank2)
    print("Königsberg: Euler circuit", has_euler_circuit(koenigsberg))
    print("Königsberg: Euler trail  ", has_euler_trail(koenigsberg))

    nikolaus = Graph.from_edges(NIKOLAUS_EDGES)
    print("Nikolaus: Euler circuit", has_euler_circuit(nikolaus))
    print("Nikolaus: Euler trail  ", has_euler_trail(nikolaus))
    print("Lönneberga: Euler trail", has_euler_trail(small_weighted_graph()))
    for n in range(2, 7):
        print(f"K_{n}: Euler circuit {has_euler_circuit(complete_graph(n))}")

    # Optional tasks:
    print("Euler trail of the Nikolaus house:", format_path(find_euler_trail(nikolaus), directed=False))
    print("Hamiltonian cycle of the Petersen graph:", find_hamiltonian_cycle(petersen_graph()))
