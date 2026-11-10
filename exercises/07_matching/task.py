"""Einheit 7 – Bipartites Matching.

Bearbeite die TODOs direkt an den Funktionen. Ersetze dort jeweils
``raise NotImplementedError(...)`` durch deinen Code.

Starte die Tests im Projektordner mit diesem Befehl.

    python -m pytest exercises/07_matching
"""

import sys
from collections import deque  # you will need deque in find_augmenting_path()
from collections.abc import Iterable
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))  # find ``lib``

from lib.graph import Graph, Vertex
from lib.utils import format_path


def find_augmenting_path(
    graph: Graph, left_vertices: Iterable[Vertex], matching: dict[Vertex, Vertex]
) -> list[Vertex] | None:
    """Search an augmenting path for ``matching`` in the bipartite ``graph``.

    ``matching`` maps left vertices to right vertices. The input may be
    assumed to be valid (no checks needed).

    Returns:
        A list ``[l0, r0, l1, r1, ..., lk, rk]`` where ``l0`` is an unmatched
        left vertex, ``rk`` is an unmatched right vertex, the edges
        ``(l_i, r_i)`` are edges of the graph that are *not* in the matching
        and ``matching[l_{i+1}] == r_i``. No vertex appears twice. If there
        are several augmenting paths, any of them may be returned.
        ``None`` if there is no augmenting path.

    Write the breadth-first search here. It should visit each vertex at
    most once and leave both the graph and the matching unchanged.
    """
    # TODO: Step 1 - build matched_right = {right: left} from the matching.
    # TODO: Step 2 - put all unmatched left vertices into a deque and create
    #                an empty dict parent (right vertex -> left vertex).
    # TODO: Step 3 - BFS: take a left vertex l; for every neighbour r of l
    #                that is not matching.get(l) and not yet in parent:
    #                set parent[r] = l. If r is unmatched, go to step 4;
    #                otherwise append matched_right[r] to the queue.
    # TODO: Step 4 - build the path backwards: r, parent[r], the partner of
    #                that left vertex, ... until a left vertex has no partner.
    #                Reverse the list and return it.
    # TODO: Step 5 - queue empty: return None.
    raise NotImplementedError("TODO: find_augmenting_path")


def augment(matching: dict[Vertex, Vertex], path: list[Vertex]) -> dict[Vertex, Vertex]:
    """Return the matching ``matching`` "symmetric difference" ``path``.

    ``path`` is an augmenting path ``[l0, r0, l1, r1, ..., lk, rk]`` as
    returned by :func:`find_augmenting_path`. The result is a *new*
    dictionary (left -> right) with exactly one edge more than ``matching``.
    ``matching`` itself is not modified.

    Raises:
        ValueError: If ``path`` is empty or has an odd number of vertices.
    """
    # TODO: Step 1 - check the length of path (raise ValueError if invalid).
    # TODO: Step 2 - copy the matching.
    # TODO: Step 3 - for every even index i: new[path[i]] = path[i + 1].
    raise NotImplementedError("TODO: augment")


def maximum_bipartite_matching(
    graph: Graph, left_vertices: Iterable[Vertex]
) -> dict[Vertex, Vertex]:
    """Return a maximum matching of the bipartite ``graph``.

    The left side consists of ``left_vertices``; all other vertices of the
    graph form the right side. Use your augmenting-path search and aim for
    O(|V| * (|V| + |E|)) time.

    Returns:
        A dictionary ``left vertex -> right vertex`` that contains exactly
        the matched left vertices. If there are several maximum matchings,
        any of them may be returned.

    Raises:
        ValueError: If the graph is directed or if an edge has both end
            vertices on the same side.
        KeyError: If a left vertex is not a vertex of the graph.
    """
    # TODO: Step 1 - check the input (directed graph, unknown left vertices,
    #                edges inside one side). Materialize left_vertices once
    #                so you can use it repeatedly even if it is a generator.
    # TODO: Step 2 - start with the empty matching {}.
    # TODO: Step 3 - repeat: find an augmenting path; if there is none,
    #                return the matching; otherwise augment along it.
    raise NotImplementedError("TODO: maximum_bipartite_matching")


def minimum_vertex_cover(graph: Graph, left_vertices: Iterable[Vertex]) -> set[Vertex]:
    """OPTIONAL: Return a minimum vertex cover of the bipartite ``graph``.

    A vertex cover contains at least one end vertex of every edge. By
    König's theorem its minimum size equals the size of a maximum matching.

    Raises:
        Same errors as :func:`maximum_bipartite_matching`.
    """
    # TODO (optional): Find a maximum matching. Starting from every unmatched
    #                  left vertex, follow non-matching edges left to right and
    #                  matching edges right to left. Let Z be the reached
    #                  vertices and return (L - Z) | (R & Z).
    raise NotImplementedError("TODO (optional): minimum_vertex_cover")


def hall_violator(graph: Graph, left_vertices: Iterable[Vertex]) -> set[Vertex] | None:
    """OPTIONAL: Return a set S of left vertices with ``|N(S)| < |S|``.

    Returns ``None`` if there is a matching that covers all left vertices
    (then no such set exists by Hall's theorem).

    Raises:
        Same errors as :func:`maximum_bipartite_matching`.
    """
    # TODO (optional): Find a maximum matching. If it leaves any left vertices
    #                  unmatched, return the left vertices reached by the same
    #                  alternating search as in minimum_vertex_cover().
    raise NotImplementedError("TODO (optional): hall_violator")


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
    path = find_augmenting_path(villa, people, greedy)
    print("Augmenting path:", format_path(path, directed=False))
    print("After augmenting:", augment(greedy, path))
    print("Maximum matching:", maximum_bipartite_matching(villa, people))
