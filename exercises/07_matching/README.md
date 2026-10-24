# Einheit 7: Bipartites Matching

## 1. Titel und Lernziele

In der Villa Kunterbunt gibt es viel zu tun, und nicht jedes Kind kann (oder will) jede Aufgabe übernehmen. Wie verteilt man möglichst viele Aufgaben so, dass jedes Kind höchstens eine bekommt? Das ist ein **Matching-Problem**. Nach dieser Einheit können Sie

- erklären, was ein Matching ist, und **inklusionsmaximale** von **größten** (kardinalitätsmaximalen) Matchings unterscheiden,
- alternierende und **augmentierende Wege** erkennen und mit ihnen ein Matching vergrößern,
- den **Satz von Berge** formulieren und seine Beweisidee wiedergeben,
- den Augmentierungsweg-Algorithmus für bipartite Graphen implementieren und seine Laufzeit $O(|V| \cdot |E|)$ begründen,
- den **Heiratssatz von Hall** (und optional den **Satz von König**) anwenden.

## 2. Mathematischer Hintergrund

Ein ungerichteter Graph $G = (V, E)$ heißt **bipartit**, wenn sich $V$ in zwei disjunkte Mengen $L$ („links“) und $R$ („rechts“) zerlegen lässt, sodass jede Kante einen Endknoten in $L$ und einen in $R$ hat. In dieser Einheit ist die Zerlegung immer **gegeben**: Sie erhalten die Liste der linken Knoten, alle anderen Knoten sind rechts.

Ein **Matching** (deutsch auch *Paarung*) ist eine Kantenmenge $M \subseteq E$, in der keine zwei Kanten einen gemeinsamen Endknoten haben. Ein Knoten heißt **gematcht** (überdeckt), wenn er Endknoten einer Kante aus $M$ ist, sonst **frei**.

- $M$ heißt **inklusionsmaximal** (nicht erweiterbar), wenn man keine weitere Kante hinzufügen kann.
- $M$ heißt **größtes Matching** (engl. *maximum matching*), wenn es kein Matching mit mehr Kanten gibt.
- $M$ heißt **perfekt**, wenn jeder Knoten gematcht ist.

Jedes größte Matching ist inklusionsmaximal, aber **nicht umgekehrt**: Im Weg $a - b - c - d$ ist $\{\{b, c\}\}$ inklusionsmaximal (jede andere Kante berührt $b$ oder $c$), aber $\{\{a, b\}, \{c, d\}\}$ ist größer. Ein „gieriges“ Verfahren, das einfach Kanten nimmt, solange es geht, findet deshalb im Allgemeinen kein größtes Matching.

**Alternierende und augmentierende Wege.** Ein Weg heißt **$M$-alternierend**, wenn sich Kanten außerhalb von $M$ und Kanten in $M$ abwechseln. Ein alternierender Weg, dessen **beide Endknoten frei** sind, heißt **$M$-augmentierend** (vergrößernd). Er beginnt und endet mit einer Kante außerhalb von $M$ und hat daher eine Kante mehr außerhalb von $M$ als in $M$.

Tauscht man entlang eines augmentierenden Weges $P$ die Rollen der Kanten (Kanten aus $M$ fliegen raus, die anderen kommen hinein), erhält man die **symmetrische Differenz**
$$M \,\triangle\, P = (M \setminus P) \cup (P \setminus M),$$
und das ist wieder ein Matching – mit genau **einer Kante mehr**.

> **Satz von Berge (1957).** Ein Matching $M$ ist genau dann ein größtes Matching, wenn es keinen $M$-augmentierenden Weg gibt.

*Beweisidee:* „$\Rightarrow$“: Gibt es einen augmentierenden Weg $P$, so ist $M \triangle P$ größer als $M$. „$\Leftarrow$“: Angenommen, $M'$ ist ein größeres Matching. Im Graphen mit der Kantenmenge $M \triangle M'$ hat jeder Knoten höchstens Grad 2 (höchstens eine Kante aus $M$, höchstens eine aus $M'$). Seine Zusammenhangskomponenten sind also Wege und Kreise, auf denen sich $M$- und $M'$-Kanten abwechseln; Kreise haben daher gleich viele Kanten aus $M$ und $M'$. Weil $|M'| > |M|$, muss es eine Komponente mit mehr $M'$- als $M$-Kanten geben – das ist ein Weg, der mit $M'$-Kanten beginnt und endet, also ein $M$-augmentierender Weg.

**Der Algorithmus.** Aus dem Satz von Berge ergibt sich sofort ein Verfahren:

1. Beginne mit dem leeren Matching $M = \emptyset$.
2. Suche einen $M$-augmentierenden Weg $P$. Gibt es keinen, ist $M$ ein größtes Matching (Berge) – fertig.
3. Ersetze $M$ durch $M \triangle P$ und gehe zu Schritt 2.

In **bipartiten** Graphen ist die Suche in Schritt 2 einfach: Ein augmentierender Weg startet an einem freien linken Knoten, geht über eine Nicht-Matching-Kante nach rechts, über eine Matching-Kante zurück nach links, wieder nach rechts usw., bis er einen freien rechten Knoten erreicht. Das ist eine Breiten- (oder Tiefen-)suche, in der die Richtung durch das Matching vorgegeben ist. Dieses Verfahren geht auf H. W. Kuhn (1955) zurück, der es als Teil seiner „Ungarischen Methode“ für das gewichtete Zuordnungsproblem beschrieb (benannt nach den ungarischen Mathematikern König und Egerváry).

**Laufzeit.** Eine Suche besucht jeden Knoten und jede Kante höchstens einmal: $O(|V| + |E|)$. Jede Augmentierung vergrößert das Matching um 1, und ein Matching hat höchstens $|V|/2$ Kanten. Also gibt es höchstens $|V|/2 + 1$ Suchen, insgesamt $O(|V| \cdot (|V| + |E|))$, üblicherweise geschrieben als $O(|V| \cdot |E|)$.

*Ausblick:* Der Algorithmus von **Hopcroft und Karp** (1973) sucht in jeder Runde gleich viele **kürzeste**, knotendisjunkte augmentierende Wege auf einmal und kommt mit $O(\sqrt{|V|} \cdot |E|)$ aus.

*Voraussetzung:* Der Algorithmus funktioniert nur für **bipartite** Graphen. In allgemeinen Graphen können ungerade Kreise („Blüten“) die einfache Suche täuschen; dafür gibt es den Blüten-Algorithmus von Edmonds (1965).

> **Heiratssatz von Hall (1935).** Ein bipartiter Graph mit Seiten $L$ und $R$ hat genau dann ein Matching, das **alle** Knoten aus $L$ überdeckt, wenn für jede Teilmenge $S \subseteq L$ gilt:
> $$|N(S)| \ge |S|.$$
> Dabei ist $N(S)$ die Menge aller Nachbarn von Knoten aus $S$.

*Beweisidee:* Die Bedingung ist offensichtlich notwendig: Die Knoten aus $S$ brauchen $|S|$ verschiedene Partner in $N(S)$. Für die Umkehrung sei $M$ ein größtes Matching und $u \in L$ frei. Sei $Z$ die Menge aller Knoten, die von $u$ aus über $M$-alternierende Wege erreichbar sind, und $S = Z \cap L$. Jeder rechte Knoten in $Z$ ist gematcht (sonst gäbe es einen augmentierenden Weg, Widerspruch zu Berge), und zwar mit einem Knoten aus $S$. Außerdem liegen alle Nachbarn von $S$ in $Z$. Also ist $N(S) = Z \cap R$, und jeder Knoten aus $N(S)$ hat einen eigenen Partner in $S \setminus \{u\}$. Damit gilt $|N(S)| = |S| - 1 < |S|$ – die Bedingung ist verletzt.

> **Satz von König (1931).** In einem bipartiten Graphen ist die Größe eines größten Matchings gleich der Größe einer kleinsten **Knotenüberdeckung** (einer Knotenmenge, die von jeder Kante mindestens einen Endknoten enthält).

*Beweisidee:* „$\le$“ gilt in jedem Graphen: Jede Matching-Kante braucht einen eigenen Überdeckungsknoten. Für „$\ge$“ sei $M$ ein größtes Matching und $Z$ die Menge der Knoten, die von **irgendeinem** freien linken Knoten aus alternierend erreichbar sind. Dann ist $C = (L \setminus Z) \cup (R \cap Z)$ eine Knotenüberdeckung mit genau einem Knoten pro Matching-Kante, also $|C| = |M|$.

## 3. Relevante Definitionen und Datenstrukturen

| Begriff | Bedeutung | In Python |
|---|---|---|
| linke Knoten $L$ | gegebene Seite der Bipartition | Parameter `left_vertices` (z. B. eine Liste); alle anderen Knoten bilden $R$ |
| Matching $M$ | Kanten ohne gemeinsame Endknoten | Wörterbuch `matching` **links → rechts**, z. B. `{"Pippi": "Pferd"}` |
| frei / gematcht | Knoten ohne / mit Matching-Kante | links: `l not in matching`; rechts: `r not in matched_right` |
| augmentierender Weg | $l_0, r_0, l_1, r_1, \dots, l_k, r_k$ | Liste `[l0, r0, l1, r1, ..., lk, rk]` (gerade Länge) |
| $M \triangle P$ | Kanten von $P$ tauschen | neues Wörterbuch, siehe `augment` |

Der augmentierende Weg `[l0, r0, l1, r1, ..., lk, rk]` erfüllt:

- `l0` ist ein **freier** linker Knoten, `rk` ein **freier** rechter Knoten,
- die Kanten $(l_i, r_i)$ sind Kanten des Graphen, aber **nicht** im Matching,
- die Kanten $(r_i, l_{i+1})$ sind **im** Matching, d. h. `matching[l_{i+1}] == r_i`,
- kein Knoten kommt doppelt vor.

Weil das Matching nur „links → rechts“ speichert, brauchen Sie oft auch die Gegenrichtung. Ein umgedrehtes Wörterbuch bauen Sie so:

```python
matching = {"Pippi": "Pferd", "Tommy": "Pfannkuchen"}
matched_right = {r: l for l, r in matching.items()}
# {'Pferd': 'Pippi', 'Pfannkuchen': 'Tommy'}

matching.get("Annika")      # None - Annika ist frei
"Garten" in matched_right   # False - der Garten ist frei
new = dict(matching)        # eine Kopie; Änderungen an new ändern matching nicht
```

## 4. Problemstellung

In der Villa Kunterbunt sollen die folgenden Aufgaben verteilt werden. Jede Person übernimmt höchstens eine Aufgabe, und jede Aufgabe wird von höchstens einer Person erledigt. Eine Kante bedeutet „kann diese Aufgabe übernehmen“:

| Person | kann übernehmen |
|---|---|
| Pippi | Pferd, Pfannkuchen |
| Tommy | Pfannkuchen, Garten |
| Annika | Garten, Einkauf |
| Kling | Pferd |

Verteilt man gierig der Reihe nach (Pippi → Pferd, Tommy → Pfannkuchen, Annika → Garten), bleibt für den Polizisten Kling nichts übrig – obwohl alle vier eine Aufgabe bekommen könnten. Der augmentierende Weg

$$\text{Kling} - \text{Pferd} - \text{Pippi} - \text{Pfannkuchen} - \text{Tommy} - \text{Garten} - \text{Annika} - \text{Einkauf}$$

repariert das: Kling übernimmt das Pferd, Pippi wechselt zu den Pfannkuchen, Tommy in den Garten und Annika zum Einkauf.

Gesucht ist allgemein: Gegeben ein ungerichteter bipartiter Graph `graph` und die Liste `left_vertices` der linken Knoten. Bestimmen Sie ein **größtes Matching**.

## 5. Arbeitsaufträge

Bearbeiten Sie die Funktionen in `task.py` in dieser Reihenfolge.

1. **Von Hand:** Finden Sie im Weg $a - b - c - d - e - f$ ein inklusionsmaximales Matching mit 2 Kanten und ein größtes Matching. Welcher augmentierende Weg führt vom einen zum anderen?
2. **`augment(matching, path)`** – Vergrößern Sie ein Matching entlang eines augmentierenden Weges. Geben Sie ein **neues** Wörterbuch zurück; `matching` bleibt unverändert.
   - Schritt 1: Prüfen Sie, dass `path` nicht leer ist und eine gerade Anzahl von Knoten hat (sonst `ValueError`).
   - Schritt 2: Kopieren Sie `matching`.
   - Schritt 3: Setzen Sie für jedes Paar `path[i], path[i + 1]` mit geradem `i` den Eintrag `new[path[i]] = path[i + 1]`.
   - Überlegen Sie: Warum verschwinden die alten Matching-Kanten $(r_i, l_{i+1})$ dabei automatisch?
3. **`find_augmenting_path(graph, left_vertices, matching)`** – Suchen Sie einen augmentierenden Weg mit einer Breitensuche. Schreiben Sie die Suche selbst in dieser Datei (kein Import aus Einheit 2).
   - Schritt 1: Bauen Sie `matched_right` (rechts → links).
   - Schritt 2: Legen Sie **alle freien linken Knoten** in eine Warteschlange. Ein Wörterbuch `parent` merkt sich für jeden entdeckten **rechten** Knoten `r`, von welchem linken Knoten aus er erreicht wurde.
   - Schritt 3: Nehmen Sie einen linken Knoten `l` aus der Warteschlange. Betrachten Sie jeden Nachbarn `r` von `l`, der noch nicht in `parent` steht und nicht `matching.get(l)` ist. Setzen Sie `parent[r] = l`.
     - Ist `r` frei: Sie haben einen augmentierenden Weg gefunden – weiter mit Schritt 4.
     - Sonst: Legen Sie den Partner `matched_right[r]` in die Warteschlange (dorthin geht es über die Matching-Kante).
   - Schritt 4: Bauen Sie den Weg **rückwärts** auf: `r`, dann `l = parent[r]`, dann dessen Partner `matching.get(l)` (das vorige `r`), usw. Ist `matching.get(l)` gleich `None`, ist `l` der freie Startknoten. Drehen Sie die Liste am Ende um.
   - Schritt 5: Ist die Warteschlange leer, ohne dass ein freier rechter Knoten gefunden wurde, geben Sie `None` zurück.
4. **`maximum_bipartite_matching(graph, left_vertices)`** – Prüfen Sie die Eingabe (siehe Abschnitt 6). Beginnen Sie mit `{}` und rufen Sie abwechselnd `find_augmenting_path` und `augment` auf, bis kein augmentierender Weg mehr existiert.
5. Führen Sie `python task.py` aus. Bekommt in der Villa Kunterbunt jede Person eine Aufgabe?

## 6. Anforderungen an die Implementierung

- **Voraussetzung:** Der Graph ist **ungerichtet** und **bipartit** mit der linken Seite `left_vertices`; rechts sind alle übrigen Knoten. `maximum_bipartite_matching` prüft das:
  - gerichteter Graph → `ValueError`,
  - ein linker Knoten ist nicht im Graphen → `KeyError`,
  - eine Kante hat beide Endknoten auf derselben Seite → `ValueError`.
- `find_augmenting_path` darf eine gültige Eingabe voraussetzen (keine Prüfungen nötig) und verändert `matching` **nicht**. Gibt es mehrere augmentierende Wege, ist jeder richtig.
- `augment` gibt ein **neues** Wörterbuch zurück und löst bei leerem Weg oder ungerader Knotenzahl einen `ValueError` aus.
- `maximum_bipartite_matching` gibt ein Wörterbuch **links → rechts** zurück, das nur die gematchten linken Knoten enthält. Gibt es mehrere größte Matchings, ist jedes richtig.
- Verwenden Sie keine fertige Matching-Bibliothek. Die Laufzeit soll $O(|V| \cdot (|V| + |E|))$ sein: Jede Suche besucht jeden Knoten höchstens einmal.
- Leere Graphen, Graphen ohne Kanten und eine leere linke Seite müssen funktionieren (Ergebnis `{}`).
- Der Graph wird nicht verändert.

## 7. Beispiele für erwartetes Verhalten

Zuerst ein kleines Beispiel, das Pfannkuchen-Problem:

```python
>>> from lib.graph import Graph
>>> g = Graph.from_edges([("Pippi", "Pfannkuchen"), ("Pippi", "Pferd"), ("Tommy", "Pfannkuchen")])
>>> left = ["Pippi", "Tommy"]
>>> find_augmenting_path(g, left, {"Pippi": "Pfannkuchen"})
['Tommy', 'Pfannkuchen', 'Pippi', 'Pferd']
>>> augment({"Pippi": "Pfannkuchen"}, ['Tommy', 'Pfannkuchen', 'Pippi', 'Pferd'])
{'Pippi': 'Pferd', 'Tommy': 'Pfannkuchen'}
>>> find_augmenting_path(g, left, {"Pippi": "Pferd", "Tommy": "Pfannkuchen"}) is None
True
```

Dann die Villa Kunterbunt aus Abschnitt 4:

```python
>>> villa = Graph.from_edges([
...     ("Pippi", "Pferd"), ("Pippi", "Pfannkuchen"),
...     ("Tommy", "Pfannkuchen"), ("Tommy", "Garten"),
...     ("Annika", "Garten"), ("Annika", "Einkauf"),
...     ("Kling", "Pferd"),
... ])
>>> people = ["Pippi", "Tommy", "Annika", "Kling"]
>>> greedy = {"Pippi": "Pferd", "Tommy": "Pfannkuchen", "Annika": "Garten"}
>>> find_augmenting_path(villa, people, greedy)
['Kling', 'Pferd', 'Pippi', 'Pfannkuchen', 'Tommy', 'Garten', 'Annika', 'Einkauf']
>>> maximum_bipartite_matching(villa, people)
{'Pippi': 'Pfannkuchen', 'Tommy': 'Garten', 'Annika': 'Einkauf', 'Kling': 'Pferd'}
>>> maximum_bipartite_matching(Graph(), [])
{}
```

(Die Reihenfolge der Einträge im Wörterbuch spielt keine Rolle.) Prüfen können Sie ein Ergebnis mit `lib.testing.assert_valid_matching(graph, matching, left=people)`.

```bash
python -m pytest exercises/07_matching
```

## 8. Hinweise und optionale Zusatzaufgaben

**Hinweise**

- Ein linker Knoten ist genau dann frei, wenn er **kein** Schlüssel von `matching` ist; ein rechter Knoten genau dann, wenn er **kein** Schlüssel von `matched_right` ist.
- Jeder rechte Knoten wird höchstens einmal in `parent` eingetragen, und jeder gematchte rechte Knoten hat genau einen Partner. Deshalb landet auch jeder linke Knoten höchstens einmal in der Warteschlange – ohne extra `visited`-Menge.
- Für die Eingabeprüfung: Wandeln Sie `left_vertices` zuerst in eine Liste und eine Menge um (`left_vertices` könnte z. B. ein Generator sein, den man nur einmal durchlaufen kann). Eine Kante `(u, v)` ist genau dann in Ordnung, wenn **genau einer** der beiden Knoten links liegt: `(u in left) != (v in left)`.
- Zeichnen Sie sich das Villa-Kunterbunt-Beispiel auf und markieren Sie Matching-Kanten farbig. Augmentierende Wege sieht man dann sofort.

**Optionale Zusatzaufgaben**

1. **`minimum_vertex_cover(graph, left_vertices)`** – Berechnen Sie mit der Konstruktion aus dem Beweis des Satzes von König eine kleinste Knotenüberdeckung: größtes Matching $M$ bestimmen, $Z$ = alle von freien linken Knoten aus alternierend erreichbaren Knoten, Ergebnis $(L \setminus Z) \cup (R \cap Z)$. Prüfen Sie, dass die Größe gleich $|M|$ ist.
2. **`hall_violator(graph, left_vertices)`** – Gibt es kein Matching, das alle linken Knoten überdeckt, geben Sie eine Menge $S \subseteq L$ mit $|N(S)| < |S|$ zurück (ein „Zeuge“ dafür, dass die Hall-Bedingung verletzt ist), sonst `None`. Tipp: Nehmen Sie $S = Z \cap L$ wie im Beweis von Hall.
3. Zeigen Sie: Ein $k$-regulärer bipartiter Graph ($k \ge 1$) hat ein perfektes Matching. (Tipp: Hall-Bedingung, Kanten zählen.)
4. Messen Sie mit `lib.utils.measure_time` Ihre Laufzeit auf `lib.generators.random_bipartite_graph(n, n, 4 / n)` für $n = 100, 200, 400, 800$.
5. Wie kann man ein bipartites Matching als **Flussproblem** lösen? (Das ist Thema der nächsten Einheit.)

## 9. Quellen und weiterführende Literatur

- R. Diestel: *Graphentheorie*. Springer, 5. Auflage 2017, Kapitel 2 (Paarungen; Sätze von König und Hall).
- J. Kleinberg, É. Tardos: *Algorithm Design*. Pearson 2005, Abschnitt 7.5 (bipartites Matching über Flüsse).
- T. H. Cormen, C. E. Leiserson, R. L. Rivest, C. Stein: *Algorithmen – Eine Einführung*. De Gruyter, 4. Auflage 2022, Kapitel über Matchings in bipartiten Graphen.
- S. O. Krumke, H. Noltemeier: *Graphentheoretische Konzepte und Algorithmen*. Springer Vieweg, 3. Auflage 2012, Kapitel über Matchings.
- C. Berge: *Two theorems in graph theory*. Proceedings of the National Academy of Sciences of the USA 43 (1957), S. 842–844.
- P. Hall: *On representatives of subsets*. Journal of the London Mathematical Society 10 (1935), S. 26–30.
- D. Kőnig: *Gráfok és mátrixok*. Matematikai és Fizikai Lapok 38 (1931), S. 116–119.
- H. W. Kuhn: *The Hungarian method for the assignment problem*. Naval Research Logistics Quarterly 2 (1955), S. 83–97.
- J. E. Hopcroft, R. M. Karp: *An $n^{5/2}$ algorithm for maximum matchings in bipartite graphs*. SIAM Journal on Computing 2(4) (1973), S. 225–231.
- J. Edmonds: *Paths, trees, and flowers*. Canadian Journal of Mathematics 17 (1965), S. 449–467.
