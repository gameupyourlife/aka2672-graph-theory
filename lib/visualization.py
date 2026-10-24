"""Simple ways to look at a graph.

* :func:`to_text` / :func:`print_graph` - readable text output in the console
  (no extra software needed).
* :func:`to_dot` / :func:`save_dot` - export to the Graphviz DOT format.
  A ``.dot`` file can be rendered with Graphviz (``dot -Tpng graph.dot -o
  graph.png``) or pasted into an online viewer such as
  https://dreampuf.github.io/GraphvizOnline/.
* :func:`draw` - optional drawing with matplotlib, **if** it is installed.
  None of the exercises require it. The window does not block your
  program, and the returned :class:`GraphDrawing` can be updated to animate
  an algorithm step by step (see :func:`pause`). Vertex positions come from
  :mod:`lib.layout`.
"""

from __future__ import annotations

import atexit
import os
from collections.abc import Hashable, Iterable, Mapping, Sequence
from pathlib import Path
from typing import Any

from lib import layout as layouts
from lib.graph import Graph, Vertex

# Colours used for vertex colourings (colour number -> Graphviz colour name).
PALETTE = [
    "tomato",
    "gold",
    "lightskyblue",
    "palegreen",
    "plum",
    "orange",
    "lightpink",
    "turquoise",
    "khaki",
    "lightgray",
]


def _has_weights(graph: Graph) -> bool:
    """Return ``True`` if at least one edge has a weight other than 1."""
    return any(weight != 1 for _, _, weight in graph.edges())


def to_text(graph: Graph, show_weights: bool | None = None) -> str:
    """Return the adjacency list of ``graph`` as a readable string.

    Args:
        graph: The graph to display.
        show_weights: Show edge weights in brackets. ``None`` (default)
            shows them only if some weight differs from 1.

    Example output::

        Undirected graph with 3 vertices and 2 edges
          Bullerby   : Lonneberga (4), Sevedstorp (2)
          Lonneberga : Bullerby (4)
          Sevedstorp : Bullerby (2)
    """
    if show_weights is None:
        show_weights = _has_weights(graph)
    kind = "Directed" if graph.directed else "Undirected"
    lines = [
        f"{kind} graph with {graph.num_vertices()} vertices "
        f"and {graph.num_edges()} edges"
    ]
    arrow = "->" if graph.directed else ":"
    width = max((len(str(v)) for v in graph.vertices()), default=0)
    for v in graph.vertices():
        entries = []
        for w in graph.neighbors(v):
            if show_weights:
                entries.append(f"{w} ({_fmt(graph.weight(v, w))})")
            else:
                entries.append(str(w))
        lines.append(f"  {str(v):<{width}} {arrow} {', '.join(entries) or '-'}")
    return "\n".join(lines)


def print_graph(graph: Graph, show_weights: bool | None = None) -> None:
    """Print the adjacency list of ``graph`` (see :func:`to_text`)."""
    print(to_text(graph, show_weights))


def to_dot(
    graph: Graph,
    name: str = "G",
    show_weights: bool | None = None,
    highlight_edges: Iterable[tuple[Vertex, Vertex]] = (),
    vertex_colors: Mapping[Vertex, int] | None = None,
    edge_labels: Mapping[tuple[Vertex, Vertex], str] | None = None,
) -> str:
    """Return a Graphviz DOT description of ``graph``.

    Args:
        graph: The graph to export.
        name: Name of the graph in the DOT file.
        show_weights: Label edges with their weights (``None``: automatic).
        highlight_edges: Edges ``(u, v)`` drawn thick and red, e.g. a
            spanning tree, a shortest path or a matching.
        vertex_colors: Colour number for each vertex, e.g. the result of a
            graph colouring (numbers are mapped to :data:`PALETTE`).
        edge_labels: Custom labels for edges, e.g. ``"3/5"`` for flows.
            Overrides the weight label.

    Returns:
        The DOT source as a string.
    """
    if show_weights is None:
        show_weights = _has_weights(graph)
    highlighted = set()
    for u, v in highlight_edges:
        highlighted.add((u, v))
        if not graph.directed:
            highlighted.add((v, u))
    keyword = "digraph" if graph.directed else "graph"
    connector = "->" if graph.directed else "--"

    lines = [f"{keyword} {_quote(name)} {{", "  node [style=filled, fillcolor=white];"]
    for v in graph.vertices():
        attributes = ""
        if vertex_colors is not None and v in vertex_colors:
            colour = PALETTE[vertex_colors[v] % len(PALETTE)]
            attributes = f" [fillcolor={colour}, xlabel={_quote(vertex_colors[v])}]"
        lines.append(f"  {_quote(v)}{attributes};")
    for u, v, weight in graph.edges():
        attrs = []
        label = None
        if edge_labels is not None:
            label = edge_labels.get((u, v))
            if label is None and not graph.directed:
                label = edge_labels.get((v, u))
        if label is None and show_weights:
            label = _fmt(weight)
        if label is not None:
            attrs.append(f"label={_quote(label)}")
        if (u, v) in highlighted:
            attrs.append("color=red, penwidth=3")
        suffix = f" [{', '.join(attrs)}]" if attrs else ""
        lines.append(f"  {_quote(u)} {connector} {_quote(v)}{suffix};")
    lines.append("}")
    return "\n".join(lines)


def save_dot(graph: Graph, path: str | Path, **options: object) -> Path:
    """Write :func:`to_dot` output to the file ``path``.

    All keyword arguments are passed on to :func:`to_dot`.

    Returns:
        The path of the written file.
    """
    path = Path(path)
    path.write_text(to_dot(graph, **options) + "\n", encoding="utf-8")  # type: ignore[arg-type]
    return path


# ----------------------------------------------------------------------
# Drawing with matplotlib (optional)
# ----------------------------------------------------------------------
DRAW_PALETTE = [
    "#8ecae6",  # light blue
    "#ffb703",  # amber
    "#90be6d",  # green
    "#f28482",  # salmon
    "#cdb4db",  # lilac
    "#f9e07f",  # yellow
    "#4cc9f0",  # cyan
    "#f8961e",  # orange
    "#b5e48c",  # lime
    "#adb5bd",  # grey
]
"""Fill colours for vertex colourings in :func:`draw` (colour classes 0, 1, 2, ...)."""

NO_PLOTS_ENV_VAR = "GRAPH_COURSE_NO_PLOTS"
"""Set this environment variable to 1 to switch off all drawings (see :func:`can_draw`)."""

_COLORS = {
    "vertex": "#eef4fb",
    "vertex_border": "#34506e",
    "edge": "#7b8794",
    "edge_dimmed": "#cbd2d9",
    "highlight": "#d62839",
    "text": "#1f2933",
    "secondary_text": "#52606d",
}

_DRAW_OPTIONS: dict[str, Any] = {
    "title": None,
    "vertex_colors": None,
    "highlight_edges": (),
    "highlight_vertices": (),
    "edge_labels": None,
    "vertex_labels": None,
    "show_weights": None,
    "legend": None,
}

_exit_hook_registered = False


def can_draw() -> bool:
    """Return ``True`` if :func:`draw` can be used.

    This is the case if matplotlib is installed and the environment variable
    ``GRAPH_COURSE_NO_PLOTS`` is not set (set it to ``1`` to suppress all
    windows, e.g. when running the demo solutions automatically).
    """
    if os.environ.get(NO_PLOTS_ENV_VAR, "").strip() not in ("", "0"):
        return False
    try:
        import matplotlib  # noqa: F401
    except ImportError:
        return False
    return True


def _pyplot() -> Any:
    """Import and return ``matplotlib.pyplot`` with a helpful error message."""
    try:
        import matplotlib.pyplot as plt
    except ImportError as error:
        raise ImportError(
            "draw() needs matplotlib. Install it with 'pip install matplotlib' "
            "or use print_graph()/to_dot() instead."
        ) from error
    return plt


def _backend_kind() -> str:
    """Return ``"window"``, ``"inline"`` (Jupyter) or ``"file"`` (no display)."""
    import matplotlib

    backend = matplotlib.get_backend().lower()
    if "inline" in backend or "ipympl" in backend or "widget" in backend:
        return "inline"
    if backend in {"agg", "cairo", "pdf", "pgf", "ps", "svg", "template"}:
        return "file"
    return "window"


class GraphDrawing:
    """A drawing of a graph that can be changed after it was shown.

    :func:`draw` returns a ``GraphDrawing``. The vertex positions stay fixed,
    so you can show the progress of an algorithm step by step::

        drawing = draw(graph, title="DFS")
        for step in range(len(order)):
            drawing.update(highlight_vertices=order[: step + 1], title=f"Step {step}")
            pause(0.5)

    Attributes:
        graph: The drawn graph.
        positions: The vertex positions (``vertex -> (x, y)``).
        figure: The matplotlib figure.
        ax: The matplotlib axes.
        options: The current drawing options (title, colours, highlights, ...).
    """

    def __init__(
        self,
        graph: Graph,
        positions: Mapping[Vertex, tuple[float, float]],
        figure: Any,
        ax: Any,
        options: Mapping[str, Any],
    ) -> None:
        """Store everything that is needed to (re)draw the graph and draw it."""
        self.graph = graph
        self.positions = dict(positions)
        self.figure = figure
        self.ax = ax
        self.options = {**_DRAW_OPTIONS, **options}
        _render(self.ax, self.graph, self.positions, self.options)

    def update(self, **options: Any) -> GraphDrawing:
        """Change drawing options and redraw in the same window.

        Accepts the styling arguments of :func:`draw`: ``title``,
        ``vertex_colors``, ``highlight_edges``, ``highlight_vertices``,
        ``edge_labels``, ``vertex_labels``, ``show_weights``, ``legend``.
        Options that are not given keep their current value.

        Returns:
            The drawing itself, so calls can be chained.

        Raises:
            TypeError: For unknown options.
        """
        unknown = set(options) - set(_DRAW_OPTIONS)
        if unknown:
            raise TypeError(f"Unknown drawing option(s): {', '.join(sorted(unknown))}")
        for name in ("highlight_edges", "highlight_vertices"):
            if name in options:
                options[name] = tuple(options[name])
        self.options.update(options)
        _render(self.ax, self.graph, self.positions, self.options)
        if self.options["title"]:
            _set_window_title(self.figure, self.options["title"])
        self.figure.canvas.draw_idle()
        if _backend_kind() == "window" and _pyplot().fignum_exists(self.figure.number):
            _pyplot().pause(0.001)  # let the window show the change
        return self

    def save(self, filename: str | Path) -> Path:
        """Save the current picture (PNG, SVG or PDF, chosen by the file extension)."""
        path = Path(filename)
        self.figure.savefig(path, dpi=150, bbox_inches="tight", facecolor="white")
        return path

    def close(self) -> None:
        """Close the window of this drawing."""
        _pyplot().close(self.figure)


def draw(
    graph: Graph,
    *,
    title: str | None = None,
    layout: str | Mapping[Vertex, tuple[float, float]] = "auto",
    left: Iterable[Vertex] | None = None,
    layers: Sequence[Sequence[Vertex]] | None = None,
    shells: Sequence[Sequence[Vertex]] | None = None,
    vertex_colors: Mapping[Vertex, Hashable] | None = None,
    highlight_edges: Iterable[tuple[Vertex, Vertex]] = (),
    highlight_vertices: Iterable[Vertex] = (),
    edge_labels: Mapping[tuple[Vertex, Vertex], object] | None = None,
    vertex_labels: Mapping[Vertex, object] | None = None,
    show_weights: bool | None = None,
    legend: bool | None = None,
    seed: int = 0,
    size: tuple[float, float] | None = None,
    filename: str | Path | None = None,
    block: bool = False,
) -> GraphDrawing:
    """Draw ``graph`` with matplotlib (optional, needs ``pip install matplotlib``).

    The window opens **without blocking**: your program keeps running, and
    you can open several windows. When the program ends, the windows stay
    open until you close them (or call :func:`wait_for_windows` yourself).

    Args:
        graph: The graph to draw.
        title: Title above the picture (and of the window).
        layout: How to place the vertices: ``"auto"`` (default), ``"spring"``,
            ``"circular"``, ``"shell"``, ``"bipartite"``, ``"layered"``,
            ``"grid"`` - or your own dictionary ``vertex -> (x, y)``.
            See :mod:`lib.layout`.
        left: Left side for ``layout="bipartite"`` (implied by ``"auto"``).
        layers: Vertex lists for ``layout="layered"``, one column per layer,
            e.g. BFS layers (implied by ``"auto"``).
        shells: Vertex lists for ``layout="shell"``, concentric circles
            (implied by ``"auto"``).
        vertex_colors: Colour class of each vertex, e.g. the result of a graph
            colouring. Any values can be used as colour names.
        highlight_edges: Edges ``(u, v)`` drawn thick and red, e.g. a
            spanning tree, a path or a matching.
        highlight_vertices: Vertices with a thick red border.
        edge_labels: Text for edges, e.g. ``{("s", "a"): "3/5"}`` for flows.
            Replaces the weight label of these edges.
        vertex_labels: Extra text below vertices, e.g. distances.
        show_weights: Show edge weights (``None``: only if some weight is not 1).
        legend: Show a legend of the vertex colours (``None``: if colours are given).
        seed: Seed of the spring layout (another seed gives another picture).
        size: Figure size in inches ``(width, height)`` (default: automatic).
        filename: If given, the picture is saved to this file (``.png``,
            ``.svg``, ``.pdf``) instead of being shown in a window.
        block: If ``True``, wait until the window is closed.

    Returns:
        A :class:`GraphDrawing` that can be changed with ``update(...)``.

    Raises:
        ImportError: If matplotlib is not installed.
        ValueError: If the layout is unknown or does not fit the graph.
    """
    plt = _pyplot()
    positions = _resolve_layout(graph, layout, left, layers, shells, seed)
    figure, ax = plt.subplots(figsize=size or _figure_size(positions))
    figure.patch.set_facecolor("white")
    if title:
        _set_window_title(figure, title)
    drawing = GraphDrawing(
        graph,
        positions,
        figure,
        ax,
        {
            "title": title,
            "vertex_colors": vertex_colors,
            "highlight_edges": tuple(highlight_edges),
            "highlight_vertices": tuple(highlight_vertices),
            "edge_labels": edge_labels,
            "vertex_labels": vertex_labels,
            "show_weights": show_weights,
            "legend": legend,
        },
    )
    figure.tight_layout()
    if filename is not None:
        drawing.save(filename)
        plt.close(figure)
    else:
        _show(block)
    return drawing


def pause(seconds: float) -> None:
    """Wait ``seconds`` while keeping the drawing windows responsive.

    Use it between ``drawing.update(...)`` calls to animate an algorithm.
    Without open windows (e.g. when saving to files) it returns immediately.
    """
    if not can_draw():
        return
    plt = _pyplot()
    if _backend_kind() == "window" and plt.get_fignums():
        plt.pause(seconds)


def wait_for_windows() -> None:
    """Block until all drawing windows have been closed.

    :func:`draw` calls this automatically when your program ends, so you
    only need it if you want to wait at a specific point.
    """
    try:
        import matplotlib.pyplot as plt
    except ImportError:
        return
    if _backend_kind() == "window" and plt.get_fignums():
        plt.show(block=True)


def _show(block: bool) -> None:
    """Show the current figure, normally without blocking."""
    global _exit_hook_registered
    plt = _pyplot()
    kind = _backend_kind()
    if kind == "inline":
        plt.show()
    elif kind == "window":
        if block:
            plt.show(block=True)
            return
        plt.show(block=False)
        plt.pause(0.001)  # draw the window now
        if not _exit_hook_registered:
            # Keep the windows open when the program ends.
            atexit.register(_wait_at_exit)
            _exit_hook_registered = True


def _wait_at_exit() -> None:
    try:
        wait_for_windows()
    except Exception:  # pragma: no cover - never fail while exiting
        pass


def _set_window_title(figure: Any, title: str) -> None:
    manager = getattr(figure.canvas, "manager", None)
    if manager is not None:
        manager.set_window_title(title)


def _resolve_layout(
    graph: Graph,
    layout: str | Mapping[Vertex, tuple[float, float]],
    left: Iterable[Vertex] | None,
    layers: Sequence[Sequence[Vertex]] | None,
    shells: Sequence[Sequence[Vertex]] | None,
    seed: int,
) -> dict[Vertex, tuple[float, float]]:
    """Turn the ``layout`` argument of :func:`draw` into vertex positions."""
    if isinstance(layout, Mapping):
        missing = [v for v in graph.vertices() if v not in layout]
        if missing:
            raise ValueError(f"No position for vertices {missing}")
        return layouts.normalize({v: layout[v] for v in graph.vertices()})
    if layout == "auto":
        if left is not None:
            layout = "bipartite"
        elif layers is not None:
            layout = "layered"
        elif shells is not None:
            layout = "shell"
        else:
            return layouts.auto_layout(graph, seed=seed)
    if layout == "spring":
        return layouts.spring_layout(graph, seed=seed)
    if layout == "circular":
        return layouts.circular_layout(graph.vertices())
    if layout == "grid":
        return layouts.grid_layout(graph)
    if layout == "bipartite":
        if left is None:
            raise ValueError("layout='bipartite' needs the argument left=...")
        return layouts.bipartite_layout(graph, left)
    if layout in ("layered", "shell"):
        groups = layers if layout == "layered" else shells
        if groups is None:
            name = "layers" if layout == "layered" else "shells"
            raise ValueError(f"layout={layout!r} needs the argument {name}=...")
        placed = {v for group in groups for v in group}
        rest = [v for v in graph.vertices() if v not in placed]
        all_groups = [list(group) for group in groups] + ([rest] if rest else [])
        if layout == "layered":
            return layouts.layered_layout(all_groups)
        return layouts.shell_layout(all_groups)
    raise ValueError(f"Unknown layout {layout!r}")


def _figure_size(positions: Mapping[Vertex, tuple[float, float]]) -> tuple[float, float]:
    """Choose a figure size that fits the shape of the layout."""
    if not positions:
        return (6.0, 4.5)
    xs = [x for x, _ in positions.values()]
    ys = [y for _, y in positions.values()]
    width = max(max(xs) - min(xs), 0.25)
    height = max(max(ys) - min(ys), 0.25)
    scale = 8.0 + 0.08 * min(len(positions), 30)  # bigger graphs get bigger pictures
    if width >= height:
        return (scale, max(4.5, scale * height / width + 0.8))
    return (max(5.0, scale * width / height), scale)


def _color_classes(values: Iterable[Hashable]) -> dict[Hashable, int]:
    """Number the distinct colour values 0, 1, 2, ... (sorted if possible)."""
    distinct = list(dict.fromkeys(values))
    try:
        distinct = sorted(distinct)  # type: ignore[type-var]
    except TypeError:
        pass
    return {value: i for i, value in enumerate(distinct)}


def _render(
    ax: Any,
    graph: Graph,
    positions: Mapping[Vertex, tuple[float, float]],
    options: Mapping[str, Any],
) -> None:
    """Draw ``graph`` into the matplotlib axes ``ax`` (clears it first)."""
    from matplotlib.patches import Patch

    ax.clear()
    ax.set_axis_off()
    n = graph.num_vertices()
    font = 12 if n <= 10 else 10 if n <= 25 else 8 if n <= 60 else 6

    vertex_colors = options["vertex_colors"] or {}
    classes = _color_classes(vertex_colors.values())
    marked_vertices = set(options["highlight_vertices"])
    marked_edges = set()
    for edge in options["highlight_edges"]:  # pairs (u, v) or Edge(u, v, weight)
        u, v = edge[0], edge[1]
        marked_edges.add((u, v))
        if not graph.directed:
            marked_edges.add((v, u))
    show_weights = options["show_weights"]
    if show_weights is None:
        show_weights = _has_weights(graph)
    edge_labels = options["edge_labels"] or {}
    vertex_labels = options["vertex_labels"] or {}

    # Vertices: the name in a rounded box. The boxes are drawn first, and
    # every edge is clipped exactly at the border of its two boxes.
    boxes = {}
    for v in graph.vertices():
        x, y = positions[v]
        marked = v in marked_vertices
        face = _COLORS["vertex"]
        if v in vertex_colors:
            face = DRAW_PALETTE[classes[vertex_colors[v]] % len(DRAW_PALETTE)]
        boxes[v] = ax.text(
            x,
            y,
            _vertex_text(v),
            ha="center",
            va="center",
            fontsize=font,
            color="none",  # only the box; the name itself is drawn on top below
            zorder=3,
            bbox={
                "boxstyle": "round,pad=0.45",
                "facecolor": face,
                "edgecolor": _COLORS["highlight"] if marked else _COLORS["vertex_border"],
                "linewidth": 2.8 if marked else 1.2,
            },
        )
        # The name on top of everything, so that no edge or label can hide it.
        ax.text(x, y, _vertex_text(v), ha="center", va="center", fontsize=font, color=_COLORS["text"], zorder=7)
        if v in vertex_labels:
            ax.annotate(
                str(vertex_labels[v]),
                xy=(x, y),
                xytext=(0, -1.9 * font),
                textcoords="offset points",
                ha="center",
                va="top",
                fontsize=font - 2,
                color=_COLORS["secondary_text"],
                zorder=6,
                bbox={"boxstyle": "round,pad=0.1", "facecolor": "white", "edgecolor": "none", "alpha": 0.85},
            )

    # Edges: straight lines, or curves for antiparallel edges u -> v, v -> u.
    for u, v, weight in graph.edges():
        rad = 0.2 if graph.directed and graph.has_edge(v, u) else 0.0
        marked = (u, v) in marked_edges
        if marked:
            color = _COLORS["highlight"]
        else:
            color = _COLORS["edge_dimmed"] if marked_edges else _COLORS["edge"]
        ax.annotate(
            "",
            xy=positions[v],
            xytext=positions[u],
            zorder=5 if marked else 4,
            arrowprops={
                "arrowstyle": "-|>" if graph.directed else "-",
                "color": color,
                "linewidth": 3.0 if marked else 1.5,
                "connectionstyle": f"arc3,rad={rad}",
                "patchA": boxes[u].get_bbox_patch(),
                "patchB": boxes[v].get_bbox_patch(),
                "shrinkA": 1,
                "shrinkB": 2,
                "mutation_scale": 16,
            },
        )
        label = edge_labels.get((u, v))
        if label is None and not graph.directed:
            label = edge_labels.get((v, u))
        if label is None and show_weights:
            label = _fmt(weight)
        if label is not None:
            (x1, y1), (x2, y2) = positions[u], positions[v]
            # Point at 45 % of the (possibly curved) edge: slightly off the
            # middle, so that labels of two crossing diagonals do not overlap.
            # A curved edge is a quadratic Bezier curve with control point c.
            cx = (x1 + x2) / 2 + rad * (y2 - y1)
            cy = (y1 + y2) / 2 - rad * (x2 - x1)
            t = 0.45
            mx = (1 - t) ** 2 * x1 + 2 * (1 - t) * t * cx + t**2 * x2
            my = (1 - t) ** 2 * y1 + 2 * (1 - t) * t * cy + t**2 * y2
            ax.text(
                mx,
                my,
                str(label),
                ha="center",
                va="center",
                fontsize=font - 2,
                zorder=6,
                color=_COLORS["highlight"] if marked else _COLORS["secondary_text"],
                bbox={"boxstyle": "round,pad=0.15", "facecolor": "white", "edgecolor": "none", "alpha": 0.9},
            )

    if positions:
        xs = [x for x, _ in positions.values()]
        ys = [y for _, y in positions.values()]
        margin = 0.1  # room for the boxes at the border
        ax.update_datalim([(min(xs) - margin, min(ys) - margin), (max(xs) + margin, max(ys) + margin)])
        ax.autoscale_view()
    ax.set_aspect("equal", adjustable="datalim")

    if options["title"]:
        ax.set_title(options["title"], fontsize=14, fontweight="bold", color=_COLORS["text"], pad=14)
    legend = options["legend"]
    if legend is None:
        legend = bool(vertex_colors)
    if legend and classes:
        handles = [
            Patch(
                facecolor=DRAW_PALETTE[i % len(DRAW_PALETTE)],
                edgecolor=_COLORS["vertex_border"],
                label=str(value),
            )
            for value, i in classes.items()
        ]
        ax.legend(
            handles=handles,
            loc="upper center",
            bbox_to_anchor=(0.5, 0.0),
            ncol=min(len(handles), 8),
            frameon=False,
            fontsize=font - 1,
        )


def _vertex_text(v: Vertex) -> str:
    """Text shown for a vertex: tuples as ``(a, 0)`` instead of ``('a', 0)``."""
    if isinstance(v, tuple):
        return "(" + ", ".join(str(part) for part in v) + ")"
    return str(v)


def _fmt(value: object) -> str:
    """Format numbers without a useless ``.0`` (``3.0`` -> ``3``)."""
    if isinstance(value, float) and value.is_integer():
        return str(int(value))
    return str(value)


def _quote(value: object) -> str:
    """Quote a value for use as an identifier in a DOT file."""
    text = str(value).replace("\\", "\\\\").replace('"', '\\"')
    return f'"{text}"'
