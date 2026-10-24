"""Example: the first steps with the course library, using Bullerbü.

Shows how to

* build a small undirected graph,
* ask for vertices, edges, neighbours and degrees,
* print the graph and export it as a Graphviz DOT file,
* draw it in a window (if matplotlib is installed),
* create standard graphs with ``lib.generators``.

Run from the project root::

    python examples/bullerby.py
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))  # find ``lib``

from lib import generators
from lib.graph import Graph
from lib.visualization import can_draw, draw, print_graph, to_dot


def build_bullerby() -> Graph:
    """Return the three farms of Bullerbü and the paths around them."""
    graph = Graph(directed=False)
    graph.add_edge("Nordhof", "Mittelhof")
    graph.add_edge("Mittelhof", "Südhof")
    graph.add_edge("Nordhof", "Südhof")
    graph.add_edge("Mittelhof", "Schule", weight=30)  # weight = minutes on foot
    graph.add_vertex("Großvaters Bank")  # an isolated vertex
    return graph


def main() -> None:
    bullerby = build_bullerby()

    print("--- The graph ---")
    print_graph(bullerby)
    print(bullerby)

    print("\n--- Questions to the graph ---")
    print("Vertices:", bullerby.vertices())
    print("Edges:")
    for u, v, weight in bullerby.edges():  # every edge is an Edge(u, v, weight)
        print(f"  {u} - {v} (weight {weight})")
    print("Neighbours of Mittelhof:", bullerby.neighbors("Mittelhof"))
    print("Degree of Mittelhof:", bullerby.degree("Mittelhof"))
    print("Is there a path edge Nordhof - Schule?", bullerby.has_edge("Nordhof", "Schule"))
    print("Is 'Stockholm' a vertex?", "Stockholm" in bullerby)

    print("\n--- A directed graph: who visits whom? ---")
    visits = Graph.from_edges([("Lisa", "Britta"), ("Britta", "Lisa"), ("Lasse", "Ole")], directed=True)
    print_graph(visits)
    print("Lisa: out-degree", visits.out_degree("Lisa"), "in-degree", visits.in_degree("Lisa"))

    print("\n--- Standard graphs from lib.generators ---")
    for name, graph in [
        ("path P5", generators.path_graph(5)),
        ("cycle C6", generators.cycle_graph(6)),
        ("complete K4", generators.complete_graph(4)),
        ("K_{2,3}", generators.complete_bipartite_graph(2, 3)),
        ("Petersen", generators.petersen_graph()),
        ("random G(8, 0.3), seed 1", generators.random_graph(8, 0.3, seed=1)),
    ]:
        print(f"{name:26} {graph}")

    print("\n--- Graphviz DOT export ---")
    print(to_dot(bullerby, name="Bullerbü"))
    print("(Paste this into https://dreampuf.github.io/GraphvizOnline/ to see a drawing.)")

    print("\n--- Drawing with matplotlib (optional) ---")
    if can_draw():
        # The windows do not block; they stay open until you close them.
        draw(bullerby, title="Bullerbü", highlight_vertices=["Mittelhof"])
        draw(visits, title="Who visits whom?")
        draw(generators.petersen_graph(), title="Petersen graph", shells=[range(5), range(5, 10)])
        print("Opened 3 windows.")
    else:
        print("Install matplotlib ('pip install matplotlib') to see drawings.")


if __name__ == "__main__":
    main()
