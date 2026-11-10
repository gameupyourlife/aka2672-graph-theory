# Einheit 3 - Spannbäume und Kruskal

Die Programmieraufträge stehen direkt in [`task.py`](task.py).

## Auftrag

1. Führe Kruskal für den Lönneberga-Graphen aus `small_weighted_graph()` auf Papier aus. Notiere für jede Kante die Entscheidung und berechne das Gesamtgewicht.
2. Implementiere `UnionFind` mit `add`, `find`, `union` und `connected`.
3. Verwende `UnionFind` in `kruskal`, um einen minimalen Spannwald zu bestimmen. Summiere die Kantengewichte mit `spanning_tree_weight`.
4. Vergleiche die Ausgabe von `task.py` mit deiner Rechnung. Füge dann den isolierten Knoten „Vimmerby“ hinzu und erkläre, wie sich das Ergebnis verändert.

## Optional

- Ergänze in `UnionFind` die Vereinigung nach Größe und die Pfadkompression.
- Implementiere `prim` und `count_components`.
- Vergleiche die Laufzeit von Union-Find mit und ohne die beiden Verbesserungen. Vereinige nacheinander `i` und `i + 1` und rufe am Ende `find(0)` auf. Verwende $n = 1000, 2000, 4000$.
- Konstruiere einen Graphen mit gleich schweren Kanten und mehreren minimalen Spannbäumen. Begründe, warum der minimale Spannbaum des Lönneberga-Graphen eindeutig ist.
- Bestimme mit deiner vorhandenen Kruskal-Funktion einen Spannbaum mit größtem Gesamtgewicht.
- Zeige, dass jeder zusammenhängende Graph mit $n$ Knoten und $n-1$ Kanten ein Baum ist.
