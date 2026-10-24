# Einheit 4: Kürzeste Wege mit Dijkstra (und Bellman-Ford)

## 1. Titel und Lernziele

In Einheit 2 hat die Breitensuche kürzeste Wege gefunden, wenn jede Kante gleich „lang“ ist. In Lönneberga sind die Wege aber unterschiedlich lang: Von Katthult zur Kirche läuft Michel direkt 7 Minuten, über Gibberyd nur $2 + 3 = 5$ Minuten. Nach dieser Einheit können Sie

- gewichtete Abstände definieren und mit Vorgängerzeigern konkrete kürzeste Wege rekonstruieren,
- den Algorithmus von **Dijkstra** mit einer Prioritätswarteschlange (`heapq`) implementieren,
- erklären, warum Dijkstra **nicht-negative Gewichte** braucht, und ein Gegenbeispiel angeben,
- die Laufzeit $O((|V| + |E|) \log |V|)$ begründen,
- (optional) den Algorithmus von **Bellman-Ford** für negative Gewichte implementieren und negative Kreise erkennen.

## 2. Mathematischer Hintergrund

Sei $G = (V, E)$ ein gerichteter oder ungerichteter Graph mit Kantengewichten $w(e)$. Die **Länge** eines Weges $P = (v_0, v_1, \dots, v_k)$ ist die Summe seiner Kantengewichte
$$w(P) = \sum_{i=1}^{k} w(v_{i-1}, v_i).$$
Ein Weg aus nur einem Knoten hat Länge $0$. Der **Abstand** $d(s, t)$ ist die kleinste Länge eines Weges von $s$ nach $t$; gibt es keinen solchen Weg, setzt man $d(s, t) = \infty$. Bei lauter Gewichten $1$ ist das genau der Abstand aus Einheit 2.

**Teilwege kürzester Wege sind kürzeste Wege.** Ist $s = v_0, \dots, v_k = t$ ein kürzester Weg, dann ist jedes Anfangsstück $v_0, \dots, v_i$ ein kürzester Weg von $s$ nach $v_i$ (sonst könnte man das Anfangsstück durch ein kürzeres ersetzen). Deshalb genügt es, für jeden Knoten $v$ seinen **Vorgänger** `parent[v]` auf einem kürzesten Weg zu speichern. Die Kanten $(\text{parent}[v], v)$ bilden einen **Kürzeste-Wege-Baum**, und den Weg zu $v$ erhält man, indem man den Vorgängern rückwärts folgt.

**Dreiecksungleichung.** Für jede Kante $(u, v)$ gilt $d(s, v) \leq d(s, u) + w(u, v)$. Das nutzt jeder Kürzeste-Wege-Algorithmus in Form der **Relaxierung**: Kennt man vorläufig $\text{dist}[u]$ und ist $\text{dist}[u] + w(u, v) < \text{dist}[v]$, so hat man einen kürzeren Weg zu $v$ gefunden und verbessert $\text{dist}[v]$ und $\text{parent}[v]$.

**Der Algorithmus von Dijkstra (1959)** – Voraussetzung: **alle Gewichte $\geq 0$**.

1. $\text{dist}[s] = 0$. Alle anderen Knoten gelten als „unbekannt“ (Abstand $\infty$).
2. Wiederhole: Wähle unter den noch nicht **fertigen** Knoten einen Knoten $u$ mit kleinstem vorläufigem $\text{dist}[u]$. Erkläre $u$ für fertig. Relaxiere alle Kanten $(u, v)$.
3. Ende, wenn kein unfertiger Knoten mit endlichem Abstand übrig ist.

> **Satz.** Sind alle Gewichte nicht-negativ, so gilt in dem Moment, in dem ein Knoten $u$ fertig wird, $\text{dist}[u] = d(s, u)$.

*Beweisidee:* Angenommen, es gibt einen kürzeren Weg $P$ von $s$ nach $u$. $P$ beginnt bei dem fertigen Knoten $s$ und endet bei dem noch unfertigen $u$. Sei $(x, y)$ die erste Kante von $P$, bei der $x$ fertig ist und $y$ nicht. Als $x$ fertig wurde, wurde $(x, y)$ relaxiert, also ist $\text{dist}[y] \leq w(\text{Anfangsstück von } P \text{ bis } y)$. Weil die restlichen Kanten von $P$ **nicht negativ** sind, ist das $\leq w(P) < \text{dist}[u]$. Dann hätte der Algorithmus aber $y$ statt $u$ gewählt – Widerspruch.

**Warum negative Gewichte Dijkstra zerstören.** Im Beweis wurde benutzt, dass ein Weg durch weitere Kanten nicht kürzer werden kann. Gegenbeispiel (gerichtet):

```text
        s --2--> a
        |        ^
        3       -2
        |        |
        +------> b
```

Dijkstra macht $s$ fertig und setzt $\text{dist}[a] = 2$, $\text{dist}[b] = 3$. Dann wird $a$ fertig (mit $2$). Erst danach wird $b$ betrachtet und der Weg $s \to b \to a$ der Länge $3 - 2 = 1$ entdeckt – aber $a$ ist schon fertig. Das Ergebnis $2$ ist falsch. Auch „zu allen Gewichten eine Konstante addieren“ hilft nicht: Wege mit vielen Kanten werden dadurch stärker verlängert als Wege mit wenigen.

**Laufzeit.** Mit einer Prioritätswarteschlange (Binärheap) und *verzögertem Löschen* (siehe Abschnitt 3) wird jede Kante höchstens einmal relaxiert und erzeugt höchstens einen Heap-Eintrag. Der Heap enthält also höchstens $|E| + 1$ Einträge, und jedes `heappush`/`heappop` kostet $O(\log |E|) = O(\log |V|)$ (denn $|E| \leq |V|^2$). Insgesamt: $O((|V| + |E|) \log |V|)$.

**Bellman-Ford (Erweiterung).** Bei negativen Gewichten kann es **negative Kreise** geben (ein Kreis mit negativer Gesamtlänge). Läuft man ihn immer wieder, werden die Wege beliebig kurz, und „kürzester Weg“ ist nicht mehr sinnvoll definiert. Ohne negative Kreise gilt: Es gibt einen kürzesten Weg mit höchstens $|V| - 1$ Kanten. Bellman-Ford relaxiert $|V| - 1$ Runden lang **alle** Kanten.

> **Lemma.** Nach Runde $k$ ist $\text{dist}[v]$ höchstens so groß wie die Länge eines kürzesten Weges von $s$ nach $v$ mit höchstens $k$ Kanten.

Kann man nach $|V| - 1$ Runden immer noch eine Kante relaxieren, muss ein von $s$ erreichbarer negativer Kreis existieren. Laufzeit: $O(|V| \cdot |E|)$.

**Achtung bei ungerichteten Graphen:** Eine ungerichtete Kante $\{u, v\}$ mit $w < 0$ kann man hin und zurück laufen ($u \to v \to u$) und erhält einen geschlossenen Weg der Länge $2w < 0$. Ein ungerichteter Graph mit einer negativen Kante hat also im Sinne von Bellman-Ford immer einen negativen Kreis. Unsere Funktion lehnt solche Graphen daher mit `ValueError` ab.

**Voraussetzungen im Überblick:**

| Algorithmus | Graph | Gewichte | Laufzeit |
|---|---|---|---|
| BFS (Einheit 2) | gerichtet/ungerichtet | alle gleich | $O(\lvert V \rvert + \lvert E \rvert)$ |
| Dijkstra | gerichtet/ungerichtet | $\geq 0$ | $O((\lvert V \rvert + \lvert E \rvert) \log \lvert V \rvert)$ |
| Bellman-Ford | gerichtet (ungerichtet nur mit Gewichten $\geq 0$) | beliebig, ohne negative Kreise | $O(\lvert V \rvert \cdot \lvert E \rvert)$ |

## 3. Relevante Definitionen und Datenstrukturen

| Begriff | Bedeutung |
|---|---|
| **`dist[v]`** | (vorläufige) Länge des kürzesten bekannten Weges von `start` nach `v`; am Ende der Abstand $d(\text{start}, v)$ |
| **`parent[v]`** | Vorgänger von `v` auf diesem Weg; `parent[start] = None` |
| **fertiger Knoten** | Knoten, dessen Abstand endgültig feststeht (wurde aus dem Heap genommen) |
| **Prioritätswarteschlange** | Sammlung, aus der man immer das **kleinste** Element entnimmt |
| **Relaxieren** der Kante $(u, v)$ | Falls `dist[u] + w(u, v) < dist[v]`: `dist[v]` und `parent[v]` verbessern |

### Die Prioritätswarteschlange `heapq`

Pythons Modul `heapq` macht aus einer normalen Liste einen **Binärheap**. `heappush` fügt ein Element ein, `heappop` entnimmt das kleinste. Beides kostet $O(\log n)$. Tupel werden von links nach rechts verglichen, also zuerst nach dem Abstand:

```python
import heapq

heap = []
heapq.heappush(heap, (7, "Kirche"))
heapq.heappush(heap, (2, "Gibberyd"))
heapq.heappush(heap, (4, "Lönneberga"))
heapq.heappop(heap)    # (2, 'Gibberyd')   - das kleinste zuerst
heapq.heappop(heap)    # (4, 'Lönneberga')
len(heap)              # 1
```

**Verzögertes Löschen (*lazy deletion*).** Findet Dijkstra einen kürzeren Weg zu `v`, müsste man den alten Eintrag von `v` im Heap verkleinern. Das kann `heapq` nicht. Stattdessen legt man einfach einen **zusätzlichen** Eintrag `(neuer_abstand, v)` in den Heap. Der alte Eintrag bleibt liegen. Wird später ein Eintrag für einen Knoten entnommen, der schon fertig ist, ist er veraltet und wird übersprungen:

```python
d, u = heapq.heappop(heap)
if u in finished:
    continue          # veralteter Eintrag - ignorieren
finished.add(u)
```

## 4. Problemstellung

Michel will von Katthult aus möglichst schnell zu allen Orten der Umgebung kommen. Gegeben ist der Graph `lib.generators.small_weighted_graph()` (Gewichte = Gehzeit in Minuten):

```text
Katthult --4-- Lönneberga --3-- Backhorva
   |  \            |              |
   2    7          5              6
   |      \        |              |
Gibberyd --3-- Kirche ----2---- Markt
```

Gesucht sind für einen Startknoten `start`

1. die Abstände $d(\text{start}, v)$ zu allen erreichbaren Knoten,
2. die Vorgänger, aus denen sich jeweils ein kürzester Weg ablesen lässt,
3. für ein Ziel `target` ein konkreter kürzester Weg und seine Länge.

Der Graph darf gerichtet sein (z. B. Einbahnstraßen in Vimmerby) – dann werden Kanten nur in Pfeilrichtung benutzt.

## 5. Arbeitsaufträge

1. **Von Hand:** Führen Sie Dijkstra ab Katthult auf Papier aus. Schreiben Sie nach jedem Schritt auf, welcher Knoten fertig wird und wie die Tabelle `dist` aussieht. (Ergebnis zum Vergleich in Abschnitt 7.)
2. **`dijkstra(graph, start)`** – Implementieren Sie Dijkstra mit `heapq`. Rückgabe: `(dist, parent)`, beide nur mit den **erreichbaren** Knoten.
   - Schritt 1: Ist `start` kein Knoten: `KeyError`.
   - Schritt 2: Hat **irgendeine** Kante des Graphen ein negatives Gewicht: `ValueError` (vor dem eigentlichen Algorithmus prüfen).
   - Schritt 3: `dist = {start: 0}`, `parent = {start: None}`, `heap = [(0, start)]`, `finished = set()`.
   - Schritt 4: Solange der Heap nicht leer ist: kleinsten Eintrag `(d, u)` entnehmen; ist `u` schon fertig, überspringen; sonst `u` als fertig markieren und jede Kante `(u, v)` relaxieren. Bei einer Verbesserung: `dist[v]`, `parent[v]` setzen und `(dist[v], v)` in den Heap legen.
3. **`reconstruct_path(parent, target)`** – Folgen Sie den Vorgängern von `target` aus, bis Sie bei `None` ankommen, und drehen Sie die Liste um. Ist `target` nicht in `parent`, Rückgabe `None`.
4. **`shortest_route(graph, start, target)`** – Kombinieren Sie die beiden Funktionen: Rückgabe `(weg, länge)` oder `None`, wenn `target` nicht erreichbar ist.
5. Führen Sie Dijkstra auf dem Gegenbeispiel aus Abschnitt 2 aus, nachdem Sie die Prüfung aus Schritt 2 **vorübergehend** auskommentiert haben. Welchen (falschen) Abstand zu `a` erhalten Sie?
6. Vergleichen Sie auf einem ungewichteten Graphen (z. B. `lib.generators.grid_graph(5, 5)`) Ihr Ergebnis mit den BFS-Abständen. Warum stimmen sie überein?

## 6. Anforderungen an die Implementierung

- `dijkstra` funktioniert für gerichtete und ungerichtete Graphen. Bei gerichteten Graphen liefert `graph.neighbors(u)` genau die Nachfolger; das Gewicht von `(u, v)` ist `graph.weight(u, v)`.
- `dijkstra` löst einen `ValueError` aus, sobald **irgendeine** Kante ein negatives Gewicht hat – auch wenn sie von `start` aus gar nicht erreichbar ist. Gewicht $0$ ist erlaubt.
- Unbekannte Knoten (`start`, bei `shortest_route` auch `target`) lösen einen `KeyError` aus.
- Die Ergebnis-Wörterbücher enthalten **nur** die von `start` aus erreichbaren Knoten. `dist[start] == 0` und `parent[start] is None`.
- Wege sind Listen `[start, ..., target]`; der Weg von `start` zu sich selbst ist `[start]` mit Länge `0`. „Kein Weg“ ist `None`.
- Gibt es mehrere kürzeste Wege, ist jeder richtig.
- Gewichte dürfen Kommazahlen sein (`float`).
- Laufzeit $O((|V| + |E|) \log |V|)$: Verwenden Sie `heapq`, nicht „in jedem Schritt das Minimum aller Knoten suchen“.
- Der Eingabegraph darf nicht verändert werden.

## 7. Beispiele für erwartetes Verhalten

```python
>>> from lib.generators import small_weighted_graph
>>> graph = small_weighted_graph()
>>> dist, parent = dijkstra(graph, "Katthult")
>>> dist
{'Katthult': 0, 'Lönneberga': 4, 'Gibberyd': 2, 'Kirche': 5, 'Backhorva': 7, 'Markt': 7}
>>> parent["Kirche"], parent["Markt"]
('Gibberyd', 'Kirche')
>>> reconstruct_path(parent, "Markt")
['Katthult', 'Gibberyd', 'Kirche', 'Markt']
>>> reconstruct_path(parent, "Stockholm") is None
True
>>> shortest_route(graph, "Katthult", "Backhorva")
(['Katthult', 'Lönneberga', 'Backhorva'], 7)
>>> shortest_route(graph, "Markt", "Markt")
(['Markt'], 0)
>>> from lib.graph import Graph
>>> bad = Graph.from_edges([("s", "a", 2), ("s", "b", 3), ("b", "a", -2)], directed=True)
>>> dijkstra(bad, "s")
Traceback (most recent call last):
ValueError: ...
```

Die Reihenfolge der Einträge im Wörterbuch `dist` darf bei Ihnen anders sein.

```bash
python -m pytest exercises/04_shortest_paths
```

## 8. Hinweise und optionale Zusatzaufgaben

**Hinweise**

- „Noch unbekannt“ prüfen Sie am einfachsten mit `v not in dist`. Statt eines Startwerts $\infty$ können Sie aber auch `dist.get(v, float("inf"))` benutzen.
- Prüfen Sie negative Gewichte mit einer Schleife über `graph.edges()` (`for u, v, weight in graph.edges(): ...`).
- Haben zwei Heap-Einträge denselben Abstand, vergleicht Python als Nächstes die Knoten. Bei Zeichenketten oder Zahlen ist das kein Problem. Wollen Sie beliebige Knoten erlauben, fügen Sie einen laufenden Zähler ein: `(d, nummer, v)` mit `nummer = next(zaehler)` und `zaehler = itertools.count()`.
- Für `reconstruct_path`: Dieselbe Idee wie `shortest_path` in Einheit 2.
- Mit `lib.testing.assert_valid_path(graph, path)` und `lib.utils.path_weight(graph, path)` können Sie Ihre Wege selbst prüfen.

**Optionale Zusatzaufgaben**

1. **`bellman_ford(graph, start)`** – Gleiches Rückgabeformat wie `dijkstra`, aber negative Gewichte in **gerichteten** Graphen sind erlaubt.
   - Schritt 1: `KeyError` für unbekanntes `start`; `ValueError` für einen ungerichteten Graphen mit einer negativen Kante (siehe Abschnitt 2).
   - Schritt 2: Wiederholen Sie $|V| - 1$ Mal: Relaxieren Sie **jede** Kante $(u, v)$, für die `u` schon einen Abstand hat. (Bei ungerichteten Graphen beide Richtungen! Am einfachsten: `for u in graph.vertices(): for v in graph.neighbors(u): ...`.) Hat sich in einer Runde nichts geändert, können Sie aufhören.
   - Schritt 3: Lässt sich danach noch eine Kante relaxieren, ist ein negativer Kreis von `start` aus erreichbar: `ValueError`.
2. Konstruieren Sie ein eigenes Gegenbeispiel (anders als das aus Abschnitt 2): einen gerichteten Graphen mit negativen Gewichten, aber **ohne** negativen Kreis, auf dem Dijkstra (ohne die Prüfung aus Schritt 2) für mindestens zwei Knoten falsche Abstände liefert. Prüfen Sie die richtigen Werte mit `bellman_ford`.
3. Messen Sie mit `lib.utils.measure_time` Ihr `dijkstra` auf `lib.generators.random_connected_graph(n, 3 * n, max_weight=100)` für $n = 1000, 2000, 4000, 8000$. Wächst die Zeit etwa wie $n \log n$?
4. **Gesamtabstände:** Schreiben Sie eine Funktion, die für jeden Ort die Summe der Abstände zu allen anderen Orten berechnet. Von welchem Ort im Lönneberga-Graphen ist alles am schnellsten erreichbar?
5. Beweisen Sie: Hat ein Graph positive Gewichte und ist $P$ ein kürzester Weg von $s$ nach $t$, so ist jedes Teilstück von $P$ ein kürzester Weg zwischen seinen Endknoten.

## 9. Quellen und weiterführende Literatur

- E. W. Dijkstra: *A note on two problems in connexion with graphs*. Numerische Mathematik 1, 1959, S. 269–271.
- R. Bellman: *On a routing problem*. Quarterly of Applied Mathematics 16(1), 1958, S. 87–90.
- L. R. Ford Jr.: *Network Flow Theory*. RAND Corporation, Paper P-923, 1956.
- M. L. Fredman, R. E. Tarjan: *Fibonacci heaps and their uses in improved network optimization algorithms*. Journal of the ACM 34(3), 1987, S. 596–615 (Dijkstra in $O(|E| + |V| \log |V|)$).
- T. H. Cormen, C. E. Leiserson, R. L. Rivest, C. Stein: *Algorithmen – Eine Einführung*. De Gruyter, 4. Auflage 2022, Kapitel „Kürzeste Wege von einem Startknoten aus“ (Bellman-Ford, Dijkstra) und Kapitel über Heaps und Prioritätswarteschlangen.
- J. Kleinberg, É. Tardos: *Algorithm Design*. Pearson 2005, Abschnitt 4.4 (Shortest Paths in a Graph) und Abschnitt 6.8 (Shortest Paths and Distance Vector Protocols).
- S. O. Krumke, H. Noltemeier: *Graphentheoretische Konzepte und Algorithmen*. Springer Vieweg, 3. Auflage 2012 (Kapitel über kürzeste Wege).
- Python-Dokumentation zu `heapq`: <https://docs.python.org/3/library/heapq.html>
