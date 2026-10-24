# Einheit 1: Graphen modellieren

## 1. Titel und Lernziele

In dieser Einheit lernen Sie, Graphen mit der Kursbibliothek `lib` in Python darzustellen. Nach der Einheit können Sie

- ein kleines Netzwerk aus einer Beschreibung in einen Graphen übersetzen,
- zwischen gerichteten und ungerichteten Graphen unterscheiden,
- Knotengrade (bzw. Eingangs- und Ausgangsgrade) selbst berechnen,
- das Handschlaglemma am Rechner überprüfen,
- erklären, wie eine Adjazenzliste und eine Adjazenzmatrix aufgebaut sind.

## 2. Mathematischer Hintergrund

Ein **Graph** ist ein Paar $G = (V, E)$ aus einer endlichen Knotenmenge $V$ und einer Kantenmenge $E$. In einem **ungerichteten** Graphen ist jede Kante eine zweielementige Teilmenge $\{u, v\} \subseteq V$. In einem **gerichteten** Graphen ist jede Kante ein geordnetes Paar $(u, v)$ mit $u \neq v$.

Wir arbeiten im ganzen Kurs mit **einfachen Graphen**: Es gibt keine Schleifen (Kanten von einem Knoten zu sich selbst) und keine Mehrfachkanten.

Das wichtigste Ergebnis dieser Einheit ist das

> **Handschlaglemma.** Für jeden ungerichteten Graphen $G = (V, E)$ gilt
> $$\sum_{v \in V} \deg(v) = 2\,|E|.$$

*Beweisidee:* Jede Kante $\{u, v\}$ wird in der Summe genau zweimal gezählt: einmal bei $\deg(u)$ und einmal bei $\deg(v)$.

**Folgerung:** Die Anzahl der Knoten mit ungeradem Grad ist gerade. (Warum? Die Summe der Grade ist gerade, also muss die Summe der ungeraden Grade auch gerade sein.)

Für gerichtete Graphen gilt entsprechend $\sum_v \deg^+(v) = \sum_v \deg^-(v) = |E|$.

## 3. Relevante Definitionen

| Begriff | Definition | In Python (`lib.graph.Graph`) |
|---|---|---|
| Knoten (Ecke) | Element von $V$ | jeder hashbare Wert, z. B. `"Nordhof"` oder `3` |
| Kante | $\{u,v\}$ bzw. $(u,v)$ | `graph.add_edge(u, v)`; `graph.edges()` liefert `Edge(u, v, weight)` |
| Nachbarn | $N(v) = \{u : \{u, v\} \in E\}$ | `graph.neighbors(v)` |
| Grad | $\deg(v) = \lvert N(v) \rvert$ | `graph.degree(v)` |
| Ausgangsgrad | $\deg^+(v)$ = Anzahl der Kanten $(v, w)$ | `graph.out_degree(v)` |
| Eingangsgrad | $\deg^-(v)$ = Anzahl der Kanten $(u, v)$ | `graph.in_degree(v)` |
| Gradfolge | Grade aller Knoten, absteigend sortiert | – (Aufgabe) |
| Adjazenzmatrix | $A_{ij} = 1$, falls Kante von $v_i$ nach $v_j$, sonst $0$ | – (Aufgabe) |

**Adjazenzliste.** Die Klasse `Graph` speichert für jeden Knoten ein Wörterbuch seiner Nachbarn (mit Kantengewicht):

```python
{
    "Nordhof":   {"Mittelhof": 1, "Südhof": 1},
    "Mittelhof": {"Nordhof": 1, "Südhof": 1},
    "Südhof":    {"Mittelhof": 1, "Nordhof": 1},
}
```

Speicherbedarf: $O(|V| + |E|)$. Eine Adjazenzmatrix braucht dagegen immer $|V|^2$ Einträge.

**Kurzer Python-Überblick** für diese Einheit:

```python
from lib.graph import Graph

graph = Graph(directed=False)          # leerer ungerichteter Graph
graph.add_edge("A", "B")               # Kante A - B (Knoten werden automatisch angelegt)
graph.add_vertex("C")                  # isolierter Knoten
graph.vertices()                       # ['A', 'B', 'C']
graph.edges()                          # [Edge(u='A', v='B', weight=1)]
for u, v, weight in graph.edges():     # Kanten auspacken
    print(u, v)
counts = {}                            # ein Wörterbuch (dict)
counts["A"] = 0
counts["A"] += 1
```

## 4. Problemstellung

In Bullerbü gibt es drei Höfe und einige Lieblingsorte der Kinder. Die Trampelpfade zwischen den Orten bilden einen ungerichteten Graphen:

| Pfad von | nach |
|---|---|
| Nordhof | Mittelhof |
| Mittelhof | Südhof |
| Nordhof | Südhof |
| Mittelhof | Schule |
| Schule | Kaufladen |
| Kaufladen | Badestelle |
| Südhof | Badestelle |
| Badestelle | Erdbeerstelle |
| Nordhof | Erdbeerstelle |

Außerdem schreiben sich die Kinder Briefe. Ein Brief hat einen Absender und einen Empfänger, daher ist dieses Netzwerk **gerichtet**:

| Absender | Empfänger |
|---|---|
| Lisa | Britta |
| Lisa | Inga |
| Britta | Lisa |
| Inga | Britta |
| Lasse | Ole |
| Bosse | Lasse |
| Ole | Bosse |
| Lasse | Lisa |

## 5. Arbeitsaufträge

Bearbeiten Sie die Funktionen in `task.py` in dieser Reihenfolge. Ersetzen Sie jeweils die Zeile `raise NotImplementedError(...)` durch Ihre Implementierung.

1. **`build_bullerby_graph()`** – Erzeugen Sie den ungerichteten Pfad-Graphen aus der ersten Tabelle. Verwenden Sie die Ortsnamen genau wie angegeben (also „Südhof“ mit „ü“).
2. **`build_letter_graph()`** – Erzeugen Sie den gerichteten Brief-Graphen aus der zweiten Tabelle.
3. **`degrees(graph)`** – Berechnen Sie für jeden Knoten seinen Grad, **ohne** `graph.degree()` zu verwenden. Zählen Sie stattdessen beim Durchlaufen von `graph.edges()` für jede Kante beide Endknoten. Isolierte Knoten haben Grad 0.
4. **`degree_sequence(graph)`** – Geben Sie die Gradfolge (absteigend sortiert) zurück.
5. **`odd_degree_vertices(graph)`** – Geben Sie alle Knoten mit ungeradem Grad zurück.
6. **`check_handshake_lemma(graph)`** – Prüfen Sie für einen ungerichteten Graphen, ob die Gradsumme gleich $2|E|$ ist.
7. **`in_and_out_degrees(graph)`** – Berechnen Sie für einen gerichteten Graphen zu jedem Knoten das Paar `(Eingangsgrad, Ausgangsgrad)`, wieder durch Zählen der Kanten.
8. **`adjacency_matrix(graph, order)`** – Erzeugen Sie die Adjazenzmatrix als Liste von Listen.
9. Führen Sie `python task.py` aus und beantworten Sie: Wie viele Knoten mit ungeradem Grad hat der Bullerbü-Graph? Passt das zur Folgerung aus dem Handschlaglemma?

## 6. Anforderungen an die Implementierung

- Verwenden Sie die Klasse `Graph` aus `lib.graph`. Andere Bibliotheken sind nicht nötig.
- `degrees` und `in_and_out_degrees` dürfen `graph.degree`, `graph.in_degree` und `graph.out_degree` **nicht** verwenden – die Tests vergleichen Ihr Ergebnis aber mit diesen Methoden.
- `check_handshake_lemma` löst bei einem gerichteten Graphen einen `ValueError` aus; `in_and_out_degrees` löst bei einem ungerichteten Graphen einen `ValueError` aus.
- `adjacency_matrix` verwendet die Knotenreihenfolge `order`; ohne `order` die Reihenfolge von `graph.vertices()`. Enthält `order` nicht genau alle Knoten (jeden einmal), wird ein `ValueError` ausgelöst.
- Auch der leere Graph (ohne Knoten) muss funktionieren.

## 7. Beispiele für erwartetes Verhalten

```python
>>> from lib.graph import Graph
>>> g = Graph.from_edges([("A", "B"), ("B", "C")], vertices=["D"])
>>> degrees(g)
{'D': 0, 'A': 1, 'B': 2, 'C': 1}
>>> degree_sequence(g)
[2, 1, 1, 0]
>>> odd_degree_vertices(g)
['A', 'C']
>>> check_handshake_lemma(g)
True
>>> adjacency_matrix(g, order=["A", "B", "C", "D"])
[[0, 1, 0, 0], [1, 0, 1, 0], [0, 1, 0, 0], [0, 0, 0, 0]]
>>> letters = Graph.from_edges([("x", "y"), ("y", "z"), ("x", "z")], directed=True)
>>> in_and_out_degrees(letters)
{'x': (0, 2), 'y': (1, 1), 'z': (2, 0)}
```

Testen Sie Ihre Lösung im Hauptordner des Projekts mit

```bash
python -m pytest exercises/01_graph_basics
```

## 8. Hinweise und optionale Zusatzaufgaben

**Hinweise**

- Ein Wörterbuch mit Startwert 0 für alle Knoten erzeugen Sie z. B. mit `{v: 0 for v in graph.vertices()}`.
- Absteigend sortieren: `sorted(liste, reverse=True)`.
- Eine Zahl `k` ist ungerade, wenn `k % 2 == 1`.
- Eine Matrix mit `n` Zeilen und `n` Spalten voller Nullen: `[[0] * n for _ in range(n)]`. (Achtung: `[[0] * n] * n` erzeugt n-mal *dieselbe* Zeile!)
- Um den Index eines Knotens schnell zu finden, lohnt sich ein Wörterbuch `index = {v: i for i, v in enumerate(order)}`.
- Mit `print_graph(graph)` aus `lib.visualization` können Sie jeden Graphen ansehen.

**Optionale Zusatzaufgaben**

1. **`complement(graph)`** (in `task.py`, getestet, wenn implementiert): Berechnen Sie den Komplementgraphen $\bar G$: gleiche Knoten, und $\{u,v\}$ ist genau dann eine Kante in $\bar G$, wenn sie keine Kante in $G$ ist. Wie viele Kanten hat das Komplement eines Graphen mit $n$ Knoten und $m$ Kanten?
2. Zeigen Sie mathematisch: In jedem Graphen mit mindestens zwei Knoten gibt es zwei Knoten mit gleichem Grad. Prüfen Sie die Aussage mit `lib.generators.random_graph` an vielen Zufallsgraphen.
3. Exportieren Sie den Bullerbü-Graphen mit `lib.visualization.save_dot` und lassen Sie ihn mit Graphviz zeichnen.
4. Ist $(3, 3, 1, 1)$ eine Gradfolge eines einfachen Graphen? Ist $(3, 2, 2, 2, 1)$ eine? Begründen Sie (Stichwort: Satz von Havel-Hakimi).

## 9. Quellen und weiterführende Literatur

- R. Diestel: *Graphentheorie*. Springer, 5. Auflage 2017, Kapitel 1.1–1.2.
- S. O. Krumke, H. Noltemeier: *Graphentheoretische Konzepte und Algorithmen*. Springer Vieweg, 3. Auflage 2012, Kapitel 2.
- T. H. Cormen, C. E. Leiserson, R. L. Rivest, C. Stein: *Algorithmen – Eine Einführung*. De Gruyter, 4. Auflage 2022, Abschnitt „Darstellung von Graphen“.
- L. Euler: *Solutio problematis ad geometriam situs pertinentis*. Commentarii academiae scientiarum Petropolitanae 8 (1736/1741), S. 128–140 – hier taucht das Zählargument des Handschlaglemmas erstmals auf.
- Python-Dokumentation zu Wörterbüchern: <https://docs.python.org/3/tutorial/datastructures.html#dictionaries>
