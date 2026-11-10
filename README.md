# Graphentheorie-Kurs – Python-Übungen für die Aka Kunterbunt

Hier findest du die Programmierübungen zum Graphentheorie-Kurs. Du brauchst Python 3.11 oder neuer. Die mitgelieferte Bibliothek `lib` stellt die Graphklasse und Hilfsfunktionen bereit.

## Schnellstart

1. Öffne ein Terminal im Projektordner und prüfe deine Python-Version mit `python --version`.
2. Lege eine virtuelle Umgebung an.

   ```bash
   python -m venv .venv
   ```

3. Aktiviere die Umgebung. In PowerShell verwendest du `.\.venv\Scripts\Activate.ps1`, unter macOS oder Linux `source .venv/bin/activate`. Installiere danach die Testabhängigkeiten.

   ```bash
   python -m pip install -r requirements.txt
   ```

4. Öffne [`exercises/01_graph_basics/task.py`](exercises/01_graph_basics/task.py). Lies die Docstrings und TODOs direkt an den Funktionen und ersetze jedes `raise NotImplementedError(...)` durch deinen Code.
5. Prüfe deine Implementierung aus dem Projektordner.

   ```bash
   python -m pytest exercises/01_graph_basics
   ```

Die Tests für die Pflichtfunktionen schlagen fehl, solange dort `NotImplementedError` ausgelöst wird. Tests für optionale Funktionen überspringt pytest, bis du sie implementiert hast.

## Übungen

| Einheit | Arbeitsaufträge |
|---|---|
| 1 | [Graphen modellieren](exercises/01_graph_basics/README.md) |
| 2 | [Breiten- und Tiefensuche](exercises/02_bfs_dfs/README.md) |
| 3 | [Spannbäume und Kruskal](exercises/03_spanning_trees/README.md) |
| 4 | [Kürzeste Wege](exercises/04_shortest_paths/README.md) |
| 5 | [Euler- und Hamiltonprobleme](exercises/05_euler_hamilton/README.md) |
| 6 | [Graphfärbung](exercises/06_graph_coloring/README.md) |
| 7 | [Bipartites Matching](exercises/07_matching/README.md) |
| 8 | [Maximale Flüsse](exercises/08_max_flow/README.md) |
| 9 | [Planarität und Komplexität](exercises/09_planarity_complexity/README.md) |
| 10 | [Abschlussprojekt Nangijala](exercises/10_final_project/README.md) |

Jede Einheit enthält `task.py` zum Bearbeiten, `test_task.py` zum Prüfen und eine README mit dem Arbeitsauftrag. Die Einheiten 1 bis 9 kannst du unabhängig bearbeiten. Im Abschlussprojekt greifst du auf Funktionen aus früheren Einheiten zurück.

Die [Bibliotheksdokumentation](docs/README.md) beschreibt `Graph`, die Hilfsfunktionen und den Browser-Player. Im Ordner [`examples/`](examples/) findest du lauffähige Beispiele.

## Hinweise für Lehrende

- `python tools/make_student_version.py` erzeugt `dist/graphentheorie-kurs-studierende.zip` ohne `demo_solution.py` und `demo_animation.py`.
- `python -m pytest --impl=demo` prüft die Musterlösungen, `python -m pytest tests` die Bibliothek und die Projektstruktur.
- `python exercises/02_bfs_dfs/demo_animation.py` öffnet die Animationen der zweiten Einheit. Die Einheiten 2 bis 9 haben jeweils eine `demo_animation.py`.
- Im Abschlussprojekt kannst du mit `PREVIOUS = "demo_solution"` auf die Musterlösungen früherer Einheiten umschalten, sofern sie vorliegen.

## Hinweise zum Kursmaterial

Das Kursmaterial ist für die Lehre erstellt. Die Orts- und Figurennamen stammen aus Werken Astrid Lindgrens. Die Netze, Entfernungen und Zahlen sind frei erfunden.
