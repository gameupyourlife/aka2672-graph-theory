"""Unit 6: Graph colouring - STEP-BY-STEP ANIMATION.

The functions below are the algorithms of ``demo_solution.py`` with
additional calls of a :class:`~lib.trace.Trace`. Every ``trace.step(...)``
records one picture; the browser player then lets you step forwards and
backwards through the run or play it automatically.

Run it with ``python exercises/06_graph_coloring/demo_animation.py``.

How to animate your own algorithm: see docs/visualisierung.md.
"""

import sys
from collections import deque
from collections.abc import Sequence
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))  # find ``lib``

from lib.generators import cycle_graph, grid_graph
from lib.graph import Graph, Vertex
from lib.trace import Trace, format_value
from lib.utils import load_module_from_path
from lib.viewer import show

# The party data comes from the demo solution.
solution = load_module_from_path(Path(__file__).with_name("demo_solution.py"))

GREEDY_PSEUDOCODE = [
    "for each vertex v in the order:",
    "    used = colours of the already coloured neighbours of v",
    "    c = smallest colour that is not in used",
    "    colour v with c",
]

BIPARTITE_PSEUDOCODE = [
    "for each vertex s without a side:",
    "    side[s] = 0;  Q = [s]",
    "    while Q is not empty:",
    "        u = Q.popleft()",
    "        for each neighbour w of u:",
    "            if w has no side: side[w] = 1 - side[u];  Q.append(w)",
    "            elif side[w] == side[u]: not bipartite (odd cycle)",
    "bipartite",
]


def party_graph() -> Graph:
    """Return Pippi's party: guests and the pairs who must not share a table."""
    graph = Graph()
    graph.add_vertices(solution.PARTY_GUESTS)
    graph.add_edges(solution.PARTY_CONFLICTS)
    return graph


def crown_graph(n: int) -> Graph:
    """Return the crown graph: ``("a", i) -- ("b", j)`` for all ``i != j``."""
    graph = Graph()
    graph.add_vertices([("a", i) for i in range(n)] + [("b", i) for i in range(n)])
    for i in range(n):
        for j in range(n):
            if i != j:
                graph.add_edge(("a", i), ("b", j))
    return graph


def trace_greedy_coloring(
    graph: Graph, order: Sequence[Vertex] | None = None, title: str = "Greedy colouring", **options: object
) -> Trace:
    """Colour the vertices greedily in ``order`` and record every step.

    The label below a vertex is its place in the order. ``current`` = the
    vertex being coloured (its fill shows the new colour), ``current``
    edges lead to its already coloured neighbours; ``trace.color`` holds the
    colouring. ``options`` are passed to :class:`Trace`.

    Raises:
        ValueError: If ``order`` is not a permutation of the vertices.
    """
    if order is None:
        order = graph.vertices()
    if len(order) != graph.num_vertices() or set(order) != set(graph.vertices()):
        raise ValueError("order must contain every vertex exactly once")
    trace = Trace(
        graph,
        title,
        description="Colour the vertices one after the other; every vertex takes the smallest colour "
        "that none of its already coloured neighbours has. The result depends on the order.",
        pseudocode=GREEDY_PSEUDOCODE,
        **options,  # type: ignore[arg-type]
    )
    # The current vertex keeps the fill of its colour class; the halo marks it.
    trace.style("current", fill=None, description="current vertex / edges to its coloured neighbours")
    for i, v in enumerate(order):
        trace.label(v, f"#{i + 1}")
    trace.variable("order", list(order))
    trace.step("The number below a vertex is its place in the order.", line=1)

    coloring: dict[Vertex, int] = {}
    for v in order:
        # Colours of the already coloured neighbours (later ones do not count yet).
        coloured_neighbours = [w for w in graph.neighbors(v) if w in coloring]
        used = {coloring[w] for w in coloured_neighbours}
        color = 0
        while color in used:
            color += 1
        coloring[v] = color
        trace.current(v)
        trace.flag_only_edges("current", [(v, w) for w in coloured_neighbours])
        trace.color(v, color)
        trace.variable("v", v)
        trace.variable("used", used)
        trace.variable("colours so far", len(set(coloring.values())))
        if used:
            trace.step(f"{format_value(v)}: neighbours use {format_set(used)}: take {color}.", line=4)
        else:
            trace.step(f"{format_value(v)}: no coloured neighbour yet: take {color}.", line=4)

    trace.current(None)
    trace.current_edge(None)
    trace.remove_variable("v")
    trace.remove_variable("used")
    count = len(set(coloring.values()))
    trace.step(f"Done: {count} colours (maximum degree + 1 = "
               f"{max((graph.degree(v) for v in graph.vertices()), default=0) + 1}).")
    return trace


def trace_bipartite_check(graph: Graph, title: str = "Bipartite check", **options: object) -> Trace:
    """Try to 2-colour the graph with a BFS per component and record every step.

    Colour classes 0 and 1 are the two sides. Flags: ``queued`` = in the
    queue, ``current`` = vertex / edge being processed, ``tree`` = BFS tree
    edge (the side of a vertex is forced along it), ``conflict`` = edge
    with two equal sides and its end vertices, ``path`` = the odd cycle
    that this edge closes. ``options`` are passed to :class:`Trace`.
    """
    trace = Trace(
        graph,
        title,
        description="A graph is bipartite (2-colourable) exactly if it has no odd cycle. In every "
        "component, a BFS gives each vertex the side 'distance from the start modulo 2'; "
        "an edge inside one side closes an odd cycle.",
        pseudocode=BIPARTITE_PSEUDOCODE,
        **options,  # type: ignore[arg-type]
    )
    # Keep the colour of the side visible under the flags.
    trace.style("current", fill=None)
    trace.style("queued", fill=None)
    trace.style("conflict", fill=None, description="conflict: both ends on the same side")
    trace.style("path", description="odd cycle")

    side: dict[Vertex, int] = {}
    parent: dict[Vertex, Vertex | None] = {}
    components = 0
    for start in graph.vertices():
        if start in side:
            continue  # this component has already been coloured
        components += 1
        side[start] = 0
        parent[start] = None
        queue = deque([start])
        trace.color(start, 0)
        trace.flag(start, "queued")
        trace.current(None)
        trace.current_edge(None)
        trace.variable("Q", queue)
        trace.remove_variable("u")
        s_name = format_value(start)
        trace.step(f"{s_name} has no side yet: new component {components}, {s_name} gets side 0.", line=2)
        while queue:
            u = queue.popleft()
            trace.unflag(u, "queued")
            trace.current(u)
            trace.current_edge(None)
            trace.variable("Q", queue)
            trace.variable("u", u)
            u_name = format_value(u)
            trace.step(f"Take {u_name} (side {side[u]}) from the queue.", line=4)
            for w in graph.neighbors(u):
                w_name = format_value(w)
                trace.current_edge(u, w)
                if w not in side:
                    # The side of w is forced: the opposite of u.
                    side[w] = 1 - side[u]
                    parent[w] = u
                    queue.append(w)
                    trace.color(w, side[w])
                    trace.flag(w, "queued")
                    trace.flag_edge(u, w, "tree")
                    trace.variable("Q", queue)
                    trace.step(f"{w_name} is new: it must get the other side {side[w]}. Append it to Q.", line=6)
                elif side[w] == side[u]:
                    # An edge inside one side: walk up the BFS tree to find the odd cycle.
                    trace.flag(u, "conflict")
                    trace.flag(w, "conflict")
                    trace.flag_edge(u, w, "conflict")
                    trace.step(f"Edge {u_name} - {w_name} joins two vertices of side {side[u]}: conflict!", line=7)
                    cycle = _odd_cycle(parent, u, w)
                    trace.current(None)
                    trace.current_edge(None)
                    trace.flag_path(cycle)
                    trace.variable("odd cycle", cycle)
                    trace.step(f"Not bipartite: the tree paths to {u_name} and {w_name} plus the edge "
                               f"{u_name} - {w_name} form an odd cycle with {len(cycle) - 1} edges.", line=7)
                    return trace
                elif w == parent[u]:
                    trace.step(f"{w_name} is the BFS parent of {u_name}: other side, fine.", line=5)
                else:
                    trace.step(f"{w_name} already has the other side {side[w]}: fine.", line=5)
        trace.current(None)

    trace.current(None)
    trace.current_edge(None)
    trace.remove_variable("u")
    trace.step(f"No conflict in {components} component(s): the graph is bipartite, the two colours "
               "are the two sides.", line=8)
    return trace


def _odd_cycle(parent: dict[Vertex, Vertex | None], u: Vertex, w: Vertex) -> list[Vertex]:
    """Return the odd cycle closed by the edge ``u - w`` (as in ``find_odd_cycle``).

    ``u`` and ``w`` have the same BFS depth, so we walk up the BFS tree from
    both in parallel until the two paths meet.
    """
    from_u = [u]
    from_w = [w]
    while from_u[-1] != from_w[-1]:
        from_u.append(parent[from_u[-1]])  # type: ignore[arg-type]
        from_w.append(parent[from_w[-1]])  # type: ignore[arg-type]
    return from_u + from_w[-2::-1] + [u]


def format_set(values: set[int]) -> str:
    """Return ``{0, 2}`` for a set of colours (sorted)."""
    return "{" + ", ".join(str(x) for x in sorted(values)) + "}"


def main() -> None:
    """Show all animations of this unit on one page."""
    n = 5
    crown = crown_graph(n)
    a_side = [("a", i) for i in range(n)]
    sides = a_side + [("b", i) for i in range(n)]
    alternating = [vertex for i in range(n) for vertex in (("a", i), ("b", i))]
    show(
        trace_greedy_coloring(party_graph(), title="Greedy: Pippi's party"),
        trace_greedy_coloring(crown, alternating, title="Greedy: crown, alternating order", left=a_side),
        trace_greedy_coloring(crown, sides, title="Greedy: crown, one side first", left=a_side),
        trace_bipartite_check(grid_graph(3, 4), title="Bipartite check: 3 x 4 grid"),
        trace_bipartite_check(cycle_graph(7), title="Bipartite check: C_7", layout="circular"),
        trace_bipartite_check(party_graph(), title="Bipartite check: Pippi's party"),
        title="Unit 6: Graph colouring",
    )


if __name__ == "__main__":
    main()
