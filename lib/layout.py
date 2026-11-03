"""Vertex positions for drawing graphs (pure Python, no extra packages).

A *layout* is a dictionary ``vertex -> (x, y)``. All functions return
coordinates scaled into the box ``[0, 1] x [0, 1]`` (the aspect ratio of the
layout is kept), so that they can be drawn directly.

* :func:`circular_layout` - vertices evenly on a circle
* :func:`shell_layout` - several concentric circles (e.g. Petersen graph)
* :func:`spring_layout` - force-directed layout (Fruchterman-Reingold)
* :func:`bipartite_layout` - two columns, left and right side
* :func:`layered_layout` - columns given by layers (e.g. BFS layers)
* :func:`grid_layout` - for vertices that are ``(row, column)`` tuples
* :func:`auto_layout` - picks a suitable layout automatically

The layouts only *place* vertices. They do not use any of the algorithms
that are implemented in the exercises.
"""

from __future__ import annotations

import math
import random
from collections.abc import Iterable, Mapping, Sequence

from lib.graph import Graph, Vertex

Position = tuple[float, float]
Layout = dict[Vertex, Position]


def normalize(positions: Mapping[Vertex, Position], margin: float = 0.0) -> Layout:
    """Scale and shift ``positions`` into ``[0, 1] x [0, 1]`` keeping the aspect ratio.

    The longer side of the bounding box becomes 1, the shorter side is
    centred. A single vertex is placed in the middle.
    """
    if not positions:
        return {}
    xs = [x for x, _ in positions.values()]
    ys = [y for _, y in positions.values()]
    width = max(xs) - min(xs)
    height = max(ys) - min(ys)
    scale = max(width, height)
    if scale == 0:
        return {v: (0.5, 0.5) for v in positions}
    scale /= 1 - 2 * margin
    x_offset = (1 - width / scale) / 2
    y_offset = (1 - height / scale) / 2
    return {
        v: ((x - min(xs)) / scale + x_offset, (y - min(ys)) / scale + y_offset)
        for v, (x, y) in positions.items()
    }


def circular_layout(vertices: Iterable[Vertex], start_angle: float = 90.0) -> Layout:
    """Place the vertices evenly on a circle, the first one at ``start_angle`` degrees."""
    vertex_list = list(vertices)
    n = len(vertex_list)
    positions = {}
    for i, v in enumerate(vertex_list):
        angle = math.radians(start_angle) - 2 * math.pi * i / max(n, 1)
        positions[v] = (math.cos(angle), math.sin(angle))
    return normalize(positions)


def shell_layout(shells: Sequence[Sequence[Vertex]]) -> Layout:
    """Place each list of vertices on its own circle (the first list outermost).

    Example: ``shell_layout([[0, 1, 2, 3, 4], [5, 6, 7, 8, 9]])`` draws the
    Petersen graph from ``lib.generators`` in its well-known form.
    """
    positions: Layout = {}
    count = len(shells)
    for index, shell in enumerate(shells):
        radius = (count - index) / count
        if len(shell) == 1 and radius == 1 / count:
            radius = 0.0  # a single vertex in the innermost shell sits in the centre
        for i, v in enumerate(shell):
            angle = math.pi / 2 - 2 * math.pi * i / len(shell)
            positions[v] = (radius * math.cos(angle), radius * math.sin(angle))
    return normalize(positions)


def bipartite_layout(graph: Graph, left: Iterable[Vertex]) -> Layout:
    """Place the ``left`` vertices in a left column and all others in a right column."""
    left_set = set(left)
    left_column = [v for v in graph.vertices() if v in left_set]
    right_column = [v for v in graph.vertices() if v not in left_set]
    # Wider columns for long columns, so the picture does not become a thin strip.
    spacing = max(1.6, 0.6 * (max(len(left_column), len(right_column)) - 1))
    return layered_layout([left_column, right_column], horizontal=True, spacing=spacing)


def layered_layout(
    layers: Sequence[Sequence[Vertex]], horizontal: bool = True, spacing: float = 1.0
) -> Layout:
    """Place every layer in its own column (``horizontal=True``) or row.

    Useful for BFS layers, flow networks (source left, sink right) or
    bipartite graphs. Within a layer the vertices are centred.
    """
    positions: Layout = {}
    for depth, layer in enumerate(layers):
        size = len(layer)
        for i, v in enumerate(layer):
            offset = (size - 1) / 2 - i  # first vertex on top
            positions[v] = (depth * spacing, offset) if horizontal else (offset, -depth * spacing)
    return normalize(positions)


def grid_layout(graph: Graph) -> Layout:
    """Place vertices ``(row, column)`` on a grid (row 0 at the top)."""
    return normalize({v: (float(v[1]), -float(v[0])) for v in graph.vertices()})


def spring_layout(graph: Graph, seed: int = 0, iterations: int = 300, attempts: int = 6) -> Layout:
    """Return a force-directed layout (Fruchterman and Reingold, 1991).

    Imagine the vertices as electrically charged balls that repel each
    other, and the edges as springs that pull adjacent vertices together.
    Starting from random positions, the vertices are moved step by step in
    the direction of the total force; the step size ("temperature") shrinks
    over time.

    Every connected component is laid out on its own (several attempts with
    different start positions; the one with the fewest edge crossings and
    edges passing close to other vertices wins),
    then the components are placed next to each other, the largest first.
    Direction of edges is ignored. The result is reproducible for a fixed
    ``seed``.

    Runtime O(attempts * iterations * |V|^2) - fine for the graphs of this
    course (up to about 100 vertices; large components get one attempt).
    """
    edges = [(u, v) for u, v, _ in graph.edges()]
    pieces = []
    for number, component in enumerate(_components(graph)):
        members = set(component)
        piece_edges = [(u, v) for u, v in edges if u in members]
        if len(component) == 1:
            piece = {component[0]: (0.0, 0.0)}
        elif len(component) == 2:
            piece = {component[0]: (0.0, 0.0), component[1]: (1.0, 0.0)}
        else:
            tries = attempts if len(component) <= 40 else 1
            best: Layout = {}
            best_badness = -1.0
            for attempt in range(tries):
                rng = random.Random(f"{seed}/{number}/{attempt}")
                candidate = _fruchterman_reingold(component, piece_edges, rng, iterations)
                badness = _badness(candidate, piece_edges)
                if best_badness < 0 or badness < best_badness:
                    best, best_badness = candidate, badness
            # Bigger components get more room.
            size = math.sqrt(len(component))
            piece = {v: (x * size, y * size) for v, (x, y) in best.items()}
        pieces.append(piece)
    return normalize(_pack(pieces))


def _components(graph: Graph) -> list[list[Vertex]]:
    """Return the connected components (direction ignored), largest first.

    Simple label propagation: every vertex starts with its own label, and
    along each edge the smaller label wins until nothing changes.
    """
    label = {v: i for i, v in enumerate(graph.vertices())}
    edges = [(u, v) for u, v, _ in graph.edges()]
    changed = True
    while changed:
        changed = False
        for u, v in edges:
            smaller = min(label[u], label[v])
            if label[u] != smaller or label[v] != smaller:
                label[u] = label[v] = smaller
                changed = True
    groups: dict[int, list[Vertex]] = {}
    for v in graph.vertices():
        groups.setdefault(label[v], []).append(v)
    return sorted(groups.values(), key=len, reverse=True)  # stable: ties keep vertex order


def _fruchterman_reingold(
    vertices: list[Vertex], edges: list[tuple[Vertex, Vertex]], rng: random.Random, iterations: int
) -> Layout:
    """Force-directed layout of one connected component, scaled into [0, 1]^2."""
    n = len(vertices)
    # Random start positions. (Starting on a circle would put the two ends
    # of a path next to each other, and the path would look like a cycle.)
    pos = {v: [rng.random(), rng.random()] for v in vertices}
    k = math.sqrt(1.0 / n)  # ideal edge length
    temperature = 0.1
    cooling = temperature / (iterations + 1)
    for _ in range(iterations):
        force = {v: [0.0, 0.0] for v in vertices}
        # Repulsion between every pair of vertices: k^2 / d
        for i in range(n):
            u = vertices[i]
            for j in range(i + 1, n):
                v = vertices[j]
                dx = pos[u][0] - pos[v][0]
                dy = pos[u][1] - pos[v][1]
                d = max(math.hypot(dx, dy), 1e-3)
                f = k * k / d
                force[u][0] += dx / d * f
                force[u][1] += dy / d * f
                force[v][0] -= dx / d * f
                force[v][1] -= dy / d * f
        # Attraction along the edges: d^2 / k
        for u, v in edges:
            dx = pos[u][0] - pos[v][0]
            dy = pos[u][1] - pos[v][1]
            d = max(math.hypot(dx, dy), 1e-3)
            f = d * d / k
            force[u][0] -= dx / d * f
            force[u][1] -= dy / d * f
            force[v][0] += dx / d * f
            force[v][1] += dy / d * f
        # Move every vertex in the direction of its force, at most "temperature" far.
        for v in vertices:
            fx, fy = force[v]
            length = max(math.hypot(fx, fy), 1e-9)
            step = min(length, temperature)
            pos[v][0] += fx / length * step
            pos[v][1] += fy / length * step
        temperature -= cooling
    return _spread_out(normalize({v: (x, y) for v, (x, y) in pos.items()}), edges)


def _spread_out(positions: Layout, edges: list[tuple[Vertex, Vertex]], rounds: int = 60) -> Layout:
    """Push apart vertices that are too close for their (wide) label boxes.

    Two vertices should be at least 0.7 median edge lengths apart, measured
    with doubled horizontal distances, because the boxes are wider than high.
    """
    lengths = sorted(math.dist(positions[u], positions[v]) for u, v in edges)
    if not lengths:
        return positions
    wanted = 0.7 * lengths[len(lengths) // 2]
    pos = {v: [x, y] for v, (x, y) in positions.items()}
    vertices = list(pos)
    for _ in range(rounds):
        moved = False
        for i in range(len(vertices)):
            for j in range(i + 1, len(vertices)):
                a, b = pos[vertices[i]], pos[vertices[j]]
                dx, dy = (a[0] - b[0]) / 2, a[1] - b[1]  # horizontal distances count half
                d = math.hypot(dx, dy)
                if d >= wanted:
                    continue
                if d < 1e-9:
                    dx, dy, d = 1e-3, 0.0, 1e-3
                push = (wanted - d) / 2
                a[0] += dx / d * push * 2
                a[1] += dy / d * push
                b[0] -= dx / d * push * 2
                b[1] -= dy / d * push
                moved = True
        if not moved:
            break
    return normalize({v: (x, y) for v, (x, y) in pos.items()})


def _badness(positions: Mapping[Vertex, Position], edges: list[tuple[Vertex, Vertex]]) -> float:
    """Rate a layout (smaller is better).

    Counts edge crossings, edges that nearly touch other vertices and pairs
    of vertices that are too close together. Distances are measured relative
    to the median edge length, so the rating does not depend on the scale.
    """
    lengths = sorted(math.dist(positions[u], positions[v]) for u, v in edges)
    unit = lengths[len(lengths) // 2] if lengths else 1.0
    vertices = list(positions)
    near_misses = 0
    for u, v in edges:
        for w in vertices:
            if w not in (u, v) and _distance_to_segment(positions[w], positions[u], positions[v]) < 0.3 * unit:
                near_misses += 1
    crowded = 0
    for i in range(len(vertices)):
        for j in range(i + 1, len(vertices)):
            (x1, y1), (x2, y2) = positions[vertices[i]], positions[vertices[j]]
            if math.hypot((x1 - x2) / 2, y1 - y2) < 0.6 * unit:
                crowded += 1
    return _count_crossings(positions, edges) + 3 * near_misses + 3 * crowded


def _distance_to_segment(p: Position, a: Position, b: Position) -> float:
    """Distance of the point ``p`` from the line segment ``a b``."""
    dx, dy = b[0] - a[0], b[1] - a[1]
    length_squared = dx * dx + dy * dy
    if length_squared == 0:
        return math.dist(p, a)
    t = max(0.0, min(1.0, ((p[0] - a[0]) * dx + (p[1] - a[1]) * dy) / length_squared))
    return math.dist(p, (a[0] + t * dx, a[1] + t * dy))


def _count_crossings(positions: Mapping[Vertex, Position], edges: list[tuple[Vertex, Vertex]]) -> int:
    """Count pairs of edges (without common end vertex) whose segments cross."""

    def orientation(a: Position, b: Position, c: Position) -> float:
        return (b[0] - a[0]) * (c[1] - a[1]) - (b[1] - a[1]) * (c[0] - a[0])

    crossings = 0
    for i in range(len(edges)):
        a, b = edges[i]
        for j in range(i + 1, len(edges)):
            c, d = edges[j]
            if len({a, b, c, d}) < 4:
                continue
            pa, pb, pc, pd = positions[a], positions[b], positions[c], positions[d]
            if orientation(pa, pb, pc) * orientation(pa, pb, pd) < 0 and (
                orientation(pc, pd, pa) * orientation(pc, pd, pb) < 0
            ):
                crossings += 1
    return crossings


def _pack(pieces: list[Layout], gap: float = 0.8) -> Layout:
    """Place the layouts of several components next to each other in rows."""
    area = sum((_extent(p)[0] + gap) * (_extent(p)[1] + gap) for p in pieces)
    row_limit = max(math.sqrt(area) * 1.4, max((_extent(p)[0] for p in pieces), default=0))
    result: Layout = {}
    x = y = row_height = 0.0
    for piece in pieces:
        width, height = _extent(piece)
        if x > 0 and x + width > row_limit:  # start a new row below
            x = 0.0
            y -= row_height + gap
            row_height = 0.0
        min_x = min(px for px, _ in piece.values())
        max_y = max(py for _, py in piece.values())
        for v, (px, py) in piece.items():
            result[v] = (x + px - min_x, y + py - max_y)
        x += width + gap
        row_height = max(row_height, height)
    return result


def _extent(piece: Layout) -> tuple[float, float]:
    xs = [x for x, _ in piece.values()]
    ys = [y for _, y in piece.values()]
    return max(xs) - min(xs), max(ys) - min(ys)


def _is_grid(graph: Graph) -> bool:
    return graph.num_vertices() > 0 and all(
        isinstance(v, tuple) and len(v) == 2 and all(isinstance(c, int) for c in v) for v in graph.vertices()
    )


def auto_layout(graph: Graph, seed: int = 0) -> Layout:
    """Choose a layout that usually looks good.

    * vertices ``(row, column)`` -> grid,
    * complete graphs and graphs in which every vertex has degree 2
      (cycles) -> circle,
    * otherwise -> spring layout.
    """
    n = graph.num_vertices()
    if _is_grid(graph):
        return grid_layout(graph)
    if n <= 2:
        return layered_layout([graph.vertices()])
    degrees = [graph.degree(v) for v in graph.vertices()]
    if graph.num_edges() == n * (n - 1) // 2 or (not graph.directed and all(d == 2 for d in degrees)):
        return circular_layout(graph.vertices())
    return spring_layout(graph, seed=seed)


def compute_layout(
    graph: Graph,
    layout: str | Mapping[Vertex, Position] = "auto",
    *,
    left: Iterable[Vertex] | None = None,
    layers: Sequence[Sequence[Vertex]] | None = None,
    shells: Sequence[Sequence[Vertex]] | None = None,
    seed: int = 0,
) -> Layout:
    """Return vertex positions for ``graph`` - the single entry point used by the viewer.

    Args:
        graph: The graph.
        layout: ``"auto"``, ``"spring"``, ``"circular"``, ``"shell"``,
            ``"bipartite"``, ``"layered"``, ``"grid"`` or a dictionary
            ``vertex -> (x, y)``. ``"auto"`` uses, in this order: the vertex
            attribute ``"pos"`` (if every vertex has one), ``left`` /
            ``layers`` / ``shells`` if given, otherwise :func:`auto_layout`.
        left: Left side for ``"bipartite"``.
        layers: Vertex lists for ``"layered"`` (one column per list).
        shells: Vertex lists for ``"shell"`` (one circle per list).
        seed: Seed of the spring layout.

    Returns:
        Positions scaled into ``[0, 1] x [0, 1]``.

    Raises:
        ValueError: If the layout is unknown, a needed argument is missing or
            a dictionary misses vertices.
    """
    if isinstance(layout, Mapping):
        missing = [v for v in graph.vertices() if v not in layout]
        if missing:
            raise ValueError(f"No position for vertices {missing}")
        return normalize({v: tuple(layout[v]) for v in graph.vertices()})  # type: ignore[misc]
    if layout == "auto":
        attributes = [graph.vertex_attributes(v) for v in graph.vertices()]
        if attributes and all("pos" in a for a in attributes):
            return normalize({v: tuple(graph.vertex_attributes(v)["pos"]) for v in graph.vertices()})  # type: ignore[misc]
        if left is not None:
            layout = "bipartite"
        elif layers is not None:
            layout = "layered"
        elif shells is not None:
            layout = "shell"
        else:
            return auto_layout(graph, seed=seed)
    if layout == "spring":
        return spring_layout(graph, seed=seed)
    if layout == "circular":
        return circular_layout(graph.vertices())
    if layout == "grid":
        return grid_layout(graph)
    if layout == "bipartite":
        if left is None:
            raise ValueError("layout='bipartite' needs the argument left=...")
        return bipartite_layout(graph, left)
    if layout in ("layered", "shell"):
        groups = layers if layout == "layered" else shells
        if groups is None:
            name = "layers" if layout == "layered" else "shells"
            raise ValueError(f"layout={layout!r} needs the argument {name}=...")
        placed = {v for group in groups for v in group}
        rest = [v for v in graph.vertices() if v not in placed]
        all_groups = [[v for v in group if v in graph] for group in groups] + ([rest] if rest else [])
        return layered_layout(all_groups) if layout == "layered" else shell_layout(all_groups)
    raise ValueError(f"Unknown layout {layout!r}")
