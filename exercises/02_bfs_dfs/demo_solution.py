"""Unit 2: Breadth-first search and depth-first search - DEMO SOLUTION.

Both searches follow the same pattern:

1. keep a collection of vertices that still have to be processed,
2. take one vertex out, look at its neighbours,
3. put every neighbour that has not been seen before into the collection.

The *only* difference is the collection: BFS uses a queue (first in, first
out) and therefore explores the graph in layers of increasing distance. DFS
uses a stack (last in, first out) and therefore goes as deep as possible
before it backtracks.

Runtime of both searches: O(|V| + |E|), because every vertex is processed
at most once and every adjacency list is read at most once.
"""

import sys
from collections import deque
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))  # find ``lib``

from lib.generators import random_graph
from lib.graph import Graph, Vertex
from lib.utils import format_path
from lib.visualization import show, snapshot


def bfs(graph: Graph, start: Vertex) -> tuple[dict[Vertex, int], dict[Vertex, Vertex | None]]:
    """Run a breadth-first search from ``start``.

    Returns:
        ``(distance, parent)`` for all vertices reachable from ``start``.

    Raises:
        KeyError: If ``start`` is not a vertex of the graph.
    """
    if start not in graph:
        raise KeyError(f"Start vertex {start!r} is not in the graph")

    distance: dict[Vertex, int] = {start: 0}
    parent: dict[Vertex, Vertex | None] = {start: None}
    queue = deque([start])

    while queue:
        u = queue.popleft()  # the vertex that waited longest
        for w in graph.neighbors(u):
            # "w not in distance" means: w has not been discovered yet.
            # We mark w as discovered *now* (by giving it a distance), so it
            # can never be appended to the queue a second time.
            if w not in distance:
                distance[w] = distance[u] + 1
                parent[w] = u
                queue.append(w)
    return distance, parent


def shortest_path(graph: Graph, start: Vertex, target: Vertex) -> list[Vertex] | None:
    """Return a shortest path ``[start, ..., target]`` or ``None``.

    Raises:
        KeyError: If ``start`` or ``target`` is not a vertex of the graph.
    """
    if target not in graph:
        raise KeyError(f"Target vertex {target!r} is not in the graph")
    _distance, parent = bfs(graph, start)
    if target not in parent:
        return None  # BFS never reached the target

    # Walk backwards along the BFS tree: target, parent[target], ... , start.
    path = []
    v: Vertex | None = target
    while v is not None:
        path.append(v)
        v = parent[v]
    path.reverse()  # we collected the path from the end
    return path


def dfs(graph: Graph, start: Vertex) -> list[Vertex]:
    """Run an iterative depth-first search from ``start`` using a stack.

    Raises:
        KeyError: If ``start`` is not a vertex of the graph.
    """
    if start not in graph:
        raise KeyError(f"Start vertex {start!r} is not in the graph")

    visited: set[Vertex] = set()
    order: list[Vertex] = []
    stack = [start]

    while stack:
        u = stack.pop()  # the vertex that was pushed last
        # A vertex may be on the stack several times (pushed by different
        # neighbours). We only process its first occurrence.
        if u in visited:
            continue
        visited.add(u)
        order.append(u)
        for w in graph.neighbors(u):
            if w not in visited:
                stack.append(w)
    return order


def connected_components(graph: Graph) -> list[set[Vertex]]:
    """Return the connected components of an undirected graph.

    Raises:
        ValueError: If the graph is directed.
    """
    if graph.directed:
        raise ValueError("connected_components() expects an undirected graph")

    components: list[set[Vertex]] = []
    seen: set[Vertex] = set()
    for v in graph.vertices():
        if v in seen:
            continue
        # Everything reachable from v forms the component of v.
        component = set(dfs(graph, v))
        components.append(component)
        seen |= component
    return components


def is_connected(graph: Graph) -> bool:
    """Return ``True`` if the undirected graph is connected (empty graph: ``True``).

    Raises:
        ValueError: If the graph is directed.
    """
    return len(connected_components(graph)) <= 1


def dfs_recursive(graph: Graph, start: Vertex) -> list[Vertex]:
    """OPTIONAL: Depth-first search written as a recursive function.

    Note: Python limits the recursion depth (about 1000 calls by default),
    so this version fails on long paths - the iterative version does not.
    """
    if start not in graph:
        raise KeyError(f"Start vertex {start!r} is not in the graph")
    visited: set[Vertex] = set()
    order: list[Vertex] = []

    def visit(u: Vertex) -> None:
        visited.add(u)
        order.append(u)
        for w in graph.neighbors(u):
            if w not in visited:
                visit(w)  # go deeper first, come back later

    visit(start)
    return order


def bfs_layers(graph: Graph, start: Vertex) -> list[list[Vertex]]:
    """OPTIONAL: Return the BFS layers ``[[start], [distance 1], [distance 2], ...]``."""
    distance, _parent = bfs(graph, start)
    layers: list[list[Vertex]] = [[] for _ in range(max(distance.values()) + 1)]
    for v, d in distance.items():
        layers[d].append(v)
    return layers


if __name__ == "__main__":
    example = Graph.from_edges([("A", "B"), ("A", "C"), ("B", "D"), ("C", "D"), ("D", "E")])
    example.add_vertex("Z")
    distance, parent = bfs(example, "A")
    print("BFS distance:", distance)
    print("BFS parent:  ", parent)
    print("Shortest path A -> E:", format_path(shortest_path(example, "A", "E")))
    print("Shortest path A -> Z:", format_path(shortest_path(example, "A", "Z")))
    print("DFS order:", dfs(example, "A"))
    print("Components:", connected_components(example))
    print("Connected:", is_connected(example))
    print("BFS layers:", bfs_layers(example, "A"))

    # Pictures in the browser (no extra packages needed).
    random_example = random_graph(18, 0.1, seed=3)
    components = connected_components(random_example)
    show(
        snapshot(
            example,
            "BFS from A: layers, distances and BFS tree",
            layers=bfs_layers(example, "A"),
            highlight_edges=[(p, v) for v, p in parent.items() if p is not None],
            vertex_labels={v: f"d = {d}" for v, d in distance.items()},
            vertex_flags={"A": ["start"]},
        ),
        snapshot(
            random_example,
            f"{len(components)} connected components",
            vertex_colors={v: i for i, component in enumerate(components) for v in component},
        ),
        title="Unit 2: results",
    )
    print("Step by step: python exercises/02_bfs_dfs/demo_animation.py")
