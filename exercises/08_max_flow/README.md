# Einheit 8: Maximale Flüsse

## 1. Titel und Lernziele

Michel aus Lönneberga soll möglichst viele Fuhren Holz pro Tag von Katthult zum Markt bringen. Jede Straße verträgt nur eine bestimmte Anzahl von Fuhren, und an den Kreuzungen geht nichts verloren. Wie viel kommt höchstens an? Das ist ein **Maximalflussproblem**. Nach dieser Einheit können Sie

- Flussnetzwerke, Flüsse und ihren **Wert** definieren und die Bedingungen (Kapazität, Flusserhaltung) prüfen,
- das **Residualnetzwerk** mit **Rückwärtskanten** aufstellen – auch bei gegenläufigen Kanten $u \to v$ und $v \to u$,
- die **Ford-Fulkerson-Methode** erklären und den **Edmonds-Karp-Algorithmus** implementieren,
- den **Max-Flow-Min-Cut-Satz** formulieren, seine Beweisidee wiedergeben und einen minimalen Schnitt ablesen,
- die Laufzeit $O(|V| \cdot |E|^2)$ und die **Ganzzahligkeit** maximaler Flüsse begründen.

## 2. Mathematischer Hintergrund

Ein **Flussnetzwerk** besteht aus einem gerichteten Graphen $G = (V, E)$, einer **Kapazität** $c(u, v) \ge 0$ für jede Kante, einer **Quelle** $s$ und einer **Senke** $t \ne s$. Für Paare $(u, v) \notin E$ setzen wir $c(u, v) = 0$.

Ein **Fluss** ist eine Funktion $f: E \to \mathbb{R}$ mit

1. **Kapazitätsbedingung:** $0 \le f(u, v) \le c(u, v)$ für jede Kante,
2. **Flusserhaltung:** Für jeden Knoten $v \notin \{s, t\}$ gilt $\sum_{u} f(u, v) = \sum_{w} f(v, w)$ (was hineinfließt, fließt auch hinaus).

Der **Wert** des Flusses ist das, was netto aus der Quelle herausfließt:
$$|f| = \sum_{w} f(s, w) - \sum_{u} f(u, s).$$

**Schnitte.** Ein **$s$-$t$-Schnitt** ist eine Zerlegung $V = S \cup T$ mit $s \in S$ und $t \in T$. Seine **Kapazität** ist $c(S, T) = \sum_{u \in S,\, v \in T} c(u, v)$ – es zählen nur Kanten von $S$ nach $T$. Für jeden Fluss und jeden Schnitt gilt
$$|f| = \sum_{u \in S,\, v \in T} f(u, v) - \sum_{u \in T,\, v \in S} f(u, v) \;\le\; c(S, T).$$
(Summiere die Flusserhaltung über alle Knoten von $S$.) Jeder Schnitt ist also eine obere Schranke für jeden Fluss.

**Residualnetzwerk.** Gegeben ein Fluss $f$: Wie viel können wir von $u$ nach $v$ **zusätzlich** schicken? Erstens die freie Kapazität $c(u, v) - f(u, v)$ der Kante $u \to v$. Zweitens können wir Fluss, der schon auf der Gegenkante $v \to u$ fließt, **zurücknehmen** – das wirkt wie ein Transport von $u$ nach $v$. Die **Residualkapazität** ist daher
$$c_f(u, v) = \bigl(c(u, v) - f(u, v)\bigr) + f(v, u),$$
wobei nicht vorhandene Kanten Kapazität 0 und Fluss 0 haben. Das **Residualnetzwerk** $G_f$ enthält eine Kante $u \to v$ für jedes Paar mit $c_f(u, v) > 0$. Kanten, die nur durch den zweiten Summanden entstehen, heißen **Rückwärtskanten**.

Ein **augmentierender Weg** ist ein Weg von $s$ nach $t$ in $G_f$. Sein **Engpass** $\delta$ ist die kleinste Residualkapazität auf dem Weg. Schickt man $\delta$ entlang des Weges, wächst der Wert des Flusses um $\delta$.

**Ford-Fulkerson-Methode (1956).**

1. Beginne mit $f = 0$.
2. Solange es in $G_f$ einen augmentierenden Weg gibt: Bestimme seinen Engpass $\delta$ und schicke $\delta$ entlang des Weges.

**Edmonds-Karp (1972)** ist Ford-Fulkerson, bei dem man immer einen **kürzesten** augmentierenden Weg (mit den wenigsten Kanten) wählt – also mit einer **Breitensuche**.

> **Max-Flow-Min-Cut-Satz (Ford/Fulkerson 1956; Elias/Feinstein/Shannon 1956).** Für einen Fluss $f$ sind äquivalent:
> 1. $f$ ist ein maximaler Fluss.
> 2. Es gibt keinen augmentierenden Weg in $G_f$.
> 3. Es gibt einen $s$-$t$-Schnitt $(S, T)$ mit $|f| = c(S, T)$.
>
> Insbesondere ist der Wert eines maximalen Flusses gleich der Kapazität eines minimalen Schnitts.

*Beweisidee:* (1 ⇒ 2) Gäbe es einen augmentierenden Weg, könnte man den Fluss vergrößern. (2 ⇒ 3) Sei $S$ die Menge der Knoten, die in $G_f$ von $s$ aus erreichbar sind; $t \notin S$. Für jede Kante $u \to v$ von $S$ nach $T$ ist $c_f(u, v) = 0$, also ist sie **gesättigt** ($f(u, v) = c(u, v)$), und jede Kante $v \to u$ von $T$ nach $S$ trägt **keinen** Fluss. Mit der Formel oben folgt $|f| = c(S, T)$. (3 ⇒ 1) Kein Fluss kann größer als $c(S, T)$ sein.

**Ganzzahligkeit.** Sind alle Kapazitäten ganze Zahlen, so sind alle Engpässe ganzzahlig. Ford-Fulkerson erhöht den Wert dann jedes Mal um mindestens 1, endet also, und liefert einen **ganzzahligen** maximalen Fluss. (Das ist z. B. für bipartites Matching als Flussproblem wichtig.) Mit irrationalen Kapazitäten und ungeschickter Wegwahl muss Ford-Fulkerson dagegen nicht einmal terminieren.

**Laufzeit von Edmonds-Karp.** Man zeigt: Die BFS-Abstände von $s$ im Residualnetzwerk werden nie kleiner, und jede Kante kann höchstens $|V|/2$-mal der Engpass eines kürzesten Weges sein. Das ergibt höchstens $O(|V| \cdot |E|)$ Augmentierungen à $O(|E|)$ (Breitensuche und Aktualisierung), insgesamt
$$O(|V| \cdot |E|^2),$$
**unabhängig** von den Kapazitäten.

*Voraussetzungen:* gerichteter Graph, nichtnegative Kapazitäten, $s \ne t$.

## 3. Relevante Definitionen und Datenstrukturen

Wir verwenden im ganzen Kurs **eine** feste Darstellung:

| Begriff | In Python |
|---|---|
| Flussnetzwerk | gerichteter `Graph`; die **Kapazität** von $u \to v$ ist das Kantengewicht `graph.weight(u, v)` |
| Fluss $f$ | Wörterbuch `flow: dict[tuple[Vertex, Vertex], float]` mit Schlüsseln `(u, v)` für die **Originalkanten**; fehlender Schlüssel = Fluss 0 |
| $f(u, v)$ für beliebige Paare | `flow.get((u, v), 0)` – liefert 0 auch für Paare, die keine Kante sind |
| $c(u, v)$ für beliebige Paare | `graph.weight(u, v) if graph.has_edge(u, v) else 0` |
| Residualnetzwerk $G_f$ | neuer gerichteter `Graph` mit allen Knoten; Gewicht = Residualkapazität $c_f(u, v) > 0$ |
| Wert $|f|$ | `lib.testing.flow_value(graph, flow, source)` |
| Schnittkapazität | `lib.testing.cut_capacity(graph, S)` |

**Gegenläufige Kanten.** In einem gerichteten `Graph` dürfen $u \to v$ und $v \to u$ **beide** existieren (mit eigenen Kapazitäten). Deshalb steht in der Formel $c_f(u, v) = (c(u, v) - f(u, v)) + f(v, u)$ die Summe beider Anteile. Beispiel: $c(a, b) = 3$, $c(b, a) = 2$, $f(a, b) = 1$, $f(b, a) = 0$:

$$c_f(a, b) = (3 - 1) + 0 = 2, \qquad c_f(b, a) = (2 - 0) + 1 = 3.$$

**Fluss schicken.** Um $\delta$ entlang des Residualpaars $(u, v)$ zu schicken, **nehmen Sie zuerst Fluss auf der Gegenkante $(v, u)$ zurück**, so weit es geht, und addieren nur den Rest auf $f(u, v)$:

```python
back = min(delta, flow.get((v, u), 0))  # so viel kann auf v -> u zurückgenommen werden
if back > 0:
    flow[(v, u)] -= back
if delta - back > 0:
    flow[(u, v)] = flow.get((u, v), 0) + (delta - back)
```

So bleibt die Darstellung sauber: Es entstehen nie Schlüssel für Paare, die keine Kante sind, und keine Kante bekommt mehr Fluss als ihre Kapazität. (Warum? Ist $(u, v)$ keine Kante, so ist $c_f(u, v) = f(v, u)$, also $\delta \le f(v, u)$ und der Rest ist 0.)

**Wörterbücher mit Tupel-Schlüsseln:**

```python
flow = {("s", "a"): 2, ("a", "t"): 2}
flow[("s", "a")]          # 2
flow.get(("a", "s"), 0)   # 0 - kein Eintrag
for (u, v), value in flow.items():
    print(u, "->", v, value)
```

## 4. Problemstellung

Das folgende Netzwerk (nach Cormen et al.) hat die Quelle `s`, die Senke `t` und die angegebenen Kapazitäten:

| Kante | Kapazität | | Kante | Kapazität |
|---|---|---|---|---|
| s → v1 | 16 | | v3 → v2 | 9 |
| s → v2 | 13 | | v3 → t | 20 |
| v1 → v3 | 12 | | v4 → v3 | 7 |
| v2 → v1 | 4 | | v4 → t | 4 |
| v2 → v4 | 14 | | | |

Der maximale Fluss hat den Wert **23**. Ein minimaler Schnitt ist $S = \{s, v1, v2, v4\}$: Die Kanten $v1 \to v3$ (12), $v4 \to v3$ (7) und $v4 \to t$ (4) ergeben zusammen $23$. (Die Kante $v3 \to v2$ zeigt von $T$ nach $S$ und zählt nicht.)

Gesucht ist allgemein: Gegeben ein gerichteter Graph `graph` mit Kapazitäten als Kantengewichten, eine Quelle `source` und eine Senke `sink`. Bestimmen Sie den Wert eines maximalen Flusses und einen solchen Fluss.

## 5. Arbeitsaufträge

1. **Von Hand:** Im Netzwerk $s \to a$, $s \to b$, $a \to b$, $a \to t$, $b \to t$ (alle Kapazitäten 1) schickt jemand zuerst eine Einheit über $s \to a \to b \to t$. Zeichnen Sie das Residualnetzwerk. Welcher augmentierende Weg benutzt die Rückwärtskante $b \to a$? Welchen Wert hat der maximale Fluss?
2. **`residual_graph(graph, flow)`** – Bauen Sie das Residualnetzwerk.
   - Schritt 1: Erzeugen Sie einen neuen **gerichteten** Graphen und fügen Sie **alle** Knoten von `graph` hinzu.
   - Schritt 2: Sammeln Sie alle geordneten Paare $(u, v)$, für die $u \to v$ **oder** $v \to u$ eine Kante ist (jedes Paar nur einmal).
   - Schritt 3: Berechnen Sie für jedes Paar $c_f(u, v)$ mit der Formel aus Abschnitt 3. Ist der Wert $> 0$, fügen Sie die Kante $u \to v$ mit diesem Gewicht hinzu.
3. **`find_augmenting_path(residual, source, sink)`** – Suchen Sie mit einer **Breitensuche** einen kürzesten Weg (wenigste Kanten) von `source` nach `sink` im Residualnetzwerk. Schreiben Sie die Breitensuche hier selbst (kein Import aus Einheit 2). Rückgabe: `[source, ..., sink]` oder `None`.
4. **`edmonds_karp(graph, source, sink)`** – Implementieren Sie den Algorithmus.
   - Schritt 1: Prüfen Sie die Eingabe (siehe Abschnitt 6).
   - Schritt 2: `flow = {(u, v): 0 for u, v, _ in graph.edges()}`.
   - Schritt 3: Wiederholen Sie: Residualnetzwerk bauen, kürzesten augmentierenden Weg suchen. Gibt es keinen, sind Sie fertig.
   - Schritt 4: Engpass $\delta$ = kleinstes Gewicht auf dem Weg im Residualnetzwerk (`residual.weight(u, v)`).
   - Schritt 5: Schicken Sie $\delta$ entlang jedes Paars $(u, v)$ des Weges (Gegenkante zuerst zurücknehmen, siehe Abschnitt 3).
   - Schritt 6: Geben Sie `(Wert, flow)` zurück. Den Wert können Sie aufsummieren (Summe aller $\delta$) oder am Ende an der Quelle ablesen.
5. Führen Sie `python task.py` aus. Kommt für das Netzwerk aus Abschnitt 4 der Wert 23 heraus?

## 6. Anforderungen an die Implementierung

- **Voraussetzungen:** `edmonds_karp` prüft die Eingabe:
  - ungerichteter Graph → `ValueError`,
  - `source` oder `sink` ist kein Knoten → `KeyError`,
  - `source == sink` → `ValueError`,
  - eine negative Kapazität → `ValueError` (Kapazität 0 ist erlaubt).
- Der zurückgegebene Fluss enthält einen Eintrag für **jede** Kante des Graphen (auch mit Wert 0) und **nur** für Kanten des Graphen. Gibt es mehrere maximale Flüsse, ist jeder richtig.
- Gegenläufige Kanten $u \to v$ und $v \to u$ müssen korrekt behandelt werden (siehe Abschnitt 3).
- `residual_graph` enthält **alle** Knoten von `graph` und nur Kanten mit Residualkapazität $> 0$. Fehlende Schlüssel in `flow` bedeuten Fluss 0.
- `find_augmenting_path` liefert einen Weg mit **möglichst wenigen Kanten**, `None`, falls `sink` nicht erreichbar ist, und `[source]`, falls `source == sink`. Fehlt `source` oder `sink` im Graphen → `KeyError`.
- Ganzzahlige Kapazitäten ergeben einen ganzzahligen Fluss; Kommazahlen (z. B. `2.5`) als Kapazitäten müssen ebenfalls funktionieren.
- Die Eingabe (Graph) wird nicht verändert. Laufzeit: $O(|V| \cdot |E|^2)$ (pro Runde eine Breitensuche und ein neues Residualnetzwerk in $O(|V| + |E|)$).

## 7. Beispiele für erwartetes Verhalten

Zuerst das kleine Netzwerk aus Arbeitsauftrag 1, mit einem Fluss über $s \to a \to b \to t$:

```python
>>> from lib.graph import Graph
>>> g = Graph.from_edges(
...     [("s", "a", 1), ("s", "b", 1), ("a", "b", 1), ("a", "t", 1), ("b", "t", 1)], directed=True
... )
>>> flow = {("s", "a"): 1, ("a", "b"): 1, ("b", "t"): 1}
>>> r = residual_graph(g, flow)
>>> sorted((u, v, w) for u, v, w in r.edges())
[('a', 's', 1), ('a', 't', 1), ('b', 'a', 1), ('s', 'b', 1), ('t', 'b', 1)]
>>> find_augmenting_path(r, "s", "t")
['s', 'b', 'a', 't']
>>> edmonds_karp(g, "s", "t")
(2, {('s', 'a'): 1, ('s', 'b'): 1, ('a', 'b'): 0, ('a', 't'): 1, ('b', 't'): 1})
```

Dann das Netzwerk aus Abschnitt 4:

```python
>>> clrs = Graph.from_edges(
...     [("s", "v1", 16), ("s", "v2", 13), ("v1", "v3", 12), ("v2", "v1", 4), ("v2", "v4", 14),
...      ("v3", "v2", 9), ("v3", "t", 20), ("v4", "v3", 7), ("v4", "t", 4)],
...     directed=True,
... )
>>> value, flow = edmonds_karp(clrs, "s", "t")
>>> value
23
>>> min_cut(clrs, "s", "t")            # optional
{'s', 'v1', 'v2', 'v4'}
```

Prüfen können Sie einen Fluss mit `lib.testing.assert_valid_flow(graph, flow, source, sink)` und seinen Wert mit `lib.testing.flow_value(graph, flow, source)`.

```bash
python -m pytest exercises/08_max_flow
```

## 8. Hinweise und optionale Zusatzaufgaben

**Hinweise**

- Für Schritt 2 von `residual_graph`: Durchlaufen Sie `graph.edges()` und merken Sie sich für jede Kante $(u, v)$ die beiden Paare $(u, v)$ und $(v, u)$ – zum Beispiel in einer Menge `pairs`. Eine Liste plus Menge „schon gesehen“ hält die Reihenfolge stabil.
- Die Breitensuche in `find_augmenting_path` ist dieselbe wie in Einheit 2: Warteschlange (`deque`), `parent`-Wörterbuch, am Ende rückwärts den Vorgängern folgen. Sie dürfen abbrechen, sobald `sink` entdeckt ist.
- Der Engpass ist `min(residual.weight(path[i], path[i + 1]) for i in range(len(path) - 1))`.
- Schreiben Sie sich eine kleine Hilfsfunktion `push(flow, u, v, delta)` für das Schicken entlang eines Paars.
- Wenn ein Test fehlschlägt, lassen Sie sich nach jeder Runde den Weg, $\delta$ und den Fluss ausgeben (`print`).

**Optionale Zusatzaufgaben**

1. **`min_cut(graph, source, sink)`** – Bestimmen Sie die Quellseite $S$ eines minimalen Schnitts: alle Knoten, die im Residualnetzwerk des maximalen Flusses von `source` aus erreichbar sind. Prüfen Sie mit `lib.testing.cut_capacity`, dass die Kapazität gleich dem Flusswert ist.
2. Lösen Sie bipartites Matching (Einheit 7) als Flussproblem: neue Quelle mit Kanten zu allen linken Knoten, alle Kanten von links nach rechts, neue Senke mit Kanten von allen rechten Knoten, alle Kapazitäten 1. Warum ist der Wert des maximalen Flusses gleich der Größe eines größten Matchings? (Stichwort: Ganzzahligkeit.)
3. Konstruieren Sie ein Netzwerk mit vier Knoten, in dem Ford-Fulkerson bei ungeschickter Wahl der Wege sehr viele Augmentierungen braucht (Tipp: zwei Wege mit Kapazität 1000 und eine „Querkante“ mit Kapazität 1). Wie viele braucht Edmonds-Karp?
4. Messen Sie mit `lib.utils.measure_time` die Laufzeit auf `lib.generators.random_weighted_graph(n, 0.3, directed=True)` für wachsendes $n$.

## 9. Quellen und weiterführende Literatur

- T. H. Cormen, C. E. Leiserson, R. L. Rivest, C. Stein: *Algorithmen – Eine Einführung*. De Gruyter, 4. Auflage 2022, Kapitel „Maximaler Fluss“ (dort auch das Beispielnetzwerk mit Wert 23).
- J. Kleinberg, É. Tardos: *Algorithm Design*. Pearson 2005, Kapitel 7 (Network Flow).
- R. Diestel: *Graphentheorie*. Springer, 5. Auflage 2017, Kapitel 6 (Flüsse).
- S. O. Krumke, H. Noltemeier: *Graphentheoretische Konzepte und Algorithmen*. Springer Vieweg, 3. Auflage 2012, Kapitel über Flüsse.
- L. R. Ford, D. R. Fulkerson: *Maximal flow through a network*. Canadian Journal of Mathematics 8 (1956), S. 399–404.
- P. Elias, A. Feinstein, C. E. Shannon: *A note on the maximum flow through a network*. IRE Transactions on Information Theory 2(4) (1956), S. 117–119.
- J. Edmonds, R. M. Karp: *Theoretical improvements in algorithmic efficiency for network flow problems*. Journal of the ACM 19(2) (1972), S. 248–264.
