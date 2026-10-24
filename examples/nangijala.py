"""Example: a first look at the network of the final project (unit 10).

Loads the data from ``exercises/10_final_project/nangijala_data.py``,
builds the road network with the plain ``Graph`` class, prints some key
figures and writes ``nangijala.dot`` for Graphviz. No algorithm from the
exercises is used here.

Run from the project root::

    python examples/nangijala.py
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))  # find ``lib``

from lib.graph import Graph
from lib.utils import EXERCISES_DIR, load_module_from_path
from lib.visualization import print_graph, save_dot

data = load_module_from_path(EXERCISES_DIR / "10_final_project" / "nangijala_data.py")


def main() -> None:
    roads = Graph.from_edges(data.ROADS)
    print("--- Roads of Nangijala (minutes) ---")
    print_graph(roads)

    total = sum(minutes for _, _, minutes in roads.edges())
    busiest = max(roads.vertices(), key=roads.degree)
    print(f"\n{roads.num_vertices()} places, {roads.num_edges()} roads, {total} minutes of road in total")
    print(f"Most roads meet at {busiest!r} ({roads.degree(busiest)} roads)")
    print("Kirschtal:", ", ".join(data.KIRSCHTAL))
    print("Heckenrosental:", ", ".join(data.HECKENROSENTAL))

    supply = Graph.from_edges(data.SUPPLY_ROUTES, directed=True)
    print("\n--- Secret supply routes (sacks per night) ---")
    print_graph(supply)

    path = save_dot(roads, Path.cwd() / "nangijala.dot", name="Nangijala")
    print(f"\nWrote {path} - render it with: dot -Tpng nangijala.dot -o nangijala.png")


if __name__ == "__main__":
    main()
