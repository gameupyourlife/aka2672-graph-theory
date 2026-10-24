"""Example: modelling colouring and assignment problems at Villa Kunterbunt.

This example only *models* the problems and *checks* hand-made solutions
with ``lib.testing``. Computing the solutions is the topic of units 6
(graph colouring) and 7 (matching).

Run from the project root::

    python examples/villa_kunterbunt.py
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))  # find ``lib``

from lib.graph import Graph
from lib.testing import assert_valid_coloring, assert_valid_matching
from lib.visualization import can_draw, draw, print_graph, to_dot

# Rooms of the villa. Two rooms are adjacent if they share a wall;
# adjacent rooms must be painted in different colours.
WALLS = [
    ("Küche", "Veranda"),
    ("Küche", "Wohnzimmer"),
    ("Küche", "Speisekammer"),
    ("Wohnzimmer", "Veranda"),
    ("Wohnzimmer", "Pippis Zimmer"),
    ("Wohnzimmer", "Treppe"),
    ("Pippis Zimmer", "Treppe"),
    ("Treppe", "Dachboden"),
    ("Speisekammer", "Wohnzimmer"),
]

# Who would like to look after which animal?
WISHES = {
    "Pippi": ["Kleiner Onkel", "Herr Nilsson"],
    "Tommy": ["Kleiner Onkel"],
    "Annika": ["Herr Nilsson", "Hühner"],
}


def main() -> None:
    rooms = Graph.from_edges(WALLS)
    print("--- Rooms and walls ---")
    print_graph(rooms)

    # A colouring chosen by hand; colours are numbered 0, 1, 2, ...
    coloring = {
        "Küche": 0,
        "Wohnzimmer": 1,
        "Veranda": 2,
        "Speisekammer": 2,
        "Pippis Zimmer": 0,
        "Treppe": 2,
        "Dachboden": 0,
    }
    assert_valid_coloring(rooms, coloring)  # raises AssertionError if invalid
    print(f"\nThe hand-made colouring with {len(set(coloring.values()))} colours is valid.")
    print("Why are fewer than 3 colours impossible? (Hint: Küche, Wohnzimmer, Veranda)")

    try:
        assert_valid_coloring(rooms, {**coloring, "Treppe": 1})
    except AssertionError as error:
        print("A broken colouring is detected:", error)

    print("\n--- Animals as a bipartite graph ---")
    animals = Graph()
    animals.add_vertices(WISHES)  # children = left side
    for child, wanted in WISHES.items():
        for animal in wanted:
            animals.add_edge(child, animal)
    print_graph(animals)
    matching = {"Pippi": "Herr Nilsson", "Tommy": "Kleiner Onkel", "Annika": "Hühner"}
    assert_valid_matching(animals, matching, left=WISHES)
    print("Every child gets an animal:", matching)

    print("\n--- DOT export with colours ---")
    print(to_dot(rooms, name="Villa Kunterbunt", vertex_colors=coloring))

    if can_draw():  # windows open without blocking (needs matplotlib)
        draw(rooms, title="Villa Kunterbunt: rooms and paint colours", vertex_colors=coloring)
        draw(animals, title="Who looks after which animal?", left=WISHES, highlight_edges=list(matching.items()))


if __name__ == "__main__":
    main()
