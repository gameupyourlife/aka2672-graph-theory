"""Record the steps of a graph algorithm for the step-by-step player.

A :class:`Trace` is a "film" of an algorithm. While the algorithm runs, it
describes its current state - which vertices are visited, which one is
being processed, what is in the queue - and calls :meth:`Trace.step` to
take a picture (a :class:`Frame`). The player in :mod:`lib.viewer` then
shows the pictures one after another: forwards, backwards or automatically.

Example (breadth-first search)::

    from lib.trace import Trace
    from lib.viewer import show

    trace = Trace(graph, "BFS from A")
    trace.flag("A", "queued")
    trace.variable("queue", ["A"])
    trace.step("Put the start vertex A into the queue")
    ...
    show(trace)

The state consists of

* **flags** of vertices and edges, e.g. ``"visited"``, ``"current"``,
  ``"tree"`` - any names are allowed; :data:`DEFAULT_STYLES` defines how
  the usual ones look, :meth:`Trace.style` defines new ones,
* **labels**: a short text below a vertex (e.g. a distance) or on an edge
  (e.g. ``"3/5"`` for a flow),
* **colours**: a colour class per vertex (e.g. the result of a colouring),
* **variables**: named values shown in a side panel (e.g. the queue),
* the current line of an optional **pseudocode** listing.

The state stays as it is until you change it; :meth:`Trace.step` records a
copy of the whole state. That is why you can step backwards in the player.
"""

from __future__ import annotations

from collections import deque
from collections.abc import Iterable, Mapping, Sequence
from dataclasses import dataclass, fields, replace
from typing import Any

from lib.graph import Graph, Vertex


@dataclass(frozen=True)
class Style:
    """How vertices or edges with a certain flag are drawn.

    ``None`` means "not set by this flag". If an element has several flags,
    the flag with the higher ``priority`` wins for every property it sets.

    Attributes:
        description: Text for the legend, e.g. ``"visited"``.
        fill: Fill colour of a vertex box (CSS colour, e.g. ``"#b7e4c7"``).
        color: Border colour of a vertex, or colour of an edge.
        width: Border width of a vertex, or line width of an edge.
        text: Colour of the vertex name.
        halo: Colour of a glow around the vertex or edge.
        dash: Draw the border / the edge dashed.
        fade: Draw the element pale (e.g. removed or rejected elements).
        priority: Flags with higher priority win.
    """

    description: str = ""
    fill: str | None = None
    color: str | None = None
    width: float | None = None
    text: str | None = None
    halo: str | None = None
    dash: bool | None = None
    fade: bool | None = None
    priority: int = 50

    def as_dict(self) -> dict[str, Any]:
        """Return the style as a dictionary (without unset properties)."""
        return {f.name: getattr(self, f.name) for f in fields(self) if getattr(self, f.name) is not None}


DEFAULT_STYLES: dict[str, Style] = {
    # Vertex states during a search
    "queued": Style("discovered, waiting (queue/stack)", fill="#dbeafe", color="#1d4ed8", dash=True, priority=40),
    "visited": Style("visited", fill="#bbf7d0", color="#15803d", priority=45),
    "finished": Style("finished", fill="#d1d5db", color="#4b5563", text="#374151", priority=50),
    "current": Style("current", fill="#fde68a", color="#d97706", width=3.5, halo="#fbbf24", priority=90),
    # Roles of vertices
    "start": Style("start / source", color="#7c3aed", width=3.5, priority=60),
    "target": Style("target / sink", color="#be123c", width=3.5, priority=60),
    # General purpose (vertices and edges)
    "highlight": Style("highlighted", color="#dc2626", width=4, priority=70),
    "path": Style("path", color="#dc2626", width=4.5, priority=75),
    "rejected": Style("rejected", color="#dc2626", dash=True, fade=True, priority=65),
    "inactive": Style("removed / inactive", fade=True, priority=30),
    "conflict": Style("conflict", fill="#fecdd3", color="#be123c", width=3.5, priority=80),
    # Edge roles
    "tree": Style("tree edge", color="#15803d", width=4.5, priority=55),
    "matched": Style("matching edge", color="#7c3aed", width=5, priority=55),
    "flow": Style("carries flow", color="#2563eb", width=3.5, priority=50),
    "saturated": Style("saturated (flow = capacity)", color="#1e3a8a", width=5, priority=52),
    "cut": Style("cut edge", color="#be123c", width=4.5, dash=True, priority=72),
}
"""Built-in flags and their styles. ``"current"`` on an edge means "the edge
that is being looked at right now"."""

# Colours for flags without a style. The player assigns them in the order in
# which the flags first appear; define a style with Trace.style() instead.
AUTO_COLORS =["#0891b2", "#c026d3", "#65a30d", "#ea580c", "#4f46e5", "#0d9488", "#db2777", "#a16207"]


@dataclass(frozen=True)
class Frame:
    """One recorded step: a complete copy of the state of a :class:`Trace`.

    Attributes:
        message: Explanation of the step.
        line: Current line of the pseudocode (1-based) or ``None``.
        vertex_flags: Vertex -> its flags.
        edge_flags: Edge ``(u, v)`` -> its flags.
        vertex_labels: Vertex -> text below the vertex.
        edge_labels: Edge ``(u, v)`` -> text on the edge.
        vertex_colors: Vertex -> colour class.
        variables: ``(name, value as text)`` pairs for the side panel.
    """

    message: str
    line: int | None
    vertex_flags: Mapping[Vertex, tuple[str, ...]]
    edge_flags: Mapping[tuple[Vertex, Vertex], tuple[str, ...]]
    vertex_labels: Mapping[Vertex, str]
    edge_labels: Mapping[tuple[Vertex, Vertex], str]
    vertex_colors: Mapping[Vertex, Any]
    variables: tuple[tuple[str, str], ...]


class Trace:
    """Records the steps of an algorithm on a graph.

    Args:
        graph: The graph the algorithm works on. The trace keeps its own
            copy, so later changes of ``graph`` do not matter.
        title: Title of the scene in the player.
        description: Optional longer explanation shown next to the graph.
        pseudocode: Optional lines of pseudocode; :meth:`step` can mark the
            current line.
        layout: Vertex placement: ``"auto"``, ``"spring"``, ``"circular"``,
            ``"shell"``, ``"bipartite"``, ``"layered"``, ``"grid"`` or a
            dictionary ``vertex -> (x, y)`` (see :mod:`lib.layout`). With
            ``"auto"``, the vertex attribute ``"pos"`` is used if every
            vertex has one.
        left: Left side for ``layout="bipartite"``.
        layers: Vertex lists for ``layout="layered"``.
        shells: Vertex lists for ``layout="shell"``.
        seed: Seed for the spring layout.
        show_weights: Show edge weights (``None``: if some weight is not 1).

    Raises:
        KeyError: Whenever a method is called with a vertex or edge that is
            not in the graph - this helps to find mistakes early.
    """

    def __init__(
        self,
        graph: Graph,
        title: str = "",
        *,
        description: str = "",
        pseudocode: Sequence[str] | None = None,
        layout: str | Mapping[Vertex, tuple[float, float]] = "auto",
        left: Iterable[Vertex] | None = None,
        layers: Sequence[Sequence[Vertex]] | None = None,
        shells: Sequence[Sequence[Vertex]] | None = None,
        seed: int = 0,
        show_weights: bool | None = None,
    ) -> None:
        """Create an empty trace for ``graph``."""
        self.graph = graph.copy()
        self.title = title
        self.description = description
        self.pseudocode = list(pseudocode) if pseudocode is not None else []
        self.layout = layout
        self.left = list(left) if left is not None else None
        self.layers = [list(layer) for layer in layers] if layers is not None else None
        self.shells = [list(shell) for shell in shells] if shells is not None else None
        self.seed = seed
        self.show_weights = show_weights
        self.styles: dict[str, Style] = dict(DEFAULT_STYLES)
        self.frames: list[Frame] = []

        # Every edge gets one key: (u, v) as listed by graph.edges().
        # For undirected graphs (v, u) is mapped to the same key.
        self._edge_keys: dict[tuple[Vertex, Vertex], tuple[Vertex, Vertex]] = {}
        for u, v, _ in self.graph.edges():
            self._edge_keys[(u, v)] = (u, v)
            if not self.graph.directed:
                self._edge_keys[(v, u)] = (u, v)

        self._vertex_flags: dict[Vertex, set[str]] = {}
        self._edge_flags: dict[tuple[Vertex, Vertex], set[str]] = {}
        self._vertex_labels: dict[Vertex, str] = {}
        self._edge_labels: dict[tuple[Vertex, Vertex], str] = {}
        self._vertex_colors: dict[Vertex, Any] = {}
        self._variables: dict[str, str] = {}

    # ------------------------------------------------------------------
    # Flags
    # ------------------------------------------------------------------
    def flag(self, v: Vertex, *names: str) -> None:
        """Give the vertex ``v`` the flags ``names`` (it keeps its other flags).

        Example: ``trace.flag("A", "visited")``
        """
        self._require_vertex(v)
        self._vertex_flags.setdefault(v, set()).update(names)

    def unflag(self, v: Vertex, *names: str) -> None:
        """Remove the flags ``names`` from ``v`` (all flags if no name is given)."""
        self._require_vertex(v)
        current = self._vertex_flags.get(v, set())
        if names:
            current.difference_update(names)
        else:
            current.clear()

    def flags(self, v: Vertex) -> set[str]:
        """Return the current flags of the vertex ``v`` (a copy)."""
        self._require_vertex(v)
        return set(self._vertex_flags.get(v, set()))

    def flag_edge(self, u: Vertex, v: Vertex, *names: str) -> None:
        """Give the edge ``u -- v`` / ``u -> v`` the flags ``names``.

        Example: ``trace.flag_edge("A", "B", "tree")``
        """
        self._edge_flags.setdefault(self._edge_key(u, v), set()).update(names)

    def unflag_edge(self, u: Vertex, v: Vertex, *names: str) -> None:
        """Remove the flags ``names`` from an edge (all flags if no name is given)."""
        current = self._edge_flags.get(self._edge_key(u, v), set())
        if names:
            current.difference_update(names)
        else:
            current.clear()

    def edge_flags(self, u: Vertex, v: Vertex) -> set[str]:
        """Return the current flags of an edge (a copy)."""
        return set(self._edge_flags.get(self._edge_key(u, v), set()))

    def current(self, v: Vertex | None) -> None:
        """Make ``v`` the only vertex with the flag ``"current"`` (``None``: no vertex)."""
        self.flag_only("current", [] if v is None else [v])

    def current_edge(self, u: Vertex | None, v: Vertex | None = None) -> None:
        """Make ``u -- v`` the only edge with the flag ``"current"`` (``None``: no edge)."""
        self.flag_only_edges("current", [] if u is None else [(u, v)])

    def flag_only(self, name: str, vertices: Iterable[Vertex]) -> None:
        """Set the flag ``name`` on exactly these vertices and remove it from all others."""
        chosen = list(vertices)
        for v in chosen:
            self._require_vertex(v)
        for flags in self._vertex_flags.values():
            flags.discard(name)
        for v in chosen:
            self.flag(v, name)

    def flag_only_edges(self, name: str, edges: Iterable[tuple[Vertex, Vertex]]) -> None:
        """Set the flag ``name`` on exactly these edges and remove it from all others.

        ``edges`` may contain pairs ``(u, v)`` or ``Edge`` objects.
        """
        keys = [self._edge_key(edge[0], edge[1]) for edge in edges]
        for flags in self._edge_flags.values():
            flags.discard(name)
        for key in keys:
            self._edge_flags.setdefault(key, set()).add(name)

    def flag_path(self, path: Sequence[Vertex], name: str = "path", vertices: bool = True) -> None:
        """Flag all edges of ``path`` (a list of vertices), and its vertices too
        if ``vertices`` is ``True``."""
        for u, v in zip(path, path[1:]):
            self.flag_edge(u, v, name)
        if vertices:
            for v in path:
                self.flag(v, name)

    def clear(self, *names: str) -> None:
        """Remove the flags ``names`` from all vertices and edges.

        Without arguments, *all* flags are removed.
        """
        for flags in [*self._vertex_flags.values(), *self._edge_flags.values()]:
            if names:
                flags.difference_update(names)
            else:
                flags.clear()

    # ------------------------------------------------------------------
    # Labels, colours, variables
    # ------------------------------------------------------------------
    def label(self, v: Vertex, text: object | None) -> None:
        """Show ``text`` below the vertex ``v`` (``None`` removes it).

        Example: ``trace.label("B", "d = 1")``. Numbers are formatted with
        :func:`format_value`.
        """
        self._require_vertex(v)
        if text is None:
            self._vertex_labels.pop(v, None)
        else:
            self._vertex_labels[v] = format_value(text)

    def edge_label(self, u: Vertex, v: Vertex, text: object | None) -> None:
        """Show ``text`` on the edge instead of its weight (``None`` removes it).

        Example: ``trace.edge_label("s", "a", "3/5")``.
        """
        key = self._edge_key(u, v)
        if text is None:
            self._edge_labels.pop(key, None)
        else:
            self._edge_labels[key] = format_value(text)

    def color(self, v: Vertex, value: Any) -> None:
        """Give ``v`` the colour class ``value`` (any value, e.g. 0, 1, 2 or
        ``"rot"``); ``None`` removes it.

        Every class gets its own fill colour. The colour class always decides
        the fill of the vertex (flags then only change border, halo, ...), so
        that a colouring stays visible while an algorithm runs.
        """
        self._require_vertex(v)
        if value is None:
            self._vertex_colors.pop(v, None)
        else:
            self._vertex_colors[v] = value

    def variable(self, name: str, value: object) -> None:
        """Show ``name = value`` in the variables panel.

        Lists, sets, dictionaries and queues are shown in a readable way
        (see :func:`format_value`). The value is copied *as text* right now,
        so later changes of a list do not change the recorded steps.
        """
        self._variables[name] = format_value(value)

    def remove_variable(self, name: str) -> None:
        """Remove a variable from the panel (no error if it does not exist)."""
        self._variables.pop(name, None)

    # ------------------------------------------------------------------
    # Steps and styles
    # ------------------------------------------------------------------
    def step(self, message: str = "", line: int | None = None) -> int:
        """Record the current state as a new step.

        Args:
            message: What happens in this step (shown in the player).
            line: Current line of the pseudocode (1-based).

        Returns:
            The number of the step (0 for the first one).

        Raises:
            ValueError: If ``line`` is not a line of the pseudocode.
        """
        if line is not None and not 1 <= line <= len(self.pseudocode):
            raise ValueError(f"line must be between 1 and {len(self.pseudocode)}, got {line}")
        self.frames.append(self.capture(message, line))
        return len(self.frames) - 1

    def capture(self, message: str = "", line: int | None = None) -> Frame:
        """Return the current state as a :class:`Frame` without recording it."""
        return Frame(
            message=message,
            line=line,
            vertex_flags={v: tuple(sorted(f)) for v, f in self._vertex_flags.items() if f},
            edge_flags={e: tuple(sorted(f)) for e, f in self._edge_flags.items() if f},
            vertex_labels=dict(self._vertex_labels),
            edge_labels=dict(self._edge_labels),
            vertex_colors=dict(self._vertex_colors),
            variables=tuple(self._variables.items()),
        )

    def style(self, name: str, **properties: Any) -> None:
        """Define how the flag ``name`` is drawn (or change a built-in flag).

        The keyword arguments are the attributes of :class:`Style`, e.g.::

            trace.style("infected", fill="#fecaca", color="#b91c1c", description="infected")
        """
        base = self.styles.get(name, Style(description=name))
        self.styles[name] = replace(base, **properties)

    def __len__(self) -> int:
        """Number of recorded steps."""
        return len(self.frames)

    def __repr__(self) -> str:
        return f"Trace({self.title!r}, {len(self.frames)} steps)"

    def _repr_html_(self) -> str:  # pragma: no cover - only used by Jupyter
        from lib.viewer import notebook_html

        return notebook_html([self])

    # ------------------------------------------------------------------
    # Helpers
    # ------------------------------------------------------------------
    def _require_vertex(self, v: Vertex) -> None:
        if v not in self.graph:
            raise KeyError(f"Vertex {v!r} is not in the graph of this trace")

    def _edge_key(self, u: Vertex, v: Vertex) -> tuple[Vertex, Vertex]:
        try:
            return self._edge_keys[(u, v)]
        except KeyError:
            raise KeyError(f"Edge {u!r} -- {v!r} is not in the graph of this trace") from None


def format_value(value: object) -> str:
    """Return a short, readable text for ``value``.

    * strings are shown without quotes: ``"A"`` -> ``A``,
    * whole floats without ``.0``: ``3.0`` -> ``3``; ``inf`` -> ``∞``,
    * lists, tuples and queues: ``[A, B]``; sets sorted: ``{A, B}``,
    * dictionaries: ``{A: 1, B: 2}``; ``None`` -> ``–``.
    """
    if value is None:
        return "–"
    if isinstance(value, str):
        return value
    if isinstance(value, bool):
        return str(value)
    if isinstance(value, float):
        if value == float("inf"):
            return "∞"
        if value == float("-inf"):
            return "-∞"
        return str(int(value)) if value.is_integer() else f"{value:g}"
    if isinstance(value, (list, deque)):
        return "[" + ", ".join(format_value(x) for x in value) + "]"
    if isinstance(value, tuple):
        return "(" + ", ".join(format_value(x) for x in value) + ")"
    if isinstance(value, (set, frozenset)):
        items = [format_value(x) for x in value]
        return "{" + ", ".join(sorted(items)) + "}"
    if isinstance(value, Mapping):
        return "{" + ", ".join(f"{format_value(k)}: {format_value(v)}" for k, v in value.items()) + "}"
    return str(value)
