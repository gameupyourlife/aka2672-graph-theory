"""Show graphs and recorded algorithms in the web browser.

The viewer writes a single, self-contained HTML file (no internet connection
and no extra Python packages needed) and opens it in the browser. The page
shows the graph as an interactive picture:

* step through a :class:`~lib.trace.Trace` with ◀ / ▶, the slider, the
  arrow keys or automatically (▶ Play, adjustable speed),
* zoom with the mouse wheel, move the picture by dragging the background,
  drag vertices to new places, hover a vertex for details,
* side panels: explanation of the step, variables, pseudocode, legend,
* export of the current picture as SVG or PNG.

Main functions:

* :func:`show` - show one or several traces (and/or graphs) on one page,
* :func:`draw` - show a single graph with highlighted parts,
* :func:`snapshot` - a one-step trace, e.g. to combine pictures with
  :func:`show`,
* :func:`save_html` - write the page to a file without opening it.

Set the environment variable ``GRAPH_COURSE_NO_PLOTS=1`` to write the files
without opening a browser (e.g. for automatic tests). In Jupyter notebooks
the player is shown directly in the notebook.
"""

from __future__ import annotations

import html
import json
import os
import re
import sys
import tempfile
import time
import webbrowser
from collections.abc import Hashable, Iterable, Mapping, Sequence
from itertools import count
from pathlib import Path
from typing import Any

from lib.graph import Graph, Vertex
from lib.layout import compute_layout
from lib.trace import AUTO_COLORS, Style, Trace, format_value

NO_PLOTS_ENV_VAR = "GRAPH_COURSE_NO_PLOTS"
"""Environment variable: if set to ``1``, no browser window is opened."""

PALETTE = [
    "#93c5fd",  # blue
    "#fcd34d",  # amber
    "#86efac",  # green
    "#fca5a5",  # red
    "#c4b5fd",  # violet
    "#fdba74",  # orange
    "#67e8f9",  # cyan
    "#f9a8d4",  # pink
    "#bef264",  # lime
    "#cbd5e1",  # grey
]
"""Fill colours of the colour classes 0, 1, 2, ... (see :meth:`Trace.color`)."""

OUTPUT_DIR = Path(tempfile.gettempdir()) / "graph-course"
"""Folder for the HTML files of :func:`show` if no file name is given."""

_ASSETS = Path(__file__).with_name("viewer_assets")
_counter = count(1)

_TEMPLATE = """<!DOCTYPE html>
<html lang="de">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>@@TITLE@@</title>
<style>
@@CSS@@
</style>
</head>
<body>
<header><h1 id="title"></h1><nav id="tabs"></nav></header>
<main>
  <section id="stage-wrap">
    <svg id="stage" xmlns="http://www.w3.org/2000/svg" preserveAspectRatio="xMidYMid meet"></svg>
    <div id="scene-title"></div>
    <div id="tools">
      <button id="fit" title="Fit to window (F)">⤢ Fit</button>
      <button id="save-svg" title="Save the current picture as SVG">SVG</button>
      <button id="save-png" title="Save the current picture as PNG">PNG</button>
    </div>
  </section>
  <aside>
    <div id="message"></div>
    <div class="panel" id="variables-panel"><h2>Variables</h2><div id="variables"></div></div>
    <div class="panel" id="code-panel"><h2>Pseudocode</h2><div id="code"></div></div>
    <div class="panel" id="legend-panel"><h2>Legend</h2><div id="legend"></div></div>
    <div class="panel" id="description-panel"><h2>About</h2><div id="description"></div></div>
  </aside>
  <footer id="controls">
    <button id="first" title="First step (Home)">⏮</button>
    <button id="prev" title="Previous step (←)">◀</button>
    <button id="play" title="Play (Space)">▶</button>
    <button id="next" title="Next step (→)">▶❘</button>
    <button id="last" title="Last step (End)">⏭</button>
    <input id="slider" type="range" min="0" max="0" value="0" aria-label="Step">
    <span id="counter"></span>
    <select id="speed" title="Speed">
      <option value="0.25">0.25×</option>
      <option value="0.5">0.5×</option>
      <option value="1" selected>1×</option>
      <option value="2">2×</option>
      <option value="4">4×</option>
    </select>
  </footer>
</main>
<div id="tooltip"></div>
<script type="application/json" id="graph-data">@@DATA@@</script>
<script>
@@JS@@
</script>
</body>
</html>
"""


# ----------------------------------------------------------------------
# Public functions
# ----------------------------------------------------------------------
def snapshot(
    graph: Graph,
    title: str = "",
    *,
    message: str = "",
    description: str = "",
    highlight_vertices: Iterable[Vertex] = (),
    highlight_edges: Iterable[tuple[Vertex, Vertex]] = (),
    vertex_flags: Mapping[Vertex, Iterable[str]] | None = None,
    edge_flags: Mapping[tuple[Vertex, Vertex], Iterable[str]] | None = None,
    vertex_colors: Mapping[Vertex, Hashable] | None = None,
    vertex_labels: Mapping[Vertex, object] | None = None,
    edge_labels: Mapping[tuple[Vertex, Vertex], object] | None = None,
    **trace_options: Any,
) -> Trace:
    """Return a :class:`Trace` with exactly one step: a single picture of ``graph``.

    Args:
        graph: The graph.
        title: Title of the picture.
        message: Text shown next to the picture.
        description: Longer explanation (panel "About").
        highlight_vertices: Vertices with the flag ``"highlight"``.
        highlight_edges: Edges with the flag ``"highlight"`` (pairs or ``Edge``).
        vertex_flags: Further flags per vertex, e.g. ``{"A": ["start"]}``.
        edge_flags: Further flags per edge.
        vertex_colors: Colour class per vertex, e.g. a graph colouring.
        vertex_labels: Text below vertices, e.g. distances.
        edge_labels: Text on edges, e.g. ``"3/5"`` for flows.
        **trace_options: Passed to :class:`Trace` (``layout``, ``left``,
            ``layers``, ``shells``, ``seed``, ``show_weights``).
    """
    trace = Trace(graph, title, description=description, **trace_options)
    for v in highlight_vertices:
        trace.flag(v, "highlight")
    for edge in highlight_edges:
        trace.flag_edge(edge[0], edge[1], "highlight")
    for v, names in (vertex_flags or {}).items():
        trace.flag(v, *names)
    for (u, v), names in (edge_flags or {}).items():
        trace.flag_edge(u, v, *names)
    for v, value in (vertex_colors or {}).items():
        trace.color(v, value)
    for v, text in (vertex_labels or {}).items():
        trace.label(v, text)
    for (u, v), text in (edge_labels or {}).items():
        trace.edge_label(u, v, text)
    trace.step(message)
    return trace


def show(
    *scenes: Trace | Graph,
    title: str | None = None,
    filename: str | Path | None = None,
    open_browser: bool | None = None,
) -> Path:
    """Show traces and/or graphs in the browser (one tab per scene).

    Args:
        *scenes: :class:`Trace` objects or plain graphs.
        title: Title of the page (default: title of the first scene).
        filename: Where to write the HTML file (default: a new file in
            :data:`OUTPUT_DIR`).
        open_browser: Open the page in the browser. Default: yes, unless
            the environment variable ``GRAPH_COURSE_NO_PLOTS`` is set. In a
            Jupyter notebook the page is shown in the notebook instead.

    Returns:
        The path of the written HTML file.

    Raises:
        ValueError: If no scene is given.
    """
    traces = _as_traces(scenes)
    page_title = title or traces[0].title or "Graph"
    if filename is None:
        OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
        _remove_old_files(OUTPUT_DIR)
        filename = OUTPUT_DIR / f"{_slug(page_title)}-{os.getpid()}-{next(_counter)}.html"
    path = save_html(*traces, filename=filename, title=page_title)

    if open_browser is None:
        open_browser = os.environ.get(NO_PLOTS_ENV_VAR, "").strip() in ("", "0")
    if open_browser:
        if _in_notebook():
            from IPython.display import HTML, display  # type: ignore[import-not-found]

            display(HTML(notebook_html(traces, title=page_title)))
        else:
            webbrowser.open(path.resolve().as_uri())
    return path


def draw(graph: Graph, title: str = "", **options: Any) -> Path:
    """Show a single picture of ``graph`` in the browser.

    Accepts all arguments of :func:`snapshot` (``highlight_vertices``,
    ``highlight_edges``, ``vertex_colors``, ``vertex_labels``,
    ``edge_labels``, ``layout``, ...) plus ``filename`` and
    ``open_browser`` of :func:`show`.

    Example::

        draw(graph, "Minimum spanning tree", highlight_edges=kruskal(graph))
    """
    show_options = {key: options.pop(key) for key in ("filename", "open_browser") if key in options}
    return show(snapshot(graph, title, **options), **show_options)


def save_html(*scenes: Trace | Graph, filename: str | Path, title: str | None = None) -> Path:
    """Write the player page for ``scenes`` to ``filename`` and return its path."""
    traces = _as_traces(scenes)
    path = Path(filename)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(to_html(traces, title=title), encoding="utf-8")
    return path


def to_html(scenes: Sequence[Trace | Graph], title: str | None = None) -> str:
    """Return the complete, self-contained HTML page for ``scenes``."""
    traces = _as_traces(scenes)
    page_title = title or traces[0].title or "Graph"
    data = {"title": page_title, "scenes": [scene_data(trace) for trace in traces]}
    # "</" must not appear inside a <script> element.
    payload = json.dumps(data, ensure_ascii=False, separators=(",", ":")).replace("</", "<\\/")
    # Plain replacements (CSS and JavaScript are full of curly braces).
    page = _TEMPLATE.replace("@@TITLE@@", html.escape(page_title))
    page = page.replace("@@CSS@@", (_ASSETS / "player.css").read_text(encoding="utf-8"))
    page = page.replace("@@JS@@", (_ASSETS / "player.js").read_text(encoding="utf-8"))
    return page.replace("@@DATA@@", payload)


def notebook_html(scenes: Sequence[Trace | Graph], title: str | None = None, height: int = 640) -> str:
    """Return an ``<iframe>`` that shows the player inside a Jupyter notebook."""
    page = to_html(scenes, title=title)
    return (
        f'<iframe srcdoc="{html.escape(page, quote=True)}" '
        f'style="width:100%;height:{height}px;border:1px solid #e2e8f0;border-radius:10px"></iframe>'
    )


def scene_data(trace: Trace) -> dict[str, Any]:
    """Convert a trace into the JSON structure read by the player (see player.js)."""
    graph = trace.graph
    positions = compute_layout(
        graph, trace.layout, left=trace.left, layers=trace.layers, shells=trace.shells, seed=trace.seed
    )
    vertices = graph.vertices()
    vertex_index = {v: i for i, v in enumerate(vertices)}
    edges = graph.edges()
    edge_index = {(e.u, e.v): i for i, e in enumerate(edges)}
    frames = trace.frames or [trace.capture()]

    # Colour classes: all colour values that occur, numbered 0, 1, 2, ...
    color_values = list(dict.fromkeys(value for f in frames for value in f.vertex_colors.values()))
    try:
        color_values.sort()
    except TypeError:
        pass  # values that cannot be compared keep their order
    color_class = {value: i for i, value in enumerate(color_values)}

    # Styles of all flags that occur (unknown flags get an automatic style).
    vertex_flag_names = list(dict.fromkeys(n for f in frames for names in f.vertex_flags.values() for n in names))
    edge_flag_names = list(dict.fromkeys(n for f in frames for names in f.edge_flags.values() for n in names))
    styles: dict[str, dict[str, Any]] = {}
    auto = 0
    for name in dict.fromkeys(vertex_flag_names + edge_flag_names):
        style = trace.styles.get(name)
        if style is None:
            style = Style(description=name, color=AUTO_COLORS[auto % len(AUTO_COLORS)], width=4, priority=55)
            auto += 1
        styles[name] = style.as_dict()

    legend = []
    for name in vertex_flag_names:
        legend.append({"flag": name, "kind": "vertex", "text": styles[name].get("description") or name})
    for name in edge_flag_names:
        text = styles[name].get("description") or name
        if name in vertex_flag_names:
            text += " (edge)"
        legend.append({"flag": name, "kind": "edge", "text": text})
    for value, i in color_class.items():
        legend.append({"kind": "color", "fill": PALETTE[i % len(PALETTE)], "text": f"colour {format_value(value)}"})

    show_weights = trace.show_weights
    if show_weights is None:
        show_weights = any(weight != 1 for _, _, weight in edges)

    return {
        "title": trace.title,
        "description": trace.description,
        "directed": graph.directed,
        "showWeights": show_weights,
        "vertices": [
            {
                "text": format_value(graph.vertex_attributes(v).get("label", _vertex_text(v))),
                "x": positions[v][0],
                "y": positions[v][1],
                "degree": graph.degree(v),
                "info": _info(graph.vertex_attributes(v)),
            }
            for v in vertices
        ],
        "edges": [
            {
                "u": vertex_index[e.u],
                "v": vertex_index[e.v],
                "w": format_value(e.weight),
                "curved": graph.directed and graph.has_edge(e.v, e.u),
            }
            for e in edges
        ],
        "pseudocode": trace.pseudocode,
        "styles": styles,
        "palette": PALETTE,
        "colorNames": [format_value(value) for value in color_values],
        "legend": legend,
        "frames": [
            {
                "m": f.message,
                "l": f.line,
                "vf": {vertex_index[v]: list(names) for v, names in f.vertex_flags.items()},
                "ef": {edge_index[e]: list(names) for e, names in f.edge_flags.items()},
                "vl": {vertex_index[v]: text for v, text in f.vertex_labels.items()},
                "el": {edge_index[e]: text for e, text in f.edge_labels.items()},
                "vc": {vertex_index[v]: color_class[value] for v, value in f.vertex_colors.items()},
                "vars": [list(pair) for pair in f.variables],
            }
            for f in frames
        ],
    }


# ----------------------------------------------------------------------
# Helpers
# ----------------------------------------------------------------------
def _as_traces(scenes: Iterable[Trace | Graph]) -> list[Trace]:
    traces = [scene if isinstance(scene, Trace) else snapshot(scene) for scene in scenes]
    if not traces:
        raise ValueError("Nothing to show: pass at least one Trace or Graph")
    return traces


def _vertex_text(v: Vertex) -> str:
    """Text of a vertex: tuples as ``(a, 0)`` instead of ``('a', 0)``."""
    if isinstance(v, tuple):
        return "(" + ", ".join(str(part) for part in v) + ")"
    return str(v)


def _info(attributes: Mapping[str, Any]) -> str:
    """Attributes for the tooltip (without position and label)."""
    shown = {key: value for key, value in attributes.items() if key not in ("pos", "label")}
    return "\n".join(f"{key}: {format_value(value)}" for key, value in shown.items())


def _slug(text: str) -> str:
    return re.sub(r"[^\w\-]+", "_", text, flags=re.ASCII).strip("_")[:60] or "graph"


def _remove_old_files(folder: Path, max_age_days: float = 3) -> None:
    """Delete player pages older than ``max_age_days`` (keeps the folder small)."""
    limit = time.time() - max_age_days * 24 * 3600
    for old in folder.glob("*.html"):
        try:
            if old.stat().st_mtime < limit:
                old.unlink()
        except OSError:
            pass


def _in_notebook() -> bool:
    """Return ``True`` inside a Jupyter notebook."""
    shell = sys.modules.get("IPython")
    if shell is None:
        return False
    try:
        ip = shell.get_ipython()  # type: ignore[attr-defined]
    except AttributeError:
        return False
    return ip is not None and ip.__class__.__name__ == "ZMQInteractiveShell"
