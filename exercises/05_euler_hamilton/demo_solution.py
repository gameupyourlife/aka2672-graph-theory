"""Unit 5: Euler and Hamilton problems - DEMO SOLUTION.

Two problems that look very similar, but behave completely differently:

* **Euler:** use every *edge* exactly once. Euler (1736) showed that this
  only depends on two easy properties: all edges lie in one connected piece,
  and (almost) all degrees are even. Both can be checked in O(|V| + |E|),
  and Hierholzer's algorithm even constructs the circuit in linear time.
* **Hamilton:** visit every *vertex* exactly once. No such simple criterion
  is known - the problem is NP-complete. The only general method in this
  file is to try all possibilities (backtracking), which takes exponential
  time in the worst case.

Run it with ``python exercises/05_euler_hamilton/demo_solution.py``.
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))  # find ``lib``

from lib.generators import complete_graph, petersen_graph, small_weighted_graph
from lib.graph import Graph, Vertex
from lib.utils import format_path
from lib.visualization import show, snapshot

# The seven bridges of Königsberg: (bridge, bank, bank). There are two
# bridges between the island and the north bank and two between the island
# and the south bank - parallel edges, which our Graph class does not allow.
KOENIGSBERG_BRIDGES = [
    ("b1", "Insel", "Nord"),
    ("b2", "Insel", "Nord"),
    ("b3", "Insel", "Süd"),
    ("b4", "Insel", "Süd"),
    ("b5", "Insel", "Ost"),
    ("b6", "Nord", "Ost"),
    ("b7", "Süd", "Ost"),
]

# "Das ist das Haus vom Ni-ko-laus": 5 corners, 8 lines.
NIKOLAUS_EDGES = [(1, 2), (1, 3), (1, 4), (2, 3), (2, 4), (3, 4), (3, 5), (4, 5)]


def _require_undirected(graph: Graph, name: str) -> None:
    """Raise ``ValueError`` if ``graph`` is directed."""
    if graph.directed:
        raise ValueError(f"{name}() expects an undirected graph")


def _odd_degree_vertices(graph: Graph) -> list[Vertex]:
    """Return all vertices of odd degree (in the order of ``graph.vertices()``)."""
    return [v for v in graph.vertices() if graph.degree(v) % 2 == 1]


def edges_connected(graph: Graph) -> bool:
    """Return ``True`` if all vertices with positive degree lie in one component.

    Isolated vertices are ignored; a graph without edges gives ``True``.

    Raises:
        ValueError: If the graph is directed.
    """
    _require_undirected(graph, "edges_connected")

    # Only vertices with at least one edge matter: an isolated vertex never
    # has to be visited by a walk along the edges.
    active = [v for v in graph.vertices() if graph.degree(v) > 0]
    if not active:
        return True  # no edges - there is nothing to connect

    # A small depth-first search (with a stack) from the first active vertex.
    seen = {active[0]}
    stack = [active[0]]
    while stack:
        u = stack.pop()
        for w in graph.neighbors(u):
            if w not in seen:
                seen.add(w)
                stack.append(w)

    # Connected (on the edges) <=> the search reached every active vertex.
    return all(v in seen for v in active)


def has_euler_circuit(graph: Graph) -> bool:
    """Return ``True`` if the undirected graph has an Euler circuit.

    Theorem (Euler 1736, Hierholzer 1873): an Euler circuit exists exactly
    if all edges lie in one component and every vertex has even degree.

    Raises:
        ValueError: If the graph is directed.
    """
    _require_undirected(graph, "has_euler_circuit")
    # Both conditions are necessary, and together they are sufficient.
    return edges_connected(graph) and len(_odd_degree_vertices(graph)) == 0


def has_euler_trail(graph: Graph) -> bool:
    """Return ``True`` if the undirected graph has an Euler trail (open or closed).

    Theorem: an Euler trail exists exactly if all edges lie in one component
    and the number of odd-degree vertices is 0 (closed trail = circuit) or
    2 (open trail between the two odd vertices).

    Raises:
        ValueError: If the graph is directed.
    """
    _require_undirected(graph, "has_euler_trail")
    # By the handshake lemma the number of odd vertices is always even,
    # so "0 or 2" is the same as "at most 2".
    return edges_connected(graph) and len(_odd_degree_vertices(graph)) in (0, 2)


def _hierholzer(graph: Graph, start: Vertex) -> list[Vertex]:
    """Return an Euler trail starting at ``start`` (Hierholzer's algorithm).

    Precondition: ``graph`` has an Euler trail that may start at ``start``
    (all degrees even, or ``start`` is one of the two odd vertices).

    Idea: walk along unused edges until you get stuck. The stack holds the
    walk we are currently on. When the top vertex has no unused edge left,
    it cannot be part of any further detour, so it is final: we move it to
    the result. If a vertex deeper in the stack still has unused edges, the
    loop automatically starts a new sub-tour from there - this is exactly
    the "splice in another closed walk" step of the proof.
    """
    remaining = graph.copy()  # we delete used edges - never in the input!
    stack = [start]
    walk: list[Vertex] = []
    while stack:
        v = stack[-1]
        neighbours = remaining.neighbors(v)
        if neighbours:
            # Walk on along an unused edge and delete it.
            w = neighbours[0]
            remaining.remove_edge(v, w)
            stack.append(w)
        else:
            # Stuck at v: v is the next vertex of the result (from the end).
            walk.append(stack.pop())
    walk.reverse()  # the vertices were collected from the end of the walk
    return walk


def find_euler_circuit(graph: Graph) -> list[Vertex] | None:
    """OPTIONAL: Return an Euler circuit ``[v0, ..., v0]`` or ``None``.

    Graphs without edges give ``[]``. The input is not modified.

    Raises:
        ValueError: If the graph is directed.
    """
    _require_undirected(graph, "find_euler_circuit")
    if graph.num_edges() == 0:
        return []
    if not has_euler_circuit(graph):
        return None
    # Any vertex with an edge can be the start of an Euler circuit.
    start = next(v for v in graph.vertices() if graph.degree(v) > 0)
    return _hierholzer(graph, start)


def find_euler_trail(graph: Graph) -> list[Vertex] | None:
    """OPTIONAL: Return an Euler trail (open or closed) or ``None``.

    If there are two odd vertices, the trail starts at one and ends at the
    other. Graphs without edges give ``[]``. The input is not modified.

    Raises:
        ValueError: If the graph is directed.
    """
    _require_undirected(graph, "find_euler_trail")
    if graph.num_edges() == 0:
        return []
    if not has_euler_trail(graph):
        return None
    odd = _odd_degree_vertices(graph)
    if odd:
        # An open Euler trail must start (and end) at an odd vertex: every
        # other vertex is left as often as it is entered.
        start = odd[0]
    else:
        start = next(v for v in graph.vertices() if graph.degree(v) > 0)
    return _hierholzer(graph, start)


def find_hamiltonian_cycle(graph: Graph) -> list[Vertex] | None:
    """OPTIONAL: Return a Hamiltonian cycle ``[v0, ..., v0]`` or ``None``.

    Naive backtracking: extend a path vertex by vertex in every possible
    way. Runtime up to O(n!) - only for small graphs. Graphs with fewer than
    3 vertices give ``None``. The input is not modified.

    Raises:
        ValueError: If the graph is directed.
    """
    _require_undirected(graph, "find_hamiltonian_cycle")
    vertices = graph.vertices()
    n = len(vertices)
    if n < 3:
        return None  # a cycle in a simple graph needs at least 3 vertices

    # Every Hamiltonian cycle passes through every vertex, so we may fix
    # the start vertex.
    start = vertices[0]
    path = [start]
    on_path = {start}

    def extend() -> bool:
        """Try to complete ``path``; return True on success."""
        if len(path) == n:
            # All vertices used: we only have to get back to the start.
            return graph.has_edge(path[-1], start)
        for w in graph.neighbors(path[-1]):
            if w not in on_path:
                path.append(w)
                on_path.add(w)
                if extend():
                    return True
                # Dead end: undo the last step and try the next neighbour.
                path.pop()
                on_path.remove(w)
        return False

    if extend():
        return path + [start]
    return None


if __name__ == "__main__":
    # Königsberg as a simple graph: every bridge becomes a vertex of degree 2
    # (subdivision). This changes neither the degrees of the land masses nor
    # the Euler property.
    koenigsberg = Graph()
    for bridge, bank1, bank2 in KOENIGSBERG_BRIDGES:
        koenigsberg.add_edge(bank1, bridge)
        koenigsberg.add_edge(bridge, bank2)
    print("Königsberg")
    for land in ["Insel", "Nord", "Süd", "Ost"]:
        print(f"  degree of {land}: {koenigsberg.degree(land)}")
    print("  Euler circuit:", has_euler_circuit(koenigsberg))
    print("  Euler trail:  ", has_euler_trail(koenigsberg))
    print()

    nikolaus = Graph.from_edges(NIKOLAUS_EDGES)
    print("Haus vom Nikolaus")
    print("  Euler circuit:", has_euler_circuit(nikolaus))
    print("  Euler trail:  ", format_path(find_euler_trail(nikolaus), directed=False))
    print()

    lonneberga = small_weighted_graph()
    print("Michel walks every path around Lönneberga once:")
    print("  ", format_path(find_euler_trail(lonneberga), directed=False))
    print()

    for n in range(2, 7):
        print(f"K_{n}: Euler circuit {has_euler_circuit(complete_graph(n))}")
    print("Euler circuit of K_5:", format_path(find_euler_circuit(complete_graph(5)), directed=False))
    print()

    print("Hamiltonian cycle of the Nikolaus house:", format_path(find_hamiltonian_cycle(nikolaus), directed=False))
    # The Petersen graph is 3-regular and connected, but has no Hamiltonian
    # cycle - the backtracking search tries everything and returns None.
    print("Hamiltonian cycle of the Petersen graph:", find_hamiltonian_cycle(petersen_graph()))

    # Pictures in the browser (no extra packages needed).
    # Königsberg like on a map: land masses and bridges (as extra vertices).
    city_map = {
        "Nord": (0.5, 2.2), "Insel": (0, 0), "Süd": (0.5, -2.2), "Ost": (3.2, 0),
        "b1": (-0.6, 1.1), "b2": (0.6, 1.1), "b3": (-0.6, -1.1), "b4": (0.6, -1.1),
        "b5": (1.6, 0), "b6": (2.1, 1.3), "b7": (2.1, -1.3),
    }
    land = ["Insel", "Nord", "Süd", "Ost"]
    # The Nikolaus house drawn without lifting the pen: edges numbered in trail order.
    house = {1: (0, 0), 2: (2, 0), 3: (0, 2), 4: (2, 2), 5: (1, 3.3)}
    trail = find_euler_trail(nikolaus) or []
    trail_edges = list(zip(trail, trail[1:]))
    show(
        snapshot(
            koenigsberg,
            "Königsberg: all four land masses have odd degree",
            layout=city_map,
            vertex_colors={v: "land" if v in land else "bridge" for v in koenigsberg.vertices()},
            highlight_vertices=land,
            vertex_labels={v: f"deg {koenigsberg.degree(v)}" for v in land},
        ),
        snapshot(
            nikolaus,
            "Das ist das Haus vom Ni-ko-laus",
            layout=house,
            highlight_edges=trail_edges,
            edge_labels={edge: i + 1 for i, edge in enumerate(trail_edges)},
            vertex_flags={trail[0]: ["start"], trail[-1]: ["target"]},
            message=f"Euler trail: {format_path(trail, directed=False)}",
        ),
        snapshot(
            petersen_graph(),
            "Petersen graph: 3-regular, connected, no Hamiltonian cycle",
            shells=[range(5), range(5, 10)],
        ),
        title="Unit 5: results",
    )
    print("Step by step: python exercises/05_euler_hamilton/demo_animation.py")
