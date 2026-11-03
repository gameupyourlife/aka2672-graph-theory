# Dokumentation der Kursbibliothek `lib`

Die Bibliothek `lib` ist das Fundament aller Übungen des Graphentheorie-Kurses. Sie stellt eine einfache Graphklasse bereit, erzeugt Beispielgraphen, prüft Ergebnisse von Algorithmen und visualisiert Graphen und Algorithmen interaktiv im Webbrowser. Sie benötigt nur die Python-Standardbibliothek (Python 3.11 oder neuer).

Die Algorithmen selbst (Breitensuche, Dijkstra, Kruskal, …) sind bewusst **nicht** enthalten. Sie werden in den Übungen implementiert.

## Inhalt

| Dokument | Inhalt |
|---|---|
| [Graphen](graph.md) | Die Klasse `Graph`: Knoten, Kanten, Gewichte, Attribute, Konventionen, vollständige Referenz |
| [Visualisierung und Algorithmen-Player](visualisierung.md) | Graphen zeichnen, Algorithmen Schritt für Schritt animieren (`Trace`), der Player im Browser, Flags und Stile, Referenz |
| [Generatoren und Layouts](generatoren-und-layouts.md) | Beispielgraphen erzeugen (`lib.generators`), Knoten anordnen (`lib.layout`) |
| [Testen und Hilfsfunktionen](testen-und-hilfsfunktionen.md) | Ergebnisse prüfen (`lib.testing`), Testinfrastruktur, Hilfsfunktionen (`lib.utils`), Text- und DOT-Ausgabe |

## Module im Überblick

| Modul | Aufgabe | Wichtigste Namen |
|---|---|---|
| `lib.graph` | Graph als Adjazenzliste | `Graph`, `Edge`, `Vertex` |
| `lib.generators` | Beispielgraphen | `path_graph`, `cycle_graph`, `complete_graph`, `petersen_graph`, `random_graph`, `small_weighted_graph`, … |
| `lib.trace` | Zustand eines Algorithmus aufzeichnen | `Trace`, `Frame`, `Style`, `DEFAULT_STYLES`, `format_value` |
| `lib.viewer` | Player im Webbrowser | `show`, `draw`, `snapshot`, `save_html` |
| `lib.layout` | Knotenpositionen für Zeichnungen | `compute_layout`, `spring_layout`, `circular_layout`, … |
| `lib.visualization` | Sammelmodul für alle Ausgaben: Text, Graphviz-DOT und die Namen aus `lib.trace` / `lib.viewer` | `print_graph`, `to_dot`, `Trace`, `show`, `draw`, `snapshot` |
| `lib.testing` | Ergebnisse prüfen, Testinfrastruktur | `assert_valid_path`, `assert_valid_flow`, `load_implementation`, … |
| `lib.utils` | Hilfsfunktionen | `load_exercise`, `path_weight`, `format_path`, `measure_time` |

## Schnelleinstieg

```python
from lib.graph import Graph
from lib.visualization import draw, print_graph

graph = Graph()
graph.add_edge("Katthult", "Lönneberga", 4)
graph.add_edge("Katthult", "Kirche", 7)
graph.add_edge("Lönneberga", "Kirche", 5)

print_graph(graph)                                   # Adjazenzliste in der Konsole
draw(graph, "Rund um Katthult", highlight_vertices=["Katthult"])   # Bild im Browser
```

Einen Algorithmus Schritt für Schritt zeigen:

```python
from lib.visualization import Trace, show

trace = Trace(graph, "Mein erster Ablauf")
trace.flag("Katthult", "current")
trace.step("Wir beginnen in Katthult.")
trace.flag("Katthult", "visited")
trace.current("Kirche")
trace.step("Weiter zur Kirche.")
show(trace)            # öffnet den Player: ◀ ▶, Abspielen, Schieberegler
```

Die ausführliche Anleitung steht in [Visualisierung und Algorithmen-Player](visualisierung.md).

## Gestaltungsgrundsätze

- **Einfach statt clever.** Die Bibliothek richtet sich an Studierende mit wenig Programmiererfahrung. Jede Funktion hat eine klare Aufgabe, Type Hints und einen Docstring.
- **Keine Überraschungen bei Datentypen.** Jede Kante hat ein Gewicht (Standard `1`), `edges()` liefert immer `Edge(u, v, weight)`, Wege sind immer Listen von Knoten.
- **Fehler früh melden.** Unbekannte Knoten führen zu `KeyError`, ungeeignete Eingaben zu `ValueError`, auch beim Aufzeichnen von Algorithmen.
- **Algorithmen verändern ihre Eingabe nicht.** Der Zustand eines laufenden Algorithmus (besucht, aktuell, …) wird deshalb nicht im Graphen gespeichert, sondern in einem `Trace`.
- **Keine Abhängigkeiten.** Auch die Visualisierung braucht kein zusätzliches Paket: Sie erzeugt eine eigenständige HTML-Datei, die in jedem modernen Browser läuft.

## Dokumentation im Code

Alle öffentlichen Klassen und Funktionen haben ausführliche (englische) Docstrings. In einer Python-Konsole zeigt `help(...)` sie an:

```python
>>> from lib.trace import Trace
>>> help(Trace.flag)
```
