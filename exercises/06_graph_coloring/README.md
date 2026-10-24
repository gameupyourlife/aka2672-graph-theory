# Einheit 6: Graphfärbung

## 1. Titel und Lernziele

Stundenpläne ohne Überschneidungen, Funkfrequenzen ohne Störungen, Sitzpläne ohne Streit: Viele Zuordnungsprobleme sind **Färbungsprobleme**. Nach dieser Einheit können Sie

- erklären, was eine (zulässige) Knotenfärbung und die chromatische Zahl $\chi(G)$ sind,
- Färbungen auf Zulässigkeit prüfen,
- den Greedy-Algorithmus implementieren und beweisen, dass er höchstens $\Delta(G) + 1$ Farben braucht,
- an Beispielen zeigen, wie stark das Ergebnis von der Knotenreihenfolge abhängt (Kronengraph, Welsh-Powell-Reihenfolge),
- den Satz von König beweisen: $G$ ist genau dann bipartit, wenn $G$ keinen Kreis ungerader Länge enthält,
- mit einer Breitensuche in $O(|V| + |E|)$ entscheiden, ob ein Graph bipartit ist,
- einordnen, warum schon die Frage „Reichen 3 Farben?“ NP-vollständig ist.

## 2. Mathematischer Hintergrund

### 2.1 Färbungen und chromatische Zahl

Sei $G = (V, E)$ ein ungerichteter Graph. Eine **$k$-Färbung** ist eine Abbildung $c : V \to \{0, 1, \dots, k-1\}$ mit
$$c(u) \ne c(v) \quad \text{für jede Kante } \{u, v\} \in E.$$
Solche Färbungen heißen auch **zulässig** oder **echt**. Die Knoten einer Farbe bilden eine **Farbklasse**; jede Farbklasse ist eine **unabhängige Menge** (keine zwei ihrer Knoten sind benachbart). Eine $k$-Färbung ist also dasselbe wie eine Zerlegung von $V$ in $k$ unabhängige Mengen.

Die **chromatische Zahl** $\chi(G)$ ist das kleinste $k$, für das $G$ eine $k$-Färbung besitzt.

Beispiele:

| Graph | $\chi$ | Begründung |
|---|---|---|
| ohne Kanten (mindestens ein Knoten) | 1 | alle Knoten dieselbe Farbe |
| $K_n$ | $n$ | alle Knoten paarweise benachbart |
| $C_n$, $n$ gerade | 2 | Farben abwechseln |
| $C_n$, $n$ ungerade | 3 | abwechseln geht nicht auf (Aufgabe 7) |
| Baum mit mindestens einer Kante | 2 | Farbe = Abstand zur Wurzel modulo 2 |
| Petersen-Graph | 3 | enthält einen 5-Kreis; eine 3-Färbung existiert (Aufgabe 11) |

**Untere Schranken.** Enthält $G$ eine **Clique** mit $\omega$ Knoten (paarweise benachbart), so gilt $\chi(G) \ge \omega$. Ist $\alpha$ die Größe einer größten unabhängigen Menge, so gilt $\chi(G) \ge |V| / \alpha$, denn jede Farbklasse hat höchstens $\alpha$ Knoten.

### 2.2 Der Greedy-Algorithmus

Gegeben ist eine Reihenfolge $v_1, v_2, \dots, v_n$ der Knoten. Färbe die Knoten in dieser Reihenfolge; $v_i$ erhält die **kleinste Farbe**, die keiner der bereits gefärbten Nachbarn von $v_i$ hat.

> **Satz.** Der Greedy-Algorithmus liefert für jede Reihenfolge eine zulässige Färbung mit höchstens $\Delta(G) + 1$ Farben. Dabei ist $\Delta(G) = \max_v \deg(v)$ der Maximalgrad. Insbesondere gilt $\chi(G) \le \Delta(G) + 1$.

*Beweis:* Zulässig ist die Färbung, weil jeder Knoten eine andere Farbe erhält als alle seine *vorher* gefärbten Nachbarn; jede Kante $\{v_i, v_j\}$ mit $i < j$ wird also beim Färben von $v_j$ berücksichtigt. Beim Färben von $v_i$ sind höchstens $\deg(v_i) \le \Delta$ Nachbarn schon gefärbt, sie belegen höchstens $\Delta$ der $\Delta + 1$ Farben $0, 1, \dots, \Delta$. Also ist eine dieser Farben frei, und $v_i$ erhält eine Farbe $\le \Delta$. $\square$

Die Schranke ist scharf: $K_n$ braucht $n = \Delta + 1$ Farben, ein ungerader Kreis $3 = \Delta + 1$. (Der **Satz von Brooks** (1941) besagt, dass das für zusammenhängende Graphen die einzigen Ausnahmen sind: Sonst gilt $\chi(G) \le \Delta(G)$.)

**Laufzeit.** Für $v_i$ sammelt man die Farben der Nachbarn in einer Menge ($O(\deg v_i)$) und sucht die kleinste freie Farbe (höchstens $\deg(v_i) + 1$ Versuche). Insgesamt ergibt das nach dem Handschlaglemma $O(|V| + |E|)$.

### 2.3 Die Reihenfolge macht den Unterschied

Schon auf dem Weg $0 - 1 - 2 - 3$ (mit $\chi = 2$) liefert die Reihenfolge $0, 3, 1, 2$ drei Farben: $0$ und $3$ erhalten Farbe 0, dann $1$ Farbe 1, und $2$ hat Nachbarn mit den Farben 1 und 0.

Noch drastischer ist der **Kronengraph**: Knoten $a_0, \dots, a_{n-1}$ und $b_0, \dots, b_{n-1}$, und $a_i$ ist mit $b_j$ genau dann benachbart, wenn $i \ne j$ (also $K_{n,n}$ ohne die Kanten $\{a_i, b_i\}$). Er ist bipartit, also $\chi = 2$. In der Reihenfolge $a_0, b_0, a_1, b_1, \dots$ verbraucht Greedy aber **$n$ Farben** (Aufgabe 8) – die Lücke zwischen Greedy und dem Optimum kann also beliebig groß werden.

Andererseits gilt: **Für jeden Graphen gibt es eine Reihenfolge, in der Greedy optimal färbt** (Aufgabe 9). Das Problem verschiebt sich nur – eine solche Reihenfolge zu finden, ist genauso schwer wie das Färben selbst.

**Welsh-Powell-Reihenfolge (1967).** Eine bewährte Heuristik: Färbe die Knoten in der Reihenfolge **absteigender Grade** $\deg(v_1) \ge \deg(v_2) \ge \dots \ge \deg(v_n)$. Knoten mit vielen Nachbarn – die „schwierigen“ – kommen zuerst an die Reihe, solange noch wenige Farben vergeben sind. Für diese Reihenfolge gilt die Schranke
$$\chi(G) \le \max_{1 \le i \le n} \min\{\deg(v_i) + 1,\; i\}.$$
*Beweisidee:* Beim Färben von $v_i$ sind höchstens $\min\{\deg(v_i), i - 1\}$ Nachbarn schon gefärbt.

### 2.4 Bipartite Graphen und der Satz von König

Ein Graph heißt **bipartit**, wenn man $V$ so in zwei Mengen $A$ und $B$ zerlegen kann, dass jede Kante einen Endknoten in $A$ und einen in $B$ hat. Das ist genau dasselbe wie: $G$ besitzt eine 2-Färbung.

> **Satz (König 1936).** Ein Graph ist genau dann bipartit, wenn er keinen Kreis ungerader Länge enthält.

*Beweis „$\Rightarrow$“:* Ein Kreis in einem bipartiten Graphen wechselt bei jeder Kante zwischen $A$ und $B$. Um zum Startknoten zurückzukehren, braucht er eine gerade Anzahl von Wechseln.

*Beweis „$\Leftarrow$“:* Es genügt, jede Zusammenhangskomponente einzeln zu färben. Wählen Sie in einer Komponente einen Knoten $r$ und setzen Sie
$$c(v) = d(r, v) \bmod 2,$$
wobei $d(r, v)$ der Abstand ist (Einheit 2). Angenommen, eine Kante $\{u, v\}$ hätte $c(u) = c(v)$, also $d(r, u) + d(r, v)$ gerade. Dann ergeben ein kürzester Weg $r \to u$, die Kante $\{u, v\}$ und ein kürzester Weg $v \to r$ einen **geschlossenen Kantenzug ungerader Länge** $d(r,u) + 1 + d(r,v)$. Jeder geschlossene Kantenzug ungerader Länge enthält einen Kreis ungerader Länge (*Beweisidee:* Wiederholt sich ein Knoten, zerlegt man den Kantenzug dort in zwei kürzere geschlossene Kantenzüge; einer davon hat ungerade Länge. Induktion über die Länge.) Das widerspricht der Voraussetzung. $\square$

**Algorithmus (2-Färbung mit BFS).** Der Beweis ist zugleich ein Algorithmus: Breitensuche in jeder Komponente, jeder neu entdeckte Knoten erhält die Gegenfarbe seines Entdeckers. Trifft man dabei auf eine Kante zwischen zwei Knoten **derselben** Farbe, ist der Graph nicht bipartit. Laufzeit $O(|V| + |E|)$. Aus dieser Konfliktkante und den BFS-Vorgängern lässt sich sogar ein ungerader Kreis als „Beweis“ ablesen (optionale Aufgabe `find_odd_cycle`).

### 2.5 Wie schwer ist Färben?

| Frage | Schwierigkeit |
|---|---|
| Reicht 1 Farbe? | trivial: genau dann, wenn es keine Kanten gibt |
| Reichen 2 Farben? | effizient lösbar: BFS, $O(\lvert V\rvert + \lvert E\rvert)$ |
| Reichen $k$ Farben, $k \ge 3$ fest? | **NP-vollständig** (Karp 1972; für $k = 3$ sogar auf planaren Graphen, Garey/Johnson/Stockmeyer 1976) |
| $\chi(G)$ bestimmen | NP-schwer; Greedy liefert nur eine obere Schranke |

**Vierfarbensatz** (nur zur Einordnung): Jeder **planare** Graph (ohne Kantenkreuzungen in die Ebene zeichenbar) besitzt eine 4-Färbung. Bewiesen 1976 von Appel und Haken mit massivem Computereinsatz; ein vereinfachter, ebenfalls computergestützter Beweis stammt von Robertson, Sanders, Seymour und Thomas (1997). Dass 5 Farben reichen (Fünffarbensatz, Heawood 1890), lässt sich dagegen von Hand beweisen.

## 3. Relevante Definitionen und Datenstrukturen

| Begriff | Definition | In Python |
|---|---|---|
| Färbung | $c : V \to \{0, 1, 2, \dots\}$ | Wörterbuch `{Knoten: Farbe}`, Farben sind `0, 1, 2, ...` |
| zulässig | $c(u) \ne c(v)$ für jede Kante $\{u, v\}$ | `is_valid_coloring(graph, coloring)` |
| Anzahl Farben | $\lvert c(V) \rvert$ | `number_of_colors(coloring)` |
| chromatische Zahl | kleinstes $k$ mit einer $k$-Färbung | – (NP-schwer) |
| Maximalgrad | $\Delta(G) = \max_v \deg(v)$ | `max(graph.degree(v) for v in graph)` |
| bipartit | 2-färbbar | `is_bipartite(graph)` |
| ungerader Kreis | Kreis mit ungerader Kantenzahl | `[v0, v1, ..., v0]`, z. B. `[1, 2, 3, 1]` |

**Kleine Python-Bausteine für diese Einheit:**

```python
used = {1, 0, 3}               # eine Menge der belegten Farben
color = 0
while color in used:           # kleinste freie Farbe suchen
    color += 1                 # -> color == 2

coloring = {"A": 0, "B": 1, "C": 0}
set(coloring.values())         # {0, 1}: jede Farbe nur einmal
"D" in coloring                # False: D hat (noch) keine Farbe

degree = {"a": 1, "b": 3, "c": 2, "d": 2}
sorted(["a", "b", "c", "d"], key=lambda v: degree[v], reverse=True)
# ['b', 'c', 'd', 'a'] - c und d (gleicher Grad) behalten ihre Reihenfolge

from collections import deque  # Warteschlange für die BFS (wie in Einheit 2)
queue = deque(["A"])
queue.append("B")
queue.popleft()                # 'A'
```

Die Sortierung in Python ist **stabil**: Elemente mit gleichem Schlüssel behalten ihre ursprüngliche Reihenfolge – auch mit `reverse=True`. Statt `lambda v: degree[v]` können Sie auch direkt `key=graph.degree` schreiben.

## 4. Problemstellung

Pippi Langstrumpf gibt ein Fest in der Villa Kunterbunt. Eingeladen sind Tommy, Annika, Herr Nilsson, das Pferd Kleiner Onkel, Fräulein Prusseliese, die Polizisten Kling und Klang und die Einbrecher Donner-Karlsson und Blom. Einige Gäste vertragen sich nicht und dürfen nicht am selben Tisch sitzen:

| Gast | verträgt sich nicht mit |
|---|---|
| Kling | Donner-Karlsson, Blom |
| Klang | Donner-Karlsson, Blom |
| Donner-Karlsson | Blom |
| Prusseliese | Pippi, Herr Nilsson |

Die Gäste sind Knoten, Streitpaare sind Kanten (die Daten stehen als `PARTY_GUESTS` und `PARTY_CONFLICTS` in `task.py`). Ein Sitzplan ist eine Färbung (Farbe = Tischnummer). Gesucht ist ein Sitzplan mit möglichst wenigen Tischen.

Allgemein: Gegeben ist ein ungerichteter Graph. Gesucht sind

1. ein Test, ob eine gegebene Färbung zulässig ist,
2. eine zulässige Färbung mit möglichst wenigen Farben (Greedy, in einer gegebenen Reihenfolge),
3. die Entscheidung, ob zwei Farben genügen (bipartit),
4. (optional) eine gute Reihenfolge (Welsh-Powell) und ein ungerader Kreis als Beleg, falls zwei Farben nicht genügen.

## 5. Arbeitsaufträge

**Teil A – Programmieren**

1. **`number_of_colors(coloring)`** – Zählen Sie die verschiedenen Farben einer Färbung.
2. **`is_valid_coloring(graph, coloring)`** – Prüfen Sie die drei Bedingungen aus dem Docstring. Schreiben Sie die Prüfung **selbst**; `lib.testing.assert_valid_coloring` benutzen nur die Tests.
3. **`greedy_coloring(graph, order=None)`** – Implementieren Sie den Greedy-Algorithmus.
   - Schritt 1: Gerichteter Graph? Dann `ValueError`.
   - Schritt 2: Ist `order` gleich `None`, nehmen Sie `graph.vertices()`. Sonst prüfen Sie, dass `order` jeden Knoten genau einmal enthält (sonst `ValueError`).
   - Schritt 3: Gehen Sie die Knoten in der Reihenfolge `order` durch. Sammeln Sie für jeden Knoten `v` die Farben der **schon gefärbten** Nachbarn in einer Menge und geben Sie `v` die kleinste Zahl, die nicht in der Menge liegt.
4. Führen Sie `python task.py` aus. Wie viele Tische braucht Pippi nach Ihrem Greedy-Sitzplan? Begründen Sie mathematisch, dass es mit weniger Tischen **nicht** geht. Vergleichen Sie die beiden Reihenfolgen für den Weg $0 - 1 - 2 - 3$.
5. **`is_bipartite(graph)`** – Entscheiden Sie mit Ihrer **eigenen Breitensuche** (keine Importe aus Einheit 2), ob der Graph bipartit ist.
   - Schritt 1: Gerichteter Graph? Dann `ValueError`.
   - Schritt 2: `side = {}`. Für jeden Knoten `s`, der noch keine Seite hat: `side[s] = 0` und eine BFS ab `s` starten (der Graph kann mehrere Komponenten haben!).
   - Schritt 3: In der BFS: Für jeden Nachbarn `w` des entnommenen Knotens `u` – hat `w` noch keine Seite, erhält er `1 - side[u]` und kommt in die Warteschlange; hat `w` dieselbe Seite wie `u`, geben Sie `False` zurück.
   - Schritt 4: Wurde kein Konflikt gefunden, geben Sie `True` zurück.

**Teil B – Auf Papier**

6. **Greedy-Schranke.** Beweisen Sie mit eigenen Worten, dass Greedy höchstens $\Delta + 1$ Farben benutzt. Zeigen Sie sogar: Der Knoten $v_i$ erhält eine Farbe $\le$ Anzahl seiner Nachbarn unter $v_1, \dots, v_{i-1}$.
7. **Chromatische Zahlen.** Bestimmen Sie $\chi(K_n)$, $\chi(C_n)$ (gerades und ungerades $n$), $\chi(K_{m,n})$ und $\chi$ eines Baumes. Zeigen Sie jeweils eine passende Färbung **und** dass es mit weniger Farben nicht geht.
8. **Kronengraph.** Zeigen Sie: In der Reihenfolge $a_0, b_0, a_1, b_1, \dots, a_{n-1}, b_{n-1}$ erhalten $a_i$ und $b_i$ beide die Farbe $i$. *Hinweis:* Induktion über $i$; welche Farben haben die Nachbarn von $a_i$ unter den bereits gefärbten Knoten? Welche Reihenfolge liefert 2 Farben?
9. **Es gibt immer eine optimale Reihenfolge.** Sei $c$ eine Färbung mit $\chi(G)$ Farben. Ordnen Sie die Knoten nach ihrer Farbe in $c$ (erst alle mit Farbe 0, dann alle mit Farbe 1, ...). Zeigen Sie, dass Greedy in dieser Reihenfolge jedem Knoten $v$ eine Farbe $\le c(v)$ gibt.
10. **Satz von König.** Arbeiten Sie den Beweis aus Abschnitt 2.4 aus. Beweisen Sie insbesondere das Lemma: Jeder geschlossene Kantenzug ungerader Länge enthält einen Kreis ungerader Länge.
11. **Petersen-Graph.** Zeigen Sie $\chi = 3$: Finden Sie einen ungeraden Kreis und eine 3-Färbung. (Am Rechner: `greedy_coloring(petersen_graph(), welsh_powell_order(petersen_graph()))`.)

**Teil C – Optionale Programmieraufgaben**

12. **`welsh_powell_order(graph)`** – Sortieren Sie die Knoten nach absteigendem Grad; bei gleichem Grad bleibt die Reihenfolge aus `graph.vertices()` erhalten.
13. **`find_odd_cycle(graph)`** – Geben Sie einen ungeraden Kreis zurück, falls der Graph nicht bipartit ist, sonst `None`.
    - Schritt 1: Erweitern Sie Ihre BFS aus `is_bipartite`: Merken Sie sich für jeden Knoten seine Tiefe `depth[v]` und seinen Vorgänger `parent[v]`.
    - Schritt 2: Finden Sie eine Kante `u – w` mit gleicher Tiefe (gleiche Parität bedeutet bei BFS gleiche Tiefe – warum?).
    - Schritt 3: Gehen Sie von `u` und von `w` **gleichzeitig** über `parent` nach oben, bis Sie beim selben Knoten ankommen.
    - Schritt 4: Setzen Sie den Kreis `u → … → Treffpunkt → … → w → u` zusammen. Warum ist seine Länge ungerade?

## 6. Anforderungen an die Implementierung

- Alle Funktionen mit Graph-Argument erwarten einen **ungerichteten** Graphen und lösen bei einem gerichteten Graphen einen `ValueError` aus.
- Farben sind die ganzen Zahlen `0, 1, 2, ...`. `greedy_coloring` gibt ein Wörterbuch zurück, das **jeden** Knoten enthält.
- `greedy_coloring` ist **deterministisch**: Für eine feste Reihenfolge ist das Ergebnis eindeutig bestimmt (die Tests vergleichen daher genaue Wörterbücher). `order=None` bedeutet die Reihenfolge von `graph.vertices()`. Ist `order` keine Permutation der Knotenmenge (Knoten fehlt, doppelt oder nicht im Graphen), wird ein `ValueError` ausgelöst.
- `greedy_coloring` muss in $O(|V| + |E|)$ laufen (bei gegebener Reihenfolge) und nie mehr als $\Delta + 1$ Farben benutzen.
- `is_valid_coloring` gibt `False` zurück, wenn ein Knoten keine Farbe hat, ein Schlüssel kein Knoten ist oder eine Kante zwei gleichfarbige Endknoten hat. Sie schreiben die Prüfung selbst und dürfen **nicht** `lib.testing` aufrufen.
- `is_bipartite` verwendet eine eigene BFS, prüft **alle** Zusammenhangskomponenten und läuft in $O(|V| + |E|)$. Graphen ohne Kanten und der leere Graph sind bipartit.
- `find_odd_cycle` liefert einen Kreis `[v0, ..., v0]` mit ungerader Kantenzahl, in dem sich außer dem ersten Knoten keiner wiederholt, oder `None`.
- Die Eingabe darf nicht verändert werden.

## 7. Beispiele für erwartetes Verhalten

```python
>>> from lib.graph import Graph
>>> from lib.generators import cycle_graph, complete_bipartite_graph
>>> path = Graph.from_edges([(0, 1), (1, 2), (2, 3)])
>>> greedy_coloring(path)
{0: 0, 1: 1, 2: 0, 3: 1}
>>> greedy_coloring(path, [0, 3, 1, 2])
{0: 0, 3: 0, 1: 1, 2: 2}
>>> greedy_coloring(cycle_graph(5))
{0: 0, 1: 1, 2: 0, 3: 1, 4: 2}
>>> greedy_coloring(path, [0, 1, 2])
Traceback (most recent call last):
    ...
ValueError: order must contain every vertex exactly once

>>> is_valid_coloring(path, {0: 0, 1: 1, 2: 0, 3: 1})
True
>>> is_valid_coloring(path, {0: 0, 1: 0, 2: 1, 3: 0})     # Kante 0 - 1
False
>>> number_of_colors({0: 0, 1: 1, 2: 0, 3: 2})
3
>>> is_bipartite(cycle_graph(6)), is_bipartite(cycle_graph(7))
(True, False)
>>> is_bipartite(complete_bipartite_graph(3, 4))
True

>>> welsh_powell_order(path)
[1, 2, 0, 3]
>>> find_odd_cycle(cycle_graph(5))      # eine mögliche Lösung
[2, 1, 0, 4, 3, 2]
>>> find_odd_cycle(cycle_graph(6)) is None
True
```

Bei Pippis Fest liefert Greedy in der Reihenfolge von `PARTY_GUESTS` drei Tische: Tisch 0 für Pippi, Tommy, Annika, Herrn Nilsson, Kleinen Onkel, Kling und Klang, Tisch 1 für Prusseliese und Donner-Karlsson, Tisch 2 für Blom.

```bash
python -m pytest exercises/06_graph_coloring
```

## 8. Hinweise und optionale Zusatzaufgaben

**Hinweise**

- Ein Knoten ist „schon gefärbt“, wenn er als Schlüssel im Wörterbuch `coloring` steht: `w in coloring`.
- Prüfen einer Permutation: Die Länge muss stimmen **und** die Mengen müssen gleich sein. (Warum reicht `set(order) == set(graph.vertices())` allein nicht?)
- `is_bipartite`: Ein Graph kann aus mehreren Komponenten bestehen – nur eine davon muss einen ungeraden Kreis enthalten, damit das Ergebnis `False` ist.
- Mit `lib.visualization.to_dot(graph, vertex_colors=coloring)` können Sie eine Färbung farbig zeichnen lassen.

**Optionale Zusatzaufgaben**

1. **Reihenfolgen vergleichen.** Färben Sie Zufallsgraphen `lib.generators.random_graph(50, 0.2, seed=s)` mit der Standardreihenfolge, mit der Welsh-Powell-Reihenfolge und mit 100 zufälligen Reihenfolgen (`random.shuffle`). Welche ist im Mittel am besten?
2. **Exakte chromatische Zahl.** Schreiben Sie für sehr kleine Graphen (bis etwa 8 Knoten) eine Funktion, die $\chi(G)$ durch Ausprobieren aller Färbungen mit $k = 1, 2, 3, \dots$ Farben bestimmt. Wie viele Färbungen sind das für $n$ Knoten und $k$ Farben? Vergleichen Sie mit Greedy.
3. **Welsh-Powell-Schranke.** Berechnen Sie $\max_i \min\{\deg(v_i) + 1, i\}$ für den Petersen-Graphen und für einen Stern $K_{1,n}$. Wie gut ist die Schranke?
4. **Stundenplan.** Fünf Kurse, Studierende in mehreren Kursen: Zwei Kurse, die eine gemeinsame Teilnehmerin haben, dürfen nicht gleichzeitig stattfinden. Formulieren Sie das als Färbungsproblem und lösen Sie ein selbst ausgedachtes Beispiel.
5. **Brooks.** Finden Sie einen zusammenhängenden Graphen, der weder vollständig noch ein ungerader Kreis ist, für den Greedy in einer ungünstigen Reihenfolge trotzdem $\Delta + 1$ Farben braucht. Warum widerspricht das nicht dem Satz von Brooks?

## 9. Quellen und weiterführende Literatur

- R. Diestel: *Graphentheorie*. Springer, 5. Auflage 2017, Abschnitt 1.6 (Bipartite Graphen) und Kapitel 5 (Färbungen).
- S. O. Krumke, H. Noltemeier: *Graphentheoretische Konzepte und Algorithmen*. Springer Vieweg, 3. Auflage 2012.
- J. Kleinberg, É. Tardos: *Algorithm Design*. Pearson 2005, Abschnitt 3.4 (Testing Bipartiteness) und Kapitel 8 (u. a. Graph Coloring).
- D. Kőnig: *Theorie der endlichen und unendlichen Graphen*. Akademische Verlagsgesellschaft, Leipzig 1936.
- D. J. A. Welsh, M. B. Powell: *An upper bound for the chromatic number of a graph and its application to timetabling problems*. The Computer Journal 10(1), 1967, S. 85–86.
- R. L. Brooks: *On colouring the nodes of a network*. Proceedings of the Cambridge Philosophical Society 37 (1941), S. 194–197.
- R. M. Karp: *Reducibility among combinatorial problems*. In: R. E. Miller, J. W. Thatcher (Hrsg.): Complexity of Computer Computations. Plenum Press 1972, S. 85–103.
- M. R. Garey, D. S. Johnson, L. Stockmeyer: *Some simplified NP-complete graph problems*. Theoretical Computer Science 1 (1976), S. 237–267.
- K. Appel, W. Haken: *Every planar map is four colorable*. Illinois Journal of Mathematics 21 (1977).
- N. Robertson, D. Sanders, P. Seymour, R. Thomas: *The four-colour theorem*. Journal of Combinatorial Theory, Series B 70 (1997).
