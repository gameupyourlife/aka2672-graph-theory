"""Unit 7: Bipartite matching - STEP-BY-STEP ANIMATION.

The function below is the augmenting-path algorithm of ``demo_solution.py``
with additional calls of a :class:`~lib.trace.Trace`. Every
``trace.step(...)`` records one picture; the browser player then lets you
step forwards and backwards through the run or play it automatically.

Run it with ``python exercises/07_matching/demo_animation.py``.

How to animate your own algorithm: see docs/visualisierung.md.
"""

import sys
from collections import deque
from collections.abc import Iterable
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))  # find ``lib``

from lib.generators import random_bipartite_graph
from lib.graph import Graph, Vertex
from lib.trace import Trace
from lib.utils import format_path
from lib.viewer import show

MATCHING_PSEUDOCODE = [
    "M = {}",
    "repeat:",
    "    Q = all free left vertices;  parent = {}",
    "    while Q is not empty:",
    "        l = Q.popleft()",
    "        for each neighbour r of l:",
    "            if l - r is in M or r is reached: continue",
    "            parent[r] = l",
    "            if r is free: augmenting path found (line 12)",
    "            Q.append(partner of r)",
    "    if no path was found: stop, M is maximum",
    "    flip the edges of the path:  |M| += 1",
]


def trace_matching(
    graph: Graph, left_vertices: Iterable[Vertex], title: str = "Maximum matching", **options: object
) -> Trace:
    """Find a maximum matching with augmenting paths and record every step.

    Flags: ``matched`` = edge of the current matching, ``queued`` = left
    vertex in the queue, ``current`` = vertex / edge being processed,
    ``visited`` = vertex reached by the alternating search, ``tree`` = edge
    over which a right vertex was reached, ``path`` = the augmenting path
    (its edges are numbered), ``conflict`` / ``highlight`` = a set S that
    violates Hall's condition and its neighbourhood N(S).
    Free vertices are labelled "free". ``options`` are passed to
    :class:`Trace` (default: bipartite layout with ``left_vertices`` on the left).
    """
    left = list(left_vertices)
    options.setdefault("left", left)
    trace = Trace(
        graph,
        title,
        description="An augmenting path starts and ends at free vertices and alternates between "
        "edges outside and inside the matching M. Flipping its edges gives one matching edge more. "
        "Berge: M is maximum if and only if there is no augmenting path.",
        pseudocode=MATCHING_PSEUDOCODE,
        **options,  # type: ignore[arg-type]
    )
    matching: dict[Vertex, Vertex] = {}

    def show_matching() -> None:
        """Flag the matching edges, label the free vertices, update the variables."""
        trace.flag_only_edges("matched", list(matching.items()))
        matched = set(matching) | set(matching.values())
        for v in graph.vertices():
            trace.label(v, None if v in matched else "free")
        trace.variable("M", matching)
        trace.variable("|M|", len(matching))

    show_matching()
    trace.step("Start with the empty matching M: every vertex is free.", line=1)

    round_number = 0
    reached_left: set[Vertex] = set()
    while True:
        round_number += 1
        matched_right = {r: l for l, r in matching.items()}
        queue = deque(l for l in left if l not in matching)
        parent: dict[Vertex, Vertex] = {}
        reached_left = set(queue)
        trace.clear("path", "visited", "tree")
        for u, v, _ in graph.edges():
            trace.edge_label(u, v, None)
        for l in queue:
            trace.flag(l, "queued")
        trace.variable("Q", queue)
        trace.variable("parent", parent)
        trace.remove_variable("path")
        trace.step(
            f"Round {round_number}: search alternating paths from all free left vertices at once.", line=3
        )

        path: list[Vertex] | None = None
        while queue and path is None:
            l = queue.popleft()
            trace.current(l)
            trace.unflag(l, "queued")
            trace.variable("Q", queue)
            trace.step(f"Take {l} from the queue.", line=5)
            for r in graph.neighbors(l):
                trace.current_edge(l, r)
                if r == matching.get(l):
                    trace.step(f"{l} - {r} is a matching edge: from the left only edges outside M are used.", line=7)
                    continue
                if r in parent:
                    trace.step(f"{r} was reached already - skip it.", line=7)
                    continue
                parent[r] = l
                trace.flag(r, "visited")
                trace.flag_edge(l, r, "tree")
                trace.variable("parent", parent)
                if r not in matched_right:
                    path = _build_path(parent, matching, r)
                    trace.step(f"{r} is free: an augmenting path ends here!", line=9)
                    break
                partner = matched_right[r]
                queue.append(partner)
                reached_left.add(partner)
                trace.flag(partner, "queued")
                trace.variable("Q", queue)
                trace.step(
                    f"{r} is matched to {partner}: the path must continue along the matching edge, "
                    f"so {partner} joins the queue.",
                    line=10,
                )
            trace.current_edge(None)
            trace.flag(l, "visited")

        trace.current(None)
        if path is None:
            trace.step(
                "The queue is empty and no free right vertex was reached: there is no augmenting path. "
                "By Berge's theorem M is maximum.",
                line=11,
            )
            break

        # Show the augmenting path with numbered edges.
        trace.clear("queued", "visited", "tree")
        trace.flag_path(path)
        edges = list(zip(path, path[1:]))
        for i, (u, v) in enumerate(edges):
            trace.edge_label(u, v, i + 1)
        trace.variable("path", path)
        trace.remove_variable("Q")
        in_matching = [str(i + 1) for i in range(1, len(edges), 2)]
        if not in_matching:
            which = "no edge is in M yet."
        elif len(in_matching) == 1:
            which = f"edge {in_matching[0]} is in M."
        else:
            which = f"edges {', '.join(in_matching)} are in M."
        trace.step(
            f"Augmenting path {format_path(path, directed=False)}: from free to free, alternating; {which}",
            line=9,
        )

        # Augment: every left vertex path[i] gets the new partner path[i + 1].
        for i in range(0, len(path), 2):
            matching[path[i]] = path[i + 1]
        trace.clear("path")
        show_matching()
        trace.step(
            f"Flip the edges: matching edges on the path leave the matching, the others join it: +1, "
            f"so |M| = {len(matching)}.",
            line=12,
        )

    # Summary.
    trace.clear("queued", "visited", "tree")
    trace.remove_variable("Q")
    trace.remove_variable("parent")
    right = [v for v in graph.vertices() if v not in set(left)]
    if 2 * len(matching) == graph.num_vertices():
        result = "it is perfect: every vertex is matched."
    elif len(matching) == len(left):
        result = "every left vertex is matched."
    else:
        result = f"left vertices without a partner: {len(left) - len(matching)} of {len(left)}."
    trace.step(f"Maximum matching with {len(matching)} edges ({len(left)} left, {len(right)} right vertices): {result}")

    if len(matching) < len(left):
        # The last (failed) search reached the set S of left vertices; all
        # their neighbours were reached too and are matched into S.
        violator = sorted(reached_left, key=left.index)
        neighbours = {r for l in violator for r in graph.neighbors(l)}
        for v in violator:
            trace.flag(v, "conflict")
        for r in neighbours:
            trace.flag(r, "highlight")
        trace.variable("S", violator)
        trace.variable("N(S)", neighbours)
        trace.step(
            f"Hall's condition fails: S = {{{', '.join(map(str, violator))}}} has |N(S)| = {len(neighbours)} "
            f"< |S| = {len(violator)}, so S cannot be matched completely."
        )
    return trace


def _build_path(parent: dict[Vertex, Vertex], matching: dict[Vertex, Vertex], end: Vertex) -> list[Vertex]:
    """Follow the parent pointers back from the free right vertex ``end``."""
    path: list[Vertex] = []
    r: Vertex | None = end
    while r is not None:
        l = parent[r]
        path.append(r)
        path.append(l)
        r = matching.get(l)  # the previous right vertex on the path
    path.reverse()
    return path


def main() -> None:
    """Show all animations of this unit on one page."""
    villa = Graph.from_edges(
        [
            ("Pippi", "Pferd"),
            ("Pippi", "Pfannkuchen"),
            ("Tommy", "Pfannkuchen"),
            ("Tommy", "Garten"),
            ("Annika", "Garten"),
            ("Annika", "Einkauf"),
            ("Kling", "Pferd"),
        ]
    )
    # Three children, but Tommy and Annika both only want to ride the horse.
    horses = Graph.from_edges([("Pippi", "Pferd"), ("Pippi", "Garten"), ("Tommy", "Pferd"), ("Annika", "Pferd")])
    show(
        trace_matching(villa, ["Pippi", "Tommy", "Annika", "Kling"], "Villa Kunterbunt"),
        trace_matching(horses, ["Pippi", "Tommy", "Annika"], "Horses: Hall's condition fails"),
        trace_matching(
            random_bipartite_graph(7, 7, 0.25, seed=1), [f"L{i}" for i in range(7)], "Random bipartite graph"
        ),
        title="Unit 7: Bipartite matching",
    )


if __name__ == "__main__":
    main()
