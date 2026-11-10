# Theorie zu Einheit 10 - Das Netzwerk von Nangijala

## 1. Überblick

| Modul | Benötigte Konzepte | Dafür brauchst du sie |
|---|---|---|
| A - Modellierung | Ungerichteter gewichteter Graph, Handschlaglemma und Knotenlöschung | Straßennetz aufbauen und Sperrungen abbilden |
| B - Erreichbarkeit | Graphsuche, Komponenten und Schnittknoten | Folgen von Ortssperrungen untersuchen |
| C - Winterwege | Minimaler Spannbaum oder Spannwald | Ein günstiges Netz aus geräumten Straßen auswählen |
| D - Schnellste Wege | Kürzester gewichteter Weg und Vorgängerkette | Eine einzelne Route mit minimaler Reisezeit bestimmen |
| E - Laternenfarben | Knotenfärbung und untere Schranken | Benachbarte Orte unterscheiden und die Farbanzahl begründen |
| F - Aufgabenverteilung | Bipartites Matching und Heiratssatz von Hall | Aufgaben möglichst vielen Personen zuordnen |
| G - Nachschub | Gerichtete Kapazitäten, maximaler Fluss und minimaler Schnitt | Transportmenge und Engpässe bestimmen |

## 2. Einführung

### A - Das Modell wählen

Ein Ort ist ein Knoten. Eine in beide Richtungen gleich schnell nutzbare Straße ist eine ungerichtete Kante mit der Reisezeit als Gewicht. Mit dem Handschlaglemma kannst du prüfen, ob die Summe der Grade doppelt so groß ist wie die Kantenzahl. Bei der Sperrung eines Orts löschst du diesen Knoten und alle angrenzenden Kanten in einer Kopie. So kannst du verschiedene Sperrungen mit demselben Ausgangsnetz vergleichen. Braucht jede Richtung eine eigene Reisezeit, modellierst du beide Fahrtrichtungen getrennt. [Graphen modellieren](../01_graph_basics/THEORIE.md)

### B - Erreichbarkeit und Schnittknoten

Breiten- oder Tiefensuche bestimmt alle Orte, zu denen es vom Start einen Weg gibt. Um die Auswirkung einer Sperrung auf das gesamte Netz zu beurteilen, vergleichst du die Anzahl der Komponenten vor und nach dem Löschen des Orts. Nimmt sie zu, ist der Ort ein Schnittknoten. Im einfachen Pfad `A - B - C` trifft das auf `B` zu. Bei einer kritischen Straße entfernst du stattdessen die Kante. Eine Kante, deren Entfernung die Zahl der Komponenten erhöht, heißt Brücke. [Breiten- und Tiefensuche](../02_bfs_dfs/THEORIE.md)

### C und D - Gesamtnetz und einzelne Route

Beim Räumen geht es um das **Gesamtgewicht aller ausgewählten Straßen**. Ein minimaler Spannbaum hält eine zusammenhängende Komponente mit der kleinstmöglichen Summe verbunden. Gibt es mehrere Komponenten, liefert Kruskal einen minimalen Spannwald. Eine auf einem Kreis eindeutig schwerste Kante kannst du aus jedem minimalen Spannbaum ausschließen. Das hilft bei der Begründung, ob ein Ergebnis eindeutig ist. [Spannbäume und Kruskal](../03_spanning_trees/THEORIE.md)

Bei der schnellsten Route geht es um die **Summe auf einem bestimmten Weg**. Im Dreieck mit Reisezeiten 3 für `A - B`, 3 für `B - C` und 5 für `A - C` verwendet der Spannbaum die ersten beiden Straßen. Im gesamten Netz ist die direkte Fahrt von `A` nach `C` trotzdem schneller. Dijkstra arbeitet auf dem für die jeweilige Sperrung verbleibenden Netz und setzt nichtnegative Reisezeiten voraus. [Kürzeste Wege](../04_shortest_paths/THEORIE.md)

### E - Farben zuordnen und begründen

Jede Kante steht für einen Konflikt zwischen zwei Laternen, die verschiedene Farben brauchen. Greedy liefert eine gültige Färbung, deren Farbanzahl von der Knotenreihenfolge abhängen kann. Für eine optimale Farbanzahl brauchst du zusätzlich eine untere Schranke. Schon ein ungerader Kreis schließt zwei Farben aus. Findest du zugleich eine gültige Färbung mit drei Farben, ist sie damit optimal. [Graphfärbung](../06_graph_coloring/THEORIE.md)

### F - Personen und Aufgaben verbinden

Lege Personen auf die linke und Aufgaben auf die rechte Seite des bipartiten Graphen. Eine Kante bedeutet, dass eine Person für eine Aufgabe qualifiziert ist. Ein größtes Matching maximiert die Zahl der zugeordneten Personen. Möchtest du begründen, dass nicht alle eine Aufgabe bekommen können, suche nach einer Personengruppe mit weniger verfügbaren Aufgaben als Personen. Nach Hall genügt eine solche Gruppe als Nachweis. [Bipartites Matching](../07_matching/THEORIE.md)

### G - Kapazitäten als Transportgrenzen

Die Nachschubrouten sind gerichtete Kanten. Ihr Gewicht steht hier für Säcke pro Nacht, also eine Kapazität. An Zwischenorten gilt Flusserhaltung. Ein maximaler Fluss kann mehrere Routen gleichzeitig nutzen. Der zugehörige minimale Schnitt zeigt, welche Vorwärtskanten zwischen Quellseite und Gegenseite zusammen die Transportmenge begrenzen. [Maximale Flüsse](../08_max_flow/THEORIE.md)

[Arbeitsauftrag](README.md)
