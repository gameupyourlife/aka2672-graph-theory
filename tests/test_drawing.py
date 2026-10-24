"""Tests for lib.visualization.draw() (only if matplotlib is installed).

The tests use the non-interactive "Agg" backend, so no windows open.
"""

import pytest

matplotlib = pytest.importorskip("matplotlib")
matplotlib.use("Agg", force=True)
import matplotlib.pyplot as plt  # noqa: E402

from lib import generators, visualization  # noqa: E402
from lib.graph import Edge, Graph  # noqa: E402


@pytest.fixture(autouse=True)
def close_figures():  # type: ignore[no-untyped-def]
    yield
    plt.close("all")


def texts(drawing: visualization.GraphDrawing) -> list[str]:
    return [t.get_text() for t in drawing.ax.texts]


def test_draw_returns_updatable_drawing() -> None:
    graph = generators.small_weighted_graph()
    drawing = visualization.draw(graph, title="Lönneberga")
    assert isinstance(drawing, visualization.GraphDrawing)
    assert set(drawing.positions) == set(graph.vertices())
    assert drawing.ax.get_title() == "Lönneberga"
    assert "Katthult" in texts(drawing)
    assert "7" in texts(drawing)  # weight label
    drawing.update(title="Schritt 2", highlight_vertices=["Kirche"])
    assert drawing.ax.get_title() == "Schritt 2"
    assert drawing.options["highlight_vertices"] == ("Kirche",)


def test_update_rejects_unknown_options() -> None:
    drawing = visualization.draw(generators.path_graph(3))
    with pytest.raises(TypeError):
        drawing.update(colour="red")


def test_draw_does_not_block_and_keeps_figure_open() -> None:
    before = len(plt.get_fignums())
    visualization.draw(generators.cycle_graph(5))
    visualization.draw(generators.cycle_graph(6))
    assert len(plt.get_fignums()) == before + 2


def test_draw_to_file(tmp_path) -> None:  # type: ignore[no-untyped-def]
    path = tmp_path / "petersen.png"
    visualization.draw(generators.petersen_graph(), shells=[range(5), range(5, 10)], filename=path)
    assert path.stat().st_size > 1000
    assert not plt.get_fignums()  # the figure is closed after saving


def test_highlight_edges_accepts_edge_objects() -> None:
    graph = generators.small_weighted_graph()
    edges = graph.edges()[:3]
    drawing = visualization.draw(graph, highlight_edges=edges)
    assert all(isinstance(e, Edge) for e in drawing.options["highlight_edges"])


def test_colours_legend_and_labels() -> None:
    graph = Graph.from_edges([("a", "b"), ("b", "c"), ("c", "d"), ("d", "a")])
    drawing = visualization.draw(
        graph,
        vertex_colors={"a": "rot", "b": "blau", "c": "rot", "d": "blau"},
        vertex_labels={"a": "Start"},
        edge_labels={("b", "a"): "3/5"},
    )
    legend = drawing.ax.get_legend()
    assert legend is not None
    assert sorted(t.get_text() for t in legend.get_texts()) == ["blau", "rot"]
    assert "Start" in texts(drawing)
    assert "3/5" in texts(drawing)
    assert "1" not in texts(drawing)  # unweighted: no weight labels


def test_directed_graph_with_antiparallel_edges() -> None:
    graph = Graph.from_edges([("a", "b", 2), ("b", "a", 3), ("b", "c", 1)], directed=True)
    drawing = visualization.draw(graph)
    assert {"2", "3", "1"} <= set(texts(drawing))


@pytest.mark.parametrize(
    "kwargs",
    [
        {"layout": "spring"},
        {"layout": "circular"},
        {"layout": "bipartite", "left": ["L0", "L1"]},
        {"left": ["L0", "L1"]},
        {"layers": [["L0"], ["R0", "R1"]]},
        {"shells": [["L0", "L1"]]},
        {"layout": {"L0": (0, 0), "L1": (0, 1), "R0": (1, 0), "R1": (1, 1), "R2": (1, 2)}},
    ],
)
def test_layout_options(kwargs: dict) -> None:  # type: ignore[type-arg]
    graph = generators.complete_bipartite_graph(2, 3)
    drawing = visualization.draw(graph, **kwargs)
    assert set(drawing.positions) == set(graph.vertices())


@pytest.mark.parametrize(
    "kwargs",
    [{"layout": "nonsense"}, {"layout": "bipartite"}, {"layout": "layered"}, {"layout": {"L0": (0, 0)}}],
)
def test_invalid_layouts(kwargs: dict) -> None:  # type: ignore[type-arg]
    with pytest.raises(ValueError):
        visualization.draw(generators.complete_bipartite_graph(2, 3), **kwargs)


def test_empty_graph() -> None:
    drawing = visualization.draw(Graph(), title="leer")
    assert drawing.positions == {}


def test_pause_and_wait_return_immediately_without_windows() -> None:
    visualization.draw(generators.path_graph(3))
    visualization.pause(5)  # Agg backend: must not sleep
    visualization.wait_for_windows()


def test_can_draw_respects_environment(monkeypatch: pytest.MonkeyPatch) -> None:
    assert visualization.can_draw()
    monkeypatch.setenv(visualization.NO_PLOTS_ENV_VAR, "1")
    assert not visualization.can_draw()
