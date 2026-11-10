# Einheit 7 - Bipartites Matching

Die Programmieraufträge stehen direkt in [`task.py`](task.py).

## Auftrag

1. Finde im Pfad `a - b - c - d - e - f` ein inklusionsmaximales Matching mit zwei Kanten. Vergrößere es entlang eines augmentierenden Wegs.
2. Implementiere `augment` und `find_augmenting_path`. Verwende beide in `maximum_bipartite_matching`, um ein größtes Matching zu bestimmen.
3. Prüfe am Beispiel in `task.py`, ob in der Villa Kunterbunt jede Person eine Aufgabe bekommt.

## Optional

- Implementiere `minimum_vertex_cover` und `hall_violator`.
- Zeige, dass ein $k$-regulärer bipartiter Graph mit $k \ge 1$ ein perfektes Matching hat.
- Miss die Laufzeit auf `random_bipartite_graph(n, n, 4 / n)` für $n = 100, 200, 400, 800$.
