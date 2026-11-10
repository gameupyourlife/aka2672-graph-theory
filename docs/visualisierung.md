# Visualisierung und Algorithmen-Player

Die Bibliothek zeigt Graphen und den Ablauf von Graphalgorithmen interaktiv im Webbrowser. Ein Algorithmus wird dabei wie ein Film aufgezeichnet: Er beschreibt seinen Zustand (welcher Knoten ist besucht, welcher wird gerade bearbeitet, was steht in der Warteschlange) und nimmt nach jedem wichtigen Schritt ein Bild auf. Der Player zeigt diese Bilder anschließend vorwärts, rückwärts oder automatisch.

Es werden **keine zusätzlichen Pakete** benötigt. Python erzeugt eine eigenständige HTML-Datei mit SVG-Grafik und JavaScript, die in jedem aktuellen Browser läuft, auch ohne Internetverbindung.

## Inhalt

1. [Schnellstart](#1-schnellstart)
2. [Der Player im Browser](#2-der-player-im-browser)
3. [Einen Algorithmus aufzeichnen: Schritt für Schritt](#3-einen-algorithmus-aufzeichnen-schritt-für-schritt)
4. [Der Zustand: Flags, Beschriftungen, Farben, Variablen](#4-der-zustand-flags-beschriftungen-farben-variablen)
5. [Eingebaute Flags](#5-eingebaute-flags)
6. [Eigene Flags und Stile](#6-eigene-flags-und-stile)
7. [Pseudocode, Beschreibung und Nachrichten](#7-pseudocode-beschreibung-und-nachrichten)
8. [Einzelne Bilder: `draw` und `snapshot`](#8-einzelne-bilder-draw-und-snapshot)
9. [Mehrere Szenen auf einer Seite](#9-mehrere-szenen-auf-einer-seite)
10. [Anordnung der Knoten (Layouts)](#10-anordnung-der-knoten-layouts)
11. [Dateien, Browser, Jupyter](#11-dateien-browser-jupyter)
12. [Tipps für gute Animationen](#12-tipps-für-gute-animationen)
13. [Referenz](#13-referenz)
14. [Aufbau und Erweiterung](#14-aufbau-und-erweiterung)
15. [Fehlerbehebung](#15-fehlerbehebung)

## 1. Schnellstart

Ein Bild eines Graphen:

```python
from lib.generators import small_weighted_graph
from lib.visualization import draw

graph = small_weighted_graph()
draw(graph, "Rund um Lönneberga", highlight_vertices=["Katthult"])
```

Ein aufgezeichneter Ablauf mit drei Schritten:

```python
from lib.visualization import Trace, show

trace = Trace(graph, "Ein kleiner Spaziergang")
trace.current("Katthult")
trace.step("Michel startet in Katthult.")

trace.flag("Katthult", "visited")
trace.current("Lönneberga")
trace.current_edge("Katthult", "Lönneberga")
trace.step("Er geht nach Lönneberga (4 Minuten).")

trace.flag("Lönneberga", "visited")
trace.current(None)
trace.current_edge(None)
trace.step("Angekommen.")

show(trace)
```

`show` schreibt eine HTML-Datei und öffnet sie im Standardbrowser. Das Programm läuft dabei sofort weiter.

Alle Namen lassen sich aus `lib.visualization` importieren. Sie sind in `lib.trace` (Aufzeichnung) und `lib.viewer` (Player) definiert.

## 2. Der Player im Browser

```text
┌──────────────────────────────────────────────────────────────┬───────────────────┐
│ Titel        [Szene 1] [Szene 2] [Szene 3]                   │                   │
├──────────────────────────────────────────────────────────────┤  Nachricht des    │
│ Szenentitel                              [⤢ Fit] [SVG] [PNG] │  aktuellen        │
│                                                              │  Schritts         │
│                 Graph (SVG)                                  │  VARIABLES        │
│                                                              │  PSEUDOCODE       │
│                                                              │  LEGEND           │
│                                                              │  ABOUT            │
├──────────────────────────────────────────────────────────────┴───────────────────┤
│ ⏮  ◀  ▶  ▶❘  ⏭   ════════○══════════════════   Step 12 / 27        [1× ▾]      │
└──────────────────────────────────────────────────────────────────────────────────┘
```

| Bedienelement | Wirkung |
|---|---|
| ⏮ / ⏭ | erster / letzter Schritt |
| ◀ / ▶❘ | ein Schritt zurück / vor |
| ▶ (blau) | automatisch abspielen; während des Abspielens ❚❚ = Pause. Am Ende beginnt ▶ wieder von vorn. |
| Schieberegler | direkt zu einem Schritt springen |
| Geschwindigkeit | 0,25× bis 4× (1× = etwa ein Schritt pro Sekunde) |
| Reiter oben | zwischen mehreren Szenen wechseln |
| ⤢ Fit | Ansicht wieder auf den ganzen Graphen einpassen |
| SVG / PNG | aktuelles Bild herunterladen (PNG in doppelter Auflösung), z. B. für Folien |

| Maus | Wirkung |
|---|---|
| Mausrad | zoomen (um die Mausposition) |
| Hintergrund ziehen | Ansicht verschieben |
| Knoten ziehen | Knoten verschieben (bleibt für alle Schritte an der neuen Stelle) |
| Über einen Knoten fahren | Tooltip: Name, Flags, Beschriftung, Farbe, Attribute, Grad |

| Taste | Wirkung |
|---|---|
| → / ← | nächster / vorheriger Schritt |
| Leertaste | Abspielen / Pause |
| Pos1 / Ende | erster / letzter Schritt |
| Bild↓ / Bild↑ | nächste / vorherige Szene |
| F | Ansicht einpassen |

Die Adresse der Seite merkt sich Szene und Schritt (`…html#scene=2&step=14`). Ein Lesezeichen oder ein geteilter Link öffnet genau diese Stelle.

Die Seitenleiste zeigt nur, was die Szene enthält: Variablen, Pseudocode (mit hervorgehobener aktueller Zeile), eine Legende aller vorkommenden Flags und Farben und die Beschreibung der Szene. Geänderte Variablenwerte blinken kurz gelb auf.

## 3. Einen Algorithmus aufzeichnen: Schritt für Schritt

Am Beispiel der Breitensuche. Ausgangspunkt ist der Algorithmus ohne Visualisierung:

```python
from collections import deque

def bfs(graph, start):
    distance = {start: 0}
    queue = deque([start])
    while queue:
        u = queue.popleft()
        for w in graph.neighbors(u):
            if w not in distance:
                distance[w] = distance[u] + 1
                queue.append(w)
    return distance
```

**Schritt 1: Einen `Trace` anlegen.** Er bekommt den Graphen, einen Titel und optional Pseudocode und eine Beschreibung.

```python
from lib.visualization import Trace, show

trace = Trace(graph, "BFS ab A", pseudocode=[
    "Q = [s]; markiere s",
    "solange Q nicht leer:",
    "    u = Q.popleft()",
    "    für jeden Nachbarn w von u:",
    "        falls w unmarkiert: markiere w; Q.append(w)",
])
```

**Schritt 2: Den Zustand beschreiben**, sobald er sich ändert. Flags sagen, in welchem Zustand ein Knoten oder eine Kante ist. Beschriftungen, Farben und Variablen ergänzen das Bild.

```python
trace.flag(start, "start", "queued")     # Startknoten, wartet in der Warteschlange
trace.label(start, "d = 0")              # Text unter dem Knoten
trace.variable("Q", queue)               # Seitenleiste: Q = [A]
```

**Schritt 3: Ein Bild aufnehmen** mit `step(nachricht, line=...)`. Die Nachricht erklärt, *was* passiert und *warum*. `line` markiert die Zeile im Pseudocode (ab 1 gezählt).

```python
trace.step(f"Start: {start} kommt in die Warteschlange.", line=1)
```

**Schritt 4: Im Algorithmus fortfahren.** Der Zustand bleibt erhalten, bis man ihn ändert; ein neues `step` nimmt das nächste Bild auf.

```python
while queue:
    u = queue.popleft()
    trace.current(u)                     # u ist jetzt der einzige "current"-Knoten
    trace.unflag(u, "queued")
    trace.variable("Q", queue)
    trace.step(f"{u} wird aus der Warteschlange genommen.", line=3)
    for w in graph.neighbors(u):
        trace.current_edge(u, w)         # die gerade betrachtete Kante
        if w not in distance:
            distance[w] = distance[u] + 1
            queue.append(w)
            trace.flag(w, "queued")
            trace.flag_edge(u, w, "tree")
            trace.label(w, f"d = {distance[w]}")
            trace.variable("Q", queue)
            trace.step(f"{w} ist neu: Abstand {distance[w]}.", line=5)
    trace.current_edge(None)
    trace.flag(u, "visited")

trace.current(None)
trace.step("Fertig: Die grünen Kanten bilden den BFS-Baum.")
show(trace)
```

Fertige, kommentierte Beispiele für alle Algorithmen des Kurses stehen in den Dateien `exercises/*/demo_animation.py` (in der Lehrendenversion), z. B. [`exercises/02_bfs_dfs/demo_animation.py`](../exercises/02_bfs_dfs/demo_animation.py).

Kopiere zum Animieren deines Algorithmus die Funktion aus `task.py`, füge wie oben `trace`-Aufrufe ein und gib den `Trace` zurück. So kannst du die einzelnen Schritte deiner Implementierung nachvollziehen.

## 4. Der Zustand: Flags, Beschriftungen, Farben, Variablen

Ein `Trace` hat einen **aktuellen Zustand**. `step()` speichert eine vollständige Kopie davon als `Frame`. Spätere Änderungen verändern bereits aufgenommene Schritte nicht.

| Bestandteil | Methoden | Darstellung |
|---|---|---|
| Flags eines Knotens | `flag(v, *namen)`, `unflag(v, *namen)`, `flags(v)` | Füllung, Rahmen, Leuchten des Knotens |
| Flags einer Kante | `flag_edge(u, v, *namen)`, `unflag_edge(u, v, *namen)`, `edge_flags(u, v)` | Farbe, Dicke, Strichelung der Kante |
| „genau diese“ | `current(v)`, `current_edge(u, v)`, `flag_only(name, knoten)`, `flag_only_edges(name, kanten)` | ein Flag wandert: alle anderen verlieren es |
| Wege | `flag_path(weg, name="path", vertices=True)` | alle Kanten (und Knoten) eines Weges |
| Aufräumen | `clear(*namen)` | Flags von allen Knoten und Kanten entfernen (ohne Namen: alle Flags) |
| Text unter Knoten | `label(v, text)` (`None` entfernt) | z. B. `d = 3`, `#2`, `deg 4` |
| Text auf Kanten | `edge_label(u, v, text)` (`None` entfernt) | ersetzt das Gewicht, z. B. `3/5` |
| Farbklasse | `color(v, wert)` (`None` entfernt) | Füllfarbe aus einer Palette; jeder Wert eine Farbe, Legende automatisch |
| Variablen | `variable(name, wert)`, `remove_variable(name)` | Tabelle in der Seitenleiste |

Wichtige Eigenschaften:

- Ein Knoten kann **mehrere Flags** gleichzeitig haben, z. B. `start` und `visited`. Welches Flag welche Eigenschaft bestimmt, regelt die Priorität der Stile (Abschnitt 6).
- Bei ungerichteten Graphen ist die Richtung einer Kante egal: `flag_edge("A", "B", …)` und `flag_edge("B", "A", …)` meinen dieselbe Kante. Bei gerichteten Graphen muss die Kante in dieser Richtung existieren.
- Unbekannte Knoten oder Kanten führen sofort zu einem `KeyError`. Das deckt Tippfehler auf.
- `variable` speichert den Wert **als Text zum aktuellen Zeitpunkt**. Ändert sich eine Liste danach, muss `variable` erneut aufgerufen werden. Listen, Tupel, Mengen, Wörterbücher und `deque` werden lesbar dargestellt (`[A, B]`, `{A, B}`, `{A: 1}`), Fließkommazahlen ohne `.0`, `math.inf` als `∞`.
- Der `Trace` arbeitet auf einer **Kopie** des Graphen: Spätere Änderungen am Original haben keine Wirkung.

## 5. Eingebaute Flags

Die eingebauten Flags (`lib.trace.DEFAULT_STYLES`) decken die üblichen Zustände ab. Verwende die Flags mit dieser Bedeutung, damit die Animationen des Kurses einheitlich bleiben.

**Knoten**

| Flag | Bedeutung | Darstellung |
|---|---|---|
| `queued` | entdeckt, wartet (Warteschlange, Stapel, Heap) | hellblau, gestrichelter blauer Rahmen |
| `current` | wird gerade bearbeitet | gelb mit orangem Rahmen und Leuchten |
| `visited` | besucht / endgültig | hellgrün, grüner Rahmen |
| `finished` | abgeschlossen (z. B. DFS „schwarz“) | grau |
| `start` | Start / Quelle | violetter, dicker Rahmen |
| `target` | Ziel / Senke | roter, dicker Rahmen |
| `highlight` | hervorgehoben | roter, dicker Rahmen |
| `path` | liegt auf einem Weg | roter, dicker Rahmen |
| `conflict` | Konflikt (z. B. gleiche Farbe benachbart) | rosa mit rotem Rahmen |
| `rejected` | verworfen | rot gestrichelt, blass |
| `inactive` | entfernt / nicht mehr relevant | blass |

**Kanten**

| Flag | Bedeutung | Darstellung |
|---|---|---|
| `current` | wird gerade betrachtet | orange, dick, leuchtend |
| `tree` | Baumkante (BFS-/DFS-Baum, Spannbaum) | grün, dick |
| `path` | Kante eines Weges | rot, dick |
| `matched` | Kante im Matching | violett, dick |
| `flow` | trägt Fluss | blau |
| `saturated` | Fluss = Kapazität | dunkelblau, sehr dick |
| `cut` | Schnittkante | rot gestrichelt, dick |
| `rejected` | verworfen (z. B. würde einen Kreis schließen) | rot gestrichelt, blass |
| `highlight` | hervorgehoben | rot, dick |
| `inactive` | entfernt / nicht mehr relevant | blass |

## 6. Eigene Flags und Stile

Beliebige Namen sind als Flags erlaubt. Ohne eigenen Stil bekommt ein unbekanntes Flag automatisch eine Rahmenfarbe; der Flagname erscheint in der Legende. Schöner ist ein eigener Stil:

```python
trace.style("infiziert", fill="#fecaca", color="#b91c1c", description="infiziert")
trace.style("immun", fill="#e0e7ff", color="#4338ca", dash=True, description="immun")
trace.flag("Bosse", "infiziert")
```

`style()` kann auch eingebaute Flags für einen `Trace` ändern, z. B. `trace.style("visited", fill="#ffffff")`. Die Eigenschaften eines Stils (`lib.trace.Style`):

| Eigenschaft | Wirkung bei Knoten | Wirkung bei Kanten |
|---|---|---|
| `description` | Text in der Legende | Text in der Legende |
| `fill` | Füllfarbe | – |
| `color` | Rahmenfarbe | Linienfarbe |
| `width` | Rahmenbreite | Linienbreite |
| `text` | Schriftfarbe des Namens | – |
| `halo` | Leuchten um den Knoten | Leuchten um die Kante |
| `dash` | gestrichelter Rahmen | gestrichelte Linie |
| `fade` | blass darstellen | blass darstellen |
| `priority` | Vorrang (Standard 50) | Vorrang |

Farben sind CSS-Farben (`"#b91c1c"`, `"crimson"`, `"rgb(200, 0, 0)"`). Hat ein Element mehrere Flags, werden ihre Stile nach `priority` aufsteigend angewandt: Das Flag mit der höchsten Priorität gewinnt bei jeder Eigenschaft, die es selbst festlegt. Beispiel: `current` (Priorität 90) färbt einen Knoten gelb, auch wenn er zugleich `visited` (45) ist; sein violetter `start`-Rahmen (60) wird dabei vom orangen `current`-Rahmen überdeckt, solange er aktuell ist. **Farbklassen gehen bei der Füllung vor:** Hat ein Knoten eine Farbklasse (`color(v, …)`), bestimmt sie immer seine Füllfarbe, damit eine Färbung sichtbar bleibt. Flags wirken dann über Rahmen, Leuchten, Strichelung und Blässe; ein aktueller Knoten behält also seine Farbe und bekommt den orangen Rahmen mit Leuchten.

## 7. Pseudocode, Beschreibung und Nachrichten

```python
trace = Trace(
    graph,
    "Dijkstra ab Katthult",
    description="Dijkstra nimmt immer den Knoten mit dem kleinsten vorläufigen Abstand. "
                "Voraussetzung: keine negativen Kantengewichte.",
    pseudocode=["d[s] = 0; H = [(0, s)]", "solange H nicht leer:", "    (d, u) = H.pop_min()", "..."],
)
trace.step("Katthult hat den kleinsten Abstand (0).", line=3)
```

- `description` erscheint im Abschnitt „About“ der Seitenleiste (Zeilenumbrüche bleiben erhalten).
- `pseudocode` ist eine Liste von Zeilen. `step(…, line=k)` hebt Zeile `k` hervor (ab 1 gezählt). Eine Zeilennummer außerhalb des Pseudocodes löst `ValueError` aus.
- Die **Nachricht** jedes Schritts steht groß über der Seitenleiste.

## 8. Einzelne Bilder: `draw` und `snapshot`

Für Ergebnisse (ein Spannbaum, eine Färbung, ein kürzester Weg) genügt oft ein einzelnes Bild.

```python
from lib.visualization import draw

draw(graph, "Minimaler Spannbaum", highlight_edges=kruskal(graph))
draw(graph, "Färbung", vertex_colors=coloring)
draw(graph, "Abstände", vertex_labels=distance, vertex_flags={"Katthult": ["start"]})
draw(network, "Fluss", edge_labels={(u, v): f"{f}/{c}" for ...}, edge_flags={...: ["saturated"]})
```

`draw(graph, titel, **optionen)` ist eine Abkürzung für `show(snapshot(graph, titel, **optionen))`. `snapshot` erzeugt einen `Trace` mit genau einem Schritt. Seine Optionen:

| Option | Bedeutung |
|---|---|
| `message` | Text in der Seitenleiste |
| `description` | Beschreibung („About“) |
| `highlight_vertices` | Knoten mit dem Flag `highlight` |
| `highlight_edges` | Kanten mit dem Flag `highlight`; Paare `(u, v)` oder `Edge`-Objekte (z. B. direkt das Ergebnis von Kruskal) |
| `vertex_flags` | `{knoten: [flags]}` |
| `edge_flags` | `{(u, v): [flags]}` |
| `vertex_colors` | `{knoten: farbklasse}`, z. B. eine Färbung |
| `vertex_labels` | `{knoten: text}`, z. B. Abstände |
| `edge_labels` | `{(u, v): text}`, z. B. Flüsse |
| `layout`, `left`, `layers`, `shells`, `seed`, `show_weights` | wie bei `Trace` (Abschnitt 10) |

## 9. Mehrere Szenen auf einer Seite

`show` nimmt beliebig viele Szenen: `Trace`-Objekte, Bilder aus `snapshot` und auch einfache Graphen. Jede Szene wird ein Reiter.

```python
show(
    trace_bfs(graph, "A"),
    trace_dfs(graph, "A"),
    snapshot(graph, "Ergebnis", highlight_edges=tree),
    title="Einheit 2: Suche in Graphen",
)
```

So öffnet ein Programm nur **eine** Browserseite statt vieler Fenster.

## 10. Anordnung der Knoten (Layouts)

Die Positionen der Knoten werden einmal pro Szene berechnet (`lib.layout.compute_layout`). Optionen von `Trace` bzw. `snapshot`:

| Option | Wirkung |
|---|---|
| `layout="auto"` (Standard) | 1. Haben alle Knoten das Attribut `pos`, werden diese Koordinaten verwendet. 2. Sonst: `left`/`layers`/`shells`, falls angegeben. 3. Sonst automatisch: Gitter für Knoten `(zeile, spalte)`, Kreis für vollständige Graphen und Kreise, sonst kräftebasiert. |
| `layout="spring"` | kräftebasiert (Fruchterman-Reingold): Kanten ziehen, Knoten stoßen sich ab. Komponenten liegen nebeneinander; mehrere Versuche, der mit den wenigsten Kreuzungen gewinnt. |
| `layout="circular"` | alle Knoten auf einem Kreis |
| `layout="shell", shells=[[…], […]]` | konzentrische Kreise, die erste Liste außen. Petersen-Graph: `shells=[range(5), range(5, 10)]` |
| `layout="bipartite", left=[…]` | zwei Spalten: `left` links, alle anderen rechts |
| `layout="layered", layers=[[…], […], …]` | eine Spalte pro Liste, z. B. BFS-Schichten oder Flussnetzwerke |
| `layout="grid"` | Knoten `(zeile, spalte)` auf einem Gitter |
| `layout={knoten: (x, y)}` | eigene Koordinaten (y nach oben), z. B. eine Landkarte |
| `seed=…` | anderer Zufallsstart für `"spring"` |

Eigene Koordinaten können auch im Graphen stehen:

```python
for ort, (x, y) in POSITIONEN.items():
    graph.add_vertex(ort, pos=(x, y))
draw(graph, "Landkarte")          # nutzt automatisch die pos-Attribute
```

Gefällt die automatische Anordnung nicht, kann man Knoten im Player mit der Maus verschieben.

## 11. Dateien, Browser, Jupyter

- `show(...)` schreibt die Seite in den Ordner `lib.viewer.OUTPUT_DIR` (ein Unterordner `graph-course` im temporären Verzeichnis des Systems) und öffnet sie. Seiten, die älter als drei Tage sind, werden dort automatisch gelöscht.
- `show(..., filename="bfs.html")` schreibt an eine feste Stelle, z. B. um die Datei weiterzugeben. Die Datei enthält alles (Daten, Stil, Programm) und funktioniert ohne Internet.
- `save_html(*szenen, filename=..., title=...)` schreibt nur, ohne zu öffnen.
- **Kein Browser:** `show(..., open_browser=False)` oder die Umgebungsvariable `GRAPH_COURSE_NO_PLOTS=1`. Das ist sinnvoll für automatische Läufe (Tests, CI).
- **Jupyter:** In einem Notebook zeigt `show` den Player direkt unter der Zelle an. Ein `Trace` als letzter Ausdruck einer Zelle wird ebenfalls als Player angezeigt.

## 12. Tipps für gute Animationen

- Nimm ein Bild auf, wenn du einen Knoten entnimmst, eine Kante prüfst oder einen Wert verbesserst. Für eine Animation genügen meist 20 bis 150 Schritte.
- **Nachrichten erklären das Warum:** „d[B] = 7 > 4 + 2: verbessere auf 6“ ist hilfreicher als „Relaxiere B“.
- **Datenstrukturen sichtbar machen:** Warteschlange, Stapel, Heap, Union-Find-Mengen, Matching als `variable`.
- **`current` wandern lassen:** `trace.current(v)` und `trace.current_edge(u, v)` entfernen das Flag automatisch vom vorherigen Element.
- **Kleine Beispiele zuerst:** 5 bis 15 Knoten. Für große Graphen lieber ein einzelnes Ergebnisbild.
- **Zum Schluss zusammenfassen:** Der letzte Schritt nennt das Ergebnis.
- **Feste Seeds** bei Zufallsgraphen, damit die Animation bei jedem Start gleich aussieht.

## 13. Referenz

### `Trace` (`lib.trace`)

```python
Trace(graph, title="", *, description="", pseudocode=None, layout="auto",
      left=None, layers=None, shells=None, seed=0, show_weights=None)
```

| Attribut | Bedeutung |
|---|---|
| `graph` | Kopie des Graphen |
| `title`, `description`, `pseudocode` | wie übergeben |
| `frames` | Liste der aufgenommenen `Frame`s |
| `styles` | `{flagname: Style}`, anfangs eine Kopie von `DEFAULT_STYLES` |
| `len(trace)` | Anzahl der Schritte |

| Methode | Beschreibung |
|---|---|
| `flag(v, *names)` | Flags zu einem Knoten hinzufügen |
| `unflag(v, *names)` | Flags entfernen (ohne Namen: alle) |
| `flags(v) -> set[str]` | aktuelle Flags eines Knotens (Kopie) |
| `flag_edge(u, v, *names)` | Flags zu einer Kante hinzufügen |
| `unflag_edge(u, v, *names)` | Flags einer Kante entfernen (ohne Namen: alle) |
| `edge_flags(u, v) -> set[str]` | aktuelle Flags einer Kante |
| `current(v)` | `v` ist der einzige Knoten mit `current` (`None`: keiner) |
| `current_edge(u, v)` | die einzige Kante mit `current` (`current_edge(None)`: keine) |
| `flag_only(name, vertices)` | genau diese Knoten haben das Flag |
| `flag_only_edges(name, edges)` | genau diese Kanten haben das Flag |
| `flag_path(path, name="path", vertices=True)` | Kanten (und Knoten) eines Weges markieren |
| `clear(*names)` | Flags überall entfernen (ohne Namen: alle) |
| `label(v, text)` | Text unter einem Knoten (`None` entfernt) |
| `edge_label(u, v, text)` | Text auf einer Kante statt des Gewichts (`None` entfernt) |
| `color(v, value)` | Farbklasse (`None` entfernt) |
| `variable(name, value)` | Variable in der Seitenleiste setzen |
| `remove_variable(name)` | Variable entfernen |
| `step(message="", line=None) -> int` | Zustand als neuen Schritt aufnehmen; gibt die Schrittnummer zurück (ab 0) |
| `capture(message="", line=None) -> Frame` | Zustand als `Frame` liefern, ohne ihn aufzunehmen |
| `style(name, **properties)` | Stil eines Flags festlegen oder ändern |

Alle Methoden mit Knoten oder Kanten lösen bei Unbekannten `KeyError` aus; `step` löst bei einer ungültigen Zeilennummer `ValueError` aus.

### `Frame` (`lib.trace`)

Ein unveränderlicher Schnappschuss mit den Feldern `message`, `line`, `vertex_flags`, `edge_flags`, `vertex_labels`, `edge_labels`, `vertex_colors`, `variables` (Paare `(name, text)`). Kanten erscheinen darin als Paar `(u, v)` in der Richtung, in der `graph.edges()` sie liefert.

### `Style`, `DEFAULT_STYLES`, `format_value` (`lib.trace`)

- `Style(description="", fill=None, color=None, width=None, text=None, halo=None, dash=None, fade=None, priority=50)`, siehe Abschnitt 6. `style.as_dict()` liefert die gesetzten Eigenschaften.
- `DEFAULT_STYLES`: Wörterbuch der eingebauten Flags (Abschnitt 5).
- `format_value(value) -> str`: so werden Beschriftungen und Variablen dargestellt.

### Player-Funktionen (`lib.viewer`)

| Funktion | Beschreibung |
|---|---|
| `show(*scenes, title=None, filename=None, open_browser=None) -> Path` | Seite mit einem Reiter pro Szene schreiben und öffnen; Szenen sind `Trace`s oder Graphen |
| `draw(graph, title="", **options) -> Path` | ein einzelnes Bild zeigen; Optionen wie `snapshot`, dazu `filename`, `open_browser` |
| `snapshot(graph, title="", **options) -> Trace` | Trace mit einem Schritt (Abschnitt 8) |
| `save_html(*scenes, filename, title=None) -> Path` | Seite schreiben, nicht öffnen |
| `to_html(scenes, title=None) -> str` | die komplette HTML-Seite als Text |
| `notebook_html(scenes, title=None, height=640) -> str` | `<iframe>` für Jupyter |
| `scene_data(trace) -> dict` | die Daten einer Szene, wie sie an den Player gehen (Abschnitt 14) |

| Konstante | Bedeutung |
|---|---|
| `OUTPUT_DIR` | Ordner für Seiten ohne Dateinamen |
| `NO_PLOTS_ENV_VAR` | `"GRAPH_COURSE_NO_PLOTS"` |
| `PALETTE` | Füllfarben der Farbklassen 0, 1, 2, … |

### Text und Graphviz (`lib.visualization`)

`to_text`, `print_graph`, `to_dot`, `save_dot`: siehe [Testen und Hilfsfunktionen](testen-und-hilfsfunktionen.md#text--und-dot-ausgabe).

## 14. Aufbau und Erweiterung

```text
Algorithmus ──trace.flag/label/step──▶ Trace (lib/trace.py)
                                          │  Frames: vollständige Zustände
                                          ▼
                         scene_data() (lib/viewer.py) ──▶ JSON
                                          │  + Layout (lib/layout.py)
                                          ▼
          HTML-Seite = Vorlage + player.css + player.js + JSON   (lib/viewer_assets/)
                                          │
                                          ▼
                     Browser: SVG-Zeichnung, Steuerung, Seitenleiste
```

- `lib/trace.py` kennt keine Darstellung, nur Zustände. Es lässt sich ohne Browser testen (`tests/test_trace.py`).
- `lib/viewer.py` wandelt Traces in JSON um (`scene_data`) und setzt die Seite aus `lib/viewer_assets/player.css` und `player.js` zusammen.
- `player.js` zeichnet mit SVG ohne fremde Bibliotheken. Ein Schritt im JSON enthält nur die Abweichungen vom Grundzustand: `m` Nachricht, `l` Zeile, `vf`/`ef` Flags von Knoten/Kanten (nach Index), `vl`/`el` Beschriftungen, `vc` Farbklassen, `vars` Variablen.

Erweiterungen:

- **Neue Flags** brauchen keinen Code: `trace.style(...)` oder ein Eintrag in `DEFAULT_STYLES`.
- **Neue Stileigenschaften** werden in `Style` (Python) und in `render()` von `player.js` ergänzt.
- **Neue Layouts** gehören nach `lib/layout.py` und werden in `compute_layout` eingehängt.

## 15. Fehlerbehebung

| Problem | Lösung |
|---|---|
| Es öffnet sich kein Browser. | Ist `GRAPH_COURSE_NO_PLOTS` gesetzt? Der Pfad der Datei ist der Rückgabewert von `show`; die Datei lässt sich auch von Hand öffnen. |
| `KeyError: Vertex 'X' is not in the graph of this trace` | Tippfehler im Knotennamen, oder der Knoten wurde erst nach dem Anlegen des `Trace` zum Graphen hinzugefügt (der `Trace` arbeitet auf einer Kopie). |
| `KeyError: Edge 'u' -- 'v' is not in the graph of this trace` | Bei gerichteten Graphen auf die Richtung achten; bei Residualgraphen die Gegenkante des Originalgraphen markieren. |
| Variablen ändern sich nicht. | Nach jeder Änderung einer Liste erneut `trace.variable(name, liste)` aufrufen. |
| Die Animation hat nur einen Schritt. | `step()` wurde nicht aufgerufen; ohne Schritte zeigt der Player den aktuellen Zustand. |
| Knoten überlappen. | Anderes `seed`, anderes `layout` oder eigene Koordinaten; im Player lassen sich Knoten verschieben. |
| Sehr große Datei, langsamer Player | Weniger Schritte aufnehmen oder kleinere Beispiele wählen; jeder Schritt speichert den kompletten Zustand. |
