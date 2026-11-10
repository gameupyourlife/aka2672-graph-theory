# Theorie zu Einheit 2 - Breiten- und Tiefensuche

## 1. Überblick

| Konzept | Dafür brauchst du es |
|---|---|
| Wege, Erreichbarkeit und Abstand | Beschreiben, welche Knoten eine Suche liefern soll |
| Warteschlange und Breitensuche (BFS) | Knoten nach Abstand entdecken und kürzeste Wege finden |
| Vorgänger und Suchbaum | Einen gefundenen Weg rekonstruieren |
| Stapel und Tiefensuche (DFS) | Einen Zweig zuerst verfolgen |
| Zusammenhangskomponenten | Einen ungerichteten Graphen in erreichbare Gruppen zerlegen |

## 2. Einführung

### Wege und Abstände

Auf einem Weg sind je zwei aufeinanderfolgende Knoten durch eine Kante verbunden. In einem gerichteten Graphen folgst du dabei der Pfeilrichtung. Die Länge eines ungewichteten Wegs ist seine Kantenzahl. Der Abstand zwischen Start und Ziel ist die kleinste solche Länge. Der Start hat Abstand 0 zu sich selbst. Für ein unerreichbares Ziel gibt es keinen Weg.

### Breitensuche und Schichten

Eine Warteschlange entnimmt das älteste Element zuerst. Entdeckst du einen Nachbarn beim Bearbeiten eines Knotens mit Abstand $d$, so erhält der Nachbar Abstand $d+1$. Die Warteschlange hält diese Schichten in der richtigen Reihenfolge. Alle Knoten mit kleinerem Abstand werden zuerst bearbeitet, daher liefert die erste Entdeckung bereits einen kürzesten Weg.

Speichere bei der Entdeckung auch den Vorgänger, also den Knoten, über den du den Nachbarn erreicht hast. Im Graphen mit `A - B`, `A - C` und `B - D` sind die Schichten ab `A` etwa `[A]`, `[B, C]` und `[D]`. Die Vorgänger führen von `D` über `B` zurück zu `A`. Umgekehrt gelesen ist das der Weg vom Start zum Ziel. Markiere einen Knoten schon beim Einreihen als entdeckt, damit ihn verschiedene Nachbarn nicht mehrfach einreihen.

### Tiefensuche und Stapel

Ein Stapel entnimmt das zuletzt abgelegte Element zuerst. Neu gefundene Nachbarn kommen dadurch vor älteren Alternativen dran. Die Suche folgt einem Zweig, bis sie auf bereits besuchte Knoten oder eine Sackgasse trifft. Die Besuchsreihenfolge hängt von der Nachbarreihenfolge ab. Bei rekursiver DFS übernimmt der Aufrufstapel diese Rolle. Ein langer Pfad kann dabei Pythons Rekursionstiefe überschreiten.

### Komponenten und Aufwand

In einem ungerichteten Graphen bilden alle von einem Start erreichbaren Knoten genau dessen Zusammenhangskomponente. Beginne die nächste Suche an einem noch unbekannten Knoten. Ein isolierter Knoten bildet eine eigene Komponente. Der Kurs zählt den leeren Graphen als zusammenhängend und gibt für ihn keine Komponenten zurück.

Mit Adjazenzlisten, einer Menge für bereits besuchte Knoten und konstantem Aufwand pro Stapel- oder Warteschlangenoperation kosten die Suchen insgesamt $O(|V|+|E|)$. Eine ungerichtete Kante erscheint in zwei Nachbarlisten. Das ändert nur den konstanten Faktor. In Python eignet sich für BFS eine `deque`, bei der du am Anfang mit `popleft()` entnimmst.

[Arbeitsauftrag](README.md)
