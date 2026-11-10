# Graphen: die Klasse `Graph`

`lib.graph.Graph` speichert einen gerichteten oder ungerichteten Graphen als **Adjazenzliste**: Für jeden Knoten gibt es ein Wörterbuch, das jedem Nachbarn das Gewicht der verbindenden Kante zuordnet.

```python
{
    "Bullerby":   {"Lonneberga": 1, "Sevedstorp": 4},
    "Lonneberga": {"Bullerby": 1},
    "Sevedstorp": {"Bullerby": 4},
}
```

Speicherbedarf: $O(|V| + |E|)$. Nachbarn eines Knotens abfragen kostet $O(\deg(v))$, eine Kante prüfen im Mittel $O(1)$.

## Inhalt

- [Erste Schritte](#erste-schritte)
- [Konventionen](#konventionen)
- [Gerichtete Graphen](#gerichtete-graphen)
- [Attribute von Knoten und Kanten](#attribute-von-knoten-und-kanten)
- [Referenz](#referenz)

## Erste Schritte

```python
from lib.graph import Graph

graph = Graph(directed=False)                 # leerer ungerichteter Graph
graph.add_edge("Bullerby", "Lonneberga")      # Kante mit Gewicht 1, Knoten entstehen automatisch
graph.add_edge("Bullerby", "Sevedstorp", 4)   # Kante mit Gewicht 4
graph.add_vertex("Stockholm")                 # isolierter Knoten

graph.vertices()              # ['Bullerby', 'Lonneberga', 'Sevedstorp', 'Stockholm']
graph.neighbors("Bullerby")   # ['Lonneberga', 'Sevedstorp']
graph.degree("Bullerby")      # 2
graph.weight("Sevedstorp", "Bullerby")   # 4  (ungerichtet: beide Richtungen)
graph.num_vertices(), graph.num_edges()  # (4, 2)

for u, v, weight in graph.edges():       # jede ungerichtete Kante genau einmal
    print(u, v, weight)
```

Du kannst Knoten und Kanten direkt beim Erzeugen angeben. Der Knoten `Z`
bleibt isoliert. Fehlende Endknoten ergänzt der Konstruktor automatisch.

```python
graph = Graph(vertices=["Z", "A"], edges=[("A", "B", 3), ("B", "C")], directed=False)
```

## Konventionen

Diese Regeln gelten im ganzen Kurs, auch in allen Übungen:

| Regel | Bedeutung |
|---|---|
| **Jede Kante hat ein Gewicht.** | Ungewichtete Graphen verwenden das Gewicht `1`. Gewichtete und ungewichtete Graphen liefern also dieselben Datentypen. Gewichte sind endliche Zahlen (`int` oder `float`); negative Gewichte sind erlaubt. |
| **Einfache Graphen.** | Keine Schleifen (`v -> v`) und keine Mehrfachkanten. `add_edge` löst sonst einen `ValueError` aus. In gerichteten Graphen dürfen `u -> v` und `v -> u` beide existieren. |
| **Knoten sind beliebige hashbare Werte.** | Zeichenketten, Zahlen, Tupel wie `(zeile, spalte)`, … |
| **Feste Reihenfolge.** | `vertices()`, `neighbors()` und `edges()` liefern ihre Elemente in der Einfügereihenfolge. Ergebnisse sind dadurch reproduzierbar. |
| **Fehler.** | Ein unbekannter Knoten oder eine unbekannte Kante führt zu `KeyError`, ungültige Gewichte, Schleifen und doppelte Kanten zu `ValueError`. |
| **Keine Algorithmen.** | Die Klasse enthält keine Graphalgorithmen (BFS, DFS, Dijkstra, …): Diese sind Inhalt der Übungen. |

**Multigraphen** (z. B. die Brücken von Königsberg) modelliert man durch Unterteilung: Jede zusätzliche parallele Kante erhält einen Hilfsknoten in der Mitte. Das ändert weder die Grade der ursprünglichen Knoten (bis auf die neuen Knoten vom Grad 2) noch die Eulereigenschaft.

## Gerichtete Graphen

```python
flow = Graph(directed=True)
flow.add_edge("s", "a", 3)
flow.add_edge("a", "s", 1)      # Gegenkante: erlaubt
flow.neighbors("s")             # Nachfolger: ['a']
flow.predecessors("s")          # Vorgänger:  ['a']
flow.out_degree("s"), flow.in_degree("s"), flow.degree("s")   # (1, 1, 2)
```

`degree(v)` ist bei gerichteten Graphen die Summe aus Eingangs- und Ausgangsgrad.

## Attribute von Knoten und Kanten

Knoten und Kanten können zusätzliche Daten tragen: ein Wörterbuch mit beliebigen Schlüsseln.

```python
graph.add_vertex("Katthult", pos=(0, 1), label="Hof Katthult", einwohner=7)
graph.add_edge("Katthult", "Kirche", 7, belag="Schotter")

graph.vertex_attributes("Katthult")          # {'pos': (0, 1), 'label': 'Hof Katthult', 'einwohner': 7}
graph.vertex_attributes("Katthult")["einwohner"] += 1   # das Wörterbuch gehört zum Graphen
graph.edge_attributes("Kirche", "Katthult")  # {'belag': 'Schotter'}  (ungerichtet: dasselbe Wörterbuch)
```

- `add_vertex` mit Attributen bei einem **bestehenden** Knoten ergänzt bzw. überschreibt dessen Attribute.
- Bei ungerichteten Kanten sind `edge_attributes(u, v)` und `edge_attributes(v, u)` dasselbe Wörterbuch, bei gerichteten Kanten zwei verschiedene.
- `copy()` kopiert die Attribute mit (flach: Listen als Attributwerte werden nicht selbst kopiert).
- `==` vergleicht nur Knoten, Kanten und Gewichte, keine Attribute.

Zwei Attribute haben in der Visualisierung eine besondere Bedeutung:

| Attribut | Wirkung im Player |
|---|---|
| `pos` | Position `(x, y)` des Knotens. Haben **alle** Knoten ein `pos`, zeichnet der Player den Graphen an diesen Stellen (wie eine Landkarte). |
| `label` | Angezeigter Name des Knotens statt `str(v)`. |

Alle anderen Attribute erscheinen im Tooltip, wenn man im Player mit der Maus über einen Knoten fährt.

**Attribute oder `Trace`?** Attribute beschreiben das *Problem* (Positionen, Namen, Einwohnerzahlen). Der *Zustand eines Algorithmus* (besucht, aktuell, Abstand) gehört in einen [`Trace`](visualisierung.md): Algorithmen sollen ihren Eingabegraphen nicht verändern, und nur der `Trace` merkt sich jeden Zwischenstand, sodass man im Player auch rückwärts gehen kann.

## Referenz

### `Edge`

```python
class Edge(NamedTuple):
    u: Vertex
    v: Vertex
    weight: float = 1
```

Ein benanntes Tupel; man kann es auspacken (`for u, v, w in graph.edges()`) oder über `edge.u`, `edge.v`, `edge.weight` zugreifen.

### Erzeugen

| Methode | Beschreibung |
|---|---|
| `Graph(directed=False, *, vertices=None, edges=None)` | Erzeugt einen Graphen. Fügt zuerst die angegebenen Knoten und dann die Kanten als Paare `(u, v)` oder Tripel `(u, v, w)` ein. Ohne Knoten und Kanten entsteht ein leerer Graph. |
| `Graph.from_edges(edges, directed=False, vertices=())` | Graph aus Paaren `(u, v)` oder Tripeln `(u, v, w)`; `vertices` fügt zusätzliche (z. B. isolierte) Knoten hinzu. Ein Eintrag mit anderer Länge löst `ValueError` aus. |
| `directed` | Eigenschaft: `True` für gerichtete Graphen (nur lesbar). |

### Verändern

| Methode | Beschreibung | Fehler |
|---|---|---|
| `add_vertex(v, **attributes)` | Knoten hinzufügen; bestehender Knoten: nur Attribute ergänzen. | - |
| `add_vertices(vertices)` | Mehrere Knoten hinzufügen. | - |
| `add_edge(u, v, weight=1, **attributes)` | Kante hinzufügen; fehlende Endknoten werden angelegt. | `ValueError`: Schleife, doppelte Kante, ungültiges Gewicht |
| `add_edges(edges)` | Mehrere Kanten als `(u, v)` oder `(u, v, w)`. | wie `add_edge` |
| `set_weight(u, v, weight)` | Gewicht einer bestehenden Kante ändern. | `KeyError`, `ValueError` |
| `remove_edge(u, v)` | Kante entfernen (mit ihren Attributen). | `KeyError` |
| `remove_vertex(v)` | Knoten mit allen anliegenden Kanten entfernen. | `KeyError` |

### Abfragen

| Methode | Rückgabe |
|---|---|
| `has_vertex(v)`, `v in graph` | `bool` |
| `has_edge(u, v)` | `bool` (gerichtet: genau diese Richtung) |
| `weight(u, v)` | Gewicht; `KeyError`, falls die Kante fehlt |
| `vertices()` | `list` aller Knoten |
| `edges()` | `list[Edge]`; ungerichtete Kanten genau einmal |
| `neighbors(v)` | Nachbarn bzw. Nachfolger (`list`) |
| `predecessors(v)` | Vorgänger (ungerichtet: wie `neighbors`) |
| `degree(v)`, `in_degree(v)`, `out_degree(v)` | Grade (`int`) |
| `num_vertices()`, `len(graph)` | Anzahl der Knoten |
| `num_edges()` | Anzahl der Kanten |
| `vertex_attributes(v)` | Attribut-Wörterbuch des Knotens (veränderbar) |
| `edge_attributes(u, v)` | Attribut-Wörterbuch der Kante (veränderbar) |
| `for v in graph` | Schleife über alle Knoten |

### Sonstiges

| Methode | Beschreibung |
|---|---|
| `copy()` | Unabhängige Kopie inklusive Attribute. |
| `check_consistency()` | Prüft die interne Datenstruktur (symmetrische Speicherung, Vorgängerlisten, Attribute) und löst bei einem Widerspruch `ValueError` aus. Nützlich, wenn man die internen Wörterbücher direkt verändert hat. |
| `graph1 == graph2` | Gleiche Richtung, Knoten, Kanten und Gewichte. |
| `repr(graph)` | z. B. `Graph(undirected, 6 vertices, 8 edges)` |
