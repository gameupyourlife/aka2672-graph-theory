"""Data for the final project "Das Netzwerk von Nangijala".

The data is kept as plain Python lists and dictionaries, independent of the
``Graph`` class. Turning it into graphs is part of the project.
"""

# ----------------------------------------------------------------------
# Roads of Nangijala (undirected), travel time in minutes.
# ----------------------------------------------------------------------
ROADS: list[tuple[str, str, int]] = [
    # Kirschtal
    ("Reiterhof", "Goldener Hahn", 20),
    ("Reiterhof", "Sofias Hof", 35),
    ("Goldener Hahn", "Sofias Hof", 25),
    ("Goldener Hahn", "Mühle", 40),
    ("Mühle", "Kirschtalbrücke", 30),
    ("Sofias Hof", "Westwald", 55),
    ("Westwald", "Kirschtalbrücke", 45),
    ("Reiterhof", "Kirschtalbrücke", 50),
    # Mountains between the valleys
    ("Kirschtalbrücke", "Wolfsschlucht", 70),
    ("Westwald", "Bärenpass", 95),
    ("Wolfsschlucht", "Bärenpass", 60),
    ("Wolfsschlucht", "Adlerhorst", 85),
    ("Bärenpass", "Waldsee", 75),
    ("Adlerhorst", "Waldsee", 65),
    ("Adlerhorst", "Karmafall", 110),
    ("Waldsee", "Stadttor", 90),
    ("Karmafall", "Katlas Höhle", 80),
    # Heckenrosental
    ("Stadttor", "Marktplatz", 15),
    ("Marktplatz", "Mattiashof", 22),
    ("Stadttor", "Mattiashof", 28),
    ("Mattiashof", "Rebellenhöhle", 64),
    ("Marktplatz", "Fischerhütte", 38),
    ("Fischerhütte", "Rebellenhöhle", 42),
    ("Rebellenhöhle", "Karmafall", 100),
    # Towards Karmanjaka
    ("Fischerhütte", "Grenzwache", 105),
    ("Bärenpass", "Grenzwache", 125),
    ("Grenzwache", "Tengils Burg", 130),
    ("Tengils Burg", "Karmanjaka", 18),
]

# Map coordinates (x = west -> east, y = south -> north) for drawings with
# ``draw(graph, layout=POSITIONS)``. "Kirschtal" and "Heckenrosental" are the
# two valleys as a whole, used by the supply routes below.
POSITIONS: dict[str, tuple[float, float]] = {
    "Sofias Hof": (0.0, 4.6),
    "Goldener Hahn": (1.2, 6.0),
    "Reiterhof": (1.6, 3.6),
    "Mühle": (4.0, 6.0),
    "Kirschtalbrücke": (3.6, 2.8),
    "Westwald": (1.0, 1.2),
    "Wolfsschlucht": (5.8, 4.2),
    "Bärenpass": (5.4, 1.0),
    "Adlerhorst": (7.6, 5.8),
    "Waldsee": (8.0, 2.6),
    "Karmafall": (10.0, 7.0),
    "Katlas Höhle": (12.4, 8.0),
    "Stadttor": (10.2, 2.6),
    "Marktplatz": (12.0, 3.2),
    "Mattiashof": (11.6, 4.8),
    "Rebellenhöhle": (13.8, 5.6),
    "Fischerhütte": (14.0, 2.4),
    "Grenzwache": (9.6, -0.4),
    "Tengils Burg": (12.0, -1.2),
    "Karmanjaka": (14.4, -1.6),
    "Kirschtal": (2.4, 3.4),
    "Heckenrosental": (12.4, 2.6),
}

KIRSCHTAL = ["Reiterhof", "Goldener Hahn", "Sofias Hof", "Mühle", "Kirschtalbrücke", "Westwald"]
HECKENROSENTAL = ["Stadttor", "Marktplatz", "Mattiashof", "Rebellenhöhle", "Fischerhütte"]

# ----------------------------------------------------------------------
# Who can do which task? (person -> list of tasks)
# ----------------------------------------------------------------------
QUALIFICATIONS: dict[str, list[str]] = {
    "Jonathan": ["Kundschaften", "Botengang"],
    "Krümel": ["Botengang", "Brieftauben"],
    "Sofia": ["Brieftauben", "Krankenpflege"],
    "Mattias": ["Brotbacken", "Wache"],
    "Orvar": ["Wache", "Kundschaften"],
    "Hubert": ["Botengang"],
    "Elias": ["Botengang"],
}

# ----------------------------------------------------------------------
# Secret supply routes (directed): sacks of flour per night.
# ----------------------------------------------------------------------
SUPPLY_ROUTES: list[tuple[str, str, int]] = [
    ("Kirschtal", "Wolfsschlucht", 10),
    ("Kirschtal", "Bärenpass", 7),
    ("Wolfsschlucht", "Bärenpass", 4),
    ("Wolfsschlucht", "Adlerhorst", 6),
    ("Bärenpass", "Waldsee", 9),
    ("Adlerhorst", "Waldsee", 3),
    ("Adlerhorst", "Karmafall", 5),
    ("Waldsee", "Heckenrosental", 8),
    ("Waldsee", "Rebellenhöhle", 2),
    ("Karmafall", "Rebellenhöhle", 6),
    ("Rebellenhöhle", "Heckenrosental", 7),
]
