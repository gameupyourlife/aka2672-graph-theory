# Theorie zu Einheit 9 – Planarität und Komplexität

## 1. Überblick

| Konzept | Dafür brauchst du es |
|---|---|
| Planare Einbettung und Flächen | Die Eulersche Formel auf Zeichnungen anwenden |
| Kantenschranken und Dreiecke | Nichtplanarität in bestimmten Fällen nachweisen |
| Minoren und Unterteilungen | Nichtplanarität nachweisen, wenn die Kantenschranken die Frage offenlassen |
| Permutationen und Fakultät | Hamiltonkreise suchen, zählen und die Laufzeit abschätzen |
| Zertifikate, P, NP und Reduktionen | Die Probleme in `COMPLEXITY_CLASSES` einordnen |

## 2. Einführung

### Ebene Zeichnungen und Flächen

Ein Graph ist **planar**, wenn er sich in der Ebene so zeichnen lässt, dass Kanten sich nur an gemeinsamen Endpunkten treffen. Eine solche Zeichnung ist eine ebene Einbettung. Ihre Kanten teilen die Ebene in Flächen. Die unbeschränkte Außenfläche zählt mit. Für $n$ Knoten, $m$ Kanten, $f$ Flächen und $c$ Zusammenhangskomponenten gilt

$$
n - m + f = 1 + c.
$$

Ein gezeichnetes Dreieck hat $n=3$, $m=3$, $c=1$ und zwei Flächen. Entfernst du eine Kante auf einem Kreis, verschmelzen zwei Flächen und der Zusammenhang bleibt erhalten. Wiederholst du das bis zum Spannwald, bleibt nur die Außenfläche. Damit lässt sich die Formel begründen.

### Kantenschranken und ihre Grenzen

Für einen einfachen zusammenhängenden planaren Graphen mit $n \ge 3$ zählen alle Flächenränder zusammen $2m$ Kantenauftritte. Eine Brücke zählt auf beiden Seiten, auch wenn diese zur selben Fläche gehören. Jeder Rand hat mindestens drei Kantenauftritte, also $3f \le 2m$. Zusammen mit der Eulerschen Formel folgt $m \le 3n-6$. Ist der Graph dreiecksfrei, braucht jeder Rand mindestens vier Auftritte und die Schranke verschärft sich zu $m \le 2n-4$. Die Schranken gelten auch für unzusammenhängende Graphen mit $n \ge 3$. In einer ebenen Zeichnung kannst du getrennte Komponenten mit Brücken verbinden, ohne Dreiecke zu erzeugen.

Eine Verletzung beweist Nichtplanarität. Sind beide Schranken erfüllt, bleibt die Entscheidung offen. Für ein Dreieck kannst du bei jeder Kante prüfen, ob ihre Endpunkte einen gemeinsamen Nachbarn haben. Für die optionale Schranke über die kürzeste Kreislänge nutzt du in einem zusammenhängenden Graphen mit mindestens einem Kreis eine entsprechend größere Mindestlänge pro Flächenrand.

Ein **Minor** entsteht durch Löschen von Knoten oder Kanten und durch Kontrahieren von Kanten, also Zusammenziehen ihrer Endpunkte. Nach dem Satz von Wagner ist ein Graph genau dann planar, wenn er weder $K_5$ noch $K_{3,3}$ als Minor enthält. Eine **Unterteilung** ersetzt Kanten durch Wege mit eigenen inneren Knoten. Nach dem Satz von Kuratowski genügt für Nichtplanarität auch der Nachweis einer Unterteilung eines dieser beiden Graphen als Teilgraph.

### Permutationen und Suche

Bei der Suche nach einem Hamiltonkreis kannst du einen Startknoten festlegen und die Reihenfolgen der anderen $n-1$ Knoten durchgehen. Prüfe dabei auch die Rückkante zum Start. Gibt es keinen Hamiltonkreis, untersucht diese Variante $(n-1)!$ Kandidaten. Ein Kandidat kostet bei konstanten Kantenabfragen bis zu $O(n)$ Zeit. Im vollständigen Graphen ergibt jede Reihenfolge einen Kreis. Beim Zählen nach Kantenmengen beschreiben die beiden Leserichtungen denselben Kreis.

Für eine Laufzeitschätzung teilst du die Zahl der Kandidaten durch die pro Sekunde prüfbare Anzahl. Gehst du von $n$ auf $n+1$ Knoten, wächst die Kandidatenzahl um den Faktor $n$. Ein schnellerer Rechner verschiebt deshalb die praktikable Grenze nur begrenzt.

### Entscheidung, Zertifikate und Reduktionen

Ein Entscheidungsproblem stellt eine Ja-Nein-Frage. **P** umfasst die Entscheidungsprobleme, die sich in Polynomialzeit lösen lassen. **NP** umfasst die Entscheidungsprobleme, deren Ja-Instanzen ein Zertifikat von polynomialer Länge haben, das sich in Polynomialzeit prüfen lässt. Zum Beispiel ist eine Liste benachbarter Knoten ein Zertifikat dafür, dass ein Ziel erreichbar ist. Du kannst die Liste Schritt für Schritt prüfen.

Bei einer polynomialen Reduktion übersetzt du Instanzen eines Problems in Instanzen eines anderen und erhältst dabei die Ja-Nein-Antwort. Ein Problem ist **NP-schwer**, wenn sich jedes Problem aus NP darauf reduzieren lässt. Liegt es zusätzlich selbst in NP, ist es **NP-vollständig**. Das Finden einer optimalen Lösung und die Frage, ob eine Lösung einen vorgegebenen Grenzwert erreicht, sind unterschiedliche Problemformen. Ordne die Aufgaben im Kurs unter der Annahme $P \ne NP$ ein. Hier steht `P` auch für in Polynomialzeit lösbare Such- und Optimierungsaufgaben. Verwende `NP-schwer` für die schweren Aufgaben, die hier keine Entscheidungsprobleme in NP sind.

[Arbeitsauftrag](README.md) · [Euler- und Hamiltonprobleme](../05_euler_hamilton/THEORIE.md)
