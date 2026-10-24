# Einheit 10: Abschlussprojekt – Das Netzwerk von Nangijala

## 1. Titel und Lernziele

Im Abschlussprojekt wenden Sie alles an, was Sie im Kurs implementiert haben. Sie schreiben **keine neuen Algorithmen**, sondern übersetzen Fragen aus einem Szenario in Graphprobleme und lösen sie mit Ihren Funktionen aus den Einheiten 2–8. Nach dem Projekt können Sie

- ein Anwendungsproblem als Graph modellieren und die Modellierungsentscheidungen begründen (gerichtet/ungerichtet, Gewichte, Knoten, Kanten),
- zu einer Frage das passende Graphproblem erkennen (Erreichbarkeit, Spannbaum, kürzester Weg, Färbung, Matching, Fluss),
- prüfen, ob die mathematischen Voraussetzungen eines Algorithmus erfüllt sind,
- Ergebnisse interpretieren, überprüfen und präsentieren.

## 2. Mathematischer Hintergrund

Das Projekt verbindet die Sätze aus dem Kurs:

| Frage im Szenario | Graphproblem | Satz / Algorithmus | Einheit |
|---|---|---|---|
| Wer kann wen noch erreichen? | Zusammenhangskomponente | BFS / DFS | 2 |
| Welche Orte sind kritisch? | Schnittknoten (Artikulationspunkte) | Komponenten zählen | 2 |
| Welche Wege räumen wir im Winter? | minimaler Spannbaum | Schnitteigenschaft, Kruskal | 3 |
| Wie kommen wir am schnellsten hin? | kürzester Weg, Gewichte $\ge 0$ | Dijkstra | 4 |
| Welche Laternenfarben? | Knotenfärbung | Greedy-Färbung, $\chi(G) \le \Delta(G) + 1$ | 6 |
| Wer übernimmt welche Aufgabe? | maximales bipartites Matching | Satz von Berge, augmentierende Wege | 7 |
| Wie viel Nachschub pro Nacht? | maximaler Fluss | Max-Flow-Min-Cut, Edmonds-Karp | 8 |

**Schnittknoten.** Ein Knoten $v$ eines Graphen $G$ heißt *Schnittknoten*, wenn $G - v$ (der Graph ohne $v$ und ohne alle Kanten an $v$) mehr Zusammenhangskomponenten hat als $G$. Fällt ein solcher Ort aus, zerfällt das Netz.

## 3. Relevante Definitionen

- **Modell.** Orte sind Knoten, Straßen sind Kanten. Straßen sind in beide Richtungen befahrbar, also ist das Straßennetz ein **ungerichteter** Graph. Das **Kantengewicht** ist die Reisezeit in Minuten.
- **Sperrung.** Ist ein Ort gesperrt, wird er mitsamt seinen Straßen entfernt: Man betrachtet den Teilgraphen $G - S$ für die Menge $S$ der gesperrten Orte.
- **Aufgabenverteilung.** Menschen und Aufgaben bilden die beiden Seiten eines **bipartiten** Graphen; eine Kante bedeutet „ist für diese Aufgabe geeignet“.
- **Nachschubwege.** Geheime Pfade sind nur in einer Richtung nutzbar (bergab, mit der Strömung, …). Sie bilden ein **Flussnetzwerk**: ein gerichteter Graph, dessen Kantengewichte Kapazitäten (Säcke Mehl pro Nacht) sind.

Alle Daten stehen in `nangijala_data.py`:

| Name | Inhalt |
|---|---|
| `ROADS` | 28 Straßen `(Ort, Ort, Minuten)` zwischen 20 Orten |
| `KIRSCHTAL`, `HECKENROSENTAL` | die Orte der beiden Täler |
| `QUALIFICATIONS` | Person → Liste geeigneter Aufgaben |
| `SUPPLY_ROUTES` | gerichtete Nachschubwege `(von, nach, Kapazität)` |

## 4. Problemstellung

Nangijala besteht aus zwei Tälern: Im Westen liegt das **Kirschtal** mit dem Reiterhof, dem Gasthof „Goldener Hahn“ und Sofias Hof. Im Osten liegt das **Heckenrosental** mit Stadttor, Marktplatz und der versteckten Rebellenhöhle. Dazwischen liegen Berge mit Pässen, Schluchten und dem Karmafall. Im Nordosten führt ein Weg über die Grenzwache zu Tengils Burg und nach Karmanjaka.

Die Menschen in Nangijala haben viele Fragen. Wer wohnt wo, und wie erreichen sie sich, wenn Wege gesperrt sind? Welche Wege sollen im Winter geräumt werden? Wie lassen sich die Aufgaben verteilen? Ihr Team beantwortet diese Fragen mit Graphentheorie.

## 5. Arbeitsaufträge

Das Projekt ist **modular**. Modul A bearbeiten alle Gruppen. Danach wählt jede Gruppe mindestens zwei der Module B–F; Modul G ist optional. Am Ende stellt jede Gruppe ihre Ergebnisse in 10 Minuten vor.

Am Anfang von `task.py` legt die Konstante `PREVIOUS` fest, welche Implementierungen der früheren Einheiten verwendet werden: `"task"` steht für Ihre eigenen (empfohlen), `"demo_solution"` für die Musterlösungen. Falls eine Ihrer früheren Lösungen noch nicht fertig ist, können Sie vorübergehend umschalten. Die Module stehen dann als `bfs_dfs`, `spanning_trees`, `shortest_paths`, `coloring`, `matching` und `max_flow` zur Verfügung, z. B. `bfs_dfs.dfs(graph, start)`.

### Modul A – Modellierung (alle Gruppen)

1. **`build_network(roads)`** – Erzeugen Sie aus `data.ROADS` den ungerichteten, gewichteten Graphen.
2. **`without_places(graph, blocked)`** – Geben Sie eine Kopie des Graphen ohne die gesperrten Orte zurück.
3. Zeichnen Sie das Netz (z. B. mit `lib.visualization.save_dot` und Graphviz oder auf Papier). Prüfen Sie das Handschlaglemma mit Ihrer Funktion aus Einheit 1.
4. *Diskussion:* Welche Eigenschaften der Wirklichkeit gehen beim Modellieren verloren? Wann wäre ein gerichteter Graph besser?

### Modul B – Erreichbarkeit (Einheit 2)

1. **`reachable_places(graph, start, blocked)`** – Tengils Soldaten sperren den Bärenpass und den Adlerhorst. Welche Orte erreicht man dann noch vom Reiterhof aus?
2. **`critical_places(graph)`** – Bestimmen Sie alle Schnittknoten. Entfernen Sie dazu nacheinander jeden Knoten und zählen Sie die Komponenten.
3. *Diskussion:* Welche Laufzeit hat Ihr Verfahren? Welche Straße müsste man bauen, damit es keinen kritischen Ort mehr gibt?

### Modul C – Winterwege (Einheit 3)

1. **`winter_roads(graph)`** – Im Winter kann man nur wenige Wege räumen. Alle Orte sollen verbunden bleiben, und die Summe der Reisezeiten der geräumten Wege soll minimal sein. Geben Sie die Wege und ihre Gesamtzeit zurück.
2. *Diskussion:* Warum ist das Ergebnis hier eindeutig? Ist der Weg vom Reiterhof zur Rebellenhöhle im Spannbaum auch der schnellste Weg im ganzen Netz?

### Modul D – Schnellste Wege (Einheit 4)

1. **`fastest_route(graph, start, target, blocked)`** – Wie kommt man am schnellsten vom Reiterhof zu Tengils Burg? Und zum Marktplatz, wenn Bärenpass und Waldsee gesperrt sind?
2. *Diskussion:* Warum darf man hier Dijkstra verwenden? Was müsste man ändern, wenn manche Wege nur bergab nutzbar sind?

### Modul E – Laternenfarben (Einheit 6)

1. **`lantern_colors(graph)`** – Benachbarte Orte geben sich nachts Lichtzeichen. Damit es keine Verwechslungen gibt, müssen benachbarte Orte verschiedene Laternenfarben benutzen. Färben Sie das Netz mit der Greedy-Färbung. Probieren Sie dabei mindestens zwei Knotenreihenfolgen und geben Sie das beste Ergebnis zurück.
2. *Diskussion:* Warum braucht man mindestens 3 Farben? Finden Sie eine Färbung mit genau 3 Farben?

### Modul F – Aufgabenverteilung (Einheit 7)

1. **`assign_tasks(qualifications)`** – Die Rebellen verteilen die Aufgaben aus `data.QUALIFICATIONS`. Jede Person übernimmt höchstens eine Aufgabe, für die sie geeignet ist, und jede Aufgabe wird höchstens einmal vergeben. Möglichst viele Personen sollen eine Aufgabe bekommen.
2. *Diskussion:* Warum bekommen nicht alle sieben Personen eine Aufgabe? Begründen Sie mit dem Heiratssatz von Hall.

### Modul G – Nachschub (Einheit 8, optional)

1. **`max_supply(routes, source, sink)`** – Wie viele Säcke Mehl können pro Nacht vom Kirschtal ins Heckenrosental gebracht werden (`data.SUPPLY_ROUTES`)?
2. *Diskussion:* Bestimmen Sie einen minimalen Schnitt. Welche Wege sind der Engpass?

## 6. Anforderungen an die Implementierung

- Verwenden Sie Ihre Funktionen aus den Einheiten 2–8 über die vorbereiteten Modulvariablen (`bfs_dfs`, `spanning_trees`, …). Implementieren Sie die Algorithmen nicht erneut.
- Keine Funktion darf den übergebenen Graphen verändern.
- Unbekannte Orte führen zu einem `KeyError`. Ist der Start- oder Zielort selbst gesperrt, wird ein `ValueError` ausgelöst.
- `fastest_route` gibt `None` zurück, wenn das Ziel nicht erreichbar ist, sonst ein Paar `(Weg, Minuten)`.
- `assign_tasks` gibt ein Wörterbuch `Person -> Aufgabe` zurück und löst einen `ValueError` aus, wenn ein Name zugleich Person und Aufgabe ist (sonst wäre der Graph nicht bipartit).
- Begründen Sie in Ihrer Präsentation für jedes Modul, warum die Voraussetzungen des verwendeten Algorithmus erfüllt sind.

## 7. Beispiele für erwartetes Verhalten

An einem kleinen Beispiel (die Werte für Nangijala sollen Sie selbst herausfinden):

```python
>>> g = build_network([("A", "B", 5), ("B", "C", 2), ("A", "C", 9), ("C", "D", 1)])
>>> reachable_places(g, "A", blocked=["C"])
{'A', 'B'}
>>> critical_places(g)
['C']
>>> winter_roads(g)
([Edge(u='C', v='D', weight=1), Edge(u='B', v='C', weight=2), Edge(u='A', v='B', weight=5)], 8)
>>> fastest_route(g, "A", "D")
(['A', 'B', 'C', 'D'], 8)
>>> fastest_route(g, "A", "D", blocked=["B"])
(['A', 'C', 'D'], 10)
>>> assign_tasks({"Pippi": ["Pferd", "Affe"], "Tommy": ["Pferd"]})
{'Pippi': 'Affe', 'Tommy': 'Pferd'}
```

Die Reihenfolge der Kanten in `winter_roads` darf abweichen.

```bash
python -m pytest exercises/10_final_project
python exercises/10_final_project/demo_solution.py   # vollständiger Bericht der Musterlösung
```

## 8. Hinweise und optionale Zusatzaufgaben

**Hinweise**

- Beginnen Sie jedes Modul mit einem kleinen, selbst ausgedachten Graphen, bei dem Sie das Ergebnis von Hand kennen. Wenden Sie Ihre Funktion erst danach auf ganz Nangijala an.
- `graph.copy()` und `graph.remove_vertex(v)` helfen bei `without_places`.
- Für `lantern_colors` ist eine gute Reihenfolge: Knoten mit großem Grad zuerst (`sorted(graph.vertices(), key=graph.degree, reverse=True)`).
- Für `assign_tasks` bauen Sie einen ungerichteten Graphen mit einer Kante Person – Aufgabe pro Eignung. Die Personen sind die „linke“ Seite.
- Die Prüffunktionen in `lib.testing` (z. B. `assert_valid_path`, `assert_valid_coloring`) helfen beim Überprüfen Ihrer Ergebnisse.

**Optionale Zusatzaufgaben**

1. **Robustheit:** Welche einzelne *Straße* zerlegt das Netz, wenn sie gesperrt wird (Brücke)? Schreiben Sie dazu eine Funktion `critical_roads(graph)`.
2. **Rundreise:** Gibt es eine Rundreise, die jede Straße genau einmal benutzt (Eulerkreis, Einheit 5)? Wie viele Straßen müsste man verdoppeln?
3. **Laufzeit:** Vergleichen Sie `critical_places` (Brute Force) auf `lib.generators.random_connected_graph(n, n)` für wachsende $n$ mit der erwarteten Laufzeit $O(|V| \cdot (|V| + |E|))$.
4. **Eigene Szenarien:** Erweitern Sie Nangijala um eigene Orte (z. B. Katlas Höhle als Gefahrenzone mit sehr hohen Reisezeiten) und untersuchen Sie, wie sich die Ergebnisse ändern.
5. **Planarität (Einheit 9):** Ist das Straßennetz planar? Zeichnen Sie es kreuzungsfrei und überprüfen Sie die Eulersche Polyederformel.

## 9. Quellen und weiterführende Literatur

- A. Lindgren: *Die Brüder Löwenherz*. Oetinger, 1974 (Original: *Bröderna Lejonhjärta*, Rabén & Sjögren 1973) – Vorlage für die Ortsnamen. Das Straßennetz und alle Zahlen sind frei erfunden.
- J. Kleinberg, É. Tardos: *Algorithm Design*. Pearson 2005 – viele Modellierungsbeispiele zu allen Algorithmen des Kurses.
- T. H. Cormen, C. E. Leiserson, R. L. Rivest, C. Stein: *Algorithmen – Eine Einführung*. De Gruyter, 4. Auflage 2022, Teil VI (Graphenalgorithmen).
- R. Diestel: *Graphentheorie*. Springer, 5. Auflage 2017, Kapitel 1–3 und 5.
- R. E. Tarjan: *Depth-first search and linear graph algorithms*. SIAM Journal on Computing 1(2), 1972, S. 146–160 – Schnittknoten in linearer Zeit.
- P. Hall: *On representatives of subsets*. Journal of the London Mathematical Society 10, 1935, S. 26–30.
