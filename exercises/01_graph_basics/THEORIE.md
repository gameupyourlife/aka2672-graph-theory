# Theorie zu Einheit 1 – Graphen modellieren

## 1. Überblick

| Konzept | Dafür brauchst du es |
|---|---|
| Knoten, Kanten und Richtung | Wege und Briefverbindungen als Graphen darstellen |
| Grad, Gradfolge und Handschlaglemma | Kanten an ihren Enden zählen und die Gradsumme prüfen |
| Eingangs- und Ausgangsgrad | Empfangene und gesendete Verbindungen getrennt zählen |
| Adjazenzliste und Adjazenzmatrix | Dieselben Kanten in unterschiedlichen Formaten speichern |
| Komplement und Gradfolgen | Die optionalen Aufgaben zu fehlenden Kanten und möglichen Graden bearbeiten |

## 2. Einführung

### Vom Modell zum Graphen

Ein Graph $G = (V,E)$ besteht aus Knoten $V$ und Kanten $E$. Du entscheidest, wofür beide stehen. Eine Straße in beide Richtungen ist eine ungerichtete Kante $\{u,v\}$. Ein Brief von $u$ an $v$ ist eine gerichtete Kante $(u,v)$. Der Rückbrief wäre eine eigene Kante. Die Kursbibliothek verwendet einfache Graphen. Zwischen zwei Knoten gibt es pro Richtung höchstens eine Kante und Schleifen vom Knoten zu sich selbst sind ausgeschlossen. Ein isolierter Knoten gehört trotzdem zu $V$.

### Grade und Handschlaglemma

Der Grad eines Knotens ist im ungerichteten Graphen die Zahl seiner Kanten. Sortierst du alle Grade absteigend, bekommst du die Gradfolge. Im Pfad `A – B – C` mit isoliertem `D` ist sie `[2, 1, 1, 0]`. Jede Kante trägt an beiden Enden je 1 zur Summe bei. Deshalb gilt $\sum_{v \in V}\deg(v) = 2|E|$. Die Summe ist gerade, also muss die Anzahl der ungeraden Summanden gerade sein.

Im gerichteten Graphen zählt der Eingangsgrad ankommende und der Ausgangsgrad abgehende Kanten. Bei `A → B` und `C → B` hat `B` das Paar `(2, 0)`. Addierst du alle Eingangsgrade oder alle Ausgangsgrade, erhältst du jeweils $|E|$.

### Nachbarn und Matrixeinträge

Eine Adjazenzliste speichert zu jedem Knoten seine Nachbarn. Im gerichteten Graphen sind das hier die Ziele seiner ausgehenden Kanten. Eine Adjazenzmatrix reserviert für jedes geordnete Knotenpaar einen Eintrag. In Zeile $i$ und Spalte $j$ steht 1, wenn eine Kante vom $i$-ten zum $j$-ten Knoten führt, sonst 0. Für `A → B` und die Reihenfolge `[A, B]` ist die Matrix `[[0, 1], [0, 0]]`. Bei ungerichteten Graphen ist sie symmetrisch.

### Komplement und mögliche Gradfolgen

Das Komplement behält die Knoten und ergänzt genau die fehlenden Kanten zwischen verschiedenen Knoten. Im vollständigen Graphen gibt es für jedes ungeordnete Knotenpaar eine Kante. Diese Gesamtzahl ist ein Ausgangspunkt für die Kantenzahl im Komplement.

Eine gerade Gradsumme allein reicht bei der Prüfung einer Gradfolge nicht aus. Beim Havel-Hakimi-Verfahren entfernst du den größten Grad $d$, verringerst die nächsten $d$ größten Grade um 1 und sortierst erneut. Fehlen dafür Einträge oder entsteht ein negativer Grad, ist die Folge unmöglich. Erreichst du nur Nullen, ist sie möglich.

[Arbeitsauftrag](README.md) · [Graph-API](../../docs/graph.md)
