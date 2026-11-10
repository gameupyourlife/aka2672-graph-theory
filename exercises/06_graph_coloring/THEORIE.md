# Theorie zu Einheit 6 - Graphfärbung

## 1. Überblick

| Konzept | Dafür brauchst du es |
|---|---|
| Gültige Knotenfärbung und chromatische Zahl | Eine Färbung prüfen und von einer optimalen Färbung unterscheiden |
| Greedy und Knotenreihenfolge | Färbungen erzeugen und unterschiedliche Ergebnisse erklären |
| Bipartitheit und ungerade Kreise | Mit Breitensuche die Zweifärbbarkeit prüfen |
| Welsh-Powell und BFS-Vorgänger | Die optionalen Aufgaben zur Reihenfolge und zum Kreis lösen |

## 2. Einführung

### Gültige Färbungen und Beweise zur Farbanzahl

Eine Knotenfärbung ordnet jedem Knoten eine Farbe zu. Sie ist gültig, wenn die beiden Endpunkte jeder Kante verschiedene Farben haben. Im Kurs stehen ganze Zahlen ab 0 für die Farben. Für die Anzahl der Farben zählt die Menge der benutzten Werte. Die Nummer der größten Farbe spielt dabei keine Rolle.

Die **chromatische Zahl** $\chi(G)$ ist die kleinste Zahl von Farben, mit der sich $G$ gültig färben lässt. Eine gültige Färbung mit $k$ Farben gibt eine obere Schranke. Eine Gruppe von $r$ paarweise benachbarten Knoten gibt eine untere Schranke von $r$. Fallen obere und untere Schranke zusammen, kennst du die chromatische Zahl.

### Greedy und die Wahl der Reihenfolge

Greedy färbt die Knoten nacheinander. Jeder Knoten bekommt die kleinste Farbe, die bei seinen bereits gefärbten Nachbarn noch frei ist. Hat er $d$ bereits gefärbte Nachbarn, können diese höchstens $d$ Farben blockieren. Unter den Zahlen 0 bis $d$ bleibt also eine frei. Mit maximalem Knotengrad $\Delta$ ergibt sich die Schranke von $\Delta+1$ Farben.

Die Reihenfolge legt fest, welche Farben schon blockiert sind. Betrachte den Pfad `A - B - C - D - E`. In Pfadreihenfolge wechselt Greedy zwischen 0 und 1. In der Reihenfolge `A, D, B, C, E` bekommen `A` und `D` zuerst beide 0. `B` bekommt 1, weil `A` schon gefärbt ist. Für `C` sind dann beide Farben blockiert, also bekommt er Farbe 2.

Bei Welsh-Powell kommen Knoten mit hohem Grad zuerst. Für die zugehörige Schranke kombinierst du zwei Beobachtungen. Der $i$-te Knoten hat höchstens $\deg(v_i)$ Nachbarn und höchstens $i-1$ bereits gefärbte Knoten vor sich. Für eine optimale Reihenfolge ist eine andere Idee hilfreich. Wenn du eine optimale Färbung schon kennst, kannst du ihre Farbklassen nacheinander abarbeiten.

### Zweifärbbarkeit und ungerade Kreise

Ein Graph ist bipartit, wenn du seine Knoten in zwei Seiten teilen kannst und jede Kante zwischen den Seiten verläuft. Die Seiten entsprechen den beiden Farben. Auf einem Kreis muss die Farbe bei jeder Kante wechseln. Ein Kreis ungerader Länge führt damit zu einem Widerspruch.

Starte für die umgekehrte Richtung eine Breitensuche in jeder Komponente. Ordne jeder BFS-Schicht eine Farbe nach ihrer Parität zu. Haben die Enden einer Kante dieselbe Farbe, verbinden sie in einer BFS Knoten derselben Tiefe, denn benachbarte Knoten unterscheiden sich um höchstens eine Schicht. Folge von beiden Enden den Vorgängern bis zum ersten gemeinsamen Knoten. Die beiden gleich langen Zweige und die Konfliktkante bilden einen ungeraden Kreis. Ohne Konflikt liefert die Schichtfärbung eine gültige Zweifärbung.

Für die Papieraufgabe zu geschlossenen Kantenzügen kannst du einen wiederholten inneren Knoten als Trennstelle verwenden. Die beiden geschlossenen Teilzüge haben zusammen die ursprüngliche Länge. Ist sie ungerade, hat auch einer der Teilzüge ungerade Länge.

Der Satz von Brooks aus der Zusatzaufgabe handelt von der chromatischen Zahl. Ein zusammenhängender einfacher Graph, der weder vollständig noch ein ungerader Kreis ist, ist mit höchstens $\Delta$ Farben färbbar. Bei einer fest vorgegebenen Greedy-Reihenfolge kann der Algorithmus trotzdem mehr Farben benötigen.

[Arbeitsauftrag](README.md) · [Breitensuche](../02_bfs_dfs/THEORIE.md)
