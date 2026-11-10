# Einheit 4 – Kürzeste Wege

Die Programmieraufträge stehen direkt in [`task.py`](task.py).

## Auftrag

1. Führe Dijkstra im Graphen aus `small_weighted_graph()` ab Katthult auf Papier aus. Notiere nach jedem Schritt den fertig bearbeiteten Knoten und die Abstände.
2. Implementiere `dijkstra` mit einem Heap. Rekonstruiere mit `reconstruct_path` einen Weg und kombiniere beide Funktionen in `shortest_route`.
3. Probiere Dijkstra in einer Kopie ohne Prüfung auf negative Gewichte auf dem gerichteten Graphen mit den Kanten `("s", "a", 2)`, `("s", "b", 3)` und `("b", "a", -2)` aus. Vergleiche den berechneten Abstand nach `a` mit dem tatsächlichen kürzesten Abstand.
4. Vergleiche auf einem ungewichteten Graphen wie `grid_graph(5, 5)` die Ergebnisse von Dijkstra und BFS. Erkläre die Übereinstimmung.

## Optional

- Implementiere `bellman_ford`.
- Konstruiere einen gerichteten Graphen ohne negativen Kreis, auf dem Dijkstra ohne Gewichtsprüfung für mindestens zwei Knoten falsche Abstände liefert. Prüfe die Abstände mit Bellman-Ford.
- Miss die Dijkstra-Laufzeit auf `random_connected_graph(n, 3 * n, max_weight=100)` für $n = 1000, 2000, 4000, 8000$. Vergleiche den Verlauf mit $n \log n$.
- Berechne für jeden Ort in Lönneberga die Summe der Abstände zu allen anderen Orten. Bestimme den Ort mit der kleinsten Summe.
- Zeige, dass bei positiven Gewichten jedes Teilstück eines kürzesten Wegs selbst kürzest ist.
