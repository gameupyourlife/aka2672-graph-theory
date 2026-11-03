"""Unit 6: Graph colouring - DEMO SOLUTION.

A (proper vertex) colouring gives every vertex a colour so that adjacent
vertices get different colours. Colours are the numbers 0, 1, 2, ...

* The greedy algorithm colours the vertices one after the other and always
  takes the smallest free colour. It never needs more than Delta + 1 colours
  (Delta = maximum degree), but the result depends on the vertex order.
* Two colours suffice exactly for bipartite graphs, i.e. graphs without odd
  cycles (König 1936). A breadth-first search decides this in O(|V| + |E|).
* For three or more colours no efficient algorithm is known: deciding
  whether k colours suffice is NP-complete for every fixed k >= 3.

Run it with ``python exercises/06_graph_coloring/demo_solution.py``.
"""

import sys
from collections import deque
from collections.abc import Mapping, Sequence
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))  # find ``lib``

from lib.generators import cycle_graph, petersen_graph
from lib.graph import Graph, Vertex
from lib.visualization import show, snapshot

# Pippi's party in Villa Kunterbunt (see README.md): all guests, and the
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


def _require_undirected(graph: Graph, name: str) -> None:
    """Raise ``ValueError`` if ``graph`` is directed."""
    if graph.directed:
        raise ValueError(f"{name}() expects an undirected graph")


def greedy_coloring(graph: Graph, order: Sequence[Vertex] | None = None) -> dict[Vertex, int]:
    """Colour the vertices greedily in the given order.

    Every vertex gets the smallest colour (0, 1, 2, ...) that none of its
    already coloured neighbours has. ``order=None`` means
    ``graph.vertices()``.

    Raises:
        ValueError: If the graph is directed or ``order`` is not a
            permutation of the vertices.
    """
    _require_undirected(graph, "greedy_coloring")
    if order is None:
        order = graph.vertices()
    # The order must contain every vertex exactly once.
    if len(order) != graph.num_vertices() or set(order) != set(graph.vertices()):
        raise ValueError("order must contain every vertex exactly once")

    coloring: dict[Vertex, int] = {}
    for v in order:
        # Colours that are already taken by neighbours of v. Neighbours that
        # come later in the order have no colour yet and do not count.
        used = {coloring[w] for w in graph.neighbors(v) if w in coloring}
        # The smallest free colour. Since |used| <= deg(v), this loop stops
        # at colour deg(v) at the latest - hence at most Delta + 1 colours.
        color = 0
        while color in used:
            color += 1
        coloring[v] = color
    return coloring


def is_valid_coloring(graph: Graph, coloring: Mapping[Vertex, int]) -> bool:
    """Return ``True`` if ``coloring`` is a proper colouring of ``graph``.

    Proper means: every vertex has a colour, there are no keys that are not
    vertices, and the end vertices of every edge have different colours.

    Raises:
        ValueError: If the graph is directed.
    """
    _require_undirected(graph, "is_valid_coloring")
    for v in graph.vertices():
        if v not in coloring:
            return False  # a vertex without colour
    for v in coloring:
        if v not in graph:
            return False  # a colour for something that is not a vertex
    for u, v, _weight in graph.edges():
        if coloring[u] == coloring[v]:
            return False  # an edge whose end vertices have the same colour
    return True


def number_of_colors(coloring: Mapping[Vertex, int]) -> int:
    """Return the number of different colours used in ``coloring``."""
    # A set removes duplicates: {0, 1, 0, 2} -> {0, 1, 2}.
    return len(set(coloring.values()))


def is_bipartite(graph: Graph) -> bool:
    """Return ``True`` if the undirected graph is bipartite (2-colourable).

    Idea: in every component, start a BFS and give each vertex the colour
    "distance from the start modulo 2". The graph is bipartite exactly if no
    edge joins two vertices of the same colour.

    Raises:
        ValueError: If the graph is directed.
    """
    _require_undirected(graph, "is_bipartite")
    side: dict[Vertex, int] = {}
    for start in graph.vertices():
        if start in side:
            continue  # this component has already been coloured
        side[start] = 0
        queue = deque([start])
        while queue:
            u = queue.popleft()
            for w in graph.neighbors(u):
                if w not in side:
                    # The colour of w is forced: the opposite of u.
                    side[w] = 1 - side[u]
                    queue.append(w)
                elif side[w] == side[u]:
                    # An edge inside one side: there is an odd cycle.
                    return False
    return True


def welsh_powell_order(graph: Graph) -> list[Vertex]:
    """OPTIONAL: Return the vertices sorted by descending degree.

    Vertices with equal degree keep their order from ``graph.vertices()``.

    Raises:
        ValueError: If the graph is directed.
    """
    _require_undirected(graph, "welsh_powell_order")
    # Python's sort is stable (also with reverse=True): equal keys keep
    # their original order.
    return sorted(graph.vertices(), key=graph.degree, reverse=True)


def find_odd_cycle(graph: Graph) -> list[Vertex] | None:
    """OPTIONAL: Return an odd cycle ``[v0, ..., v0]`` or ``None`` if bipartite.

    The cycle has an odd number of edges, and no vertex is repeated except
    that the first vertex appears again at the end.

    Raises:
        ValueError: If the graph is directed.
    """
    _require_undirected(graph, "find_odd_cycle")
    depth: dict[Vertex, int] = {}
    parent: dict[Vertex, Vertex | None] = {}
    for start in graph.vertices():
        if start in depth:
            continue
        depth[start] = 0
        parent[start] = None
        queue = deque([start])
        while queue:
            u = queue.popleft()
            for w in graph.neighbors(u):
                if w not in depth:
                    depth[w] = depth[u] + 1
                    parent[w] = u
                    queue.append(w)
                elif depth[w] % 2 == depth[u] % 2:
                    # BFS depths of neighbours differ by at most 1, so equal
                    # parity means equal depth. Walk up the BFS tree from u
                    # and w in parallel until both paths meet.
                    from_u = [u]
                    from_w = [w]
                    while from_u[-1] != from_w[-1]:
                        from_u.append(parent[from_u[-1]])
                        from_w.append(parent[from_w[-1]])
                    # from_u = [u, ..., meet], from_w = [w, ..., meet].
                    # Cycle: u -> ... -> meet -> ... -> w -> u. Both tree
                    # paths have the same length k, so it has 2k + 1 edges.
                    return from_u + from_w[-2::-1] + [u]
    return None


if __name__ == "__main__":
    party = Graph()
    party.add_vertices(PARTY_GUESTS)
    party.add_edges(PARTY_CONFLICTS)
    tables = greedy_coloring(party)
    print("Pippi's party - tables (greedy, default order):")
    for table in range(number_of_colors(tables)):
        guests = [guest for guest, t in tables.items() if t == table]
        print(f"  table {table}: {', '.join(guests)}")
    print("Valid seating plan:", is_valid_coloring(party, tables))
    print("Two tables enough (bipartite)?", is_bipartite(party))
    print("Odd cycle:", find_odd_cycle(party))
    print()

    # The order matters: a path coloured in a bad order needs 3 colours.
    path = Graph.from_edges([(0, 1), (1, 2), (2, 3)])
    print("Path, order 0,1,2,3:", greedy_coloring(path))
    print("Path, order 0,3,1,2:", greedy_coloring(path, [0, 3, 1, 2]))

    # Crown graph: a_i -- b_j for i != j. Bipartite, but the alternating
    # order a0, b0, a1, b1, ... forces greedy to use n colours.
    n = 5
    sides = [("a", i) for i in range(n)] + [("b", i) for i in range(n)]
    alternating = [vertex for i in range(n) for vertex in (("a", i), ("b", i))]
    crown = Graph()
    crown.add_vertices(sides)
    for i in range(n):
        for j in range(n):
            if i != j:
                crown.add_edge(("a", i), ("b", j))
    print(f"Crown graph ({2 * n} vertices), alternating order:",
          number_of_colors(greedy_coloring(crown, alternating)), "colours")
    print(f"Crown graph ({2 * n} vertices), one side first:   ",
          number_of_colors(greedy_coloring(crown, sides)), "colours")
    print()

    petersen = petersen_graph()
    print("Petersen graph, Welsh-Powell order:", welsh_powell_order(petersen))
    print("Petersen graph, greedy colours:", number_of_colors(greedy_coloring(petersen, welsh_powell_order(petersen))))
    print("C_7 bipartite?", is_bipartite(cycle_graph(7)), "- odd cycle:", find_odd_cycle(cycle_graph(7)))

    # Pictures in the browser (no extra packages needed).
    odd_cycle = find_odd_cycle(party) or []
    a_side = [("a", i) for i in range(n)]
    crown_pictures = []
    for name, order in [("alternating order", alternating), ("one side first", sides)]:
        coloring = greedy_coloring(crown, order)
        crown_pictures.append(
            snapshot(
                crown,
                f"Crown graph, {name}: {number_of_colors(coloring)} colours",
                left=a_side,
                vertex_colors=coloring,
            )
        )
    petersen_colors = greedy_coloring(petersen, welsh_powell_order(petersen))
    show(
        snapshot(
            party,
            f"Pippi's party: {number_of_colors(tables)} tables (odd cycle in red)",
            vertex_colors={guest: f"table {t}" for guest, t in tables.items()},
            highlight_edges=list(zip(odd_cycle, odd_cycle[1:])),
        ),
        *crown_pictures,
        snapshot(
            petersen,
            f"Petersen graph, Welsh-Powell: {number_of_colors(petersen_colors)} colours",
            shells=[range(5), range(5, 10)],
            vertex_colors=petersen_colors,
        ),
        title="Unit 6: results",
    )
    print("Step by step: python exercises/06_graph_coloring/demo_animation.py")
