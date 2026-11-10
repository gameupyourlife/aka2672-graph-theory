# Einheit 1 - Graphen modellieren

Die Programmieraufträge stehen direkt in [`task.py`](task.py).

Um die Test auszuführen: `python -m pytest exercises/01_graph_basics`

## Auftrag

1. Baue mit `build_bullerby_graph` das ungerichtete Wegenetz und mit `build_letter_graph` das gerichtete Briefnetz. Die Kanten stehen in den Docstrings.
2. Implementiere `degrees`, `degree_sequence`, `odd_degree_vertices`, `check_handshake_lemma` und `in_and_out_degrees`. Zähle die Grade anhand der Kanten.
3. Erzeuge mit `adjacency_matrix` die Adjazenzmatrix für eine vorgegebene Knotenreihenfolge.
4. Führe `task.py` aus. Wie viele Knoten mit ungeradem Grad hat der Bullerbü-Graph? Passt das zur Folgerung aus dem Handschlaglemma?

## Optional

- Implementiere `complement`.
- Berechne die Kantenzahl des Komplementgraphen aus der Knoten- und Kantenzahl des Ausgangsgraphen.
- Zeige, dass in jedem einfachen ungerichteten Graphen mit mindestens zwei Knoten zwei Knoten denselben Grad haben. Prüfe die Aussage an Zufallsgraphen.
- Exportiere den Bullerbü-Graphen mit `lib.visualization.save_dot` und zeichne ihn mit Graphviz.
- Prüfe, ob $(3, 3, 1, 1)$ und $(3, 2, 2, 2, 1)$ Gradfolgen einfacher Graphen sind.
