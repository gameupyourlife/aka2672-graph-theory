"""Unit 2: Breadth-first search and depth-first search - STEP-BY-STEP ANIMATION.

The functions below are the algorithms of ``demo_solution.py`` with
additional calls of a :class:`~lib.trace.Trace`. Every ``trace.step(...)``
records one picture; the browser player then lets you step forwards and
backwards through the run or play it automatically.

Run it with ``python exercises/02_bfs_dfs/demo_animation.py``.

How to animate your own algorithm: see docs/visualisierung.md.
"""

import sys
from collections import deque
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))  # find ``lib``

from lib.generators import grid_graph, random_graph
from lib.graph import Graph, Vertex
from lib.trace import Trace
from lib.viewer import show

BFS_PSEUDOCODE = [
    "mark s;  d[s] = 0;  Q = [s]",
    "while Q is not empty:",
    "    u = Q.popleft()",
    "    for each neighbour w of u:",
    "        if w is marked: continue",
    "        mark w;  d[w] = d[u] + 1;  parent[w] = u",
    "        Q.append(w)",
    "    u is finished",
]

DFS_PSEUDOCODE = [
    "S = [s]",
    "while S is not empty:",
    "    u = S.pop()",
    "    if u is visited: continue",
    "    visit u",
    "    for each neighbour w of u:",
    "        if w is not visited: S.append(w)",
]


def trace_bfs(graph: Graph, start: Vertex, **options: object) -> Trace:
    """Run a breadth-first search from ``start`` and record every step.

    Flags: ``queued`` = in the queue, ``current`` = being processed,
    ``visited`` = finished, ``tree`` = edge of the BFS tree.
    ``options`` are passed to :class:`Trace` (e.g. ``layout``).
    """
    trace = Trace(
        graph,
        f"BFS from {start}",
        description="Breadth-first search uses a queue (first in, first out). "
        "It reaches the vertices in the order of their distance d from the start.",
        pseudocode=BFS_PSEUDOCODE,
        **options,  # type: ignore[arg-type]
    )
    distance = {start: 0}
    queue = deque([start])
    trace.flag(start, "start", "queued")
    trace.label(start, "d = 0")
    trace.variable("Q", queue)
    trace.step(f"Start: {start} gets distance 0 and goes into the queue.", line=1)

    while queue:
        u = queue.popleft()
        trace.current(u)
        trace.unflag(u, "queued")
        trace.variable("Q", queue)
        trace.variable("u", u)
        trace.step(f"Take {u} from the front of the queue.", line=3)
        for w in graph.neighbors(u):
            trace.current_edge(u, w)
            if w in distance:
                trace.step(f"{w} is already marked - nothing to do.", line=5)
                continue
            distance[w] = distance[u] + 1
            queue.append(w)
            trace.flag(w, "queued")
            trace.flag_edge(u, w, "tree")
            trace.label(w, f"d = {distance[w]}")
            trace.variable("Q", queue)
            trace.step(f"{w} is new: d[{w}] = {distance[w]}, parent {u}. Append {w} to the queue.", line=7)
        trace.current_edge(None)
        trace.flag(u, "visited")
        trace.step(f"All neighbours of {u} are done.", line=8)

    trace.current(None)
    trace.remove_variable("u")
    trace.step(f"The queue is empty: {len(distance)} vertices reached. The green edges form the BFS tree.")
    return trace


def trace_dfs(graph: Graph, start: Vertex, **options: object) -> Trace:
    """Run an iterative depth-first search from ``start`` and record every step.

    The stack stores pairs (vertex, parent), so that the edges of the DFS
    tree can be shown. The number below a vertex is its visiting order.
    """
    trace = Trace(
        graph,
        f"DFS from {start}",
        description="Depth-first search uses a stack (last in, first out). "
        "It goes as deep as possible before it goes back.",
        pseudocode=DFS_PSEUDOCODE,
        **options,  # type: ignore[arg-type]
    )
    visited: set[Vertex] = set()
    order: list[Vertex] = []
    stack: list[tuple[Vertex, Vertex | None]] = [(start, None)]
    trace.flag(start, "start", "queued")
    trace.variable("S", [v for v, _ in stack])
    trace.step(f"Start: put {start} on the stack.", line=1)

    while stack:
        u, parent = stack.pop()
        trace.variable("S", [v for v, _ in stack])
        trace.current(u)
        if u in visited:
            trace.step(f"{u} was visited already - skip it.", line=4)
            continue
        visited.add(u)
        order.append(u)
        if not any(v == u for v, _ in stack):
            trace.unflag(u, "queued")
        trace.flag(u, "visited")
        trace.label(u, f"#{len(order)}")
        if parent is not None:
            trace.flag_edge(parent, u, "tree")
        trace.variable("order", order)
        trace.step(f"Visit {u} (number {len(order)}).", line=5)
        for w in graph.neighbors(u):
            if w not in visited:
                stack.append((w, u))
                trace.flag(w, "queued")
                trace.current_edge(u, w)
                trace.variable("S", [v for v, _ in stack])
                trace.step(f"Push {w} onto the stack.", line=7)
        trace.current_edge(None)

    trace.current(None)
    trace.step(f"The stack is empty. Visiting order: {', '.join(map(str, order))}.")
    return trace


def trace_components(graph: Graph, **options: object) -> Trace:
    """Find the connected components; each component gets its own colour."""
    trace = Trace(
        graph,
        "Connected components",
        description="Start a search from every vertex that has no colour yet. "
        "Everything the search reaches belongs to the same component.",
        **options,  # type: ignore[arg-type]
    )
    component_of: dict[Vertex, int] = {}
    for s in graph.vertices():
        if s in component_of:
            continue
        number = len(set(component_of.values()))
        trace.current(s)
        trace.step(f"{s} has no colour yet: start component {number}.")
        stack = [s]
        component_of[s] = number
        while stack:
            u = stack.pop()
            trace.color(u, number)
            for w in graph.neighbors(u):
                if w not in component_of:
                    component_of[w] = number
                    stack.append(w)
            trace.current(u)
            trace.step(f"{u} belongs to component {number}.")
    trace.current(None)
    count = len(set(component_of.values()))
    trace.step(f"Done: {count} connected components.")
    return trace


def main() -> None:
    """Show all animations of this unit on one page."""
    example = Graph.from_edges([("A", "B"), ("A", "C"), ("B", "D"), ("C", "D"), ("D", "E"), ("C", "F"), ("F", "E")])
    show(
        trace_bfs(example, "A"),
        trace_dfs(example, "A"),
        trace_bfs(grid_graph(4, 6), (0, 0)),
        trace_components(random_graph(16, 0.1, seed=3)),
        title="Unit 2: BFS and DFS",
    )


if __name__ == "__main__":
    main()
