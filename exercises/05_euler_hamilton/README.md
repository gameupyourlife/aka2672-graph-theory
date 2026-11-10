# Einheit 5 – Euler- und Hamiltonprobleme

Die Programmieraufträge stehen direkt in [`task.py`](task.py).

## Auftrag

1. Implementiere `edges_connected`, `has_euler_circuit` und `has_euler_trail`.
2. Prüfe deine Funktionen am Königsberger Brückenproblem und am Haus vom Nikolaus. Beide Graphen werden in `task.py` aufgebaut.
3. Begründe, für welche $n$ der vollständige Graph $K_n$ einen Eulerkreis hat. Zeige, dass die Unterteilung einer Kante die Existenz eines Eulerkreises nicht ändert.

## Auf Papier

1. Zeige, dass $K_n$ für $n \ge 3$ hamiltonsch ist, und zähle seine Hamiltonkreise als Kantenmengen. Zeige, dass $K_{m,n}$ genau dann hamiltonsch ist, wenn $m = n \ge 2$.
2. Untersuche Hamiltonkreise in den Gittern $3 \times 3$, $2 \times 3$ und $4 \times 4$.
3. Zeige, dass der Petersen-Graph aus `petersen_graph()` keinen Hamiltonkreis hat. Unterscheide die Fälle mit zwei und vier Speichen zwischen dem äußeren Fünfkreis und dem inneren Pentagramm.
4. Nummeriere die Knoten zweier Fünfkreise jeweils von 0 bis 4 und verbinde die Knoten mit gleicher Nummer. Finde im entstandenen Prisma einen Hamiltonkreis und vergleiche seine Gradfolge mit der des Petersen-Graphen.
5. Zeige, dass der Satz von Ore den Satz von Dirac impliziert. Prüfe die Voraussetzungen beider Sätze für $C_n$ mit $n \ge 5$. Untersuche $K_{k,k+1}$ für $k \ge 1$ als Beispiel zur Schärfe der Dirac-Schranke.
6. Entscheide, ob zwei Dreiecke mit genau einem gemeinsamen Knoten einen Hamiltonkreis haben.

## Optional

- Implementiere `find_euler_circuit`, `find_euler_trail` und `find_hamiltonian_cycle`.
- Verbinde in einem zusammenhängenden Graphen einen neuen Knoten mit allen Knoten ungeraden Grades. Begründe, warum das Ergebnis einen Eulerkreis hat.
- Formuliere ein Euler-Kriterium für gerichtete Graphen.
- Vergleiche die Laufzeit der Hamiltonkreissuche auf Gittern $3 \times k$ für ungerades $k$ mit der Laufzeit der Eulerzugsuche auf großen Graphen.
- Bestimme für das Haus vom Nikolaus und für Königsberg, wie viele Kanten bei einer geschlossenen Rundreise über alle Kanten mindestens doppelt benutzt werden müssen. Verwende Kantenlänge 1.
- Baue den Dodekaeder-Graphen nach und finde einen Hamiltonkreis.
