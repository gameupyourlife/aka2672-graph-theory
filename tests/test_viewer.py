"""Tests for the browser player (lib/viewer.py).

The JavaScript part is tested by hand in a browser; these tests check the
data that is handed to it and the written HTML file.
"""

import json
import re
from pathlib import Path

import pytest

from lib import generators, viewer
from lib.graph import Graph
from lib.trace import Trace


@pytest.fixture(autouse=True)
def no_browser(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv(viewer.NO_PLOTS_ENV_VAR, "1")


def page_data(html: str) -> dict:  # type: ignore[type-arg]
    match = re.search(r'<script type="application/json" id="graph-data">(.*?)</script>', html, re.S)
    assert match is not None
    return json.loads(match.group(1))


def test_scene_data_of_a_trace() -> None:
    graph = Graph.from_edges([("A", "B", 2), ("B", "C", 1)])
    trace = Trace(graph, "BFS", pseudocode=["x", "y"], description="about")
    trace.flag("A", "visited")
    trace.flag_edge("A", "B", "tree")
    trace.label("B", "d = 1")
    trace.color("C", "rot")
    trace.variable("queue", ["B"])
    trace.step("hello", line=2)
    data = viewer.scene_data(trace)
    assert data["title"] == "BFS"
    assert data["showWeights"] is True
    assert [v["text"] for v in data["vertices"]] == ["A", "B", "C"]
    assert all(0 <= v["x"] <= 1 and 0 <= v["y"] <= 1 for v in data["vertices"])
    assert data["edges"][0] == {"u": 0, "v": 1, "w": "2", "curved": False}
    frame = data["frames"][0]
    assert frame == {
        "m": "hello",
        "l": 2,
        "vf": {0: ["visited"]},
        "ef": {0: ["tree"]},
        "vl": {1: "d = 1"},
        "el": {},
        "vc": {2: 0},
        "vars": [["queue", "[B]"]],
    }
    assert set(data["styles"]) == {"visited", "tree"}
    kinds = {entry["kind"] for entry in data["legend"]}
    assert kinds == {"vertex", "edge", "color"}


def test_trace_without_steps_shows_current_state() -> None:
    trace = Trace(generators.path_graph(3))
    trace.flag(1, "current")
    data = viewer.scene_data(trace)
    assert len(data["frames"]) == 1
    assert data["frames"][0]["vf"] == {1: ["current"]}


def test_unknown_flags_get_automatic_styles() -> None:
    trace = Trace(generators.path_graph(3))
    trace.flag(0, "infected")
    trace.flag(1, "immune")
    trace.step()
    styles = viewer.scene_data(trace)["styles"]
    assert styles["infected"]["color"] != styles["immune"]["color"]
    assert styles["infected"]["description"] == "infected"


def test_curved_antiparallel_edges_and_tuple_names() -> None:
    graph = Graph.from_edges([(("a", 0), ("b", 1)), (("b", 1), ("a", 0))], directed=True)
    data = viewer.scene_data(Trace(graph))
    assert [e["curved"] for e in data["edges"]] == [True, True]
    assert data["vertices"][0]["text"] == "(a, 0)"


def test_vertex_attributes_are_used() -> None:
    graph = Graph()
    graph.add_vertex("A", pos=(0, 0), label="Anfang", population=12)
    graph.add_vertex("B", pos=(4, 0))
    graph.add_edge("A", "B")
    data = viewer.scene_data(Trace(graph))
    a, b = data["vertices"]
    assert a["text"] == "Anfang"
    assert a["info"] == "population: 12"
    assert (a["x"], b["x"]) == (0, 1)


def test_snapshot() -> None:
    graph = generators.cycle_graph(4)
    trace = viewer.snapshot(
        graph,
        "Bild",
        message="msg",
        highlight_vertices=[0],
        highlight_edges=[(1, 0)],
        vertex_flags={2: ["start"]},
        edge_flags={(2, 3): ["tree"]},
        vertex_colors={3: 1},
        vertex_labels={1: "x"},
        edge_labels={(3, 0): "7"},
        layout="circular",
    )
    assert len(trace) == 1
    frame = trace.frames[0]
    assert frame.vertex_flags == {0: ("highlight",), 2: ("start",)}
    assert frame.edge_flags == {(0, 1): ("highlight",), (2, 3): ("tree",)}
    assert frame.message == "msg"


def test_show_writes_a_self_contained_page(tmp_path: Path) -> None:
    trace = viewer.snapshot(generators.petersen_graph(), "Petersen </script> test", shells=[range(5), range(5, 10)])
    path = viewer.show(trace, generators.path_graph(3), filename=tmp_path / "page.html")
    html = path.read_text(encoding="utf-8")
    assert html.startswith("<!DOCTYPE html>")
    assert "@@" not in html  # all placeholders replaced
    assert "http" not in re.sub(r'xmlns="http://www\.w3\.org/2000/svg"|"http://www\.w3\.org/2000/svg"', "", html)
    data = page_data(html)
    assert data["title"] == "Petersen </script> test"
    assert len(data["scenes"]) == 2
    assert html.count("</script>") == 2  # the title did not close the data block


def test_show_default_file_and_draw(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(viewer, "OUTPUT_DIR", tmp_path)
    first = viewer.draw(generators.path_graph(3), "Pfad", highlight_edges=[(0, 1)])
    second = viewer.draw(generators.path_graph(3), "Pfad")
    assert first != second  # every call gets its own file
    assert first.parent == tmp_path and first.exists()


def test_show_opens_browser(monkeypatch: pytest.MonkeyPatch, tmp_path: Path) -> None:
    opened = []
    monkeypatch.setattr(viewer.webbrowser, "open", opened.append)
    viewer.show(generators.path_graph(2), filename=tmp_path / "a.html", open_browser=True)
    assert opened and opened[0].startswith("file:")
    viewer.show(generators.path_graph(2), filename=tmp_path / "b.html")  # env var set: no browser
    assert len(opened) == 1


def test_show_needs_a_scene() -> None:
    with pytest.raises(ValueError):
        viewer.show()


def test_notebook_html() -> None:
    frame = viewer.notebook_html([generators.path_graph(2)])
    assert frame.startswith("<iframe srcdoc=")
    assert "&lt;!DOCTYPE html&gt;" in frame


def test_empty_graph() -> None:
    data = viewer.scene_data(Trace(Graph(), "leer"))
    assert data["vertices"] == [] and len(data["frames"]) == 1
