# Testen und Hilfsfunktionen

## Ergebnisse prüfen: `lib.testing`

Die `assert_*`-Funktionen prüfen, ob ein Ergebnis **gültig** ist, z. B. ob eine Liste von Knoten wirklich ein Weg im Graphen ist. Ist es das nicht, lösen sie einen `AssertionError` mit einer Erklärung aus. In pytest-Tests kann man sie deshalb direkt verwenden; auch beim Entwickeln sind sie nützlich.

Sie **berechnen nichts**: Die Algorithmen sind Aufgabe der Übungen. Wo eine Prüfung Zusammenhangsinformationen braucht, verwendet sie absichtlich ein einfaches, langsames Verfahren (Markierungen entlang der Kanten weiterreichen, bis sich nichts mehr ändert), das keiner der Kursalgorithmen ist.

| Funktion | Prüft |
|---|---|
| `assert_valid_path(graph, path, start=None, end=None)` | `path` ist ein Weg: nicht leer, keine Wiederholung, aufeinanderfolgende Knoten durch Kanten verbunden (gerichtet: in Pfeilrichtung); optional Start und Ende |
| `assert_valid_euler_circuit(graph, walk)` | geschlossener Kantenzug `[v0, …, v0]`, der jede Kante genau einmal benutzt (ohne Kanten: `[]` oder `[v]`) |
| `assert_valid_euler_trail(graph, walk)` | Kantenzug (offen oder geschlossen), der jede Kante genau einmal benutzt |
| `assert_valid_hamiltonian_cycle(graph, cycle)` | `[v0, …, v_{n-1}, v0]` besucht jeden Knoten genau einmal |
| `assert_valid_spanning_forest(graph, edges)` | Kanten des Graphen, kreisfrei, verbinden genau das, was im Graphen verbunden ist |
| `assert_valid_spanning_tree(graph, edges)` | wie oben, Graph zusammenhängend |
| `assert_valid_coloring(graph, coloring, max_colors=None)` | jeder Knoten gefärbt, benachbarte Knoten verschieden, optional höchstens `max_colors` Farben |
| `assert_valid_matching(graph, matching, left=None)` | Kanten ohne gemeinsame Endknoten; `matching` als Wörterbuch `links -> rechts` oder Liste von Paaren |
| `assert_valid_flow(graph, flow, source, sink, tolerance=1e-9)` | Kapazitätsbedingung $0 \le f \le c$ und Flusserhaltung; `flow` ist `{(u, v): wert}` |

Weitere Hilfen:

| Funktion | Rückgabe |
|---|---|
| `count_components(graph)` | Anzahl der Zusammenhangskomponenten (Richtung ignoriert) |
| `flow_value(graph, flow, source)` | Wert des Flusses: Abfluss minus Zufluss an der Quelle |
| `cut_capacity(graph, source_side)` | Kapazität des Schnitts $(S, V \setminus S)$ |

```python
from lib.testing import assert_valid_path

path = shortest_path(graph, "A", "E")
assert_valid_path(graph, path, start="A", end="E")
```

### Testinfrastruktur der Übungen

Jede `test_task.py` beginnt mit

```python
from lib.testing import load_implementation
impl = load_implementation(__file__)
```

und testet `impl.funktion(...)`. Welche Datei geladen wird, entscheidet die Umgebungsvariable `GRAPH_COURSE_IMPL` (`task` oder `demo`), die `conftest.py` aus der Kommandozeilenoption setzt:

```bash
python -m pytest exercises/02_bfs_dfs              # testet task.py (eigene Lösung)
python -m pytest --impl=demo exercises/02_bfs_dfs  # testet demo_solution.py
```

| Name | Bedeutung |
|---|---|
| `load_implementation(test_file)` | lädt `task.py` oder `demo_solution.py` aus dem Ordner der Testdatei |
| `selected_implementation()` | `"task"` oder `"demo"` |
| `skip_if_not_implemented` | Dekorator für Tests **optionaler** Aufgaben: Löst die Funktion `NotImplementedError` aus, wird der Test übersprungen statt als Fehler gezählt |
| `IMPLEMENTATION_ENV_VAR` | `"GRAPH_COURSE_IMPL"` |

## Hilfsfunktionen: `lib.utils`

| Name | Beschreibung |
|---|---|
| `load_exercise(unit, module="demo_solution")` | eine andere Übung importieren, z. B. `load_exercise("02_bfs_dfs", "task")`. Ordnernamen mit Ziffern lassen sich nicht mit `import` laden. |
| `load_module_from_path(path, module_name=None)` | beliebige `.py`-Datei als Modul laden (zwischengespeichert in `sys.modules`) |
| `path_weight(graph, path)` | Summe der Kantengewichte entlang eines Weges (ein Knoten: 0) |
| `format_path(path, directed=True)` | `"A -> B -> C"`; `None` wird `"(kein Weg)"` |
| `measure_time(function, *args, repeat=3)` | beste Laufzeit in Sekunden aus `repeat` Aufrufen |
| `PROJECT_ROOT`, `EXERCISES_DIR` | Pfade des Projekts |

## Text- und DOT-Ausgabe

In `lib.visualization`:

| Funktion | Beschreibung |
|---|---|
| `to_text(graph, show_weights=None) -> str` | Adjazenzliste als Text; Gewichte werden gezeigt, wenn eines ungleich 1 ist |
| `print_graph(graph, show_weights=None)` | dasselbe, direkt ausgegeben |
| `to_dot(graph, name="G", show_weights=None, highlight_edges=(), vertex_colors=None, edge_labels=None) -> str` | Graphviz-DOT-Beschreibung, mit hervorgehobenen Kanten und Knotenfarben |
| `save_dot(graph, path, **options) -> Path` | DOT-Datei schreiben |

```text
Undirected graph with 3 vertices and 2 edges
  Bullerby   : Lonneberga (4), Sevedstorp (2)
  Lonneberga : Bullerby (4)
  Sevedstorp : Bullerby (2)
```

DOT-Dateien lassen sich mit Graphviz (`dot -Tpng graph.dot -o graph.png`) oder online unter <https://dreampuf.github.io/GraphvizOnline/> darstellen.
