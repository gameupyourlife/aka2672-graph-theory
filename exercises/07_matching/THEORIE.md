# Theorie zu Einheit 7 – Bipartites Matching

## 1. Überblick

| Konzept | Dafür brauchst du es |
|---|---|
| Bipartiter Graph und Matching | Personen und Aufgaben als zulässige Paare modellieren |
| Inklusionsmaximal und größtmöglich | Eine Zuordnung bewerten, die sich nicht direkt erweitern lässt |
| Alternierende und augmentierende Wege | Bestehende Paare umlegen und die Zuordnung vergrößern |
| Satz von Berge und Breitensuche | Begründen, wann die Suche fertig ist |
| Heiratssatz von Hall und Satz von König | Die optionalen Nachweise und die Knotenüberdeckung verstehen |

## 2. Einführung

### Zuordnungen als Kantenmengen

Im bipartiten Graphen verbindet jede Kante einen linken mit einem rechten Knoten. Die Seiten sind in der Übung gegeben. Ein Matching ist eine Auswahl von Kanten, bei der kein Knoten mehr als eine ausgewählte Kante berührt. Für Personen links und Aufgaben rechts bedeutet das höchstens eine Aufgabe pro Person und höchstens eine Person pro Aufgabe. Ein Wörterbuch von links nach rechts speichert die ausgewählten Paare. Die rechten Werte müssen dabei ebenfalls eindeutig sein.

Ein inklusionsmaximales Matching lässt keine einzelne zusätzliche Kante zu. Ein größtes Matching hat unter allen Matchings die meisten Kanten. Stell dir zwei Personen vor. Ada kann Garten oder Küche übernehmen, Ben nur Garten. Die Zuordnung Ada–Garten lässt sich nicht direkt erweitern. Wenn Ada in die Küche wechselt, können beide eine Aufgabe bekommen.

### Alternieren und vergrößern

Ein alternierender Weg wechselt zwischen Kanten außerhalb und innerhalb des Matchings. Ist der Start ein freier linker und das Ende ein freier rechter Knoten, und liegen erste und letzte Kante außerhalb des Matchings, ist der Weg **augmentierend**. Im Beispiel führt er von Ben über Garten und Ada zur Küche. Nimm die bisherigen Matchingkanten auf dem Weg heraus und die anderen hinein. Die inneren Knoten tauschen ihren Partner. Die beiden Enden werden neu zugeordnet und die Größe steigt um 1.

Bei der Suche folgst du von links nach rechts nur Kanten außerhalb des Matchings. Von rechts nach links geht es jeweils nur über die aktuelle Matchingkante zurück. Eine Breitensuche kann an allen freien linken Knoten starten. Erreichst du einen freien rechten Knoten, führen die Vorgänger zum Start zurück. Nach dem **Satz von Berge** ist ein Matching genau dann größtmöglich, wenn es keinen augmentierenden Weg gibt.

### Hall und König

Für eine Teilmenge $S$ der linken Knoten sei $N(S)$ die Menge ihrer rechten Nachbarn. Wenn $|N(S)| < |S|$, reichen die verfügbaren Aufgaben für diese Gruppe nicht aus. Der **Heiratssatz von Hall** besagt, dass es genau dann ein Matching für die gesamte linke Seite gibt, wenn $|N(S)| \ge |S|$ für jede Teilmenge $S$ gilt.

Eine Knotenüberdeckung enthält mindestens einen Endpunkt jeder Kante. Nach dem **Satz von König** hat in bipartiten Graphen eine kleinste Knotenüberdeckung dieselbe Größe wie ein größtes Matching. Für beide optionalen Aufgaben ist die Menge $Z$ der von freien linken Knoten aus alternierend erreichbaren Knoten wichtig. Alle Nachbarn der erreichten linken Knoten sind in $Z$. Über eine Nicht-Matchingkante kannst du sie besuchen. Über eine Matchingkante bist du bereits zum linken Knoten gelangt. Bei einem größten Matching ist jeder erreichte rechte Knoten belegt und sein Partner ist ebenfalls erreichbar. Das erklärt, warum die erreichten linken Knoten bei verbleibenden freien Starts eine Hall-Verletzung zeigen. Für die Überdeckung nimmst du die linken Knoten außerhalb von $Z$ und die rechten Knoten in $Z$.

[Arbeitsauftrag](README.md) · [Graphfärbung und Bipartitheit](../06_graph_coloring/THEORIE.md)
