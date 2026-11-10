# Einheit 9 – Planarität und Komplexität

Die Programmieraufträge stehen direkt in [`task.py`](task.py).

## Auftrag

1. Implementiere `faces_by_euler_formula`, `max_planar_edges`, `has_triangle` und `is_certainly_nonplanar`.
2. Implementiere `hamiltonian_cycle_bruteforce` und `number_of_hamiltonian_cycles_complete`. Prüfe, wie viele Permutationen die Suche beim Petersen-Graphen untersucht.
3. Ersetze die Platzhalter in `COMPLEXITY_CLASSES` durch die passenden Labels.

## Auf Papier

1. Zeichne $K_4$, den Würfelgraphen, ein $2 \times 3$-Gitter und zwei getrennte Dreiecke kreuzungsfrei. Zähle Knoten, Kanten, Flächen und Komponenten und prüfe die Eulersche Formel.
2. Zeige mit den Kantenschranken, dass $K_5$ und $K_{3,3}$ nicht planar sind. Erkläre, welche Schranke du jeweils brauchst.
3. Prüfe beide Kantenschranken für den Petersen-Graphen. Zeige mit dem Satz von Wagner, dass er trotzdem nicht planar ist. Was liefert `is_certainly_nonplanar`?
4. Schätze die Laufzeit der Hamiltonkreissuche bei $10^9$ Permutationen pro Sekunde für $n = 20$ und $n = 25$. Bestimme das größte $n$, das innerhalb eines Tages bearbeitet werden kann. Wiederhole die Rechnung für einen 1000-mal schnelleren Rechner.
5. Gib ein Zertifikat für die Existenz eines Hamiltonkreises an und bestimme den Aufwand der Prüfung. Kennst du ein ebenso kurzes Zertifikat für die Nichtexistenz?
6. Vergleiche den Aufwand, die Existenz eines Eulerkreises und die eines Hamiltonkreises zu entscheiden.

## Optional

- Implementiere `runtime_experiment`. Miss für `range(5, 11)` und vergleiche aufeinanderfolgende Laufzeiten.
- Leite die Kantenschranke $m \le \frac{g}{g-2}(n-2)$ für einen zusammenhängenden planaren Graphen mit kürzester Kreislänge $g$ her und wende sie auf den Petersen-Graphen an.
- Finde im Petersen-Graphen eine Unterteilung von $K_{3,3}$.
- Prüfe, was `is_certainly_nonplanar` für $K_5$ mit zwei isolierten Knoten liefert. Verbessere die Funktion durch eine Zerlegung in Komponenten.
- Vergleiche Brute Force mit Backtracking am Petersen-Graphen.
- Reduziere die Suche nach einem Hamiltonweg zwischen zwei vorgegebenen Knoten auf die Entscheidung, ob ein Hamiltonkreis existiert.
