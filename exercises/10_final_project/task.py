"""Einheit 10 – Das Netzwerk von Nangijala.

Bearbeite mit deiner Gruppe Modul A und mindestens zwei der Module B bis F.
Modul G ist optional. Nutze die vorbereiteten Daten und die Funktionen aus
den früheren Einheiten. Stelle eure Ergebnisse in zehn Minuten vor und
begründe für jedes Modul, warum der verwendete Algorithmus anwendbar ist.

Bearbeite die TODOs direkt an den Funktionen. Ersetze dort jeweils
``raise NotImplementedError(...)`` durch deinen Code.

Starte die Tests im Projektordner mit diesem Befehl.

    python -m pytest exercises/10_final_project
"""

import sys
from collections.abc import Iterable, Mapping
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))  # find ``lib``

from lib.graph import Edge, Graph, Vertex
from lib.utils import format_path, load_exercise, load_module_from_path
from lib.visualization import print_graph

# Verwende mit "task" deine Lösungen aus den früheren Einheiten.
# Mit "demo_solution" kannst du auf die Musterlösungen umschalten, sofern sie vorliegen.
PREVIOUS = "task"

bfs_dfs = load_exercise("02_bfs_dfs", PREVIOUS)  # bfs, dfs, connected_components, ...
spanning_trees = load_exercise("03_spanning_trees", PREVIOUS)  # kruskal, ...
shortest_paths = load_exercise("04_shortest_paths", PREVIOUS)  # dijkstra, ...
coloring = load_exercise("06_graph_coloring", PREVIOUS)  # greedy_coloring, ...
matching = load_exercise("07_matching", PREVIOUS)  # maximum_bipartite_matching
max_flow = load_exercise("08_max_flow", PREVIOUS)  # edmonds_karp

data = load_module_from_path(Path(__file__).with_name("nangijala_data.py"))


# ----------------------------------------------------------------------
# Module A: modelling
# ----------------------------------------------------------------------
def build_network(roads: Iterable[tuple[str, str, float]]) -> Graph:
    """Return the undirected road network; edge weight = travel time in minutes.

    Args:
        roads: Triples ``(place, place, minutes)`` such as ``data.ROADS``.
    """
    # TODO: Füge pro Straße eine ungerichtete Kante mit der Reisezeit als Gewicht ein.
    # Zeichne anschließend das Netz aus data.ROADS und prüfe das Handschlaglemma.
    raise NotImplementedError("TODO: build_network")


def without_places(graph: Graph, blocked: Iterable[Vertex]) -> Graph:
    """Return a copy of ``graph`` in which the ``blocked`` places are removed.

    The input graph is not modified.

    Raises:
        KeyError: If a blocked place is not a vertex of the graph.
    """
    # TODO: copy the graph, then remove every blocked vertex from the copy.
    raise NotImplementedError("TODO: without_places")


# ----------------------------------------------------------------------
# Module B: connectivity and reachability (unit 2)
# ----------------------------------------------------------------------
def reachable_places(graph: Graph, start: Vertex, blocked: Iterable[Vertex] = ()) -> set[Vertex]:
    """Return all places reachable from ``start`` if the ``blocked`` places are closed.

    Raises:
        KeyError: If ``start`` or a blocked place is not in the graph.
        ValueError: If ``start`` itself is blocked.
    """
    # TODO: use without_places() and a search from unit 2 (bfs_dfs.dfs or bfs_dfs.bfs).
    # Prüfe am Beispielnetz die Erreichbarkeit vom Reiterhof aus, wenn
    # Bärenpass und Adlerhorst gesperrt sind.
    raise NotImplementedError("TODO: reachable_places")


def critical_places(graph: Graph) -> list[Vertex]:
    """Return all *cut vertices*: places whose closure splits the network.

    A vertex ``v`` is a cut vertex if ``G - v`` has more connected components
    than ``G``. Return them in the order of ``graph.vertices()``.
    """
    # TODO: for every vertex v: count the components of without_places(graph, [v])
    #       with bfs_dfs.connected_components and compare with the original.
    raise NotImplementedError("TODO: critical_places")


# ----------------------------------------------------------------------
# Module C: spanning trees (unit 3)
# ----------------------------------------------------------------------
def winter_roads(graph: Graph) -> tuple[list[Edge], float]:
    """Return the roads to clear of snow so that all places stay connected,
    with minimum total travel time, and that total.

    Returns:
        ``(edges, total_minutes)`` of a minimum spanning tree (forest).
    """
    # TODO: use spanning_trees.kruskal.
    raise NotImplementedError("TODO: winter_roads")


# ----------------------------------------------------------------------
# Module D: shortest paths (unit 4)
# ----------------------------------------------------------------------
def fastest_route(
    graph: Graph, start: Vertex, target: Vertex, blocked: Iterable[Vertex] = ()
) -> tuple[list[Vertex], float] | None:
    """Return the fastest route ``(path, minutes)`` avoiding the ``blocked`` places.

    Returns ``None`` if ``target`` cannot be reached.

    Raises:
        KeyError: If ``start``, ``target`` or a blocked place is not in the graph.
        ValueError: If ``start`` or ``target`` is blocked.
    """
    # TODO: use without_places() and shortest_paths.dijkstra / reconstruct_path.
    # Suche im Beispielnetz den schnellsten Weg vom Reiterhof zu Tengils Burg
    # und zum Marktplatz bei gesperrtem Bärenpass und Waldsee.
    raise NotImplementedError("TODO: fastest_route")


# ----------------------------------------------------------------------
# Module E: colouring (unit 6)
# ----------------------------------------------------------------------
def lantern_colors(graph: Graph) -> dict[Vertex, int]:
    """Assign a lantern colour (0, 1, 2, ...) to every place such that
    neighbouring places have different colours, using as few colours as you can.

    Try greedy colouring with several vertex orders and return the best result.
    """
    # TODO: use coloring.greedy_coloring with at least two different orders.
    raise NotImplementedError("TODO: lantern_colors")


# ----------------------------------------------------------------------
# Module F: matching (unit 7)
# ----------------------------------------------------------------------
def assign_tasks(qualifications: Mapping[str, Iterable[str]]) -> dict[str, str]:
    """Assign tasks to people: everyone gets at most one task they are
    qualified for, every task goes to at most one person, and as many people
    as possible get a task.

    Args:
        qualifications: ``person -> tasks`` such as ``data.QUALIFICATIONS``.

    Returns:
        Dictionary ``person -> task``.

    Raises:
        ValueError: If a name is used both as a person and as a task.
    """
    # TODO: build a bipartite graph (people on the left) and use
    #       matching.maximum_bipartite_matching.
    raise NotImplementedError("TODO: assign_tasks")


# ----------------------------------------------------------------------
# Module G (optional): maximum flow (unit 8)
# ----------------------------------------------------------------------
def max_supply(
    routes: Iterable[tuple[str, str, float]], source: str, sink: str
) -> tuple[float, dict[tuple[Vertex, Vertex], float]]:
    """OPTIONAL: Return the maximum number of sacks per night from ``source``
    to ``sink`` and a corresponding flow.

    Args:
        routes: Directed triples ``(from, to, capacity)`` such as ``data.SUPPLY_ROUTES``.

    Raises:
        Same errors as ``max_flow.edmonds_karp``.
    """
    # TODO (optional): build a directed graph and use max_flow.edmonds_karp.
    # Prüfe data.SUPPLY_ROUTES mit "Kirschtal" als Quelle und "Heckenrosental" als Senke.
    raise NotImplementedError("TODO (optional): max_supply")


if __name__ == "__main__":
    nangijala = build_network(data.ROADS)
    print_graph(nangijala)
    print("Reachable with Bärenpass and Adlerhorst closed:",
          sorted(reachable_places(nangijala, "Reiterhof", ["Bärenpass", "Adlerhorst"])))
    print("Critical places:", critical_places(nangijala))
    edges, total = winter_roads(nangijala)
    print(f"Winter roads: {len(edges)} roads, {total} minutes")
    route = fastest_route(nangijala, "Reiterhof", "Tengils Burg")
    if route is not None:
        print("Fastest route:", format_path(route[0]), f"({route[1]} minutes)")
    print("Lantern colours:", lantern_colors(nangijala))
    print("Tasks:", assign_tasks(data.QUALIFICATIONS))
