# Einheit 2 - Breiten- und Tiefensuche

Die Programmieraufträge stehen direkt in [`task.py`](task.py).

## Auftrag

1. Implementiere `bfs` mit einer Warteschlange. Gib Abstände und Vorgänger der erreichbaren Knoten zurück.
2. Rekonstruiere mit `shortest_path` einen kürzesten Weg aus den BFS-Vorgängern.
3. Implementiere `dfs` mit einem Stapel. Gib die Knoten in Besuchsreihenfolge zurück.
4. Bestimme mit `connected_components` die Komponenten eines ungerichteten Graphen und prüfe mit `is_connected`, ob er zusammenhängend ist.
5. Tausche in einer Kopie von `dfs` den Stapel gegen eine Warteschlange. Vergleiche die Besuchsreihenfolgen.

## Optional

- Implementiere `dfs_recursive` und `bfs_layers`.
- Miss die BFS-Laufzeit für `random_graph(n, 4 / n)` mit $n = 1000, 2000, 4000, 8000$.
- Beweise, dass ein Graph mit $n$ Knoten und weniger als $n - 1$ Kanten nicht zusammenhängend ist.
