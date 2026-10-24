"""Unit 8: Maximum flows - YOUR SOLUTION.

Read README.md in this folder first. Replace every
``raise NotImplementedError(...)`` by your own code.

Run the tests from the project root with::

    python -m pytest exercises/08_max_flow
"""

import sys
from collections import deque  # you will need deque in find_augmenting_path()
from collections.abc import Mapping
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))  # find ``lib``

from lib.graph import Graph, Vertex
from lib.utils import format_path


def residual_graph(graph: Graph, flow: Mapping[tuple[Vertex, Vertex], float]) -> Graph:
    """Return the residual network of ``flow`` in the directed ``graph``.

    The capacities are the edge weights of ``graph``; ``flow`` maps
    original edges ``(u, v)`` to their flow (missing key = flow 0).

    Returns:
        A new directed graph that contains all vertices of ``graph`` and an
        edge ``u -> v`` for every ordered pair with residual capacity
        ``(c(u, v) - f(u, v)) + f(v, u) > 0``; its weight is this residual
        capacity. Non-existing edges have capacity 0 and flow 0.

    ``graph`` and ``flow`` are not modified.
    """
    # TODO: Step 1 - create a new directed Graph with all vertices of graph.
    # TODO: Step 2 - collect every ordered pair (u, v) such that u -> v or
    #                v -> u is an edge of graph (each pair only once).
    # TODO: Step 3 - for every pair compute the residual capacity and add
    #                the edge u -> v if it is positive.
    raise NotImplementedError("TODO: residual_graph")


def find_augmenting_path(residual: Graph, source: Vertex, sink: Vertex) -> list[Vertex] | None:
    """Return a shortest path ``[source, ..., sink]`` (fewest edges) in ``residual``.

    Uses a breadth-first search. Returns ``[source]`` if ``source == sink``
    and ``None`` if ``sink`` cannot be reached.

    Raises:
        KeyError: If ``source`` or ``sink`` is not a vertex of ``residual``.
    """
    # TODO: Step 1 - check that source and sink are vertices (KeyError).
    # TODO: Step 2 - BFS from source with a deque and a parent dictionary.
    # TODO: Step 3 - if sink was reached, follow the parents back from sink,
    #                reverse the list and return it; otherwise return None.
    raise NotImplementedError("TODO: find_augmenting_path")


def edmonds_karp(
    graph: Graph, source: Vertex, sink: Vertex
) -> tuple[float, dict[tuple[Vertex, Vertex], float]]:
    """Compute a maximum flow from ``source`` to ``sink`` (Edmonds-Karp).

    The capacities are the edge weights of the directed ``graph``.

    Returns:
        A pair ``(value, flow)``: the value of a maximum flow and the flow
        itself as a dictionary ``(u, v) -> flow`` with an entry for EVERY
        edge of the graph (and only for edges of the graph).

    Raises:
        ValueError: If the graph is undirected, if ``source == sink`` or if
            a capacity is negative.
        KeyError: If ``source`` or ``sink`` is not a vertex of the graph.
    """
    # TODO: Step 1 - check the input.
    # TODO: Step 2 - start with flow 0 on every edge.
    # TODO: Step 3 - repeat: build the residual graph and find a shortest
    #                augmenting path; stop if there is none.
    # TODO: Step 4 - delta = smallest residual capacity on the path.
    # TODO: Step 5 - push delta along every pair (u, v) of the path: first
    #                cancel flow on (v, u) as far as possible, then add the
    #                rest to flow[(u, v)].
    # TODO: Step 6 - return (value, flow).
    raise NotImplementedError("TODO: edmonds_karp")


def min_cut(graph: Graph, source: Vertex, sink: Vertex) -> set[Vertex]:
    """OPTIONAL: Return the source side S of a minimum ``source``-``sink`` cut.

    S consists of all vertices that are reachable from ``source`` in the
    residual network of a maximum flow. Its cut capacity equals the value
    of the maximum flow.

    Raises:
        Same errors as :func:`edmonds_karp`.
    """
    # TODO (optional): run edmonds_karp, build the final residual graph and
    #                  collect everything reachable from source.
    raise NotImplementedError("TODO (optional): min_cut")


if __name__ == "__main__":
    clrs = Graph.from_edges(
        [
            ("s", "v1", 16),
            ("s", "v2", 13),
            ("v1", "v3", 12),
            ("v2", "v1", 4),
            ("v2", "v4", 14),
            ("v3", "v2", 9),
            ("v3", "t", 20),
            ("v4", "v3", 7),
            ("v4", "t", 4),
        ],
        directed=True,
    )
    first = find_augmenting_path(residual_graph(clrs, {}), "s", "t")
    print("First augmenting path:", format_path(first))
    value, flow = edmonds_karp(clrs, "s", "t")
    print("Maximum flow value:", value)
    print("Flow:", flow)
