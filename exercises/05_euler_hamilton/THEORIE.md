# Theorie zu Einheit 5 - Euler- und Hamiltonprobleme

## 1. Überblick

| Konzept | Dafür brauchst du es |
|---|---|
| Kantenzug, Eulerzug und Eulerkreis | Eine Route erkennen, die jede Kante genau einmal verwendet |
| Zusammenhang und Gradparität | Die Existenz von Eulerzügen und Eulerkreisen entscheiden |
| Unterteilung von Kanten | Parallele Brücken mit einem einfachen Graphen modellieren |
| Hamiltonkreis, notwendige und hinreichende Bedingungen | Die Papieraufgaben zu Hamiltonkreisen begründen |
| Hierholzer und Backtracking | Die optionalen Suchfunktionen verstehen |

## 2. Einführung

### Eulerzüge und Eulerkreise

Ein Kantenzug darf einen Knoten mehrfach besuchen. Ein Eulerzug benutzt jede Kante des Graphen genau einmal. Kehrt er zum Start zurück, heißt er Eulerkreis. Betrachte einen ungerichteten Graphen mit mindestens einer Kante. Damit ein Eulerzug existiert, müssen alle Knoten mit positivem Grad in derselben Komponente liegen. Isolierte Knoten spielen dabei keine Rolle.

An jedem inneren Besuch eines Knotens gehören eine Ankunft und ein Abgang zusammen. Bei einem geschlossenen Zug haben daher alle Knoten geraden Grad. Bei einem offenen Zug bleiben genau am Start und am Ziel je eine Kante ohne Gegenstück. Umgekehrt reichen der beschriebene Zusammenhang und genau null oder zwei ungerade Grade für einen Eulerzug aus. Ein Eulerkreis braucht null ungerade Grade. Ein Graph ohne Kanten hat in dieser Übung einen trivialen Eulerzug und Eulerkreis.

Ein Dreieck `A - B - C - A` hat einen Eulerkreis. Hängst du die Kante `A - D` an, werden nur die Grade von `A` und `D` ungerade. Nun gibt es den offenen Eulerzug `D - A - B - C - A`.

Der Satz lässt sich konstruktiv verstehen. Bei geraden Graden kannst du entlang noch unbenutzter Kanten erst am Start stecken bleiben. Solange Kanten übrig sind, kannst du an einem geeigneten Knoten des bisherigen geschlossenen Zugs einen weiteren geschlossenen Zug beginnen und ihn einfügen. Dieses Verfahren heißt **Hierholzer**. Bei zwei ungeraden Knoten kannst du für den Existenzbeweis eine zusätzliche Kante zwischen ihnen denken und nachher aus dem Kreis herausnehmen. In der Suche für einen offenen Eulerzug startest du an einem der beiden ungeraden Knoten.

### Brücken als unterteilte Kanten

Bei der Unterteilung wird aus einer Kante $u-v$ ein Weg $u-x-v$ mit einem neuen Zwischenknoten $x$ vom Grad 2. Die Grade von $u$ und $v$ bleiben gleich. Durch eigene Zwischenknoten lassen sich parallele Brücken im Königsberger Modell voneinander unterscheiden. Überlege bei einem Kantenzug, welche Wahl an einem solchen Zwischenknoten bleibt.

### Hamiltonkreise

Ein Hamiltonkreis besucht jeden Knoten einmal und kehrt zum Start zurück. Der dabei verwendete Kantensatz hat Grad 2 an jedem Knoten. Ein Schnittknoten verhindert einen Hamiltonkreis, denn entfernst du einen Knoten aus einem solchen Kreis, bleibt ein Pfad durch alle übrigen Knoten. In einem bipartiten Graphen wechselt der Kreis bei jeder Kante die Seite. Daher braucht ein Hamiltonkreis gleich viele Knoten auf beiden Seiten.

Beim Zählen von Hamiltonkreisen als Kantenmengen kannst du einen Startknoten festlegen. Ein Kreis hat dann noch zwei Leserichtungen. Beim Petersen-Graphen hilft es, die Speichen als Übergänge zwischen äußerem Kreis und innerem Pentagramm zu betrachten. Ein geschlossener Zug muss so oft hinein- wie hinauswechseln.

Für einen einfachen Graphen mit $n \ge 3$ liefert **Dirac** die hinreichende Bedingung $\deg(v) \ge n/2$ für alle $v$. **Ore** verlangt $\deg(u)+\deg(v) \ge n$ für jedes nicht benachbarte Knotenpaar. Beide Bedingungen garantieren einen Hamiltonkreis. Ein Graph kann auch dann einen Hamiltonkreis haben, wenn er die Bedingungen verfehlt.

### Suche mit Backtracking

Beim Backtracking verlängerst du einen Pfad jeweils um einen bisher unbenutzten Nachbarn. Lässt sich der Pfad nicht mehr ergänzen oder fehlt nach dem letzten Knoten die Rückkante zum Start, nimmst du den letzten Schritt zurück und versuchst die nächste Möglichkeit. Die Zahl der möglichen Pfade kann stark wachsen. Das Verfahren eignet sich vor allem für kleine Graphen.

### Erweiterungen für die Zusatzaufgaben

Im gerichteten Graphen entspricht ein Besuch einer ankommenden und einer abgehenden Kante. Für einen Eulerkreis müssen daher Eingangs- und Ausgangsgrad an jedem Knoten übereinstimmen. Zusätzlich müssen die Knoten mit Kanten zusammenhängen, wenn du die Richtungen ignorierst. Für einen offenen Eulerzug haben Start und Ziel je eine Abweichung um 1 in entgegengesetzter Richtung.

Beim Briefträgerproblem darfst du Kanten mehrfach nutzen. Stell dir jede zusätzliche Benutzung als Kopie der Kante vor. Der entstehende Graph muss einen Eulerkreis haben. Eine zusätzlich durchlaufene Verbindung zwischen zwei ungeraden Knoten ändert die Parität ihrer Grade. An den inneren Knoten des Wegs kommen je zwei Kanten hinzu.

[Arbeitsauftrag](README.md) · [Komplexität der Hamiltonkreissuche](../09_planarity_complexity/THEORIE.md)
