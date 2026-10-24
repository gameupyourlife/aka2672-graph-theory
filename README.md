# Graphentheorie-Kurs – Python-Übungsprojekte („Aka Kunterbunt“)

Dieses Projekt enthält die Programmierübungen zu einem 30-stündigen Graphentheorie-Kurs. Der Kurs wird gemeinsam von einem Mathematiker und einem Informatiker gehalten. In der Theorie lernen Sie Definitionen, Sätze und Beweise. In den Übungen implementieren Sie die besprochenen Algorithmen selbst in Python.

Sie brauchen **keine Programmiererfahrung**, nur Python 3.11 oder neuer. Alle Algorithmen werden ohne fertige Graphbibliotheken programmiert (kein NetworkX). Eine kleine gemeinsame Bibliothek `lib` stellt die Graphklasse und Hilfsfunktionen bereit, damit Sie sich auf die Algorithmen konzentrieren können.

Ab und zu begegnen Ihnen Orte und Figuren aus den Büchern von Astrid Lindgren: Bullerbü, die Villa Kunterbunt, Lönneberga und Nangijala. Die Mathematik ist aber auch ohne diese Geschichten verständlich.

## Schnellstart

1. **Python installieren** (Version 3.11 oder neuer): <https://www.python.org/downloads/>. Prüfen Sie die Version mit `python --version`.
2. **Projektordner öffnen** (z. B. in VS Code oder PyCharm) und im Terminal in den Ordner `graphentheorie-kurs` wechseln.
3. **Virtuelle Umgebung anlegen und pytest installieren** (einmalig):

   ```bash
   python -m venv .venv
   ```

   Aktivieren unter Windows mit `.venv\Scripts\activate`, unter macOS/Linux mit `source .venv/bin/activate`. Danach:

   ```bash
   python -m pip install -r requirements.txt
   ```

   Empfohlen, aber nicht nötig: `python -m pip install matplotlib`. Dann zeichnen die Musterlösungen und Beispiele ihre Ergebnisse in Fenstern.

4. **Erste Übung starten:** Lesen Sie `exercises/01_graph_basics/README.md` und bearbeiten Sie `exercises/01_graph_basics/task.py`.
5. **Testen:**

   ```bash
   python -m pytest exercises/01_graph_basics
   ```

Am Anfang schlagen die Tests fehl (`NotImplementedError: TODO ...`). Mit jeder Funktion, die Sie implementieren, werden mehr Tests grün.

## So arbeiten Sie mit den Übungen

Jede Einheit liegt in einem eigenen Ordner unter `exercises/` und besteht aus vier Dateien:

| Datei | Inhalt |
|---|---|
| `README.md` | Aufgabenblatt: Lernziele, mathematischer Hintergrund, Definitionen, Arbeitsaufträge, Beispiele, Hinweise, Literatur |
| `task.py` | **Ihre Datei.** Funktionsköpfe mit Beschreibung und `TODO`-Kommentaren. Ersetzen Sie `raise NotImplementedError(...)` durch Ihren Code. |
| `test_task.py` | Automatische Tests. Sie prüfen standardmäßig Ihre `task.py`. |
| `demo_solution.py` | Kommentierte Musterlösung (in der Studierendenversion nicht enthalten) |

Arbeitsablauf:

1. README der Einheit lesen, die Definitionen mit der Vorlesung vergleichen.
2. Eine Funktion in `task.py` implementieren und mit eigenen kleinen Beispielen ausprobieren (`python exercises/02_bfs_dfs/task.py`).
3. Tests ausführen und Fehlermeldungen lesen. Die Tests sagen meist genau, welcher Fall noch nicht stimmt.
4. Optionale Zusatzaufgaben bearbeiten. Deren Tests werden übersprungen (`skipped`), solange die Funktion nicht implementiert ist.

## Projektstruktur

```text
graphentheorie-kurs/
├── README.md              diese Datei
├── pyproject.toml         Projekt- und pytest-Konfiguration
├── requirements.txt       benötigte Pakete (nur pytest)
├── conftest.py            pytest-Option --impl=task|demo
├── lib/                   gemeinsame Bibliothek
│   ├── graph.py           Klasse Graph (Adjazenzlisten)
│   ├── generators.py      Beispielgraphen (Pfade, Kreise, Zufallsgraphen, ...)
│   ├── visualization.py   Textausgabe, Graphviz-DOT-Export, Zeichnen mit matplotlib (optional)
│   ├── layout.py          Knotenpositionen für Zeichnungen
│   ├── testing.py         Prüffunktionen für Wege, Bäume, Färbungen, Matchings, Flüsse
│   └── utils.py           Hilfsfunktionen (andere Übungen laden, Zeitmessung, ...)
├── exercises/             die zehn Einheiten
│   ├── 01_graph_basics/        Graphen modellieren
│   ├── 02_bfs_dfs/             Breiten- und Tiefensuche
│   ├── 03_spanning_trees/      Union-Find und Kruskal
│   ├── 04_shortest_paths/      Dijkstra (und Bellman-Ford)
│   ├── 05_euler_hamilton/      Euler- und Hamiltonprobleme
│   ├── 06_graph_coloring/      Greedy-Färbung, Bipartitheit
│   ├── 07_matching/            bipartites Matching mit augmentierenden Wegen
│   ├── 08_max_flow/            Edmonds-Karp, minimaler Schnitt
│   ├── 09_planarity_complexity/  Eulersche Formel, P und NP
│   └── 10_final_project/       Abschlussprojekt „Netzwerk von Nangijala“
├── examples/              lauffähige Beispiele zur Bibliothek
│   ├── bullerby.py
│   ├── villa_kunterbunt.py
│   └── nangijala.py
├── tests/                 Tests der Bibliothek und Qualitätsprüfungen
└── tools/
    └── make_student_version.py   ZIP ohne Musterlösungen erzeugen
```

## Kursplan (Vorschlag für 30 Stunden)

| Einheit | Thema | Mathematik | Informatik / Übung | Zeit |
|---|---|---|---|---|
| 1 | Graphen modellieren | Graphen, Grad, Handschlaglemma | Graph-Klasse, Adjazenzliste und -matrix | 2 h |
| 2 | BFS und DFS | Wege, Abstand, Zusammenhang | Queue, Stack, $O(\lvert V\rvert+\lvert E\rvert)$ | 3 h |
| 3 | Spannbäume | Bäume, Schnitteigenschaft | Union-Find, Kruskal, Sortieren | 3 h |
| 4 | Kürzeste Wege | gewichtete Abstände, Optimalität | Dijkstra mit Heap, Bellman-Ford | 3 h |
| 5 | Euler und Hamilton | Satz von Euler, Hamiltonkreise | Gradbedingungen, Hierholzer, Backtracking | 3 h |
| 6 | Graphfärbung | chromatische Zahl, bipartite Graphen, ungerade Kreise | Greedy-Färbung, Knotenreihenfolgen | 3 h |
| 7 | Bipartites Matching | Satz von Berge, Satz von Hall | augmentierende Wege | 3 h |
| 8 | Maximale Flüsse | Max-Flow-Min-Cut | Residualgraph, Edmonds-Karp | 3 h |
| 9 | Planarität und Komplexität | Eulersche Polyederformel, $K_5$, $K_{3,3}$ | P, NP, NP-Vollständigkeit, Laufzeitexperimente | 3 h |
| 10 | Abschlussprojekt Nangijala | Modellierung | alle Algorithmen im Zusammenspiel | 4 h |

Die Einheiten bauen inhaltlich aufeinander auf, lassen sich aber **unabhängig voneinander bearbeiten und testen**. Algorithmen aus früheren Einheiten, die man später erneut braucht (z. B. eine Suche zur Zusammenhangsprüfung in Einheit 5), werden dort als kleine Hilfsfunktion neu geschrieben. Nur das Abschlussprojekt verwendet ausdrücklich die Lösungen der Einheiten 2–8.

## Die Bibliothek `lib`

```python
from lib.graph import Graph

graph = Graph(directed=False)
graph.add_edge("Bullerby", "Lonneberga")
graph.add_edge("Bullerby", "Sevedstorp", weight=4)

print(graph.neighbors("Bullerby"))   # ['Lonneberga', 'Sevedstorp']
print(graph.degree("Bullerby"))      # 2
print(graph.edges())                 # [Edge(u='Bullerby', v='Lonneberga', weight=1), ...]
```

| Methode | Bedeutung |
|---|---|
| `Graph(directed=False)` | leerer gerichteter oder ungerichteter Graph |
| `Graph.from_edges(edges, directed=False, vertices=())` | Graph aus einer Liste von Paaren `(u, v)` oder Tripeln `(u, v, Gewicht)` |
| `add_vertex(v)`, `add_vertices(vs)` | Knoten hinzufügen |
| `add_edge(u, v, weight=1)`, `add_edges(edges)` | Kante hinzufügen (fehlende Knoten werden angelegt) |
| `remove_edge(u, v)`, `remove_vertex(v)`, `set_weight(u, v, w)` | Graph verändern |
| `vertices()`, `edges()` | Liste der Knoten / Liste von `Edge(u, v, weight)` |
| `neighbors(v)`, `predecessors(v)` | Nachbarn (bei gerichteten Graphen: Nachfolger) / Vorgänger |
| `has_vertex(v)`, `v in graph`, `has_edge(u, v)`, `weight(u, v)` | Abfragen |
| `degree(v)`, `in_degree(v)`, `out_degree(v)` | Knotengrade |
| `num_vertices()`, `num_edges()`, `len(graph)` | Anzahl der Knoten und Kanten |
| `copy()`, `check_consistency()` | unabhängige Kopie / interne Konsistenzprüfung |

**Konventionen, die im ganzen Kurs gelten:**

- **Jede Kante hat ein Gewicht.** Bei ungewichteten Graphen ist es `1`. Gewichtete und ungewichtete Graphen liefern also dieselben Datentypen.
- **Einfache Graphen:** keine Schleifen, keine Mehrfachkanten. In gerichteten Graphen dürfen `u -> v` und `v -> u` beide existieren.
- Knoten können beliebige hashbare Werte sein (Zeichenketten, Zahlen, Tupel). Die Reihenfolge der Knoten und Nachbarn ist die Einfügereihenfolge.
- Ein unbekannter Knoten führt zu einem `KeyError`, ein ungeeigneter Graph oder ein ungültiges Argument zu einem `ValueError`.
- Wege sind Listen von Knoten `[start, ..., ziel]`; „kein Weg“ ist `None`. Geschlossene Wege (Kreise) wiederholen den Startknoten am Ende.
- Algorithmen verändern den übergebenen Graphen nicht.

Weitere Module:

- `lib.generators`: `path_graph`, `cycle_graph`, `complete_graph`, `complete_bipartite_graph`, `star_graph`, `grid_graph`, `petersen_graph`, `random_graph`, `random_tree`, `random_connected_graph`, `random_bipartite_graph`, `random_weighted_graph`, `small_weighted_graph`. Zufallsgeneratoren haben einen optionalen `seed` für reproduzierbare Ergebnisse.
- `lib.visualization`: `print_graph(graph)` für die Konsole, `to_dot`/`save_dot` für Graphviz (mit hervorgehobenen Kanten und Knotenfarben), `draw(graph)` zeichnet mit matplotlib in einem nicht blockierenden Fenster, das sich für Animationen aktualisieren lässt (siehe [Visualisierung](#visualisierung)).
- `lib.layout`: Knotenpositionen zum Zeichnen (Kreis, konzentrische Kreise, kräftebasiert, bipartit, Schichten, Gitter), reines Python.
- `lib.testing`: `assert_valid_path`, `assert_valid_spanning_tree`, `assert_valid_spanning_forest`, `assert_valid_coloring`, `assert_valid_matching`, `assert_valid_flow`, `assert_valid_euler_circuit`, `assert_valid_hamiltonian_cycle`, `flow_value`, `cut_capacity`. Diese Funktionen **prüfen** Ergebnisse, sie berechnen sie nicht.
- `lib.utils`: `load_exercise("02_bfs_dfs", "task")` lädt eine andere Übung, `path_weight`, `format_path`, `measure_time`.

Die Beispiele in `examples/` zeigen die Bibliothek in Aktion:

```bash
python examples/bullerby.py
python examples/villa_kunterbunt.py
python examples/nangijala.py
```

## Tests ausführen

```bash
python -m pytest                              # alle Tests, prüft Ihre task.py-Dateien
python -m pytest exercises/04_shortest_paths  # nur eine Einheit
python -m pytest exercises/04_shortest_paths -k dijkstra   # nur Tests mit "dijkstra" im Namen
python -m pytest --impl=demo                  # prüft stattdessen die Musterlösungen
python -m pytest tests                        # nur die Tests der Bibliothek
```

Statt `--impl=demo` können Sie auch die Umgebungsvariable `GRAPH_COURSE_IMPL=demo` setzen.

## Visualisierung

Die Übungen benötigen keine grafische Ausgabe. `print_graph` zeigt jeden Graphen als Adjazenzliste in der Konsole.

### Graphen zeichnen mit `draw` (empfohlen, optional)

Mit matplotlib (`python -m pip install matplotlib`) zeichnet `lib.visualization.draw` Graphen in einem Fenster. Alle Musterlösungen und Beispiele zeigen ihre Ergebnisse auf diese Weise: Spannbäume, kürzeste Wege, Färbungen, Matchings und Flüsse. Einige Musterlösungen spielen den Algorithmus Schritt für Schritt als Animation ab, z. B. Breitensuche, Kruskal, das Haus vom Nikolaus, augmentierende Wege und Edmonds-Karp.

```python
from lib.visualization import draw

draw(graph, title="Minimaler Spannbaum", highlight_edges=tree)            # Kanten rot hervorheben
draw(graph, vertex_colors=coloring)                                       # Färbung mit Legende
draw(graph, vertex_labels=distance, highlight_vertices=["Katthult"])      # Text unter Knoten
draw(network, edge_labels={("s", "a"): "3/5"})                            # eigene Kantenbeschriftung
draw(graph, left=people)                                                  # bipartit: zwei Spalten
draw(graph, layers=bfs_layers)                                            # eine Spalte pro Schicht
draw(graph, layout={"A": (0, 0), "B": (1, 2)})                            # eigene Koordinaten
draw(graph, filename="bild.png")                                          # als Datei speichern
```

- **Blockiert nicht:** Das Programm läuft nach `draw` sofort weiter, mehrere Fenster sind möglich. Am Programmende bleiben die Fenster offen, bis Sie sie schließen.
- **Animationen:** `draw` gibt ein Objekt zurück, dessen Darstellung sich mit `update(...)` im selben Fenster ändern lässt. `pause(sekunden)` wartet dazwischen:

  ```python
  from lib.visualization import draw, pause

  drawing = draw(graph, title="Tiefensuche")
  for step in range(1, len(order) + 1):
      drawing.update(title=f"Schritt {step}", highlight_vertices=order[:step])
      pause(0.5)
  ```

- **Anordnung der Knoten** (`lib.layout`): Standardmäßig wird ein passendes Layout gewählt. Gitter werden als Gitter gezeichnet, vollständige Graphen und Kreise auf einem Kreis, alle anderen mit einem kräftebasierten Verfahren (Fruchterman-Reingold), bei dem Komponenten nebeneinander liegen. Mit `layout="circular"`, `"spring"`, `"shell"` (z. B. `shells=[range(5), range(5, 10)]` für den Petersen-Graphen), `"bipartite"`, `"layered"`, `"grid"` oder eigenen Koordinaten wählen Sie selbst.
- **Ohne matplotlib** laufen alle Programme trotzdem. Sie prüfen vorher mit `can_draw()`, ob gezeichnet werden kann. Setzen Sie die Umgebungsvariable `GRAPH_COURSE_NO_PLOTS=1`, um alle Fenster abzuschalten (z. B. bei automatischen Läufen).

### Export für Graphviz

```python
from lib.visualization import save_dot
save_dot(graph, "graph.dot", highlight_edges=[("A", "B")], vertex_colors={"A": 0, "B": 1})
```

Die Datei lässt sich mit Graphviz (`dot -Tpng graph.dot -o graph.png`) oder online unter <https://dreampuf.github.io/GraphvizOnline/> darstellen.

## Hinweise für Lehrende

- **Studierendenversion:** `python tools/make_student_version.py` erzeugt `dist/graphentheorie-kurs-studierende.zip` ohne die Dateien `demo_solution.py`.
- **Qualitätssicherung:** `python -m pytest --impl=demo` muss vollständig grün sein. `tests/test_project_structure.py` prüft unter anderem, ob jede Einheit alle Dateien besitzt, ob die READMEs alle neun Abschnitte enthalten und ob `task.py` wirklich nur `TODO`s enthält (keine versehentlich mitgelieferte Lösung). Außerdem wird geprüft, ob `task.py` und `demo_solution.py` dieselben Schnittstellen haben.
- **Abschlussprojekt:** In `exercises/10_final_project/task.py` legt die Konstante `PREVIOUS` fest, ob die eigenen Lösungen der Studierenden oder die Musterlösungen der früheren Einheiten verwendet werden. So können Gruppen auch dann arbeiten, wenn eine frühere Einheit unvollständig ist (nur in der Lehrendenversion, da die Studierendenversion keine Musterlösungen enthält).
- Die Tests hängen nicht von Implementierungsdetails ab. Sie akzeptieren jede gültige Besuchsreihenfolge, jeden kürzesten Weg und jeden minimalen Spannbaum mit optimalem Gewicht.

## Häufige Probleme

| Problem | Lösung |
|---|---|
| `ModuleNotFoundError: No module named 'lib'` | Befehle im Ordner `graphentheorie-kurs` ausführen. Die Dateien `task.py` und `demo_solution.py` finden `lib` auch beim direkten Start selbst. |
| `No module named pytest` | Virtuelle Umgebung aktivieren und `python -m pip install -r requirements.txt` ausführen. |
| `NotImplementedError: TODO: ...` | Die Funktion ist noch nicht implementiert. Das ist der Ausgangszustand. |
| Syntaxfehler bei `int \| None` o. Ä. | Python-Version prüfen: mindestens 3.11 ist nötig. |
| Umlaute werden falsch angezeigt | Terminal auf UTF-8 umstellen (Windows: `chcp 65001`) oder ein aktuelles Terminal wie Windows Terminal verwenden. |

## Lizenz und Hinweise

Das Kursmaterial ist für die Lehre erstellt. Die Orts- und Figurennamen sind den Werken Astrid Lindgrens entlehnt und dienen nur als Motiv. Alle Netze, Entfernungen und Zahlen sind frei erfunden.
