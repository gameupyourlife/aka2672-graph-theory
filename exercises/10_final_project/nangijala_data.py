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
