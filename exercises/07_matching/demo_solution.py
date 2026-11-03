"""Unit 7: Bipartite matching - DEMO SOLUTION.

The whole unit rests on Berge's theorem (1957):

    A matching M is maximum  <=>  there is no M-augmenting path.

An augmenting path starts and ends at unmatched vertices and alternates
between edges outside and inside M. Swapping the roles of its edges
("symmetric difference") gives a matching with one edge more. So we

1. start with the empty matching,
2. search an augmenting path (a BFS whose direction is dictated by M),
3. augment along it, and repeat until no augmenting path exists.

In a bipartite graph an augmenting path always goes
left -> right (edge not in M) -> left (edge in M) -> right -> ...
which makes the search a simple breadth-first search.

Runtime: at most |V|/2 augmentations, each search costs O(|V| + |E|),
in total O(|V| * (|V| + |E|)).

Run it with ``python exercises/07_matching/demo_solution.py``.
"""

import sys
from collections import deque
from collections.abc import Iterable
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))  # find ``lib``

from lib.graph import Graph, Vertex
from lib.utils import format_path
from lib.visualization import show, snapshot


def find_augmenting_path(
    graph: Graph, left_vertices: Iterable[Vertex], matching: dict[Vertex, Vertex]
) -> list[Vertex] | None:
    """Search an augmenting path ``[l0, r0, ..., lk, rk]`` for ``matching``.

    Returns ``None`` if there is no augmenting path. ``matching`` (left ->
    right) is not modified.
    """
    # The matching stores left -> right; for the way back we need right -> left.
    matched_right = {r: l for l, r in matching.items()}

    # We start the search at ALL unmatched left vertices at the same time.
    queue = deque(l for l in left_vertices if l not in matching)
    # parent[r] = the left vertex from which the right vertex r was reached.
    parent: dict[Vertex, Vertex] = {}

    while queue:
        l = queue.popleft()
        for r in graph.neighbors(l):
            # From the left we may only use edges that are NOT in the matching,
            # and we visit every right vertex at most once.
            if r == matching.get(l) or r in parent:
                continue
            parent[r] = l
            if r not in matched_right:
                # r is unmatched: we have found an augmenting path.
                return _build_path(parent, matching, r)
            # r is matched: the path must continue along the matching edge
            # r -- matched_right[r] back to the left side.
            queue.append(matched_right[r])
    return None  # no unmatched right vertex is reachable


def _build_path(
    parent: dict[Vertex, Vertex], matching: dict[Vertex, Vertex], end: Vertex
) -> list[Vertex]:
    """Follow the parent pointers back from the unmatched right vertex ``end``."""
    path: list[Vertex] = []
    r: Vertex | None = end
    while r is not None:
        l = parent[r]
        path.append(r)
        path.append(l)
        # The previous right vertex on the path is the partner of l.
        # For the unmatched start vertex there is none: then we are done.
        r = matching.get(l)
    path.reverse()  # we collected the path from the end
    return path


def augment(matching: dict[Vertex, Vertex], path: list[Vertex]) -> dict[Vertex, Vertex]:
    """Return a NEW matching: ``matching`` with the edges of ``path`` swapped.

    Raises:
        ValueError: If ``path`` is empty or has an odd number of vertices.
    """
    if len(path) == 0 or len(path) % 2 == 1:
        raise ValueError(f"An augmenting path has an even, positive length, got {path!r}")
    new = dict(matching)  # copy: the caller's matching stays unchanged
    # The pairs (path[0], path[1]), (path[2], path[3]), ... are the edges that
    # were NOT in the matching; they become matching edges now. The old
    # matching edges (path[1], path[2]), ... disappear automatically, because
    # every left vertex path[i] gets a new partner path[i + 1].
    for i in range(0, len(path), 2):
        new[path[i]] = path[i + 1]
    return new


def _check_bipartite_input(graph: Graph, left_vertices: Iterable[Vertex]) -> list[Vertex]:
    """Validate the input and return the left vertices as a list."""
    if graph.directed:
        raise ValueError("Matchings are defined for undirected graphs")
    left = list(left_vertices)
    left_set = set(left)
    for v in left:
        if v not in graph:
            raise KeyError(f"Left vertex {v!r} is not in the graph")
    for u, v, _ in graph.edges():
        # Exactly one end vertex must be on the left side.
        if (u in left_set) == (v in left_set):
            raise ValueError(f"The edge {u!r} - {v!r} does not connect the two sides")
    return left


def maximum_bipartite_matching(
    graph: Graph, left_vertices: Iterable[Vertex]
) -> dict[Vertex, Vertex]:
    """Return a maximum matching (left -> right) of the bipartite ``graph``.

    Raises:
        ValueError: If the graph is directed or an edge stays on one side.
        KeyError: If a left vertex is not a vertex of the graph.
    """
    left = _check_bipartite_input(graph, left_vertices)
    matching: dict[Vertex, Vertex] = {}
    while True:
        path = find_augmenting_path(graph, left, matching)
        if path is None:
            # Berge: no augmenting path means the matching is maximum.
            return matching
        matching = augment(matching, path)  # one edge more


def _alternating_reachable(
    graph: Graph, left: list[Vertex], matching: dict[Vertex, Vertex]
) -> set[Vertex]:
    """Return all vertices reachable from unmatched left vertices by alternating paths."""
    matched_right = {r: l for l, r in matching.items()}
    reached = {l for l in left if l not in matching}
    queue = deque(reached)
    while queue:
        l = queue.popleft()
        for r in graph.neighbors(l):
            if r == matching.get(l) or r in reached:
                continue
            reached.add(r)
            # For a maximum matching every reached right vertex is matched
            # (otherwise there would be an augmenting path).
            if r in matched_right:
                reached.add(matched_right[r])
                queue.append(matched_right[r])
    return reached


def minimum_vertex_cover(graph: Graph, left_vertices: Iterable[Vertex]) -> set[Vertex]:
    """OPTIONAL: Return a minimum vertex cover (König's theorem)."""
    left = _check_bipartite_input(graph, left_vertices)
    matching = maximum_bipartite_matching(graph, left)
    reached = _alternating_reachable(graph, left, matching)
    left_set = set(left)
    right_set = {v for v in graph.vertices() if v not in left_set}
    # Left vertices NOT reached and right vertices that WERE reached.
    # Every matching edge contributes exactly one of its end vertices.
    return (left_set - reached) | (right_set & reached)


def hall_violator(graph: Graph, left_vertices: Iterable[Vertex]) -> set[Vertex] | None:
    """OPTIONAL: Return S (left) with |N(S)| < |S|, or None if all of L can be matched."""
    left = _check_bipartite_input(graph, left_vertices)
    matching = maximum_bipartite_matching(graph, left)
    if len(matching) == len(set(left)):
        return None  # every left vertex is matched: Hall's condition holds
    reached = _alternating_reachable(graph, left, matching)
    # S = reached left vertices. N(S) = reached right vertices, and each of
    # them is matched to a different vertex of S. The unmatched left vertices
    # in S have no partner, so |N(S)| < |S|.
    return {v for v in left if v in reached}


if __name__ == "__main__":
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
    people = ["Pippi", "Tommy", "Annika", "Kling"]
    greedy = {"Pippi": "Pferd", "Tommy": "Pfannkuchen", "Annika": "Garten"}
    print("Greedy matching:  ", greedy)
    path = find_augmenting_path(villa, people, greedy)
    print("Augmenting path:  ", format_path(path, directed=False))
    print("After augmenting: ", augment(greedy, path))
    print("Maximum matching: ", maximum_bipartite_matching(villa, people))
    print("Min. vertex cover:", minimum_vertex_cover(villa, people))
    print()
    # Three children, but Tommy and Annika both only want to ride the horse.
    horses = Graph.from_edges([("Pippi", "Pferd"), ("Pippi", "Garten"), ("Tommy", "Pferd"), ("Annika", "Pferd")])
    children = ["Pippi", "Tommy", "Annika"]
    print("Maximum matching:", maximum_bipartite_matching(horses, children))
    print("Hall violator:   ", hall_violator(horses, children))

    # Pictures in the browser (no extra packages needed).
    bigger = augment(greedy, path) if path is not None else greedy
    violator = hall_violator(horses, children) or set()
    pictures = [
        snapshot(
            villa,
            f"Greedy matching: {len(greedy)} pairs",
            left=people,
            edge_flags={e: ["matched"] for e in greedy.items()},
        )
    ]
    if path is not None:
        pictures.append(
            snapshot(
                villa,
                "Augmenting path: alternates non-matching / matching edges",
                left=people,
                highlight_edges=list(zip(path, path[1:])),
                highlight_vertices=[path[0], path[-1]],
                edge_labels={edge: str(i + 1) for i, edge in enumerate(zip(path, path[1:]))},
            )
        )
    pictures.append(
        snapshot(
            villa,
            f"After augmenting: {len(bigger)} pairs (maximum)",
            left=people,
            edge_flags={e: ["matched"] for e in bigger.items()},
        )
    )
    pictures.append(
        snapshot(
            horses,
            f"Hall's condition fails for {sorted(violator)}",
            left=children,
            edge_flags={e: ["matched"] for e in maximum_bipartite_matching(horses, children).items()},
            vertex_flags={v: ["conflict"] for v in violator},
        )
    )
    show(*pictures, title="Unit 7: results")
    print("Step by step: python exercises/07_matching/demo_animation.py")
