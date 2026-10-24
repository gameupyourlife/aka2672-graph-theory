# Einheit 2: Breitensuche (BFS) und Tiefensuche (DFS)

## 1. Titel und Lernziele

Breiten- und Tiefensuche sind die Grundbausteine fast aller Graphalgorithmen. Nach dieser Einheit können Sie

- Breitensuche und Tiefensuche selbst implementieren,
- erklären, warum BFS eine **Warteschlange** (Queue) und DFS einen **Stapel** (Stack) benutzt,
- mit BFS kürzeste Wege in ungewichteten Graphen bestimmen und konkrete Wege rekonstruieren,
- alle Zusammenhangskomponenten eines Graphen berechnen,
- die Laufzeit $O(|V| + |E|)$ begründen.

## 2. Mathematischer Hintergrund

Ein **Weg** (Pfad) von $s$ nach $t$ ist eine Folge paarweise verschiedener Knoten $s = v_0, v_1, \dots, v_k = t$, in der aufeinanderfolgende Knoten durch eine Kante verbunden sind. Seine **Länge** ist die Anzahl $k$ der Kanten. Der **Abstand** $d(s, t)$ ist die Länge eines kürzesten Weges von $s$ nach $t$.

Ein ungerichteter Graph heißt **zusammenhängend**, wenn je zwei Knoten durch einen Weg verbunden sind. Die Relation „$u$ und $v$ sind durch einen Weg verbunden“ ist eine Äquivalenzrelation; ihre Äquivalenzklassen heißen **Zusammenhangskomponenten**.

**Satz (BFS-Abstände).** Die Breitensuche ab $s$ besucht die Knoten in nicht-fallender Reihenfolge ihres Abstands zu $s$. Der Wert `distance[v]` ist genau $d(s, v)$.

*Beweisidee:* Durch Induktion über $k$ zeigt man: Alle Knoten mit Abstand $k$ werden in die Warteschlange gelegt, bevor ein Knoten mit Abstand $k+1$ hineinkommt. Ein Knoten mit Abstand $k + 1$ hat einen Nachbarn mit Abstand $k$ und wird von dem ersten solchen Nachbarn entdeckt.

**Laufzeit.** Jeder Knoten wird höchstens einmal in die Warteschlange bzw. auf den Stapel gelegt und einmal bearbeitet. Bei der Bearbeitung von $v$ werden seine $\deg(v)$ Nachbarn betrachtet. Nach dem Handschlaglemma (Einheit 1) ist $\sum_v \deg(v) = 2|E|$. Insgesamt ergibt das $O(|V| + |E|)$.

## 3. Relevante Definitionen und Datenstrukturen

| Begriff | Bedeutung |
|---|---|
| **Warteschlange (Queue)** | „Wer zuerst kommt, mahlt zuerst“ (FIFO: *first in, first out*). In Python: `collections.deque` mit `append` (hinten anfügen) und `popleft` (vorne entnehmen). Beides kostet $O(1)$. |
| **Stapel (Stack)** | „Was zuletzt hingelegt wurde, wird zuerst genommen“ (LIFO: *last in, first out*). In Python: eine normale Liste mit `append` und `pop`. |
| **Vorgänger** `parent[v]` | Der Knoten, von dem aus $v$ entdeckt wurde. Die Kanten $(\text{parent}[v], v)$ bilden einen **BFS-Baum**. Für den Startknoten ist `parent[start] = None`. |
| **Besuchte Knoten** | Eine Menge (`set`), damit kein Knoten zweimal bearbeitet wird. `v in visited` kostet im Mittel $O(1)$. |

```python
from collections import deque

queue = deque(["A"])
queue.append("B")      # deque(['A', 'B'])
first = queue.popleft()  # 'A'

stack = ["A"]
stack.append("B")      # ['A', 'B']
top = stack.pop()      # 'B'
```

## 4. Problemstellung

Michel aus Lönneberga will wissen, wie viele Wegabschnitte er mindestens braucht, um von Katthult zu einem anderen Ort zu kommen. Mit welchen Orten ist Katthult überhaupt verbunden? Gegeben ist ein Graph `graph` und ein Startknoten `start`. Gesucht sind

1. alle von `start` aus erreichbaren Knoten,
2. die Abstände (Anzahl der Kanten) zu diesen Knoten,
3. jeweils ein kürzester Weg,
4. die Zusammenhangskomponenten des ganzen Graphen.

## 5. Arbeitsaufträge

1. **`bfs(graph, start)`** – Implementieren Sie die Breitensuche. Rückgabe: ein Paar `(distance, parent)` von Wörterbüchern, die **nur die erreichbaren Knoten** enthalten.
   - Schritt 1: `distance = {start: 0}`, `parent = {start: None}`, Warteschlange mit `start`.
   - Schritt 2: Solange die Warteschlange nicht leer ist: vordersten Knoten `u` entnehmen, alle Nachbarn `w` betrachten. Ist `w` noch nicht entdeckt, so setzen Sie `distance[w]`, `parent[w]` und hängen `w` hinten an.
2. **`shortest_path(graph, start, target)`** – Bestimmen Sie mit `bfs` einen kürzesten Weg als Liste `[start, ..., target]`. Gehen Sie dazu von `target` aus den Vorgängern rückwärts bis zu `start` nach und drehen Sie die Liste am Ende um. Ist `target` nicht erreichbar, geben Sie `None` zurück.
3. **`dfs(graph, start)`** – Implementieren Sie die Tiefensuche **iterativ mit einem Stapel**. Rückgabe: die Liste der erreichbaren Knoten in der Reihenfolge, in der sie besucht werden (`start` zuerst).
4. **`connected_components(graph)`** – Bestimmen Sie alle Zusammenhangskomponenten eines ungerichteten Graphen als Liste von Mengen. Idee: Starten Sie von jedem noch nicht gesehenen Knoten eine Suche (BFS oder DFS); alles, was sie findet, ist eine Komponente.
5. **`is_connected(graph)`** – Prüfen Sie, ob der Graph zusammenhängend ist.
6. Ersetzen Sie in `dfs` den Stapel durch eine Warteschlange. Was passiert mit der Besuchsreihenfolge? Notieren Sie Ihre Beobachtung.

## 6. Anforderungen an die Implementierung

- Alle Funktionen funktionieren für gerichtete und ungerichtete Graphen. Bei gerichteten Graphen werden die Kanten nur in Pfeilrichtung benutzt (`graph.neighbors` liefert genau diese Nachfolger). **Ausnahme:** `connected_components` und `is_connected` lösen bei gerichteten Graphen einen `ValueError` aus.
- Ist `start` kein Knoten des Graphen, wird ein `KeyError` ausgelöst (das passiert automatisch, wenn Sie `graph.neighbors(start)` aufrufen; prüfen Sie es trotzdem am Anfang mit `start not in graph`).
- Jeder Knoten darf höchstens einmal besucht werden; die Laufzeit muss $O(|V| + |E|)$ sein. Verwenden Sie daher `deque` statt `list.pop(0)` (das kostet $O(n)$).
- Der leere Graph gilt als zusammenhängend (`is_connected(Graph())` ist `True`) und hat keine Komponenten.
- Die Eingabe darf nicht verändert werden.

## 7. Beispiele für erwartetes Verhalten

```python
>>> from lib.graph import Graph
>>> g = Graph.from_edges([("A", "B"), ("A", "C"), ("B", "D"), ("C", "D"), ("D", "E")])
>>> g.add_vertex("Z")
>>> distance, parent = bfs(g, "A")
>>> distance
{'A': 0, 'B': 1, 'C': 1, 'D': 2, 'E': 3}
>>> parent
{'A': None, 'B': 'A', 'C': 'A', 'D': 'B', 'E': 'D'}
>>> shortest_path(g, "A", "E")
['A', 'B', 'D', 'E']
>>> shortest_path(g, "A", "Z") is None
True
>>> dfs(g, "A")            # eine mögliche Reihenfolge
['A', 'C', 'D', 'E', 'B']
>>> connected_components(g)
[{'A', 'B', 'C', 'D', 'E'}, {'Z'}]
>>> is_connected(g)
False
```

Die Reihenfolge bei `dfs` hängt davon ab, in welcher Reihenfolge Sie Nachbarn auf den Stapel legen; die Tests akzeptieren jede gültige Reihenfolge.

```bash
python -m pytest exercises/02_bfs_dfs
```

## 8. Hinweise und optionale Zusatzaufgaben

**Hinweise**

- Markieren Sie einen Knoten bei der BFS als entdeckt, **sobald** Sie ihn in die Warteschlange legen – nicht erst beim Herausnehmen. Sonst kann ein Knoten mehrfach in der Warteschlange landen.
- Bei der iterativen DFS ist es einfacher, einen Knoten erst beim **Herausnehmen** vom Stapel als besucht zu markieren (und bereits besuchte Knoten dann zu überspringen).
- Für `shortest_path`: `path.reverse()` dreht eine Liste um.
- Mit `lib.testing.assert_valid_path(graph, path)` können Sie selbst prüfen, ob eine Liste ein gültiger Weg ist.

**Optionale Zusatzaufgaben**

1. **`dfs_recursive(graph, start)`** – Schreiben Sie die Tiefensuche rekursiv. Für sehr große Graphen (z. B. ein Pfad mit 5000 Knoten) scheitert das an Pythons Rekursionstiefe. Warum?
2. **`bfs_layers(graph, start)`** – Geben Sie die BFS-„Schichten“ als Liste von Listen zurück: `[[start], [Knoten mit Abstand 1], [Knoten mit Abstand 2], ...]`.
3. Messen Sie mit `lib.utils.measure_time` die Laufzeit Ihrer BFS auf `lib.generators.random_graph(n, 4 / n)` für $n = 1000, 2000, 4000, 8000$. Wächst sie ungefähr linear?
4. Beweisen Sie: Ein Graph mit $n$ Knoten und weniger als $n - 1$ Kanten ist nicht zusammenhängend.

## 9. Quellen und weiterführende Literatur

- T. H. Cormen, C. E. Leiserson, R. L. Rivest, C. Stein: *Algorithmen – Eine Einführung*. De Gruyter, 4. Auflage 2022, Kapitel „Elementare Graphalgorithmen“ (Breitensuche, Tiefensuche).
- J. Kleinberg, É. Tardos: *Algorithm Design*. Pearson 2005, Kapitel 3 (Graphs).
- R. Diestel: *Graphentheorie*. Springer, 5. Auflage 2017, Abschnitt 1.4 (Zusammenhang).
- E. F. Moore: *The shortest path through a maze*. Proceedings of the International Symposium on the Theory of Switching, Harvard University Press 1959, S. 285–292 (eine frühe Beschreibung der Breitensuche).
- R. E. Tarjan: *Depth-first search and linear graph algorithms*. SIAM Journal on Computing 1(2), 1972, S. 146–160.
- Python-Dokumentation zu `collections.deque`: <https://docs.python.org/3/library/collections.html#collections.deque>
