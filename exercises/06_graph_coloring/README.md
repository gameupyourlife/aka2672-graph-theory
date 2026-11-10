# Einheit 6 - Graphfärbung

Die Programmieraufträge stehen direkt in [`task.py`](task.py).

## Auftrag

1. Implementiere `number_of_colors`, `is_valid_coloring` und `greedy_coloring`.
2. Prüfe mit den Beispielen in `task.py`, wie viele Tische Pippis Gäste brauchen. Begründe, warum weniger Tische nicht ausreichen. Vergleiche die beiden Greedy-Färbungen des Pfads.
3. Prüfe mit `is_bipartite` per Breitensuche, ob der Graph zweifärbbar ist.

## Auf Papier

1. Beweise die Greedy-Schranke $\Delta + 1$, indem du für jeden Knoten nur seine zuvor gefärbten Nachbarn zählst.
2. Bestimme die chromatische Zahl von $K_n$, $C_n$, $K_{m,n}$ und Bäumen. Begründe jeweils, dass keine kleinere Färbung möglich ist.
3. Entferne aus $K_{n,n}$ alle Kanten $a_i b_i$. Zeige für den so entstehenden Kronengraphen, dass Greedy in der Reihenfolge $a_0, b_0, a_1, b_1, \dots$ jedem Paar $a_i, b_i$ die Farbe $i$ gibt. Finde eine Reihenfolge mit zwei Farben.
4. Beweise, dass Greedy eine optimale Färbung findet, wenn du die Knoten nach den Farben einer optimalen Färbung sortierst.
5. Zeige, dass jeder geschlossene Kantenzug ungerader Länge einen ungeraden Kreis enthält. Verwende das Lemma im Beweis, dass ein Graph genau dann bipartit ist, wenn er keinen ungeraden Kreis enthält.
6. Finde im Petersen-Graphen einen ungeraden Kreis und eine 3-Färbung.

## Optional

- Implementiere `welsh_powell_order` und `find_odd_cycle`.
- Vergleiche auf `random_graph(50, 0.2, seed=s)` die Standardreihenfolge, die Welsh-Powell-Reihenfolge und 100 zufällige Reihenfolgen.
- Berechne für kleine Graphen die chromatische Zahl durch Ausprobieren und vergleiche mit Greedy. Zähle die möglichen Färbungen mit $k$ Farben für $n$ Knoten.
- Berechne für Petersen-Graph und Stern die Welsh-Powell-Schranke $\max_i \min\{\deg(v_i) + 1, i\}$ in absteigender Gradreihenfolge.
- Modelliere einen Stundenplan für fünf Kurse als Färbungsproblem. Kurse mit gemeinsamen Teilnehmenden dürfen sich zeitlich nicht überschneiden.
- Konstruiere einen zusammenhängenden Graphen, der weder vollständig noch ein ungerader Kreis ist und bei ungünstiger Reihenfolge $\Delta + 1$ Greedy-Farben braucht. Vergleiche das Ergebnis mit dem Satz von Brooks.
