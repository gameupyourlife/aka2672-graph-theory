# Einheit 5: Euler- und Hamiltonprobleme

## 1. Titel und Lernziele

Zwei Fragen, die fast gleich klingen: Kann man einen Spaziergang machen, der **jede Kante** genau einmal benutzt (Euler)? Kann man eine Rundreise machen, die **jeden Knoten** genau einmal besucht (Hamilton)? Die erste Frage ist mathematisch vollständig gelöst und schnell zu beantworten, die zweite gehört zu den schwersten Problemen der Informatik. Nach dieser Einheit können Sie

- das Königsberger Brückenproblem als Graphproblem formulieren und mit einem einfachen Graphen (ohne Mehrfachkanten) modellieren,
- den Satz von Euler über Eulerkreise und Eulerzüge formulieren, begründen und in Laufzeit $O(|V| + |E|)$ prüfen,
- (optional) einen Eulerkreis mit dem Algorithmus von Hierholzer konstruieren,
- Hamiltonkreise mathematisch untersuchen: notwendige Bedingungen, hinreichende Bedingungen (Dirac, Ore) und Gegenbeispiele (Petersen-Graph),
- genau erklären, **warum sich die Euler-Kriterien nicht auf Hamiltonkreise übertragen lassen**,
- (optional) eine naive Suche nach Hamiltonkreisen schreiben und ihre exponentielle Laufzeit beobachten.

## 2. Mathematischer Hintergrund

### 2.1 Das Königsberger Brückenproblem

Durch Königsberg (heute Kaliningrad) fließt der Pregel. Er trennt vier Landmassen: das Nordufer (N), das Südufer (S), die Insel Kneiphof (I) und ein Gebiet im Osten (O). Im 18. Jahrhundert führten sieben Brücken über den Fluss:

| Brücke | verbindet |
|---|---|
| b1, b2 | Insel – Nord |
| b3, b4 | Insel – Süd |
| b5 | Insel – Ost |
| b6 | Nord – Ost |
| b7 | Süd – Ost |

Gibt es einen Spaziergang, der jede Brücke genau einmal überquert und zum Ausgangspunkt zurückkehrt? Leonhard Euler zeigte 1736, dass das unmöglich ist – und begründete damit die Graphentheorie. Die Landmassen sind Knoten, die Brücken Kanten. Die Grade sind $\deg(I) = 5$ und $\deg(N) = \deg(S) = \deg(O) = 3$: **alle vier** Grade sind ungerade.

### 2.2 Eulerzüge und Eulerkreise

Ein **Kantenzug** ist eine Folge $v_0, v_1, \dots, v_k$ von Knoten, in der aufeinanderfolgende Knoten durch eine Kante verbunden sind. Knoten dürfen sich wiederholen. Er ist **geschlossen**, wenn $v_0 = v_k$ gilt.

- Ein **Eulerzug** (oft auch *Eulerweg*) ist ein Kantenzug, der **jede Kante genau einmal** benutzt. Er darf offen oder geschlossen sein.
- Ein **Eulerkreis** (auch *Eulertour*) ist ein geschlossener Eulerzug. Ein Graph mit Eulerkreis heißt **eulersch**.

> **Satz (Euler 1736, Hierholzer 1873).** Sei $G$ ein ungerichteter Graph, in dem alle Knoten mit positivem Grad in derselben Zusammenhangskomponente liegen. Dann gilt:
>
> 1. $G$ hat einen Eulerkreis $\iff$ jeder Knoten hat geraden Grad.
> 2. $G$ hat einen Eulerzug $\iff$ genau $0$ oder genau $2$ Knoten haben ungeraden Grad. Bei zwei ungeraden Knoten beginnt jeder offene Eulerzug in einem von ihnen und endet im anderen.

Die Zusammenhangsvoraussetzung ist nötig: Zwei getrennte Dreiecke haben nur Knoten vom Grad 2, aber keinen Eulerkreis. Isolierte Knoten (Grad 0) stören dagegen nicht – ein Spaziergang entlang der Kanten muss sie nie besuchen.

*Beweisidee „$\Rightarrow$“:* Jedes Mal, wenn der Kantenzug durch einen Knoten **hindurch** läuft, verbraucht er zwei seiner Kanten: eine hinein, eine hinaus. Beim Eulerkreis gilt das auch für den Startknoten (die erste Kante führt hinaus, die letzte hinein). Da jede Kante genau einmal benutzt wird, ist jeder Grad gerade. Bei einem offenen Eulerzug sind Start- und Endknoten die einzigen Ausnahmen – genau sie haben ungeraden Grad.

*Beweisidee „$\Leftarrow$“ (Hierholzer):* Starten Sie in einem Knoten $v$ und laufen Sie über unbenutzte Kanten, bis es nicht mehr weitergeht. Weil alle Grade gerade sind, kann man nur in $v$ stecken bleiben: Betritt man einen anderen Knoten $w$, hat man dort eine ungerade Anzahl Kanten verbraucht, es bleibt also mindestens eine unbenutzte übrig. Man erhält einen geschlossenen Kantenzug $K$. Bleiben noch Kanten übrig, so gibt es (wegen des Zusammenhangs) einen Knoten $u$ auf $K$ mit einer unbenutzten Kante. Im Restgraphen sind wieder alle Grade gerade; also findet man ab $u$ einen weiteren geschlossenen Kantenzug und fügt ihn bei $u$ in $K$ ein. Das wiederholt man, bis alle Kanten verbraucht sind.

*Eulerzug:* Haben genau $u$ und $v$ ungeraden Grad, fügen Sie einen neuen Knoten $x$ mit den Kanten $\{u, x\}$ und $\{x, v\}$ hinzu. Jetzt sind alle Grade gerade, es gibt einen Eulerkreis; streicht man $x$ wieder, bleibt ein Eulerzug von $u$ nach $v$. (Man nimmt einen *neuen* Knoten statt einer Kante $\{u, v\}$, weil diese Kante schon existieren könnte.)

**Laufzeit.** Die Grade bestimmt man in $O(|V|)$, den Zusammenhang mit einer Suche (BFS/DFS) in $O(|V| + |E|)$. Ob ein Eulerkreis existiert, ist also in **linearer Zeit** entscheidbar. Auch Hierholzers Algorithmus lässt sich mit geeigneten Datenstrukturen in $O(|V| + |E|)$ implementieren.

**Bemerkung zu Königsberg:** Vier ungerade Knoten – es gibt nicht einmal einen offenen Eulerzug.

**Das Haus vom Nikolaus.** „Das ist das Haus vom Ni-ko-laus“ – acht Silben, acht Striche, ohne den Stift abzusetzen:

```
        5
       / \
      3---4
      |\ /|
      | X |
      |/ \|
      1---2
```

Kanten: $\{1,2\}, \{1,3\}, \{1,4\}, \{2,3\}, \{2,4\}, \{3,4\}, \{3,5\}, \{4,5\}$. Die Grade sind $\deg(1) = \deg(2) = 3$, $\deg(3) = \deg(4) = 4$, $\deg(5) = 2$. Es gibt also einen Eulerzug, aber keinen Eulerkreis – und man **muss** in einer unteren Ecke anfangen.

### 2.3 Mehrfachkanten modellieren: Unterteilung

Die Kursbibliothek erlaubt nur einfache Graphen, Königsberg hat aber Mehrfachkanten (zwei Brücken zwischen Insel und Nordufer). Abhilfe schafft eine **Unterteilung**: Man ersetzt eine Kante $\{u, v\}$ durch einen Weg $u - x - v$ mit einem neuen Knoten $x$. Am einfachsten machen wir aus **jeder** Brücke einen eigenen Knoten:

```python
graph = Graph()
graph.add_edge("Insel", "b1")   # Brücke b1 als Knoten ...
graph.add_edge("b1", "Nord")    # ... mit genau zwei Kanten
graph.add_edge("Insel", "b2")
graph.add_edge("b2", "Nord")
# usw. für b3, ..., b7
```

> **Lemma.** Entsteht $G'$ aus $G$ durch Unterteilen einer Kante, so hat $G'$ genau dann einen Eulerkreis (Eulerzug), wenn $G$ einen hat.

*Beweisidee:* Die Grade der alten Knoten ändern sich nicht, der neue Knoten $x$ hat den geraden Grad 2. Der Zusammenhang der Kanten ändert sich nicht. Direkter: Jeder Eulerkreis von $G$ wird zu einem von $G'$, indem man den Schritt $u \to v$ durch $u \to x \to v$ ersetzt. Umgekehrt hat $x$ nur die beiden Kanten zu $u$ und $v$, also läuft jeder Eulerkreis von $G'$ als $u, x, v$ oder $v, x, u$ durch $x$ – streicht man $x$, erhält man einen Eulerkreis von $G$.

### 2.4 Hamiltonkreise

Ein **Hamiltonkreis** ist ein Kreis, der **jeden Knoten genau einmal** enthält. Ein Graph mit Hamiltonkreis heißt **hamiltonsch**. Der Name geht auf William Rowan Hamilton zurück, der 1857 ein Spiel erfand, bei dem man eine solche Rundreise entlang der Kanten eines Dodekaeders finden muss. Ein Hamiltonkreis braucht mindestens 3 Knoten.

Beispiele: $C_n$ und $K_n$ ($n \ge 3$) sind hamiltonsch. Ein Baum ist nie hamiltonsch.

**Notwendige Bedingungen** (gelten für jeden hamiltonschen Graphen):

- (N1) $G$ ist zusammenhängend und jeder Knoten hat Grad mindestens 2.
- (N2) Für jede nichtleere Knotenmenge $S \subsetneq V$ hat $G - S$ höchstens $|S|$ Zusammenhangskomponenten. Insbesondere gibt es keinen **Schnittknoten** (einen Knoten, dessen Entfernen den Graphen zerfallen lässt). *Beweisidee:* Entfernt man $|S|$ Knoten aus einem Kreis, zerfällt er in höchstens $|S|$ Bögen; jede Komponente von $G - S$ enthält mindestens einen dieser Bögen.
- (N3) Ist $G$ bipartit mit den Seiten $A$ und $B$, so gilt $|A| = |B|$. *Beweisidee:* Ein Kreis wechselt bei jeder Kante die Seite.

**Hinreichende Bedingungen** (garantieren einen Hamiltonkreis):

> **Satz (Dirac 1952).** Hat $G$ $n \ge 3$ Knoten und gilt $\deg(v) \ge n/2$ für alle $v$, so ist $G$ hamiltonsch.

> **Satz (Ore 1960).** Hat $G$ $n \ge 3$ Knoten und gilt $\deg(u) + \deg(v) \ge n$ für je zwei **nicht benachbarte** Knoten $u \ne v$, so ist $G$ hamiltonsch.

Ore verallgemeinert Dirac: Sind alle Grade $\ge n/2$, so ist jede Summe zweier Grade $\ge n$.

### 2.5 Warum sich die Euler-Kriterien nicht auf Hamiltonkreise übertragen lassen

Man könnte hoffen, dass es für Hamiltonkreise einen ebenso einfachen Satz gibt. Das ist nicht der Fall, und zwar aus folgenden Gründen:

1. **Lokal gegen global.** Die Euler-Bedingung prüft jeden Knoten **einzeln** („Ist der Grad gerade?“) und dazu den Zusammenhang. Beides kostet zusammen nur $O(|V| + |E|)$. Ob ein Hamiltonkreis existiert, hängt dagegen davon ab, wie der **ganze** Graph zusammengesetzt ist: Ein Kreis, der alle Knoten genau einmal besucht, ist eine globale Struktur, die man an keinem einzelnen Knoten ablesen kann.
2. **Gleiche Gradfolge, verschiedene Antworten.** Der Petersen-Graph und das fünfseitige Prisma (zwei 5-Kreise, deren entsprechende Knoten verbunden sind) sind beide zusammenhängend, 3-regulär, haben 10 Knoten und 15 Kanten – also dieselbe Gradfolge $(3, 3, \dots, 3)$. Das Prisma ist hamiltonsch, der Petersen-Graph nicht (Aufgabe 9). Eine Bedingung, die wie bei Euler nur von den Graden und dem Zusammenhang abhängt, **kann es daher nicht geben**.
3. **Komplexität.** Das Hamiltonkreisproblem ist **NP-vollständig** (Karp 1972). Bis heute kennt niemand einen Algorithmus mit polynomieller Laufzeit; gäbe es einen, so wäre P = NP. Ein Kriterium, das so leicht zu prüfen ist wie das von Euler, würde genau so einen Algorithmus liefern. Bekannte exakte Verfahren brauchen exponentielle Zeit: die naive Suche bis zu $O(n!)$ Schritte, das dynamische Programm von Held und Karp $O(n^2 \, 2^n)$.
4. **Nur „halbe“ Kriterien.** Wir kennen notwendige Bedingungen (N1–N3) und hinreichende Bedingungen (Dirac, Ore) – aber keine, die beides zugleich ist. Dazwischen klafft eine Lücke: Der Kreis $C_n$ ($n \ge 5$) erfüllt weder Dirac noch Ore und ist trotzdem hamiltonsch. Der Petersen-Graph erfüllt N1–N3 und ist trotzdem nicht hamiltonsch.

Zusammengefasst: **Euler ist ein lokales Problem mit einer Charakterisierung über Grade, Hamilton ein globales Problem ohne bekannte effiziente Charakterisierung.**

### 2.6 Naive Suche nach Hamiltonkreisen (Backtracking)

Man legt einen Startknoten fest (jeder Hamiltonkreis enthält ihn ja) und verlängert einen Weg Schritt für Schritt um einen noch unbenutzten Nachbarn. Kommt man nicht weiter, nimmt man den letzten Schritt zurück („Backtracking“) und probiert den nächsten Nachbarn. Hat der Weg alle $n$ Knoten und ist der letzte Knoten zum Start benachbart, ist ein Hamiltonkreis gefunden. Im schlimmsten Fall werden alle $(n-1)!$ Reihenfolgen ausprobiert – für $n = 20$ sind das über $10^{17}$.

## 3. Relevante Definitionen und Datenstrukturen

| Begriff | Definition | In Python |
|---|---|---|
| Kantenzug | $v_0, v_1, \dots, v_k$ mit $\{v_{i-1}, v_i\} \in E$ | Liste von Knoten |
| geschlossener Kantenzug | Kantenzug mit $v_0 = v_k$ | Liste `[v0, ..., v0]` |
| Eulerzug | Kantenzug, der jede Kante genau einmal benutzt | Liste mit $\lvert E\rvert + 1$ Einträgen |
| Eulerkreis | geschlossener Eulerzug | `[v0, ..., v0]` mit $\lvert E\rvert + 1$ Einträgen |
| Hamiltonkreis | Kreis, der jeden Knoten genau einmal enthält | `[v0, v1, ..., v_{n-1}, v0]` mit $n + 1$ Einträgen |
| isolierter Knoten | Knoten mit Grad 0 | `graph.degree(v) == 0` |
| Unterteilung | Kante $\{u, v\}$ durch Weg $u - x - v$ ersetzen | neuer Knoten `x`, zwei `add_edge` |

**Konventionen in dieser Einheit:**

- Alle Funktionen sind für **ungerichtete** Graphen gedacht; bei gerichteten Graphen wird ein `ValueError` ausgelöst.
- **Isolierte Knoten werden ignoriert.**
- Ein Graph **ohne Kanten** (auch der leere Graph ohne Knoten) hat einen trivialen Eulerkreis: `has_euler_circuit` und `has_euler_trail` liefern `True`, `find_euler_circuit` und `find_euler_trail` liefern `[]`.
- Ein Eulerkreis ist insbesondere ein (geschlossener) Eulerzug: Wer einen Eulerkreis hat, hat auch einen Eulerzug.

**Datenstrukturen.** Für die Suche in `edges_connected` genügt ein Stapel (eine Liste) und eine Menge der gesehenen Knoten wie in Einheit 2. Für Hierholzer arbeiten Sie auf einer **Kopie** des Graphen und löschen benutzte Kanten:

```python
remaining = graph.copy()          # die Eingabe bleibt unverändert
remaining.neighbors(3)            # [1, 2, 4, 5]
remaining.remove_edge(3, 1)       # Kante 3 - 1 ist jetzt "verbraucht"
remaining.neighbors(3)            # [2, 4, 5]

stack = [1]                       # ein Stapel: oben ist stack[-1]
stack.append(3)                   # [1, 3]
top = stack[-1]                   # 3 (nur ansehen, nicht entfernen)
stack.pop()                       # 3 (entfernen)
```

Für das Backtracking eignet sich eine **innere Funktion**, die sich selbst aufruft:

```python
def find(graph):
    path = [start]

    def extend() -> bool:
        ...                       # path verlängern, extend() aufrufen,
        ...                       # bei Misserfolg path.pop()
        return False

    if extend():
        ...
```

Die innere Funktion kann `path` lesen und verändern (`append`, `pop`), ohne dass Sie es als Argument übergeben müssen.

## 4. Problemstellung

Gegeben ist ein ungerichteter (einfacher) Graph.

1. Entscheiden Sie, ob er einen **Eulerkreis** bzw. einen **Eulerzug** besitzt – für Königsberg, das Haus vom Nikolaus und die Wege rund um Lönneberga (`lib.generators.small_weighted_graph()`): Michel möchte jeden Weg genau einmal abgehen.
2. (Optional) Konstruieren Sie einen solchen Eulerkreis bzw. Eulerzug.
3. Untersuchen Sie mathematisch, welche Graphen **Hamiltonkreise** haben – und warum sich das nicht so leicht entscheiden lässt.
4. (Optional) Suchen Sie für kleine Graphen naiv nach einem Hamiltonkreis.

## 5. Arbeitsaufträge

**Teil A – Eulerkreise und Eulerzüge (programmieren)**

1. **`edges_connected(graph)`** – Prüfen Sie, ob alle Knoten mit positivem Grad in einer Zusammenhangskomponente liegen. Schreiben Sie dafür **Ihre eigene kleine Suche** (importieren Sie nichts aus Einheit 2).
   - Schritt 1: Gerichteter Graph? Dann `ValueError`.
   - Schritt 2: Sammeln Sie alle Knoten mit `graph.degree(v) > 0`. Gibt es keine, ist das Ergebnis `True`.
   - Schritt 3: Starten Sie bei einem dieser Knoten eine Tiefen- oder Breitensuche und merken Sie sich alle erreichten Knoten in einer Menge.
   - Schritt 4: Das Ergebnis ist `True`, wenn alle Knoten aus Schritt 2 erreicht wurden.
2. **`has_euler_circuit(graph)`** – Wenden Sie den Satz von Euler an: Kanten zusammenhängend und alle Grade gerade.
3. **`has_euler_trail(graph)`** – Kanten zusammenhängend und genau 0 oder 2 Knoten mit ungeradem Grad.
4. Führen Sie `python task.py` aus. Der `__main__`-Block baut Königsberg mit unterteilten Brücken (siehe Abschnitt 2.3) und das Haus vom Nikolaus. Stimmen die Ergebnisse mit Ihrer Rechnung auf Papier überein? Für welche $n$ hat $K_n$ einen Eulerkreis? Begründen Sie mit den Graden.
5. Zeigen Sie auf Papier: Die Unterteilung einer Kante ändert nichts daran, ob ein Eulerkreis existiert (Abschnitt 2.3). Warum darf man die Brücken von Königsberg also als Knoten modellieren?

**Teil B – Hamiltonkreise (auf Papier)**

Bearbeiten Sie diese Aufgaben mathematisch, mit Bleistift und Begründung. Mit `find_hamiltonian_cycle` (Teil C) können Sie Ihre Ergebnisse später am Rechner überprüfen.

6. **Vollständige Graphen.** Zeigen Sie, dass $K_n$ für $n \ge 3$ hamiltonsch ist. Wie viele verschiedene Hamiltonkreise (als Kantenmengen) hat $K_n$? *Hinweis:* Zählen Sie die Reihenfolgen mit festem Startknoten und überlegen Sie, welche Reihenfolgen denselben Kreis beschreiben.
7. **Vollständig bipartite Graphen.** Zeigen Sie: $K_{m,n}$ ist genau dann hamiltonsch, wenn $m = n \ge 2$. *Hinweis:* Bedingung (N3).
8. **Gitter.** Zeigen Sie, dass das $3 \times 3$-Gitter (`grid_graph(3, 3)`) keinen Hamiltonkreis hat. *Hinweis:* Färben Sie die Knoten wie ein Schachbrett. Finden Sie dagegen einen Hamiltonkreis im $2 \times 3$- und im $4 \times 4$-Gitter.
9. **Petersen-Graph.** Zeigen Sie, dass der Petersen-Graph (`petersen_graph()`: äußerer 5-Kreis $0,\dots,4$, inneres Pentagramm $5,\dots,9$, „Speichen“ $\{i, i+5\}$) keinen Hamiltonkreis hat.
   - Schritt 1: Ein Hamiltonkreis $H$ wechselt nur über Speichen zwischen außen und innen. Warum benutzt $H$ eine **gerade** Anzahl von Speichen, und zwar 2 oder 4?
   - Schritt 2 (zwei Speichen): Dann läuft $H$ außen über einen Weg durch alle 5 äußeren Knoten. Dessen Endpunkte sind im äußeren Kreis benachbart, etwa $i$ und $i + 1$. Innen braucht $H$ einen Weg durch alle 5 inneren Knoten von $i + 5$ nach $i + 6$. Warum sind diese beiden Knoten im Pentagramm **nicht** benachbart, die Endpunkte eines solchen Weges aber schon?
   - Schritt 3 (vier Speichen): Genau eine Speiche fehlt in $H$; wegen der Drehsymmetrie des Graphen dürfen Sie annehmen, dass es die Speiche $\{0, 5\}$ ist. Bestimmen Sie Schritt für Schritt, welche Kanten $H$ dann benutzen muss (jeder Knoten hat in $H$ genau Grad 2), und zeigen Sie, dass diese Kanten bereits einen Kreis durch nur 5 Knoten schließen – ein Widerspruch.
10. **Gleiche Gradfolge.** Zeigen Sie, dass das fünfseitige Prisma (Abschnitt 2.5) einen Hamiltonkreis hat. Erklären Sie mit diesem Beispiel und Aufgabe 9 in eigenen Worten, warum es kein „Grad-Kriterium“ für Hamiltonkreise geben kann.
11. **Dirac und Ore.**
    - (a) Zeigen Sie, dass der Satz von Ore den Satz von Dirac impliziert.
    - (b) Zeigen Sie, dass $C_n$ für $n \ge 5$ die Voraussetzungen von Dirac und Ore verletzt, aber hamiltonsch ist. Was folgt daraus über diese Sätze?
    - (c) Zeigen Sie, dass $K_{k,k+1}$ Minimalgrad $k = (n-1)/2$ hat und nicht hamiltonsch ist. Die Schranke $n/2$ im Satz von Dirac lässt sich also nicht verbessern.
12. **Schnittknoten.** Zwei Dreiecke mit einem gemeinsamen Knoten bilden einen eulerschen Graphen. Hat dieser Graph einen Hamiltonkreis? Begründen Sie mit (N2).

**Teil C – Optionale Programmieraufgaben**

13. **`find_euler_circuit(graph)`** – Implementieren Sie den Algorithmus von Hierholzer mit einem Stapel:
    - Schritt 1: Behandeln Sie gerichtete Graphen (`ValueError`), Graphen ohne Kanten (`[]`) und Graphen ohne Eulerkreis (`None`).
    - Schritt 2: `remaining = graph.copy()`; wählen Sie einen Startknoten mit positivem Grad.
    - Schritt 3: `stack = [start]`, `walk = []`. Solange der Stapel nicht leer ist: Sehen Sie sich den obersten Knoten `v` an. Hat `v` in `remaining` noch einen Nachbarn `w`, löschen Sie die Kante `v – w` und legen `w` auf den Stapel. Sonst nehmen Sie `v` vom Stapel und hängen ihn an `walk` an.
    - Schritt 4: `walk` enthält den Eulerkreis rückwärts – drehen Sie die Liste um.
    - Überlegen Sie: Wo im Algorithmus steckt das „Einfügen eines weiteren geschlossenen Kantenzugs“ aus dem Beweis?
14. **`find_euler_trail(graph)`** – Derselbe Algorithmus. Gibt es zwei ungerade Knoten, starten Sie in einem von ihnen.
15. **`find_hamiltonian_cycle(graph)`** – Implementieren Sie die naive Suche aus Abschnitt 2.6. Überprüfen Sie damit Ihre Ergebnisse aus Teil B.

## 6. Anforderungen an die Implementierung

- Alle Funktionen erwarten einen **ungerichteten** Graphen und lösen bei einem gerichteten Graphen einen `ValueError` aus.
- `edges_connected` enthält eine eigene Suche; Importe aus anderen Übungsordnern sind nicht erlaubt.
- Konventionen: Isolierte Knoten werden ignoriert; ein Graph ohne Kanten hat einen (trivialen) Eulerkreis und Eulerzug.
- `has_euler_circuit` und `has_euler_trail` sollen die Sätze aus Abschnitt 2.2 benutzen und in $O(|V| + |E|)$ laufen – probieren Sie **nicht** alle Kantenzüge aus.
- `find_euler_circuit` gibt eine Liste `[v0, ..., v0]` mit $|E| + 1$ Einträgen zurück, die jede Kante genau einmal benutzt, `None`, falls es keinen Eulerkreis gibt, und `[]` für Graphen ohne Kanten. `find_euler_trail` ebenso (offen oder geschlossen); bei zwei ungeraden Knoten beginnt und endet der Zug in diesen.
- `find_hamiltonian_cycle` gibt `[v0, v1, ..., v_{n-1}, v0]` zurück oder `None`, falls es keinen Hamiltonkreis gibt oder der Graph weniger als 3 Knoten hat. Die Funktion ist nur für kleine Graphen (etwa bis 15 Knoten) gedacht.
- Die Eingabe darf nicht verändert werden. Arbeiten Sie, wenn Sie Kanten löschen wollen, auf `graph.copy()`.
- Die Tests akzeptieren **jeden** gültigen Eulerkreis, Eulerzug bzw. Hamiltonkreis.

## 7. Beispiele für erwartetes Verhalten

```python
>>> from lib.graph import Graph
>>> from lib.generators import complete_graph, petersen_graph
>>> haus = Graph.from_edges([(1, 2), (1, 3), (1, 4), (2, 3), (2, 4), (3, 4), (3, 5), (4, 5)])
>>> has_euler_circuit(haus), has_euler_trail(haus)
(False, True)
>>> has_euler_circuit(complete_graph(5)), has_euler_circuit(complete_graph(4))
(True, False)
>>> two_triangles = Graph.from_edges([(1, 2), (2, 3), (3, 1), (4, 5), (5, 6), (6, 4)])
>>> edges_connected(two_triangles), has_euler_circuit(two_triangles)
(False, False)
>>> lonely = Graph()
>>> lonely.add_vertices(["Michel", "Ida"])
>>> edges_connected(lonely), has_euler_circuit(lonely)
(True, True)
>>> has_euler_circuit(Graph(directed=True))
Traceback (most recent call last):
    ...
ValueError: has_euler_circuit() expects an undirected graph

>>> find_euler_trail(haus)                  # eine mögliche Lösung
[1, 2, 3, 1, 4, 3, 5, 4, 2]
>>> find_euler_circuit(complete_graph(5))   # eine mögliche Lösung
[0, 1, 2, 0, 3, 1, 4, 2, 3, 4, 0]
>>> find_euler_circuit(haus) is None, find_euler_circuit(lonely)
(True, [])
>>> find_hamiltonian_cycle(haus)            # eine mögliche Lösung
[1, 2, 3, 5, 4, 1]
>>> find_hamiltonian_cycle(petersen_graph()) is None
True
```

```bash
python -m pytest exercises/05_euler_hamilton
```

## 8. Hinweise und optionale Zusatzaufgaben

**Hinweise**

- Die Anzahl der Knoten mit ungeradem Grad ist nach dem Handschlaglemma (Einheit 1) immer gerade. „Genau 0 oder 2“ ist also dasselbe wie „höchstens 2“.
- Achtung: Ein Graph mit Eulerkreis hat **auch** einen Eulerzug – `has_euler_trail` muss dann `True` liefern.
- Mit `lib.testing.assert_valid_euler_circuit(graph, walk)`, `assert_valid_euler_trail` und `assert_valid_hamiltonian_cycle` können Sie Ihre Ergebnisse selbst prüfen.
- Bei Hierholzer: `remaining.neighbors(v)` liefert eine Liste; ist sie leer, ist `v` „festgefahren“.
- Beim Backtracking: Vergessen Sie nicht, einen Schritt wieder rückgängig zu machen (Knoten aus dem Weg **und** aus der Menge der benutzten Knoten entfernen).

**Optionale Zusatzaufgaben**

1. **Eulersch machen.** Gegeben ist ein zusammenhängender Graph. Fügen Sie einen neuen Knoten hinzu und verbinden Sie ihn mit allen Knoten ungeraden Grades. Warum ist das Ergebnis eulersch? (So erzeugen auch die Tests zufällige eulersche Graphen.)
2. **Gerichtete Graphen.** Formulieren Sie das Euler-Kriterium für gerichtete Graphen. *Hinweis:* Vergleichen Sie für jeden Knoten Eingangs- und Ausgangsgrad.
3. **Laufzeit messen.** Messen Sie mit `lib.utils.measure_time` die Laufzeit von `find_hamiltonian_cycle` auf `lib.generators.grid_graph(3, k)` für ungerade $k = 3, 5, 7, \dots$ (kein Hamiltonkreis, die Suche muss alles ausprobieren) und vergleichen Sie mit `find_euler_trail` auf großen Graphen.
4. **Chinesisches Briefträgerproblem.** Der Briefträger muss jede Straße mindestens einmal ablaufen und zurückkehren. Wenn der Graph nicht eulersch ist, muss er manche Straßen doppelt gehen. Welche? Überlegen Sie für das Haus vom Nikolaus und für Königsberg (jede Brücke Länge 1), wie viele Kanten mindestens doppelt benutzt werden müssen.
5. **Ikosaeder-Spiel.** Finden Sie einen Hamiltonkreis im Dodekaeder-Graphen (20 Knoten, 3-regulär). Bauen Sie den Graphen in Python nach und testen Sie Ihre Lösung mit `assert_valid_hamiltonian_cycle`.

## 9. Quellen und weiterführende Literatur

- L. Euler: *Solutio problematis ad geometriam situs pertinentis*. Commentarii academiae scientiarum Petropolitanae 8 (1736/1741), S. 128–140.
- C. Hierholzer: *Ueber die Möglichkeit, einen Linienzug ohne Wiederholung und ohne Unterbrechung zu umfahren*. Mathematische Annalen 6 (1873), S. 30–32.
- G. A. Dirac: *Some theorems on abstract graphs*. Proceedings of the London Mathematical Society (3) 2 (1952), S. 69–81.
- O. Ore: *Note on Hamilton circuits*. The American Mathematical Monthly 67 (1960), S. 55.
- R. M. Karp: *Reducibility among combinatorial problems*. In: R. E. Miller, J. W. Thatcher (Hrsg.): Complexity of Computer Computations. Plenum Press 1972, S. 85–103.
- R. Diestel: *Graphentheorie*. Springer, 5. Auflage 2017, Abschnitt 1.8 (Eulertouren) und Kapitel 10 (Hamiltonkreise).
- S. O. Krumke, H. Noltemeier: *Graphentheoretische Konzepte und Algorithmen*. Springer Vieweg, 3. Auflage 2012.
- J. Kleinberg, É. Tardos: *Algorithm Design*. Pearson 2005, Kapitel 8 (NP-Vollständigkeit, u. a. des Hamiltonkreisproblems).
- M. R. Garey, D. S. Johnson: *Computers and Intractability: A Guide to the Theory of NP-Completeness*. W. H. Freeman 1979.
