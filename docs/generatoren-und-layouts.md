# Generatoren und Layouts

## Beispielgraphen: `lib.generators`

Alle Generatoren liefern einen `Graph`. Wenn nicht anders angegeben, heißen die Knoten `0, 1, …, n-1`. Zufallsgeneratoren haben einen optionalen `seed`: Mit demselben Seed entsteht immer derselbe Graph. Das macht Experimente und Tests reproduzierbar. Negative Größen führen zu `ValueError`.

### Feste Graphen

| Funktion | Graph | Knoten / Kanten |
|---|---|---|
| `path_graph(n, directed=False)` | Pfad $P_n$: `0 - 1 - … - (n-1)` | $n$ / $n-1$ |
| `cycle_graph(n, directed=False)` | Kreis $C_n$ ($n \ge 3$) | $n$ / $n$ |
| `complete_graph(n)` | vollständiger Graph $K_n$ | $n$ / $\binom{n}{2}$ |
| `complete_bipartite_graph(m, n)` | $K_{m,n}$; Knoten `"L0"…`, `"R0"…` | $m+n$ / $mn$ |
| `star_graph(n)` | Stern $K_{1,n}$, Mittelpunkt `0` | $n+1$ / $n$ |
| `grid_graph(rows, cols)` | Gitter; Knoten `(zeile, spalte)` | $rc$ / $r(c-1)+c(r-1)$ |
| `petersen_graph()` | Petersen-Graph: außen `0…4`, innen `5…9` | 10 / 15 |
| `small_weighted_graph()` | kleines gewichtetes Netz rund um Lönneberga (Gehzeiten in Minuten) | 6 / 8 |

### Zufallsgraphen

| Funktion | Beschreibung |
|---|---|
| `random_graph(n, p, seed=None, directed=False)` | $G(n, p)$ nach Erdős und Rényi: jede mögliche Kante unabhängig mit Wahrscheinlichkeit $p$ |
| `random_tree(n, seed=None)` | zufälliger Baum: Knoten $i$ hängt an einem zufälligen Knoten $j < i$ |
| `random_connected_graph(n, extra_edges, seed=None, min_weight=1, max_weight=1)` | Zufallsbaum plus `extra_edges` weitere Kanten, garantiert zusammenhängend; ganzzahlige Zufallsgewichte |
| `random_bipartite_graph(m, n, p, seed=None)` | zufälliger bipartiter Graph, Knoten `"L…"` und `"R…"` |
| `random_weighted_graph(n, p, min_weight=1, max_weight=10, seed=None, directed=False)` | $G(n, p)$ mit ganzzahligen Zufallsgewichten |

```python
from lib import generators

grid = generators.grid_graph(4, 6)
net = generators.random_connected_graph(12, 6, seed=7, min_weight=1, max_weight=20)
```

## Knoten anordnen: `lib.layout`

Ein Layout ist ein Wörterbuch `knoten -> (x, y)`. Alle Funktionen liefern Koordinaten im Quadrat $[0,1] \times [0,1]$; das Seitenverhältnis bleibt erhalten, `y` zeigt nach oben. Die Funktionen sind reines Python und verwenden keinen der Algorithmen aus den Übungen. Im Alltag braucht man sie selten direkt: Der Player ruft `compute_layout` mit den Optionen von `Trace` bzw. `snapshot` auf (siehe [Visualisierung, Abschnitt 10](visualisierung.md#10-anordnung-der-knoten-layouts)).

| Funktion | Beschreibung |
|---|---|
| `compute_layout(graph, layout="auto", *, left=None, layers=None, shells=None, seed=0)` | zentraler Einstieg: wählt das passende Verfahren (Reihenfolge bei `"auto"`: `pos`-Attribute, `left`/`layers`/`shells`, dann `auto_layout`) |
| `auto_layout(graph, seed=0)` | Gitter für `(zeile, spalte)`-Knoten; Kreis für vollständige Graphen und Kreise; sonst `spring_layout` |
| `spring_layout(graph, seed=0, iterations=300, attempts=6)` | kräftebasiert (siehe unten) |
| `circular_layout(vertices, start_angle=90.0)` | gleichmäßig auf einem Kreis, der erste Knoten oben |
| `shell_layout(shells)` | eine Liste pro Kreis, die erste außen |
| `bipartite_layout(graph, left)` | zwei Spalten |
| `layered_layout(layers, horizontal=True, spacing=1.0)` | eine Spalte (oder Zeile) pro Schicht |
| `grid_layout(graph)` | Knoten `(zeile, spalte)`, Zeile 0 oben |
| `normalize(positions, margin=0.0)` | beliebige Koordinaten in $[0,1]^2$ skalieren |

### Das kräftebasierte Layout

`spring_layout` folgt dem Verfahren von Fruchterman und Reingold (1991). Man stellt sich die Knoten als elektrisch geladene Kugeln vor, die sich gegenseitig abstoßen (Kraft $k^2/d$), und die Kanten als Federn, die benachbarte Knoten anziehen (Kraft $d^2/k$). Ausgehend von zufälligen Startpositionen bewegt sich jeder Knoten schrittweise in Richtung der Gesamtkraft, die Schrittweite („Temperatur“) nimmt dabei ab.

Ergänzungen für schöne Bilder:

- **Komponenten einzeln:** Jede Zusammenhangskomponente wird für sich angeordnet. Danach werden die Komponenten nebeneinander gesetzt, die größte zuerst.
- **Mehrere Versuche:** Pro Komponente werden mehrere Startpositionen probiert. Gewonnen hat der Versuch mit den wenigsten Kantenkreuzungen, den wenigsten Kanten dicht an fremden Knoten und den wenigsten zu eng stehenden Knoten.
- **Platz für Beschriftungen:** Ein Nachbearbeitungsschritt schiebt zu nahe Knoten auseinander, waagerecht mit doppeltem Abstand, weil die Namensboxen breiter als hoch sind.

Laufzeit $O(\text{Versuche} \cdot \text{Iterationen} \cdot |V|^2)$: für die Graphen des Kurses (bis etwa 100 Knoten) ausreichend schnell. Ein anderer `seed` liefert ein anderes Bild.

Literatur: T. M. J. Fruchterman, E. M. Reingold: *Graph drawing by force-directed placement*. Software – Practice and Experience 21(11), 1991, S. 1129–1164.
