"""Tests for the recording of algorithm steps (lib/trace.py)."""

from collections import deque

import pytest

from lib.graph import Graph
from lib.trace import DEFAULT_STYLES, Trace, format_value


@pytest.fixture
def graph() -> Graph:
    return Graph.from_edges([("A", "B", 2), ("B", "C", 1), ("A", "C", 5)])


def test_flags_and_steps(graph: Graph) -> None:
    trace = Trace(graph, "Test")
    trace.flag("A", "visited", "start")
    trace.flag_edge("B", "A", "tree")  # undirected: orientation does not matter
    assert trace.step("first") == 0
    trace.unflag("A", "start")
    trace.step("second")
    assert len(trace) == 2
    first, second = trace.frames
    assert first.vertex_flags == {"A": ("start", "visited")}
    assert second.vertex_flags == {"A": ("visited",)}
    assert first.edge_flags == {("A", "B"): ("tree",)}
    assert first.message == "first"
    assert trace.flags("A") == {"visited"}
    assert trace.edge_flags("A", "B") == {"tree"}


def test_frames_are_independent_copies(graph: Graph) -> None:
    trace = Trace(graph)
    trace.flag("A", "visited")
    trace.step()
    trace.unflag("A")
    trace.label("B", 3.0)
    trace.step()
    assert trace.frames[0].vertex_flags == {"A": ("visited",)}
    assert trace.frames[0].vertex_labels == {}
    assert trace.frames[1].vertex_flags == {}
    assert trace.frames[1].vertex_labels == {"B": "3"}


def test_trace_copies_the_graph(graph: Graph) -> None:
    trace = Trace(graph)
    graph.add_edge("C", "D")
    assert "D" not in trace.graph
    with pytest.raises(KeyError):
        trace.flag("D", "visited")


def test_current_and_flag_only(graph: Graph) -> None:
    trace = Trace(graph)
    trace.current("A")
    trace.current("B")
    assert trace.flags("A") == set()
    assert trace.flags("B") == {"current"}
    trace.current(None)
    assert trace.flags("B") == set()
    trace.current_edge("A", "B")
    trace.current_edge("C", "B")
    assert trace.edge_flags("A", "B") == set()
    assert trace.edge_flags("B", "C") == {"current"}
    trace.current_edge(None)
    assert trace.edge_flags("B", "C") == set()
    trace.flag_only("visited", ["A", "C"])
    assert trace.flags("A") == {"visited"} and trace.flags("B") == set()


def test_flag_path_and_clear(graph: Graph) -> None:
    trace = Trace(graph)
    trace.flag_path(["A", "B", "C"])
    assert trace.edge_flags("A", "B") == {"path"}
    assert trace.flags("C") == {"path"}
    trace.flag("A", "visited")
    trace.clear("path")
    assert trace.flags("A") == {"visited"}
    assert trace.edge_flags("B", "C") == set()
    trace.clear()
    assert trace.flags("A") == set()


def test_labels_colors_variables(graph: Graph) -> None:
    trace = Trace(graph)
    trace.label("A", "d = 0")
    trace.edge_label("C", "A", "3/5")
    trace.color("B", 2)
    queue = deque(["A", "B"])
    trace.variable("queue", queue)
    queue.append("C")  # later changes do not change the recorded value
    trace.step()
    frame = trace.frames[0]
    assert frame.vertex_labels == {"A": "d = 0"}
    assert frame.edge_labels == {("A", "C"): "3/5"}
    assert frame.vertex_colors == {"B": 2}
    assert frame.variables == (("queue", "[A, B]"),)
    trace.label("A", None)
    trace.edge_label("A", "C", None)
    trace.color("B", None)
    trace.remove_variable("queue")
    trace.remove_variable("does not exist")
    trace.step()
    frame = trace.frames[1]
    assert (frame.vertex_labels, frame.edge_labels, frame.vertex_colors, frame.variables) == ({}, {}, {}, ())


def test_directed_edges_keep_their_direction() -> None:
    graph = Graph.from_edges([("s", "t")], directed=True)
    trace = Trace(graph)
    trace.flag_edge("s", "t", "flow")
    with pytest.raises(KeyError):
        trace.flag_edge("t", "s", "flow")


def test_unknown_vertices_and_edges_raise(graph: Graph) -> None:
    trace = Trace(graph)
    for call in [
        lambda: trace.flag("X", "visited"),
        lambda: trace.label("X", "1"),
        lambda: trace.color("X", 1),
        lambda: trace.flag_edge("A", "X", "tree"),
        lambda: trace.edge_label("A", "X", "1"),
        lambda: trace.current("X"),
    ]:
        with pytest.raises(KeyError):
            call()


def test_pseudocode_lines() -> None:
    trace = Trace(Graph(), pseudocode=["first", "second"])
    trace.step("ok", line=2)
    assert trace.frames[0].line == 2
    with pytest.raises(ValueError):
        trace.step("bad", line=3)
    with pytest.raises(ValueError):
        Trace(Graph()).step("no pseudocode", line=1)


def test_styles() -> None:
    trace = Trace(Graph())
    assert trace.styles["visited"] == DEFAULT_STYLES["visited"]
    trace.style("infected", fill="#fecaca", description="infected")
    trace.style("visited", fill="#000000")
    assert trace.styles["infected"].fill == "#fecaca"
    assert trace.styles["visited"].fill == "#000000"
    assert DEFAULT_STYLES["visited"].fill != "#000000"  # defaults unchanged
    assert trace.styles["visited"].as_dict()["description"] == "visited"
    with pytest.raises(TypeError):
        trace.style("x", colour="red")


@pytest.mark.parametrize(
    ("value", "text"),
    [
        ("A", "A"),
        (3.0, "3"),
        (2.5, "2.5"),
        (float("inf"), "∞"),
        (None, "-"),
        ([1, "B"], "[1, B]"),
        (deque([1, 2]), "[1, 2]"),
        ((1, 2), "(1, 2)"),
        ({"B", "A"}, "{A, B}"),
        ({"A": 1.0}, "{A: 1}"),
        (True, "True"),
        (7, "7"),
    ],
)
def test_format_value(value: object, text: str) -> None:
    assert format_value(value) == text
