"""Unit 10: Final project "Das Netzwerk von Nangijala" - DEMO SOLUTION.

Every question of the project is answered by *modelling* it as a graph
problem and then calling an algorithm from an earlier unit:

======================  ==========================  =======================
question                graph problem               algorithm (unit)
======================  ==========================  =======================
Who can still meet?     reachability                DFS (2)
Which places are        cut vertices                connected components (2)
critical?
Which roads to clear    minimum spanning tree       Kruskal (3)
in winter?
Fastest route?          shortest path               Dijkstra (4)
Lantern colours?        vertex colouring            greedy colouring (6)
Who does which task?    bipartite matching          augmenting paths (7)
How much flour?         maximum flow                Edmonds-Karp (8)
======================  ==========================  =======================

This file uses the demo solutions of the earlier units.
"""

import sys
from collections.abc import Iterable, Mapping
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))  # find ``lib``

from lib.graph import Edge, Graph, Vertex
from lib.utils import format_path, load_exercise, load_module_from_path
from lib.visualization import can_draw, draw, print_graph

PREVIOUS = "demo_solution"

bfs_dfs = load_exercise("02_bfs_dfs", PREVIOUS)
spanning_trees = load_exercise("03_spanning_trees", PREVIOUS)
shortest_paths = load_exercise("04_shortest_paths", PREVIOUS)
coloring = load_exercise("06_graph_coloring", PREVIOUS)
matching = load_exercise("07_matching", PREVIOUS)
max_flow = load_exercise("08_max_flow", PREVIOUS)

data = load_module_from_path(Path(__file__).with_name("nangijala_data.py"))


# ----------------------------------------------------------------------
# Module A: modelling
# ----------------------------------------------------------------------
def build_network(roads: Iterable[tuple[str, str, float]]) -> Graph:
    """Return the undirected road network; edge weight = travel time in minutes.

    Modelling decisions: places are vertices, roads are edges. Roads can be
    used in both directions, so the graph is undirected. The travel time is
    the edge weight.
    """
    graph = Graph(directed=False)
    for u, v, minutes in roads:
        graph.add_edge(u, v, minutes)
    return graph


def without_places(graph: Graph, blocked: Iterable[Vertex]) -> Graph:
    """Return a copy of ``graph`` in which the ``blocked`` places are removed.

    Raises:
        KeyError: If a blocked place is not a vertex of the graph.
    """
    # Work on a copy: the original network must stay unchanged.
    result = graph.copy()
    for v in blocked:
        if v not in graph:
            raise KeyError(f"Unknown place {v!r}")
        if v in result:  # a place may be listed twice
            result.remove_vertex(v)
    return result


# ----------------------------------------------------------------------
# Module B: connectivity and reachability (unit 2)
# ----------------------------------------------------------------------
def reachable_places(graph: Graph, start: Vertex, blocked: Iterable[Vertex] = ()) -> set[Vertex]:
    """Return all places reachable from ``start`` if the ``blocked`` places are closed.

    Raises:
        KeyError: If ``start`` or a blocked place is not in the graph.
        ValueError: If ``start`` itself is blocked.
    """
    blocked = set(blocked)
    if start not in graph:
        raise KeyError(f"Unknown place {start!r}")
    if start in blocked:
        raise ValueError("The start place must not be blocked")
    # Closing a place = deleting the vertex (and all its roads).
    # Then reachability is exactly what a graph search computes.
    return set(bfs_dfs.dfs(without_places(graph, blocked), start))


def critical_places(graph: Graph) -> list[Vertex]:
    """Return all cut vertices in the order of ``graph.vertices()``.

    Brute force: remove each vertex once and count components.
    Runtime O(|V| * (|V| + |E|)) - fine for 20 places. (Tarjan's algorithm
    finds all cut vertices with a single DFS in O(|V| + |E|).)
    """
    components_before = len(bfs_dfs.connected_components(graph))
    critical = []
    for v in graph.vertices():
        components_after = len(bfs_dfs.connected_components(without_places(graph, [v])))
        if components_after > components_before:
            critical.append(v)
    return critical


# ----------------------------------------------------------------------
# Module C: spanning trees (unit 3)
# ----------------------------------------------------------------------
def winter_roads(graph: Graph) -> tuple[list[Edge], float]:
    """Return a minimum spanning tree (forest) and its total weight.

    "All places stay connected with minimum total length of cleared road"
    is exactly the definition of a minimum spanning tree.
    """
    edges = spanning_trees.kruskal(graph)
    return edges, spanning_trees.spanning_tree_weight(edges)


# ----------------------------------------------------------------------
# Module D: shortest paths (unit 4)
# ----------------------------------------------------------------------
def fastest_route(
    graph: Graph, start: Vertex, target: Vertex, blocked: Iterable[Vertex] = ()
) -> tuple[list[Vertex], float] | None:
    """Return the fastest route ``(path, minutes)`` avoiding the ``blocked`` places.

    Raises:
        KeyError: If ``start``, ``target`` or a blocked place is not in the graph.
        ValueError: If ``start`` or ``target`` is blocked.
    """
    blocked = set(blocked)
    for v in (start, target):
        if v not in graph:
            raise KeyError(f"Unknown place {v!r}")
        if v in blocked:
            raise ValueError(f"{v!r} is blocked")
    # Travel times are non-negative, so Dijkstra is applicable.
    distance, parent = shortest_paths.dijkstra(without_places(graph, blocked), start)
    if target not in distance:
        return None
    return shortest_paths.reconstruct_path(parent, target), distance[target]


# ----------------------------------------------------------------------
# Module E: colouring (unit 6)
# ----------------------------------------------------------------------
def lantern_colors(graph: Graph) -> dict[Vertex, int]:
    """Return a proper colouring, the best greedy result over several orders.

    Greedy colouring depends on the vertex order. We try
    1. the given order,
    2. descending degree (Welsh-Powell idea: difficult vertices first),
    3. the reversed order,
    and keep the colouring with the fewest colours.
    """
    vertices = graph.vertices()
    by_degree = sorted(vertices, key=graph.degree, reverse=True)  # stable sort
    orders = [vertices, by_degree, list(reversed(vertices))]

    best: dict[Vertex, int] | None = None
    for order in orders:
        candidate = coloring.greedy_coloring(graph, order)
        if best is None or coloring.number_of_colors(candidate) < coloring.number_of_colors(best):
            best = candidate
    return best if best is not None else {}


# ----------------------------------------------------------------------
# Module F: matching (unit 7)
# ----------------------------------------------------------------------
def assign_tasks(qualifications: Mapping[str, Iterable[str]]) -> dict[str, str]:
    """Return a maximum assignment ``person -> task``.

    Model: people on the left, tasks on the right, an edge means "is
    qualified for". A valid assignment is a matching; we want a maximum one.

    Raises:
        ValueError: If a name is used both as a person and as a task.
    """
    graph = Graph()
    people = list(qualifications)
    graph.add_vertices(people)  # people without qualifications are still people
    for person, tasks in qualifications.items():
        for task in tasks:
            if task in qualifications:
                raise ValueError(f"{task!r} is used as a person and as a task")
            graph.add_edge(person, task)
    return matching.maximum_bipartite_matching(graph, people)


# ----------------------------------------------------------------------
# Module G (optional): maximum flow (unit 8)
# ----------------------------------------------------------------------
def max_supply(
    routes: Iterable[tuple[str, str, float]], source: str, sink: str
) -> tuple[float, dict[tuple[Vertex, Vertex], float]]:
    """OPTIONAL: Return the maximum flow value and a maximum flow.

    Model: a directed graph whose edge weights are capacities.
    """
    network = Graph(directed=True)
    for u, v, capacity in routes:
        network.add_edge(u, v, capacity)
    return max_flow.edmonds_karp(network, source, sink)


def main() -> None:
    """Print a complete report for the Nangijala network."""
    nangijala = build_network(data.ROADS)
    print("=== A: Modell ===")
    print_graph(nangijala)

    print("\n=== B: Erreichbarkeit ===")
    closed = ["Bärenpass", "Adlerhorst"]
    reachable = reachable_places(nangijala, "Reiterhof", closed)
    print(f"Gesperrt: {closed} -> von Reiterhof erreichbar: {sorted(reachable)}")
    print("Kritische Orte (Schnittknoten):", critical_places(nangijala))

    print("\n=== C: Winterwege (minimaler Spannbaum) ===")
    edges, total = winter_roads(nangijala)
    for u, v, minutes in edges:
        print(f"  {u} - {v}: {minutes} min")
    print(f"  {len(edges)} Wege, zusammen {total} Minuten "
          f"(von insgesamt {sum(w for _, _, w in nangijala.edges())} Minuten)")

    print("\n=== D: Schnellste Wege ===")
    for target, closed in [("Tengils Burg", []), ("Marktplatz", []), ("Marktplatz", ["Bärenpass", "Waldsee"])]:
        route = fastest_route(nangijala, "Reiterhof", target, closed)
        text = "kein Weg" if route is None else f"{format_path(route[0])} ({route[1]} min)"
        print(f"  Reiterhof -> {target}, gesperrt {closed}: {text}")

    print("\n=== E: Laternenfarben ===")
    colors = lantern_colors(nangijala)
    print(f"  {coloring.number_of_colors(colors)} Farben:", colors)

    print("\n=== F: Aufgabenverteilung ===")
    assignment = assign_tasks(data.QUALIFICATIONS)
    for person, task in assignment.items():
        print(f"  {person}: {task}")
    print("  ohne Aufgabe:", [p for p in data.QUALIFICATIONS if p not in assignment])

    print("\n=== G: Nachschub (maximaler Fluss) ===")
    value, flow = max_supply(data.SUPPLY_ROUTES, "Kirschtal", "Heckenrosental")
    print(f"  maximal {value} Säcke pro Nacht")
    for (u, v), amount in flow.items():
        if amount > 0:
            print(f"  {u} -> {v}: {amount}")

    if can_draw():
        _draw_report(nangijala)


def _draw_report(nangijala: Graph) -> None:
    """Show the results of the modules on the map (needs matplotlib, does not block)."""
    edges, total = winter_roads(nangijala)
    draw(
        nangijala,
        title=f"Winterwege ({total} Minuten) und kritische Orte (rot umrandet)",
        layout=data.POSITIONS,
        highlight_edges=edges,
        highlight_vertices=critical_places(nangijala),
    )

    route = fastest_route(nangijala, "Reiterhof", "Tengils Burg")
    if route is not None:
        path, minutes = route
        draw(
            nangijala,
            title=f"Schnellster Weg Reiterhof -> Tengils Burg: {minutes} Minuten",
            layout=data.POSITIONS,
            highlight_edges=list(zip(path, path[1:])),
            highlight_vertices=[path[0], path[-1]],
        )

    colors = lantern_colors(nangijala)
    draw(
        nangijala,
        title=f"Laternenfarben: {coloring.number_of_colors(colors)} Farben",
        layout=data.POSITIONS,
        vertex_colors={place: f"Farbe {c}" for place, c in colors.items()},
        show_weights=False,
    )

    people = list(data.QUALIFICATIONS)
    qualified = Graph()
    qualified.add_vertices(people)
    for person, tasks in data.QUALIFICATIONS.items():
        for task in tasks:
            qualified.add_edge(person, task)
    assignment = assign_tasks(data.QUALIFICATIONS)
    draw(
        qualified,
        title=f"Aufgabenverteilung: {len(assignment)} von {len(people)} Personen",
        left=people,
        highlight_edges=list(assignment.items()),
    )

    value, flow = max_supply(data.SUPPLY_ROUTES, "Kirschtal", "Heckenrosental")
    supply = Graph.from_edges(data.SUPPLY_ROUTES, directed=True)
    draw(
        supply,
        title=f"Nachschub: maximal {value} Säcke pro Nacht (Fluss/Kapazität)",
        layout=data.POSITIONS,
        edge_labels={(u, v): f"{flow[(u, v)]}/{c}" for u, v, c in supply.edges()},
        highlight_edges=[edge for edge, amount in flow.items() if amount > 0],
    )


if __name__ == "__main__":
    main()
