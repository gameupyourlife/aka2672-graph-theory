# Theorie zu Einheit 3 - Spannbäume und Kruskal

## 1. Überblick

| Konzept | Dafür brauchst du es |
|---|---|
| Baum, Spannbaum und Spannwald | Die zulässigen Ergebnisse von Kruskal erkennen |
| Gesamtgewicht und Schnitteigenschaft | Begründen, warum günstige Kanten gewählt werden dürfen |
| Disjunkte Mengen und Union-Find | Erkennen, ob eine Kante einen Kreis schließt |
| Pfadkompression, Vereinigung nach Größe und Prim | Die optionalen Verbesserungen und Vergleichsaufgaben bearbeiten |

## 2. Einführung

### Bäume, Wälder und Gewichte

Ein Baum ist zusammenhängend und kreisfrei. Zwischen zwei seiner Knoten gibt es genau einen einfachen Weg. Ein Spannbaum eines Graphen verwendet alle Knoten, aber nur so viele seiner Kanten, wie zum Verbinden nötig sind. Ein Baum mit $n$ Knoten hat $n-1$ Kanten. Bei mehreren Komponenten erhältst du einen Spannwald mit einem Baum pro Komponente. Ein isolierter Knoten zählt als Baum ohne Kanten.

Das Gewicht eines Spannbaums ist die Summe seiner Kantengewichte. Ein minimaler Spannbaum minimiert diese Summe. Negative Gewichte sind erlaubt. Das Ziel unterscheidet sich von einer kürzesten Route zwischen zwei Orten.

### Warum Kruskal günstige Kanten wählen darf

Ein Schnitt teilt die Knoten in zwei Gruppen. Eine Schnittkante verbindet die Gruppen. Wenn keine bisher gewählte Kante den Schnitt kreuzt, kannst du eine leichteste Schnittkante hinzufügen und weiterhin einen minimalen Spannbaum erreichen. Stell dir dazu einen optimalen Baum vor, der die bisher gewählten Kanten enthält. Ist die günstige Kante noch nicht im Baum, entsteht beim Hinzufügen ein Kreis. Auf diesem Kreis kannst du eine andere Schnittkante entfernen. Die Gesamtkosten steigen dabei nicht.

Kruskal betrachtet die Kanten vom kleinsten zum größten Gewicht. Liegen ihre Endpunkte in verschiedenen bisherigen Komponenten, verbindet die Kante sie ohne Kreis. Liegen sie in derselben Komponente, existiert dort bereits ein Weg. Die zusätzliche Kante würde einen Kreis schließen. Bei gleichen Gewichten kann es mehrere gültige Ergebnisse geben.

In einem Dreieck mit Kantengewichten 1, 2 und 4 verbinden die Kanten mit Gewicht 1 und 2 alle Knoten. Die letzte Kante würde nur einen Kreis schließen. Sind alle Kantengewichte eines zusammenhängenden Graphen verschieden, ist sein minimaler Spannbaum eindeutig. Gleiche Gewichte erlauben mehrere Optima, erzwingen sie aber nicht. Für den Vergleich einzelner Kanten hilft die Kreiseigenschaft. Eine eindeutig schwerste Kante auf einem Kreis gehört zu keinem minimalen Spannbaum.

### Wie Union-Find die Komponenten speichert

Zu Beginn bildet jeder Knoten eine eigene Menge. Ein interner Elternzeiger führt von jedem Element zur Wurzel seiner Menge. Die Wurzel zeigt auf sich selbst. `find` bestimmt diese Wurzel, `union` hängt bei verschiedenen Wurzeln eine unter die andere. Zwei Elemente sind genau dann verbunden, wenn sie dieselbe Wurzel haben. Jede erfolgreiche Vereinigung reduziert die Zahl der Mengen um 1.

Bei der Pfadkompression zeigen die bei `find` durchlaufenen Knoten anschließend direkt auf die Wurzel. Bei der Vereinigung nach Größe wird die kleinere Menge unter die größere gehängt. Beide Maßnahmen halten die Wege im internen Wald kurz. Mit diesen Verbesserungen dominiert bei Kruskal neben dem Anlegen der Knoten das Sortieren der Kanten.

### Prim als zweite Strategie

Prim beginnt an einem Startknoten und vergrößert einen einzelnen Baum. In jedem Schritt nimmt der Algorithmus die leichteste Kante, die vom aktuellen Baum zu einem noch unbesuchten Knoten führt. Ein Heap hält die Kandidaten bereit. Ist kein Kandidat mehr verfügbar, ist der Spannbaum für die Komponente des Starts vollständig.

[Arbeitsauftrag](README.md)
