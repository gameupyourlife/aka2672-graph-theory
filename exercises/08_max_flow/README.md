# Einheit 8 - Maximale Flüsse

Die Programmieraufträge stehen direkt in [`task.py`](task.py).

## Auftrag

1. Betrachte das Netzwerk mit den Kanten `s → a`, `s → b`, `a → b`, `a → t` und `b → t`, jeweils mit Kapazität 1. Schicke eine Einheit über `s → a → b → t`. Zeichne das Residualnetzwerk und finde den augmentierenden Weg über `b → a`.
2. Implementiere `residual_graph` und `find_augmenting_path`. Verwende beide in `edmonds_karp`, um einen maximalen Fluss zu berechnen.
3. Prüfe, ob dein Algorithmus für das Beispiel in `task.py` den Flusswert 23 liefert.

## Optional

- Implementiere `min_cut` und vergleiche die Schnittkapazität mit dem maximalen Flusswert.
- Löse bipartites Matching als Flussproblem und begründe, warum der Flusswert der Größe eines größten Matchings entspricht.
- Konstruiere ein Netzwerk mit vier Knoten, in dem Ford-Fulkerson bei ungünstiger Wegwahl viele Augmentierungen braucht. Vergleiche mit Edmonds-Karp.
- Miss die Laufzeit auf `random_weighted_graph(n, 0.3, directed=True)` für wachsendes $n$.
