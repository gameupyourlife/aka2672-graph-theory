# Einheit 9: Planarität und Komplexität

## 1. Titel und Lernziele

Diese Einheit verbindet zwei Fragen, die am Ende des Kurses stehen: *Welche Graphen kann man ohne Kreuzungen zeichnen?* und *Welche Graphenprobleme kann man effizient lösen?* Nach der Einheit können Sie

- die Begriffe planarer Graph, ebene Einbettung und Fläche erklären,
- die Eulersche Polyederformel $n - m + f = 1 + c$ anwenden und ihre Beweisidee wiedergeben,
- aus der Formel die Kantenschranken $m \le 3n - 6$ und (ohne Dreiecke) $m \le 2n - 4$ herleiten und damit zeigen, dass $K_5$ und $K_{3,3}$ nicht planar sind,
- begründen, warum diese Schranken nur **notwendige** Bedingungen sind (Petersen-Graph), und die Sätze von Kuratowski und Wagner formulieren,
- die Laufzeiten der Kursalgorithmen in $O$-Notation vergleichen,
- die Klassen P, NP, NP-schwer und NP-vollständig unterscheiden und typische Graphenprobleme einordnen,
- an der naiven Hamiltonkreis-Suche erleben, wie schnell $(n-1)!$ wächst.

Diese Einheit implementiert **keinen** vollständigen Planaritätstest. Solche Tests gibt es (siehe Abschnitt 2.5), sie sind aber deutlich zu aufwendig für diesen Kurs.

## 2. Mathematischer Hintergrund

### 2.1 Planare Graphen und Flächen

Ein Graph heißt **planar**, wenn man ihn so in die Ebene zeichnen kann, dass sich Kanten höchstens in ihren gemeinsamen Endknoten berühren. Eine solche kreuzungsfreie Zeichnung heißt **ebene Einbettung** (oder **ebener Graph**).

Entfernt man die gezeichneten Knoten und Kanten aus der Ebene, zerfällt der Rest in zusammenhängende Gebiete, die **Flächen** (Gebiete, engl. *faces*). Genau eine davon ist unbeschränkt: die **äußere Fläche**.

*Beispiel:* Zeichnen Sie $K_4$ als Dreieck mit einem Knoten in der Mitte, der mit allen drei Ecken verbunden ist. Es entstehen drei innere Dreiecksflächen und die äußere Fläche, also $f = 4$.

### 2.2 Die Eulersche Polyederformel

> **Satz (Euler).** Für jeden ebenen Graphen mit $n \ge 1$ Knoten, $m$ Kanten, $f$ Flächen und $c$ Zusammenhangskomponenten gilt
> $$n - m + f = 1 + c.$$
> Insbesondere gilt für zusammenhängende ebene Graphen $n - m + f = 2$.

Bemerkenswert: Die Anzahl der Flächen hängt **nicht** von der gewählten Zeichnung ab, sondern nur von $n$, $m$ und $c$.

*Beweisidee (zusammenhängender Fall, Induktion über $m$):*

- Ist $G$ ein **Baum**, so ist $m = n - 1$ und es gibt nur die äußere Fläche, $f = 1$. Also $n - (n-1) + 1 = 2$.
- Ist $G$ kein Baum, so enthält $G$ einen Kreis. Eine Kante $e$ auf diesem Kreis trennt zwei *verschiedene* Flächen (der Kreis ist eine geschlossene Kurve, die das Innere vom Äußeren trennt – Jordanscher Kurvensatz). Entfernt man $e$, verschmelzen diese zwei Flächen zu einer; der Graph bleibt zusammenhängend. Also sinken $m$ und $f$ jeweils um 1, und $n - m + f$ bleibt gleich. Nach Induktionsvoraussetzung ist der Wert 2.

Alternativ: Man startet mit einem Spannbaum ($f = 1$) und fügt die übrigen $m - n + 1$ Kanten einzeln hinzu; jede davon teilt eine Fläche in zwei.

*Mehrere Komponenten:* Für jede Komponente $i$ gilt $n_i - m_i + f_i = 2$. Summiert man über alle $c$ Komponenten, wird die äußere Fläche $c$-mal gezählt, obwohl sie nur einmal existiert. Also $f = \sum f_i - (c - 1)$ und damit $n - m + f = 2c - (c-1) = 1 + c$.

### 2.3 Folgerung: Kantenschranken

> **Korollar.** Für jeden einfachen planaren Graphen mit $n \ge 3$ Knoten gilt
> $$m \le 3n - 6.$$
> Enthält der Graph zusätzlich **kein Dreieck** (keinen Kreis der Länge 3), so gilt sogar
> $$m \le 2n - 4.$$

*Beweisidee:* Zunächst sei $G$ zusammenhängend. Umrundet man den Rand einer Fläche, so zählt man dessen Kanten (eine Kante, die auf beiden Seiten an dieselbe Fläche grenzt, wird doppelt gezählt). Da $G$ einfach ist und $n \ge 3$ gilt, hat jeder Flächenrand mindestens 3 Kanten. Jede Kante wird beim Umrunden aller Flächen genau zweimal gezählt. Daher
$$3f \le 2m.$$
Eingesetzt in $n - m + f = 2$ ergibt sich $2 \le n - m + \tfrac{2}{3}m$, also $m \le 3n - 6$. Ohne Dreiecke hat jeder Flächenrand mindestens 4 Kanten, also $4f \le 2m$ und analog $m \le 2n - 4$.

Ist $G$ nicht zusammenhängend, verbindet man die Komponenten durch zusätzliche Kanten (Brücken). Das erhält die Planarität, erzeugt kein Dreieck und erhöht $m$ – die Schranken gelten also erst recht.

**Wichtige Konsequenz für Algorithmen:** Planare Graphen haben nur $m = O(n)$ Kanten. Eine BFS auf einem planaren Graphen kostet daher $O(n)$.

### 2.4 $K_5$ und $K_{3,3}$ sind nicht planar

- $K_5$: $n = 5$, $m = 10 > 9 = 3n - 6$. Also nicht planar.
- $K_{3,3}$: $n = 6$, $m = 9 \le 12 = 3n - 6$ – die erste Schranke entscheidet nichts! Aber $K_{3,3}$ ist bipartit, enthält also keinen Kreis ungerader Länge und insbesondere kein Dreieck. Dann müsste $m \le 2n - 4 = 8$ gelten, aber $m = 9$. Also nicht planar.

$K_{3,3}$ ist das bekannte **Drei-Häuser-Problem** (siehe Abschnitt 4).

### 2.5 Charakterisierung planarer Graphen (nur Aussagen)

Eine **Unterteilung** eines Graphen entsteht, indem man Kanten durch Wege ersetzt (also neue Knoten vom Grad 2 auf Kanten setzt). Ein **Minor** entsteht durch Löschen von Knoten und Kanten und durch **Kontrahieren** von Kanten (die beiden Endknoten werden zu einem Knoten verschmolzen).

> **Satz von Kuratowski (1930).** Ein Graph ist genau dann planar, wenn er keine Unterteilung von $K_5$ oder $K_{3,3}$ als Teilgraphen enthält.

> **Satz von Wagner (1937).** Ein Graph ist genau dann planar, wenn er weder $K_5$ noch $K_{3,3}$ als Minor enthält.

**Die Kantenschranken sind nur notwendig.** Der **Petersen-Graph** hat $n = 10$, $m = 15$ und kein Dreieck. Es gilt $15 \le 24 = 3n - 6$ und $15 \le 16 = 2n - 4$ – beide Schranken sind erfüllt. Trotzdem ist er nicht planar: Kontrahiert man die fünf „Speichen“ zwischen äußerem Fünfeck und innerem Pentagramm, entsteht $K_5$ (Wagner). Aus „Schranken erfüllt“ folgt also **nicht** „planar“.

*Ausblick:* Hopcroft und Tarjan (1974) haben gezeigt, dass man Planarität in **linearer Zeit** $O(n)$ testen kann. Ihr Algorithmus (und spätere Vereinfachungen) beruht auf Tiefensuche, ist aber zu aufwendig für diesen Kurs.

*Ausblick 2:* Der **Vierfarbensatz** (Appel und Haken, 1976/77, computergestützter Beweis) besagt: Jeder planare Graph ist mit 4 Farben knotenfärbbar. Für jede Landkarte reichen also 4 Farben.

### 2.6 Komplexität: Wiederholung der $O$-Notation

Für Funktionen $f, g : \mathbb{N} \to \mathbb{R}_{\ge 0}$ schreibt man $f \in O(g)$, wenn es Konstanten $c > 0$ und $n_0$ gibt mit
$$f(n) \le c \cdot g(n) \quad \text{für alle } n \ge n_0.$$
$O(g)$ beschreibt also, wie die Laufzeit *höchstens* wächst – konstante Faktoren und kleine Eingaben werden ignoriert. Ein Algorithmus heißt **polynomiell**, wenn seine Laufzeit in $O(N^k)$ für eine feste Zahl $k$ liegt, wobei $N$ die Eingabegröße ist (bei Graphen: $n + m$).

**Die Algorithmen dieses Kurses** ($n = |V|$, $m = |E|$):

| Problem | Algorithmus | Laufzeit | Voraussetzungen |
|---|---|---|---|
| Erreichbarkeit, Komponenten, ungewichtete kürzeste Wege | BFS / DFS | $O(n + m)$ | – |
| Minimaler Spannbaum | Kruskal mit Union-Find | $O(m \log m)$ | ungerichtet, gewichtet |
| Kürzeste Wege von einem Start | Dijkstra mit Binärheap | $O((n + m) \log n)$ | nichtnegative Gewichte |
| Eulerkreis prüfen (und finden) | Gradtest + Zusammenhang (Hierholzer) | $O(n + m)$ | ungerichtet |
| Färbung (nicht unbedingt optimal) | Greedy-Färbung | $O(n + m)$ bei fester Reihenfolge | ungerichtet |
| Maximales Matching | Augmentierende Wege | $O(n \cdot m)$ | bipartit |
| Maximaler Fluss | Edmonds–Karp | $O(n \cdot m^2)$ | gerichtet, Kapazitäten $\ge 0$ |
| Hamiltonkreis (naiv) | alle Reihenfolgen probieren | $O(n! \cdot n)$ bzw. $(n-1)!$ Permutationen | – |

Alle Zeilen außer der letzten sind polynomiell. Die letzte Zeile ist es **nicht** – und das ist kein Zufall der Implementierung, sondern (vermutlich) eine Eigenschaft des Problems.

**Wie schnell wächst was?** Angenommen, ein Rechner schafft $10^9$ Schritte pro Sekunde:

| $n$ | $n^2$ | $2^n$ | $n!$ |
|---|---|---|---|
| 10 | $10^2$ (sofort) | $\approx 10^3$ (sofort) | $\approx 3{,}6 \cdot 10^6$ (4 ms) |
| 20 | $400$ (sofort) | $\approx 10^6$ (1 ms) | $\approx 2{,}4 \cdot 10^{18}$ (77 Jahre) |
| 30 | $900$ (sofort) | $\approx 10^9$ (1 s) | $\approx 2{,}7 \cdot 10^{32}$ (unvorstellbar) |
| 50 | $2500$ (sofort) | $\approx 10^{15}$ (13 Tage) | $\approx 3 \cdot 10^{64}$ |

### 2.7 P, NP, NP-schwer, NP-vollständig

Ein **Entscheidungsproblem** hat die Antwort *ja* oder *nein* („Besitzt $G$ einen Hamiltonkreis?“). Ein **Optimierungsproblem** sucht eine beste Lösung („Finde eine kürzeste Rundreise“). Zu jedem Optimierungsproblem gehört ein Entscheidungsproblem mit Schranke („Gibt es eine Rundreise der Länge höchstens $L$?“).

- **P** ist die Klasse der Entscheidungsprobleme, die ein Algorithmus in polynomieller Zeit löst. *Beispiele:* Eulerkreis, 2-Färbbarkeit (= bipartit?), Planarität.
- **NP** ist die Klasse der Entscheidungsprobleme, bei denen man eine *Ja*-Antwort mit einem kurzen **Zertifikat** (Beleg) in polynomieller Zeit **überprüfen** kann. Der Prüfalgorithmus heißt **Verifizierer**. *Beispiel:* Für „Besitzt $G$ einen Hamiltonkreis?“ ist das Zertifikat der Kreis selbst. Ob eine Liste von Knoten ein Hamiltonkreis ist, prüft man schnell – einen zu *finden* ist das Schwierige. Es gilt $\text{P} \subseteq \text{NP}$.
- Eine **(polynomielle) Reduktion** von Problem $A$ auf Problem $B$ ist eine in polynomieller Zeit berechenbare Übersetzung jeder Eingabe von $A$ in eine Eingabe von $B$ mit derselben Antwort. *Intuition:* Wer $B$ schnell lösen kann, kann dann auch $A$ schnell lösen – $B$ ist „mindestens so schwer“ wie $A$.
- Ein Problem heißt **NP-schwer**, wenn sich **jedes** Problem aus NP darauf reduzieren lässt. Es muss selbst nicht in NP liegen (z. B. weil es ein Optimierungsproblem ist).
- Ein Problem heißt **NP-vollständig**, wenn es NP-schwer ist **und** in NP liegt. Diese Probleme sind die „schwersten“ in NP.

**Cook (1971)** zeigte, dass das Erfüllbarkeitsproblem der Aussagenlogik (SAT) NP-vollständig ist. **Karp (1972)** bewies darauf aufbauend durch Reduktionen die NP-Vollständigkeit von 21 Problemen, darunter Hamiltonkreis, Clique und Graphfärbung.

**Leicht und schwer liegen nah beieinander:**

| in P | NP-vollständig bzw. NP-schwer |
|---|---|
| Eulerkreis: jede **Kante** genau einmal | Hamiltonkreis: jeder **Knoten** genau einmal |
| 2-Färbbarkeit | 3-Färbbarkeit |
| Kürzester Weg von $s$ nach $t$ | Kürzeste Rundreise durch **alle** Knoten (TSP, NP-schwer) |

> **Offene Frage: Gilt P = NP?** Niemand weiß es. Findet jemand einen polynomiellen Algorithmus für *ein* NP-vollständiges Problem, so gilt P = NP. Die meisten Fachleute vermuten P ≠ NP. Die Frage ist eines der sieben Millennium-Probleme des Clay Mathematics Institute.

### 2.8 Wie viele Hamiltonkreise hat $K_n$?

Ein Hamiltonkreis in $K_n$ ($n \ge 3$) ist eine zyklische Anordnung aller $n$ Knoten. Hält man den Startknoten fest, gibt es $(n-1)!$ Reihenfolgen für die übrigen Knoten. Jeder Kreis wird dabei genau zweimal erzeugt – einmal in jeder Richtung ($a, b, c, d, a$ und $a, d, c, b, a$ sind derselbe Kreis). Also:
$$\#\{\text{Hamiltonkreise in } K_n\} = \frac{(n-1)!}{2} \qquad (n \ge 3).$$

| $n$ | 3 | 4 | 5 | 6 | 10 | 20 |
|---|---|---|---|---|---|---|
| $(n-1)!/2$ | 1 | 3 | 12 | 60 | 181 440 | $\approx 6{,}1 \cdot 10^{16}$ |

Die naive Suche probiert im schlimmsten Fall (kein Hamiltonkreis vorhanden) alle $(n-1)!$ Reihenfolgen und prüft jede in $O(n)$ – Laufzeit $O(n!)$.

## 3. Relevante Definitionen und Datenstrukturen

| Begriff | Bedeutung |
|---|---|
| planar | Es gibt eine kreuzungsfreie Zeichnung in der Ebene. |
| Fläche | Zusammenhängendes Gebiet der Ebene ohne die Zeichnung; genau eine Fläche ist unbeschränkt. |
| Dreieck | Kreis der Länge 3: drei paarweise benachbarte Knoten $u, v, w$. |
| dreiecksfrei | Der Graph enthält kein Dreieck (z. B. alle bipartiten Graphen). |
| Hamiltonkreis | Kreis, der jeden Knoten genau einmal besucht; in Python `[v0, v1, ..., v0]`. |
| Permutation | Eine Anordnung (Reihenfolge) von Objekten; $k$ Objekte haben $k!$ Permutationen. |
| Zertifikat | Ein Beleg für eine *Ja*-Antwort, der schnell überprüft werden kann. |

**Neue Python-Werkzeuge**

```python
import itertools
import math

list(itertools.permutations([1, 2, 3]))
# [(1, 2, 3), (1, 3, 2), (2, 1, 3), (2, 3, 1), (3, 1, 2), (3, 2, 1)]

for order in itertools.permutations(["b", "c"]):   # liefert Tupel, eins nach dem anderen
    cycle = ["a", *order, "a"]                     # ['a', 'b', 'c', 'a'], dann ['a', 'c', 'b', 'a']

math.factorial(5)        # 120
math.factorial(5) // 2   # 60  (ganzzahlige Division)

set([1, 2, 3]) & set([2, 3, 4])   # {2, 3}  (Schnittmenge)
```

`itertools.permutations` erzeugt die Permutationen **nacheinander**, statt sie alle gleichzeitig im Speicher zu halten – sonst wäre bei $n = 12$ schon der Arbeitsspeicher voll.

Für Zeitmessungen gibt es `measure_time` aus `lib.utils`:

```python
from lib.utils import measure_time
seconds = measure_time(hamiltonian_cycle_bruteforce, graph, repeat=1)
```

## 4. Problemstellung

In Bullerbü sollen die drei Höfe – Nordhof, Mittelhof und Südhof – jeweils an Wasser, Strom und Telefon angeschlossen werden. Die Leitungen sollen sich nicht kreuzen (alle liegen in derselben Tiefe). Das ist genau die Frage, ob $K_{3,3}$ planar ist. Lisa probiert es eine ganze Regenwoche lang – vergeblich. Warum, zeigt die Kantenschranke.

Allgemein soll Ihr Programm

1. aus $n$, $m$ und $c$ die Anzahl der Flächen einer ebenen Einbettung berechnen,
2. die maximale Kantenzahl eines planaren Graphen angeben,
3. für einen gegebenen Graphen entscheiden, ob er **nach den Kantenschranken sicher nicht planar** ist,
4. einen Hamiltonkreis durch Ausprobieren aller Reihenfolgen suchen und dabei mitzählen, wie viele Reihenfolgen geprüft wurden,
5. die Anzahl der Hamiltonkreise in $K_n$ berechnen,
6. typische Graphenprobleme einer Komplexitätsklasse zuordnen.

## 5. Arbeitsaufträge

**Teil A: Planarität (Programmieren)**

1. **`faces_by_euler_formula(num_vertices, num_edges, num_components=1)`** – Berechnen Sie $f$ aus der Eulerschen Formel.
   - Schritt 1: Prüfen Sie die Eingaben (siehe Abschnitt 6) und lösen Sie bei Unsinn einen `ValueError` aus.
   - Schritt 2: Lösen Sie $n - m + f = 1 + c$ nach $f$ auf.
2. **`max_planar_edges(num_vertices)`** – Geben Sie die maximale Kantenzahl eines einfachen planaren Graphen zurück. Überlegen Sie sich die Fälle $n = 0, 1, 2$ selbst (Wie viele Kanten hat $K_2$?).
3. **`has_triangle(graph)`** – Prüfen Sie, ob der ungerichtete Graph ein Dreieck enthält.
   - Idee: Eine Kante $\{u, v\}$ liegt genau dann in einem Dreieck, wenn $u$ und $v$ einen **gemeinsamen Nachbarn** haben.
4. **`is_certainly_nonplanar(graph)`** – Kombinieren Sie die beiden Kantenschranken aus Abschnitt 2.3.
   - Schritt 1: Gerichtete Graphen ablehnen; bei weniger als 3 Knoten `False` zurückgeben.
   - Schritt 2: Ist $m > 3n - 6$, geben Sie `True` zurück.
   - Schritt 3: Ist der Graph dreiecksfrei und $m > 2n - 4$, geben Sie `True` zurück.
   - Schritt 4: Sonst `False` – das heißt nur „die Schranken können es nicht entscheiden“.

**Teil B: Komplexität (Programmieren)**

5. **`hamiltonian_cycle_bruteforce(graph)`** – Suchen Sie einen Hamiltonkreis durch Ausprobieren.
   - Schritt 1: Gerichtete Graphen ablehnen; bei weniger als 3 Knoten `(None, 0)` zurückgeben.
   - Schritt 2: Halten Sie den ersten Knoten `v0 = graph.vertices()[0]` fest und durchlaufen Sie mit `itertools.permutations` alle Reihenfolgen der übrigen Knoten.
   - Schritt 3: Zählen Sie jede geprüfte Permutation. Bilden Sie `[v0, *order, v0]` und prüfen Sie mit `graph.has_edge`, ob alle aufeinanderfolgenden Knoten benachbart sind. Wenn ja: Kreis und Zähler zurückgeben.
   - Schritt 4: Wurde nichts gefunden, geben Sie `(None, Zähler)` zurück. Der Zähler muss dann genau $(n-1)!$ sein.
6. **`number_of_hamiltonian_cycles_complete(n)`** – Berechnen Sie $(n-1)!/2$ (Abschnitt 2.8). Vergleichen Sie für $n = 4$ mit einer Zeichnung: Finden Sie alle 3 Hamiltonkreise von $K_4$?
7. **`COMPLEXITY_CLASSES`** – Ersetzen Sie in `task.py` jedes `"TODO"` durch genau eines der Labels `"P"`, `"NP-vollständig"` oder `"NP-schwer"`. Ändern Sie die Problembeschreibungen (Schlüssel) nicht.
8. Führen Sie `python task.py` aus. Wie viele Permutationen prüft Ihre Suche beim Petersen-Graphen (`lib.generators.petersen_graph()`)? Warum genau so viele?

**Teil C: Papier und Bleistift**

1. **Euler nachrechnen.** Zeichnen Sie kreuzungsfrei: $K_4$, den Würfelgraphen (8 Ecken, 12 Kanten), ein $2 \times 3$-Gitter und zwei getrennte Dreiecke. Zählen Sie jeweils $n$, $m$, $f$, $c$ und prüfen Sie $n - m + f = 1 + c$.
2. **$K_5$ und $K_{3,3}$.** Zeigen Sie mit den Kantenschranken, dass $K_5$ und $K_{3,3}$ nicht planar sind. Warum reicht für $K_{3,3}$ die Schranke $3n - 6$ nicht aus, und warum darf man die Schranke $2n - 4$ verwenden?
3. **Petersen-Graph.** Bestimmen Sie $n$, $m$ und die Länge eines kürzesten Kreises. Zeigen Sie, dass beide Kantenschranken erfüllt sind. Begründen Sie mit dem Satz von Wagner (Speichen kontrahieren!), dass der Graph trotzdem nicht planar ist. Was folgt daraus für `is_certainly_nonplanar`?
4. **Rechenzeit schätzen.** Ein sehr schneller Rechner prüft $10^9$ Permutationen pro Sekunde. Wie lange braucht die naive Suche im schlimmsten Fall für $n = 20$? Für $n = 25$? Für welches größte $n$ ist sie an einem Tag fertig? Wie viele Knoten gewinnt man mit einem 1000-mal schnelleren Rechner?
5. **Zertifikate.** Was ist ein Zertifikat für „$G$ besitzt einen Hamiltonkreis“, und wie lange dauert seine Überprüfung? Kennen Sie ein ebenso kurzes Zertifikat für „$G$ besitzt **keinen** Hamiltonkreis“?
6. **Eulerkreis versus Hamiltonkreis.** Erklären Sie in zwei Sätzen, warum man die Existenz eines Eulerkreises schnell entscheiden kann (Stichwort: Grade), während für Hamiltonkreise kein solches Kriterium bekannt ist.

Die Lösungen zu Teil C stehen im Kopfkommentar von `demo_solution.py` – schauen Sie erst hinein, wenn Sie es selbst versucht haben.

## 6. Anforderungen an die Implementierung

- `faces_by_euler_formula` löst einen `ValueError` aus, wenn `num_vertices < 1`, `num_edges < 0`, `num_components < 1`, `num_components > num_vertices` oder `num_edges < num_vertices - num_components` ist. (Der letzte Fall: Ein Graph mit $c$ Komponenten braucht mindestens $n - c$ Kanten – jede Komponente enthält einen Spannbaum.) Eine Obergrenze für `num_edges` wird nicht geprüft.
- `max_planar_edges` liefert $0$ für $n = 0$ und $n = 1$, $1$ für $n = 2$ und $3n - 6$ für $n \ge 3$; negative $n$ ergeben einen `ValueError`.
- `has_triangle`, `is_certainly_nonplanar` und `hamiltonian_cycle_bruteforce` arbeiten nur mit **ungerichteten** Graphen und lösen sonst einen `ValueError` aus.
- `is_certainly_nonplanar` gibt `True` nur dann zurück, wenn eine der Kantenschranken verletzt ist. **`False` bedeutet ausdrücklich nicht „planar“**, sondern „mit diesen Schranken nicht entscheidbar“. Der leere Graph und Graphen mit weniger als 3 Knoten ergeben `False`.
- `hamiltonian_cycle_bruteforce` gibt ein Paar `(cycle, checked)` zurück. `cycle` beginnt und endet mit `graph.vertices()[0]` oder ist `None`. `checked` zählt die geprüften Permutationen (einschließlich der erfolgreichen). Ohne Hamiltonkreis ist `checked == math.factorial(n - 1)`. Bei weniger als 3 Knoten: `(None, 0)`. Laufzeit $O((n-1)! \cdot n)$ – testen Sie nur mit kleinen Graphen ($n \le 10$)!
- `number_of_hamiltonian_cycles_complete(n)` liefert $(n-1)!/2$ als ganze Zahl (`int`) für $n \ge 3$, $0$ für $n < 3$ und einen `ValueError` für negative $n$.
- `COMPLEXITY_CLASSES` enthält nur die Labels `"P"`, `"NP-vollständig"` und `"NP-schwer"`. **Konvention:** Gesucht ist die präziseste nach heutigem Kenntnisstand bekannte Klasse, unter der Annahme P ≠ NP. Optimierungsprobleme, die sich in polynomieller Zeit lösen lassen (z. B. kürzester Weg), bekommen das Label `"P"`. `"NP-schwer"` ist für Probleme gedacht, die NP-schwer sind, aber selbst keine Entscheidungsprobleme in NP sind.
- Keine Funktion verändert den übergebenen Graphen.

## 7. Beispiele für erwartetes Verhalten

```python
>>> from lib.generators import complete_graph, complete_bipartite_graph, petersen_graph, path_graph
>>> faces_by_euler_formula(4, 6)           # K4
4
>>> faces_by_euler_formula(6, 6, 2)        # zwei getrennte Dreiecke
3
>>> max_planar_edges(5)
9
>>> has_triangle(complete_bipartite_graph(3, 3))
False
>>> is_certainly_nonplanar(complete_graph(5))
True
>>> is_certainly_nonplanar(complete_bipartite_graph(3, 3))
True
>>> is_certainly_nonplanar(petersen_graph())   # nicht planar, aber die Schranken sehen es nicht!
False
>>> hamiltonian_cycle_bruteforce(complete_graph(4))   # ein möglicher Kreis
([0, 1, 2, 3, 0], 1)
>>> hamiltonian_cycle_bruteforce(path_graph(5))       # kein Hamiltonkreis: 4! = 24 Versuche
(None, 24)
>>> hamiltonian_cycle_bruteforce(petersen_graph())
(None, 362880)
>>> number_of_hamiltonian_cycles_complete(5)
12
```

Welcher Hamiltonkreis gefunden wird und nach wie vielen Versuchen, hängt von der Reihenfolge der Permutationen ab; die Tests akzeptieren jeden gültigen Kreis. Ohne Hamiltonkreis muss die Anzahl aber genau $(n-1)!$ sein.

```bash
python -m pytest exercises/09_planarity_complexity
```

## 8. Hinweise und optionale Zusatzaufgaben

**Hinweise**

- Die Nachbarn eines Knotens als Menge: `set(graph.neighbors(u))`. Die Schnittmenge zweier Mengen: `a & b`. Eine nichtleere Menge ist in einer `if`-Bedingung „wahr“.
- `all(bedingung for i in range(k))` ist genau dann `True`, wenn die Bedingung für alle `i` gilt, und bricht beim ersten `False` ab.
- `graph.vertices()[1:]` sind alle Knoten außer dem ersten.
- Für `is_certainly_nonplanar` genügt `graph.num_vertices()`, `graph.num_edges()` und Ihre Funktion `has_triangle`.
- Rufen Sie `hamiltonian_cycle_bruteforce` nicht mit einem Graphen mit 15 Knoten **ohne** Hamiltonkreis auf – das wären $14! \approx 8{,}7 \cdot 10^{10}$ Permutationen. Bei $K_n$ wird dagegen sofort ein Kreis gefunden. Überlegen Sie, warum.

**Optionale Zusatzaufgaben**

1. **`runtime_experiment(sizes, seed=0)`** (in `task.py`, getestet, wenn implementiert): Messen Sie für jedes $n$ in `sizes` die Laufzeit von `hamiltonian_cycle_bruteforce` auf einem Graphen **ohne** Hamiltonkreis, z. B. `random_tree(n, seed=seed + n)` aus `lib.generators`. Rückgabe: Liste von Paaren `(n, sekunden)`. Rufen Sie die Funktion mit `range(5, 11)` auf und berechnen Sie den Quotienten aufeinanderfolgender Zeiten. Ungefähr welcher Faktor ergibt sich, und warum?
2. **Schärfere Schranke über die Taillenweite.** Ist jeder Kreis eines planaren zusammenhängenden Graphen mindestens $g$ lang, so gilt $m \le \frac{g}{g-2}(n - 2)$. Beweisen Sie das wie in Abschnitt 2.3 und zeigen Sie damit, dass der Petersen-Graph ($g = 5$) nicht planar ist.
3. **Kuratowski von Hand.** Finden Sie im Petersen-Graphen eine Unterteilung von $K_{3,3}$. (Tipp: Löschen Sie einen Knoten.)
4. **Grenzen der Schranke.** `is_certainly_nonplanar` erkennt $K_5$ nicht mehr, wenn man zwei isolierte Knoten hinzufügt. Warum? Wie könnte man die Funktion mit einer Zerlegung in Zusammenhangskomponenten verbessern? (Schreiben Sie dafür eine eigene kleine Suchfunktion in dieser Einheit.)
5. **Bessere Hamiltonkreis-Suche.** Bauen Sie den Kreis schrittweise auf und brechen Sie ab, sobald zwei aufeinanderfolgende Knoten nicht benachbart sind (*Backtracking*). Wie viel schneller wird der Petersen-Graph? Warum bleibt die Laufzeit im schlimmsten Fall trotzdem exponentiell? (Der Algorithmus von Bellman, Held und Karp schafft $O(n^2 2^n)$ – immer noch exponentiell.)
6. **Reduktion.** Zeigen Sie: Kann man „Hat $G$ einen Hamiltonkreis?“ schnell entscheiden, dann auch „Hat $G$ einen Hamiltonweg zwischen $s$ und $t$?“. (Tipp: Fügen Sie einen neuen Knoten hinzu.)

## 9. Quellen und weiterführende Literatur

- R. Diestel: *Graphentheorie*. Springer, 5. Auflage 2017, Kapitel 4 (Planare Graphen) und Kapitel 5 (Färbungen, Vierfarbensatz).
- S. O. Krumke, H. Noltemeier: *Graphentheoretische Konzepte und Algorithmen*. Springer Vieweg, 3. Auflage 2012.
- T. H. Cormen, C. E. Leiserson, R. L. Rivest, C. Stein: *Algorithmen – Eine Einführung*. De Gruyter, 4. Auflage 2022, Kapitel zur asymptotischen Notation und Kapitel „NP-Vollständigkeit“.
- J. Kleinberg, É. Tardos: *Algorithm Design*. Pearson 2005, Kapitel 8 (NP and Computational Intractability).
- M. R. Garey, D. S. Johnson: *Computers and Intractability: A Guide to the Theory of NP-Completeness*. W. H. Freeman, 1979.
- K. Kuratowski: *Sur le problème des courbes gauches en topologie*. Fundamenta Mathematicae 15 (1930), S. 271–283.
- K. Wagner: *Über eine Eigenschaft der ebenen Komplexe*. Mathematische Annalen 114 (1937), S. 570–590.
- J. Hopcroft, R. Tarjan: *Efficient planarity testing*. Journal of the ACM 21(4), 1974, S. 549–568.
- K. Appel, W. Haken: *Every planar map is four colorable. Part I: Discharging*. Illinois Journal of Mathematics 21 (1977), S. 429–490; K. Appel, W. Haken, J. Koch: *Part II: Reducibility*, ebenda, S. 491–567.
- S. A. Cook: *The complexity of theorem-proving procedures*. Proceedings of the Third Annual ACM Symposium on Theory of Computing (STOC), 1971, S. 151–158.
- R. M. Karp: *Reducibility among combinatorial problems*. In: R. E. Miller, J. W. Thatcher (Hrsg.): *Complexity of Computer Computations*. Plenum Press, New York 1972, S. 85–103.
- Python-Dokumentation zu `itertools.permutations`: <https://docs.python.org/3/library/itertools.html#itertools.permutations>
