# Einheit 10 - Das Netzwerk von Nangijala

Die Programmieraufträge stehen direkt in [`task.py`](task.py).

## Auftrag

Bearbeite mit deiner Gruppe Modul A und mindestens zwei der Module B bis F. Modul G ist optional. Verwende die vorbereiteten Daten aus `nangijala_data.py` und deine Algorithmen aus den früheren Einheiten. Stelle eure Ergebnisse in zehn Minuten vor und begründe, warum die Voraussetzungen der eingesetzten Algorithmen erfüllt sind.

| Modul | Auftrag |
|---|---|
| A - Modellierung | Implementiere `build_network` und `without_places`. Zeichne das Straßennetz, prüfe das Handschlaglemma und beschreibe, was das Modell vereinfacht. |
| B - Erreichbarkeit | Implementiere `reachable_places` und `critical_places`. Sperre Bärenpass und Adlerhorst und prüfe, welche Orte vom Reiterhof erreichbar bleiben. Ermittle die Schnittknoten und untersuche, wie eine neue Straße helfen könnte. |
| C - Winterwege | Bestimme mit `winter_roads` einen minimalen Spannwald. Begründe die Eindeutigkeit im Beispiel und vergleiche den Weg vom Reiterhof zur Rebellenhöhle im Spannbaum mit dem schnellsten Weg im ganzen Netz. |
| D - Schnellste Wege | Implementiere `fastest_route`. Bestimme den schnellsten Weg vom Reiterhof zu Tengils Burg und den zum Marktplatz bei gesperrtem Bärenpass und Waldsee. Überlege, wie du Einbahnstraßen modellierst. |
| E - Laternenfarben | Vergleiche mit `lantern_colors` mindestens zwei Greedy-Reihenfolgen. Begründe, warum zwei Farben nicht reichen, und suche eine 3-Färbung. |
| F - Aufgabenverteilung | Weise mit `assign_tasks` möglichst vielen Personen eine passende Aufgabe zu. Begründe mit dem Heiratssatz von Hall, warum nicht alle sieben Personen eine bekommen. |
| G - Nachschub | Berechne mit `max_supply` den maximalen Nachschub zwischen den Tälern. Bestimme einen minimalen Schnitt und benenne die Engpässe. |

## Optional

- Finde mit einer eigenen Funktion `critical_roads` alle Straßen, deren Sperrung das Netz zerlegt.
- Prüfe, ob eine Rundreise jede Straße genau einmal nutzen kann. Ermittle gegebenenfalls, welche Straßen du verdoppeln musst.
- Miss die Laufzeit von `critical_places` für wachsende Zufallsgraphen.
- Ergänze eigene Orte und untersuche, wie sich die Ergebnisse ändern.
- Untersuche die Planarität des Straßennetzes.
