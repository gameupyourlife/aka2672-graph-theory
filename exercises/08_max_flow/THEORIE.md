# Theorie zu Einheit 8 - Maximale Flüsse

## 1. Überblick

| Konzept | Dafür brauchst du es |
|---|---|
| Kapazität, Flusserhaltung und Flusswert | Prüfen, wie viel von der Quelle zur Senke transportiert wird |
| Residualnetz und Gegenkanten | Freie Kapazität und rücknehmbaren Fluss darstellen |
| Augmentierender Weg und Engpass | Den Fluss in einem Schritt vergrößern |
| Edmonds-Karp und Breitensuche | Einen maximalen Fluss berechnen |
| Schnitt und Max-Flow-Min-Cut | Die Optimalität prüfen und Engpässe bestimmen |

## 2. Einführung

### Was einen Fluss zulässig macht

Jede gerichtete Kante $u \to v$ hat eine Kapazität $c(u,v) \ge 0$. Der Fluss $f(u,v)$ liegt zwischen 0 und dieser Kapazität. An jedem Knoten außer Quelle $s$ und Senke $t$ kommt insgesamt genauso viel an, wie abfließt. Der Flusswert ist der Nettoabfluss an der Quelle, also ausgehender minus eingehender Fluss. Er ist gleich dem Nettozufluss an der Senke.

### Was noch verändert werden kann

Das Residualnetz zeigt, wie der bisherige Fluss geändert werden kann. Von $u$ nach $v$ kannst du freie Kapazität auf $u \to v$ nutzen oder bestehenden Fluss auf $v \to u$ zurücknehmen. Beides ergibt zusammen die Residualkapazität

$$
c_f(u,v) = c(u,v) - f(u,v) + f(v,u).
$$

Für fehlende Originalkanten sind Kapazität und Fluss 0. Residualkanten gibt es nur bei positiver Residualkapazität. Hat etwa $u \to v$ Kapazität 5 und Fluss 3 und trägt $v \to u$ zusätzlich Fluss 1, dann hat $u \to v$ im Residualnetz Kapazität 3. Erhöhst du entlang dieses Paars um 2, kannst du zuerst die 1 in Gegenrichtung zurücknehmen und dann 1 zur Vorwärtskante addieren. Auch eine reine Rückwärtskante im Residualnetz kann dadurch nützlich sein.

### Augmentieren mit Edmonds-Karp

Ein Weg von $s$ nach $t$ im Residualnetz heißt augmentierender Weg. Sein Engpass ist die kleinste Residualkapazität auf diesem Weg. Um genau diese Menge kannst du den Flusswert erhöhen. An den Zwischenknoten ändert sich der Nettofluss dabei um 0.

Edmonds-Karp wählt in jeder Runde per Breitensuche einen augmentierenden Weg mit möglichst wenigen Kanten. Die Suche beginnt nach jeder Änderung im neuen Residualnetz. Die Wahl nach Kantenzahl unterscheidet Edmonds-Karp von Ford-Fulkerson mit beliebiger Wegwahl.

### Schnitte als Nachweis

Ein $s$-$t$-Schnitt teilt die Knoten in eine Quellseite $S$ mit $s$ und eine Gegenseite mit $t$. Seine Kapazität ist die Summe der **Originalkapazitäten von $S$ nach außen**. Da der Flusswert dem Nettofluss über den Schnitt entspricht, ist jede Schnittkapazität eine obere Schranke für den Flusswert.

Findet die Breitensuche keinen Weg zur Senke mehr, nimm für $S$ alle im Residualnetz von $s$ aus erreichbaren Knoten. Jede Originalkante von $S$ nach außen ist gesättigt und auf Originalkanten nach $S$ hinein fließt nichts. Andernfalls gäbe es eine positive Residualkante nach außen. Der erreichte Flusswert entspricht damit der Kapazität dieses Schnitts. Das ist der Nachweis, dass der Fluss maximal und der Schnitt minimal ist.

Beim Matching als Flussproblem kannst du jede Person und jede Aufgabe nur einmal nutzen, indem du entsprechende Kanten mit Kapazität 1 an Quelle und Senke anschließt. Bei ganzzahligen Kapazitäten bleiben die Augmentierungen ganzzahlig. Jede Einheit Fluss über eine Person-Aufgabe-Kante steht für ein Paar.

[Arbeitsauftrag](README.md) · [Breitensuche](../02_bfs_dfs/THEORIE.md) · [Bipartites Matching](../07_matching/THEORIE.md)
