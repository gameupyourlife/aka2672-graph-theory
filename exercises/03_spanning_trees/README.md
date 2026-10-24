# Einheit 3: Spannbäume und der Algorithmus von Kruskal

## 1. Titel und Lernziele

In Lönneberga sollen die Höfe durch Telefonleitungen verbunden werden. Jede Leitung kostet Geld, und es soll so billig wie möglich gebaut werden – aber jeder Hof muss (eventuell über Umwege) jeden anderen erreichen. Das ist das Problem des **minimalen Spannbaums**. Nach dieser Einheit können Sie

- Bäume, Wälder, Spannbäume und Spannwälder definieren und die wichtigsten Charakterisierungen von Bäumen angeben,
- die **Schnitteigenschaft** und die **Kreiseigenschaft** formulieren und erklären, warum ein gieriges Verfahren hier optimal ist,
- die Datenstruktur **Union-Find** (disjunkte Mengen) selbst implementieren und erklären,
- den Algorithmus von **Kruskal** implementieren und seine Laufzeit $O(|E| \log |E|)$ begründen,
- erklären, was auf nicht zusammenhängenden Graphen passiert (Spannwald).

## 2. Mathematischer Hintergrund

**Bäume.** Ein **Wald** ist ein ungerichteter Graph ohne Kreise. Ein **Baum** ist ein zusammenhängender Wald.

> **Satz (Charakterisierung von Bäumen).** Für einen Graphen $T$ mit $n \geq 1$ Knoten sind äquivalent:
> 1. $T$ ist ein Baum (zusammenhängend und kreisfrei).
> 2. $T$ ist zusammenhängend und hat genau $n - 1$ Kanten.
> 3. $T$ ist kreisfrei und hat genau $n - 1$ Kanten.
> 4. Zwischen je zwei Knoten von $T$ gibt es genau einen Weg.
> 5. $T$ ist minimal zusammenhängend: Entfernt man irgendeine Kante, zerfällt $T$.
> 6. $T$ ist maximal kreisfrei: Fügt man irgendeine neue Kante hinzu, entsteht ein Kreis.

**Folgerung:** Ein Wald mit $n$ Knoten und $c$ Zusammenhangskomponenten hat genau $n - c$ Kanten (jede Komponente ist ein Baum).

**Spannbäume.** Sei $G = (V, E)$ ein ungerichteter Graph. Ein **Spannbaum** von $G$ ist ein Baum $T = (V, F)$ mit $F \subseteq E$, der *alle* Knoten von $G$ enthält. Einen Spannbaum gibt es genau dann, wenn $G$ zusammenhängend ist. Ist $G$ nicht zusammenhängend, betrachtet man einen **Spannwald**: einen Spannbaum in jeder Zusammenhangskomponente. Er hat $|V| - c$ Kanten, wenn $G$ aus $c$ Komponenten besteht.

**Minimale Spannbäume.** Jede Kante $e$ hat ein Gewicht $w(e) \in \mathbb{R}$. Das Gewicht eines Spannbaums ist $w(T) = \sum_{e \in F} w(e)$. Ein **minimaler Spannbaum** (engl. *minimum spanning tree*, MST) ist ein Spannbaum mit kleinstmöglichem Gewicht. Da ein Graph nur endlich viele Spannbäume hat, existiert für zusammenhängende Graphen immer ein minimaler Spannbaum. Negative Gewichte sind übrigens erlaubt – im Gegensatz zu kürzesten Wegen (Einheit 4) stört das hier nicht.

**Schnitte.** Für eine Knotenmenge $S$ mit $\emptyset \neq S \neq V$ heißt die Menge der Kanten mit genau einem Endknoten in $S$ ein **Schnitt** $\delta(S)$.

> **Satz (Schnitteigenschaft).** Sei $G$ zusammenhängend, $S$ wie oben und $e$ eine Kante in $\delta(S)$ mit kleinstem Gewicht unter allen Kanten in $\delta(S)$. Dann gibt es einen minimalen Spannbaum, der $e$ enthält. Allgemeiner: Ist $A$ eine Kantenmenge, die in einem minimalen Spannbaum enthalten ist, und verläuft keine Kante von $A$ über den Schnitt, dann ist auch $A \cup \{e\}$ in einem minimalen Spannbaum enthalten.

*Beweisidee (Austauschargument):* Sei $T$ ein minimaler Spannbaum mit $A \subseteq T$, aber $e = \{u, v\} \notin T$. In $T$ gibt es genau einen Weg von $u$ nach $v$. Weil $u$ und $v$ auf verschiedenen Seiten des Schnitts liegen, benutzt dieser Weg eine Kante $f \in \delta(S)$, und $f \notin A$. Tauscht man $f$ gegen $e$, erhält man wieder einen Spannbaum $T' = T - f + e$ (er ist zusammenhängend und hat $n - 1$ Kanten). Da $w(e) \leq w(f)$, ist $w(T') \leq w(T)$, also ist auch $T'$ minimal – und $T'$ enthält $A \cup \{e\}$.

> **Satz (Kreiseigenschaft).** Ist $f$ eine Kante auf einem Kreis $C$ und ist $w(f)$ *echt* größer als das Gewicht jeder anderen Kante von $C$, dann liegt $f$ in keinem minimalen Spannbaum.

*Beweisidee:* Läge $f$ in einem minimalen Spannbaum $T$, so zerfällt $T - f$ in zwei Teile. Der Kreis $C$ muss diese beiden Teile über eine weitere Kante $e \neq f$ verbinden. Dann ist $T - f + e$ ein Spannbaum mit kleinerem Gewicht – Widerspruch.

Eine nützliche Umkehrung: Ein Spannbaum $T$ ist genau dann minimal, wenn für jede Kante $\{u, v\} \notin T$ gilt: ihr Gewicht ist mindestens so groß wie das größte Gewicht auf dem Weg von $u$ nach $v$ in $T$. (Die Tests benutzen genau dieses Kriterium.)

**Der Algorithmus von Kruskal (1956).**

1. Sortiere alle Kanten aufsteigend nach Gewicht.
2. Beginne mit dem leeren Wald $F = \emptyset$ (jeder Knoten ist ein eigener Baum).
3. Gehe die Kanten der Reihe nach durch: Verbindet die Kante $\{u, v\}$ zwei **verschiedene** Bäume des aktuellen Waldes, nimm sie in $F$ auf. Liegen $u$ und $v$ schon im selben Baum, würde die Kante einen Kreis schließen – überspringe sie.

**Warum ist dieses gierige Vorgehen korrekt?** Wenn Kruskal die Kante $e = \{u, v\}$ aufnimmt, sei $S$ der Baum des aktuellen Waldes, der $u$ enthält. Alle leichteren Kanten wurden schon betrachtet: Sie liegen entweder im Wald oder wurden verworfen, weil beide Endknoten im selben Baum lagen. Keine davon verläuft also über den Schnitt $\delta(S)$. Damit ist $e$ eine leichteste Kante in $\delta(S)$, und nach der Schnitteigenschaft bleibt der Wald in einem minimalen Spannbaum enthalten. Per Induktion über die Anzahl der aufgenommenen Kanten folgt: Am Ende ist $F$ ein minimaler Spannbaum (bzw. Spannwald).

**Eindeutigkeit.** Sind alle Kantengewichte paarweise verschieden, ist der minimale Spannbaum eindeutig.

*Beweisidee:* Angenommen, $T \neq T'$ sind beide minimal. Sei $e$ die leichteste Kante, die in genau einem der beiden Bäume liegt, etwa $e \in T \setminus T'$. Dann enthält $T' + e$ einen Kreis, und auf diesem Kreis liegt eine Kante $f \in T' \setminus T$. Da $e$ die leichteste Kante der symmetrischen Differenz ist und alle Gewichte verschieden sind, gilt $w(f) > w(e)$. Also ist $T' + e - f$ ein Spannbaum mit kleinerem Gewicht als $T'$ – Widerspruch. Gibt es gleiche Gewichte, kann es mehrere minimale Spannbäume geben (z. B. jeder Spannbaum eines vollständigen Graphen mit lauter Gewichten 1); das **minimale Gewicht** ist aber immer eindeutig.

**Laufzeit.** Das Sortieren kostet $O(|E| \log |E|)$. Danach gibt es für jede Kante eine Prüfung „gleicher Baum?“ und eventuell eine Vereinigung zweier Bäume. Mit einer guten Union-Find-Struktur (siehe Abschnitt 3) kosten diese $|E|$ Operationen zusammen fast nur linear viel Zeit. Deshalb **dominiert das Sortieren** die Laufzeit: insgesamt $O(|E| \log |E|)$. Wegen $|E| \leq |V|^2$ ist $\log |E| \leq 2 \log |V|$, man liest daher oft auch $O(|E| \log |V|)$.

**Voraussetzungen:** ungerichteter Graph, beliebige reelle Gewichte. (Für gerichtete Graphen heißt das entsprechende Problem „minimale Arboreszenz“ und braucht andere Algorithmen.)

## 3. Relevante Definitionen und Datenstrukturen

| Begriff | Bedeutung |
|---|---|
| **Wald / Baum** | kreisfreier Graph / zusammenhängender kreisfreier Graph |
| **Spannbaum / Spannwald** | kreisfreier Teilgraph mit allen Knoten, der genau die Knoten verbindet, die auch in $G$ verbunden sind; $\lvert V \rvert - c$ Kanten |
| **Schnitt** $\delta(S)$ | alle Kanten mit genau einem Endknoten in $S$ |
| **`Edge(u, v, weight)`** | benanntes Tupel aus `lib.graph`; `graph.edges()` liefert jede ungerichtete Kante genau einmal |
| **Union-Find** | Datenstruktur für eine Zerlegung einer Menge in disjunkte Teilmengen |

**Sortieren nach Gewicht.** `sorted` nimmt mit `key` eine Funktion, die angibt, *wonach* sortiert wird:

```python
edges = graph.edges()                              # [Edge(u=..., v=..., weight=...), ...]
by_weight = sorted(edges, key=lambda e: e.weight)  # leichteste Kante zuerst
```

### Union-Find (disjunkte Mengen)

Kruskal muss immer wieder fragen: *Liegen $u$ und $v$ schon im selben Baum?* Eine Suche (BFS/DFS) bei jeder Kante wäre viel zu langsam. Union-Find verwaltet eine Zerlegung der Knoten in disjunkte Mengen und kann genau zwei Dinge schnell:

- `find(x)`: Gib einen **Repräsentanten** der Menge von `x` zurück. Zwei Elemente liegen genau dann in derselben Menge, wenn `find` für beide dasselbe Ergebnis liefert.
- `union(x, y)`: Vereinige die Mengen von `x` und `y`.

**Idee:** Jede Menge wird als Baum gespeichert (das sind *nicht* die Bäume des Graphen, sondern interne Hilfsbäume). Jedes Element zeigt auf ein „Elternelement“; die Wurzel zeigt auf sich selbst und ist der Repräsentant. Wir speichern das in einem Wörterbuch `parent`.

```text
Mengen {A, B, C} und {D, E}:

    parent = {"A": "A", "B": "A", "C": "B", "D": "D", "E": "D"}

        A           D        find("C"): C -> B -> A, also Repräsentant A
        |           |        find("E"): E -> D,      also Repräsentant D
        B           E
        |
        C
```

**Einfache Version** (so sollten Sie anfangen):

```python
parent = {x: x for x in ["A", "B", "C", "D"]}   # jeder ist seine eigene Menge

def find(x):
    while parent[x] != x:      # nach oben laufen, bis zur Wurzel
        x = parent[x]
    return x

def union(x, y):
    root_x, root_y = find(x), find(y)
    if root_x == root_y:
        return False           # schon dieselbe Menge
    parent[root_x] = root_y    # eine Wurzel unter die andere hängen
    return True
```

Achtung: Man hängt immer die **Wurzel** um, nicht `x` selbst – sonst verliert man die übrigen Elemente der Menge.

Diese Version ist korrekt, kann aber lange Ketten bilden (`find` kostet dann $O(n)$). Zwei kleine Verbesserungen machen sie extrem schnell:

1. **Vereinigung nach Größe** (*union by size*): Merken Sie sich in einem zweiten Wörterbuch `size[root]` die Größe jeder Menge und hängen Sie immer die **kleinere** Menge unter die Wurzel der größeren. Dann ist jeder interne Baum höchstens $\log_2 n$ hoch (die Menge eines Elements verdoppelt sich mindestens, wann immer seine Tiefe wächst).
2. **Pfadkompression** (*path compression*): Nachdem `find(x)` die Wurzel gefunden hat, lassen Sie alle Elemente auf dem durchlaufenen Weg **direkt** auf die Wurzel zeigen. Spätere Aufrufe sind dann sehr kurz.

Mit beiden Verbesserungen kosten $m$ Operationen auf $n$ Elementen $O(m \cdot \alpha(n))$, wobei $\alpha$ die inverse Ackermann-Funktion ist – für alle praktisch vorkommenden $n$ gilt $\alpha(n) \leq 4$ (Tarjan 1975).

## 4. Problemstellung

Gegeben ist der gewichtete ungerichtete Graph `lib.generators.small_weighted_graph()` (Wege rund um Lönneberga, Gewichte = Kosten in Hundertkronen):

```text
Katthult --4-- Lönneberga --3-- Backhorva
   |  \            |              |
   2    7          5              6
   |      \        |              |
Gibberyd --3-- Kirche ----2---- Markt
```

Michels Vater Anton will möglichst wenig Geld ausgeben und trotzdem alle sechs Orte verbinden. Gesucht ist ein minimaler Spannbaum – und allgemein für jeden ungerichteten gewichteten Graphen ein minimaler Spannwald.

## 5. Arbeitsaufträge

1. **Von Hand:** Führen Sie Kruskal auf dem Lönneberga-Graphen auf Papier aus. Notieren Sie für jede Kante, ob sie aufgenommen oder verworfen wird und warum. Welches Gesamtgewicht erhalten Sie?
2. **`UnionFind`** – Implementieren Sie die Klasse in `task.py`.
   - Schritt 1: `__init__` legt das Wörterbuch `self.parent` an und ruft für jedes Element `self.add(x)` auf.
   - Schritt 2: `add(x)` macht `x` zu einer neuen einelementigen Menge (`parent[x] = x`). Ist `x` schon vorhanden, passiert nichts.
   - Schritt 3: `find(x)` läuft von `x` aus über `parent` nach oben bis zur Wurzel. Unbekannte Elemente lösen einen `KeyError` aus.
   - Schritt 4: `union(x, y)` bestimmt beide Wurzeln. Sind sie gleich, Rückgabe `False`. Sonst wird eine Wurzel unter die andere gehängt, Rückgabe `True`.
   - Schritt 5: `connected(x, y)` vergleicht die beiden Wurzeln.
   - Schritt 6 (empfohlen, sobald die Tests grün sind): Bauen Sie *Vereinigung nach Größe* und *Pfadkompression* ein (siehe Abschnitt 3). Die Tests müssen danach immer noch grün sein.
3. **`kruskal(graph)`** – Implementieren Sie Kruskal mit Ihrer Union-Find-Struktur.
   - Schritt 1: Gerichteter Graph? Dann `ValueError`.
   - Schritt 2: Union-Find mit allen Knoten anlegen, Kanten nach Gewicht sortieren.
   - Schritt 3: Für jede Kante `edge`: Liefert `union(edge.u, edge.v)` den Wert `True`, gehört die Kante zum Ergebnis.
   - Rückgabe: die Liste der gewählten `Edge`-Objekte (so wie sie `graph.edges()` liefert).
4. **`spanning_tree_weight(edges)`** – Summieren Sie die Gewichte einer Kantenliste.
5. Wenden Sie `kruskal` auf den Lönneberga-Graphen an (`python task.py`). Stimmt das Ergebnis mit Auftrag 1 überein?
6. Fügen Sie dem Graphen einen isolierten Knoten „Vimmerby“ hinzu (`graph.add_vertex("Vimmerby")`). Was liefert `kruskal` jetzt? Wie viele Kanten hat das Ergebnis, und warum?

## 6. Anforderungen an die Implementierung

- `UnionFind.find`, `union` und `connected` lösen für unbekannte Elemente einen `KeyError` aus. `add` für ein bereits vorhandenes Element verändert nichts (insbesondere wird es nicht von seiner Menge getrennt).
- `UnionFind.union` gibt `True` zurück, wenn zwei verschiedene Mengen vereinigt wurden, sonst `False`.
- `kruskal` löst bei gerichteten Graphen einen `ValueError` aus. Bei nicht zusammenhängenden Graphen liefert es einen minimalen **Spannwald** mit $|V| - c$ Kanten. Für den leeren Graphen und für Graphen ohne Kanten ist das Ergebnis `[]`.
- `kruskal` muss Kreise mit Union-Find vermeiden (keine Suche pro Kante). Die Laufzeit soll $O(|E| \log |E|)$ sein.
- Die Reihenfolge der Kanten im Ergebnis ist egal. Gibt es mehrere minimale Spannbäume, ist jeder richtig.
- Negative und nicht-ganzzahlige Gewichte müssen funktionieren.
- Der Eingabegraph darf nicht verändert werden.

## 7. Beispiele für erwartetes Verhalten

```python
>>> uf = UnionFind(["Michel", "Ida", "Alfred", "Lina"])
>>> uf.union("Michel", "Ida")
True
>>> uf.union("Ida", "Michel")
False
>>> uf.connected("Michel", "Ida"), uf.connected("Michel", "Alfred")
(True, False)
>>> uf.find("Krösa-Maja")
Traceback (most recent call last):
KeyError: ...
>>> from lib.generators import small_weighted_graph
>>> tree = kruskal(small_weighted_graph())
>>> len(tree)
5
>>> spanning_tree_weight(tree)
14
>>> sorted(e.weight for e in tree)
[2, 2, 3, 3, 4]
```

Die gewählten Kanten sind Katthult–Gibberyd (2), Kirche–Markt (2), Lönneberga–Backhorva (3), Gibberyd–Kirche (3) und Katthult–Lönneberga (4). Lönneberga–Kirche (5) wird verworfen, weil sie den Kreis Lönneberga–Katthult–Gibberyd–Kirche schließen würde.

```bash
python -m pytest exercises/03_spanning_trees
```

## 8. Hinweise und optionale Zusatzaufgaben

**Hinweise**

- Zwei Endknoten eines `Edge` erhalten Sie mit `edge.u` und `edge.v` oder durch Auspacken: `u, v, weight = edge`.
- Ein Wald mit $n$ Knoten hat höchstens $n - 1$ Kanten. Wenn Ihr Ergebnis mehr Kanten hat, prüft Ihr Code Kreise falsch.
- Testen Sie `UnionFind` erst allein (z. B. mit den Beispielen aus Abschnitt 7), bevor Sie `kruskal` schreiben.
- Mit `lib.testing.assert_valid_spanning_forest(graph, edges)` können Sie selbst prüfen, ob eine Kantenliste ein Spannwald ist.
- Mit `lib.visualization.save_dot(graph, "mst.dot", highlight_edges=[(e.u, e.v) for e in tree])` können Sie den Spannbaum rot einzeichnen lassen.

**Optionale Zusatzaufgaben**

1. **`count_components(graph)`** – Zählen Sie die Zusammenhangskomponenten eines ungerichteten Graphen **nur mit Union-Find** (ohne BFS/DFS). Tipp: Jedes erfolgreiche `union` verringert die Anzahl der Mengen um genau 1. Gerichtete Graphen: `ValueError`.
2. **`prim(graph, start)`** – Der Algorithmus von Prim lässt einen *einzigen* Baum ab `start` wachsen: Nimm immer die leichteste Kante, die einen Knoten im Baum mit einem Knoten außerhalb verbindet (Schnitteigenschaft mit $S$ = aktueller Baum!). Verwenden Sie eine Prioritätswarteschlange `heapq`:
   ```python
   import heapq
   heap = []
   heapq.heappush(heap, (4, "Katthult", "Lönneberga"))
   heapq.heappush(heap, (2, "Katthult", "Gibberyd"))
   heapq.heappop(heap)        # (2, 'Katthult', 'Gibberyd') - das kleinste Tupel zuerst
   ```
   Kanten, deren zweiter Endknoten beim Herausnehmen schon im Baum liegt, werden einfach übersprungen. Ergebnis: minimaler Spannbaum der Komponente von `start`. Unbekanntes `start`: `KeyError`; gerichteter Graph: `ValueError`. Laufzeit: $O(|E| \log |V|)$.
3. Messen Sie mit `lib.utils.measure_time` Ihre Union-Find-Struktur mit und ohne Verbesserungen: Vereinigen Sie z. B. `union(i, i + 1)` für $i = 0, \dots, n-2$ und rufen Sie dann `find(0)` für $n = 1000, 2000, 4000$ auf.
4. Zeigen Sie mit einem Beispiel: Wenn zwei Kanten gleiches Gewicht haben, kann es zwei verschiedene minimale Spannbäume geben. Umgekehrt ist der minimale Spannbaum des Lönneberga-Graphen eindeutig, obwohl die Gewichte 2 und 3 je zweimal vorkommen. Begründen Sie das mit der Kreiseigenschaft.
5. **Maximaler Spannbaum:** Wie bekommen Sie mit Ihrer Funktion `kruskal` (ohne sie zu ändern) einen Spannbaum mit *größtem* Gewicht?
6. Beweisen Sie: Ein zusammenhängender Graph mit $n$ Knoten und $n - 1$ Kanten ist ein Baum.

## 9. Quellen und weiterführende Literatur

- R. Diestel: *Graphentheorie*. Springer, 5. Auflage 2017, Abschnitt 1.5 (Bäume und Wälder).
- T. H. Cormen, C. E. Leiserson, R. L. Rivest, C. Stein: *Algorithmen – Eine Einführung*. De Gruyter, 4. Auflage 2022, Kapitel „Datenstrukturen für disjunkte Mengen“ und „Minimale Spannbäume“.
- J. Kleinberg, É. Tardos: *Algorithm Design*. Pearson 2005, Kapitel 4 (Greedy Algorithms), Abschnitte 4.5 (The Minimum Spanning Tree Problem) und 4.6 (Implementing Kruskal's Algorithm: The Union-Find Data Structure).
- S. O. Krumke, H. Noltemeier: *Graphentheoretische Konzepte und Algorithmen*. Springer Vieweg, 3. Auflage 2012 (Kapitel über Bäume und minimale aufspannende Bäume).
- J. B. Kruskal: *On the shortest spanning subtree of a graph and the traveling salesman problem*. Proceedings of the American Mathematical Society 7(1), 1956, S. 48–50.
- R. C. Prim: *Shortest connection networks and some generalizations*. Bell System Technical Journal 36(6), 1957, S. 1389–1401.
- O. Borůvka: *O jistém problému minimálním*. Práce moravské přírodovědecké společnosti 3, 1926, S. 37–58 (die erste Arbeit zum minimalen Spannbaum, motiviert durch die Elektrifizierung Mährens).
- B. A. Galler, M. J. Fischer: *An improved equivalence algorithm*. Communications of the ACM 7(5), 1964, S. 301–303 (Union-Find mit Baumdarstellung).
- R. E. Tarjan: *Efficiency of a good but not linear set union algorithm*. Journal of the ACM 22(2), 1975, S. 215–225.
- Python-Dokumentation zu `sorted` und `heapq`: <https://docs.python.org/3/howto/sorting.html>, <https://docs.python.org/3/library/heapq.html>
