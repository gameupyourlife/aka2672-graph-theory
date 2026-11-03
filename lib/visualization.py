"""All ways to look at a graph - the module to import for visualisation.

* :func:`to_text` / :func:`print_graph` - readable text output in the console.
* :func:`to_dot` / :func:`save_dot` - export to the Graphviz DOT format.
  A ``.dot`` file can be rendered with Graphviz (``dot -Tpng graph.dot -o
  graph.png``) or pasted into an online viewer such as
  https://dreampuf.github.io/GraphvizOnline/.
* :func:`draw`, :func:`show`, :func:`snapshot`, :class:`Trace` - the
  interactive player in the web browser (defined in :mod:`lib.viewer` and
  :mod:`lib.trace`, imported here for convenience)::

      from lib.visualization import Trace, draw, show

  No extra packages are needed.
"""

from __future__ import annotations

from collections.abc import Iterable, Mapping
from pathlib import Path

from lib.graph import Graph, Vertex
from lib.trace import DEFAULT_STYLES, Frame, Style, Trace, format_value
from lib.viewer import draw, save_html, show, snapshot

__all__ = [
    "DEFAULT_STYLES",
    "Frame",
    "PALETTE",
    "Style",
    "Trace",
    "draw",
    "format_value",
    "print_graph",
    "save_dot",
    "save_html",
    "show",
    "snapshot",
    "to_dot",
    "to_text",
]

# Colours used for vertex colourings in DOT files (colour number -> Graphviz colour name).
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


def _fmt(value: object) -> str:
    """Format numbers without a useless ``.0`` (``3.0`` -> ``3``)."""
    if isinstance(value, float) and value.is_integer():
        return str(int(value))
    return str(value)


def _quote(value: object) -> str:
    """Quote a value for use as an identifier in a DOT file."""
    text = str(value).replace("\\", "\\\\").replace('"', '\\"')
    return f'"{text}"'
