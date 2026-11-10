# Theorie zu Einheit 4 – Kürzeste Wege

## 1. Überblick

| Konzept | Dafür brauchst du es |
|---|---|
| Weggewicht und gewichteter Abstand | Routen anhand der Summe ihrer Gewichte vergleichen |
| Relaxation und Dijkstra | Vorläufige Abstände verbessern und endgültig festlegen |
| Prioritätswarteschlange | Den nächsten Knoten mit dem kleinsten Abstand auswählen |
| Vorgänger | Eine kürzeste Route aus dem Suchergebnis rekonstruieren |
| Negative Gewichte und Bellman-Ford | Die Grenzen von Dijkstra verstehen und die optionale Erweiterung lösen |

## 2. Einführung

### Gewichtete Wege

Das Gewicht eines Wegs ist die Summe seiner Kantengewichte. Weniger Kanten bedeuten daher nicht automatisch eine kürzere Route. Kostet `A → C` direkt 7 und kosten `A → B` und `B → C` je 2, ist die Route über `B` kürzer. Haben alle Kanten Gewicht 1, stimmen gewichteter Abstand und Kantenzahl überein. Dann liefert BFS dieselben Abstände.

### Relaxation und endgültige Abstände

Kennst du einen Weg mit Länge $d(u)$ nach $u$, dann bietet eine Kante $u \to v$ mit Gewicht $w(u,v)$ einen Kandidaten der Länge $d(u)+w(u,v)$ für $v$. Ist er besser als der bisherige Abstand, speicherst du die neue Länge und $u$ als Vorgänger. Diese Verbesserung heißt Relaxation.

Dijkstra startet mit Abstand 0 am Start. In jedem Schritt bearbeitet der Algorithmus den noch offenen Knoten mit dem kleinsten bekannten Abstand. Bei nichtnegativen Gewichten ist dieser Abstand endgültig. Denn jeder alternative Weg über einen anderen offenen Knoten muss die Menge der fertig bearbeiteten Knoten irgendwo verlassen. Der Abstand am ersten offenen Knoten auf diesem Weg kann den gerade ausgewählten Abstand nicht unterbieten. Die restlichen Kanten können die Länge nur gleich lassen oder vergrößern.

### Heap und Vorgängerkette

Ein Min-Heap liefert den kleinsten Eintrag, ohne alle offenen Knoten zu durchsuchen. Bei einer Verbesserung kannst du einen neuen Eintrag hinzufügen und den alten später überspringen. Ein eindeutiger Zähler zwischen Abstand und Knoten im Heap-Tupel entscheidet Gleichstände, auch wenn die Knotennamen untereinander nicht vergleichbar sind. Mit dem Heap liegt der Aufwand bei $O((|V|+|E|)\log |V|)$ für $|V| \ge 2$.

Die Vorgänger führen vom Ziel zum Start zurück. Der Start hat keinen Vorgänger. Drehst du die Kette um, erhältst du die Route. Für ein unerreichbares Ziel existiert kein Eintrag. Bei gleich langen Routen reicht eine davon.

### Negative Gewichte und Bellman-Ford

Eine negative Kante kann einen bereits festgelegten Abstand nachträglich verbessern. Deshalb verlangt Dijkstra im Kurs nichtnegative Gewichte im gesamten Graphen. Bellman-Ford verarbeitet auch negative Kanten in gerichteten Graphen. In einer Runde versucht der Algorithmus, jede Kante zu relaxieren, deren Start bereits erreichbar ist. Nach spätestens $|V|-1$ Runden sind alle kürzesten Abstände gefunden, sofern kein negativer Zyklus vom Start aus erreichbar ist. Dann gibt es für jedes erreichbare Ziel einen kürzesten einfachen Weg mit höchstens $|V|-1$ Kanten.

Eine weitere mögliche Verbesserung weist auf einen erreichbaren negativen Zyklus hin. Wiederholtes Durchlaufen dieses Zyklus kann die Weglänge beliebig weit senken. Bei einer ungerichteten Kante mit negativem Gewicht genügt dafür bereits Hin- und Rückweg.

[Arbeitsauftrag](README.md) · [Breitensuche](../02_bfs_dfs/THEORIE.md)
