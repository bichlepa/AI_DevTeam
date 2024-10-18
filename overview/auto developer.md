Die Software Auto Developer soll fast den gesamten Entwicklungsprozess von Software mit Hilfe von KI automatisieren. Dabei sollen neben einem gut dokumentierten Quellcode auch eine vollständige Anforderungsdefinition, Dokumentation und Testfälle mit erzeugt werden (gemäß V-Modell) Und es soll auch mit großen Projekten arbeiten können.

## Anforderungen
- Die Software soll basierend auf den Benutzeingaben eine Anforderungsdefinition erstellen.
- Die Software soll eine Projektübersicht erstellen.
- Die Software soll eine Architekturspezifikation erstellen.
- Die Software soll Modulanforderungen aus der Anforderungsdefinition ableiten.
- Die Software soll Spezifikationen für die Module und deren Schnittstellen erstellen.
- Die Software soll den Quellcode für die Module generieren.
- Die Software soll Testfälle erstellen auf allen Ebenen des V-Modells.
- Die Software soll Testpläne erstellen.
- Die Software soll die Traceability zwischen den Artefakten sicherstellen.
- Die Software soll dem Benuzter die Möglichkeit geben, Änderungen auf allen Ebenen vorzunehmen.
- Die Software soll bei allen Änderungen die anderen Artefakte anpassen.
- Die Software soll dem Benuzter erlauben, für jeden Schritt die gewünschte KI (Anbieter und Modell) auszuwählen.
- Die Software soll dem Benutzer die Möglichkeit geben, die KI-Prompts zu bearbeiten, ohne den Queellcode zu ändern.
- Die Software soll durch eine Benutzeroberfläche bedienbar sein.
- Die Software soll in einem CI/CD-Prozess integrierbar sein.

Qualitätsanforderungen:
- Die Software soll mit großen Projekten arbeiten können.
- Die Software soll gut wartbar sein. Insbesondere sollen einfache Änderungen, wie KI-Prompts, leicht anpassbar sein.
- Die Software soll die gesamte Interaktion mit der KI nachvollziehbar machen.


## User Stories
- Wenn ich die Software zum ersten Mal verwende, möchte ich die Konfiguration auf unkomplizierte Weise anpassen können.
- Ich möchte beliebige Änderungswünsche an den Artefakten eingeben können, die dann von der Software umgesetzt werden.
- Ich möchte Bugs in den Artefakten melden können, die dann von der Software behoben werden.
- Wenn bei der Abarbeitung meines Änderungswunsches die KI nicht weiterkommt, weil sie nicht genug Informationen hat, möchte ich die fehlenden Informationen eingeben können.
- Ich möchte, dass wenn mein Änderungswunsch eindeutig ist, die Software die Änderungen automatisch durchführt.
- Ich möchte bei Bedarf die Ausführung schrittweise stoppen und die Prompts sowie die Änderungen an den Artefakten überprüfen können.
- Ich möchte im Fehlerfall einen genauen Fehlerbericht erhalten, um den Fehler beheben zu können.
- Ich möchte die Software jederzeit beenden können und sie soll beim nächsten Start an der Stelle weitermachen, an der sie beendet wurde.

### Abläufe bei bestimmten User Stories bei bestimmten Bedingungen
Fall 1: Der Benutzer verwendet die Software an einem leeren Projekt.
- Der Benutzer startet die Software.
- Die Software erkennt, dass das Projekt leer ist und fragt den Benutzer nach Informationen zum Projekt.
- Die Software erzeugt die Projektübersicht. Bei Bedarf fragt die Software den Benutzer nach weiteren Informationen.
- Die Software erzeugt die Anforderungsdefinition. Sie fragt den Benutzer nach weiteren Informationen, aus denen sie die Anforderungsdefinition ableiten kann.
- Die Software erzeugt die Architekturspezifikation. Bei wichtigen Architekturentscheidungen fragt die Software den Benutzer nach seiner Meinung.
- Die Software erzeugt die Modulanforderungen.
- Die Software erzeugt die Spezifikationen für die Module und deren Schnittstellen.
- Die Software erzeugt den Quellcode für die Module.
- Die Software erzeugt die Testfälle.
- Die Software erzeugt die Testpläne.
- Die Software stellt die Traceability sicher.

Fall 2: Der Benutzer möchte Änderungen an den Artefakten vornehmen.
- Der Benutzer startet die Software.
- Die Software erkennt, dass ein Projekt vorhanden ist und bietet eine Auswahl an Aktionen. Der Benutzer wählt "Änderungen vornehmen".
- Die Software bewertet, welche Artefakte von den Änderungen betroffen sein können.
- Die Software durchläuft den gesamten Entwicklungsprozess ab dem Schritt, der von den Änderungen betroffen ist.
- Die Software führt die Änderungen durch und stellt die Traceability sicher.

Fall 3: Der Benutzer möchte einen Bug melden.
- Der Benutzer startet die Software.
- Die Software erkennt, dass ein Projekt vorhanden ist und bietet eine Auswahl an Aktionen. Der Benutzer wählt "Bug melden".
- Die Software bewertet, welche Artefakte von dem Bug betroffen sein können.
- Die Software analysiert den Bug und sucht nach der Ursache. Sie fragt den Benutzer nach weiteren Informationen, wenn sie nicht weiterkommt.
- Wenn die Software den Fehler findet, führt sie die Änderungen durch und stellt die Traceability sicher.

Fall 4: Der Benutzer beendet die Software während der Ausführung.
- Der Benutzer startet die Software.
- Die Software erkennt, dass ein Projekt vorhanden ist und die vorherige Ausführung nicht abgeschlossen wurde. Sie bietet dem Benutzer an, die vorherige Ausführung fortzusetzen oder eine neue Ausführung zu starten.
- Der Benutzer wählt "vorherige Ausführung fortsetzen".
- Die Software führt die vorherige Ausführung fort.


## Architektur

### Ablauf
Die KI wird folgendermaßen eingesetzt:
- Es werden unterschiedliche Agenten mit der jeweiligen Rolle für die KI definiert, die sich für unterschiedliche Aufgaben eignen.
  - Projektleiter: Der Projektleiter koordiniert die gesamte Entwicklung. Er überlegt sich, in welchen Schritten eine Aufgabe abgearbeitet werden soll und übergibt die Teilaufgaben an geeignete Agenten.
  - Anforderungsmanager: Der Anforderungsmanager erstellt die Anforderungsdefinition.
  - Architekt: Der Architekt erstellt die Architekturspezifikation.
  - Entwickler: Der Entwickler erstellt die Modulanforderungen, Spezifikationen, Quellcode und Testfälle.
  - Tester: Der Tester erstellt die Testpläne.
  - Reviewer: Der Reviewer stellt die Traceability und die Konsistenz der Artefakte sicher.
Bei jeder Benutzereingabe entscheidet der Projektleiter, welcher Agent aktiv wird, und formuliert eine Aufgabenbeschreibung. Diese wird an den Agenten weitergegeben, der dann die Aufgabe bearbeitet und am Ende ein Bericht über das Ergebnis schreibt. Der Projektleiter liest den Bericht und entscheidet, ob die Aufgabe abgeschlossen ist oder ob ein weiterer Agent aktiv werden soll.



### Komponenten

Die Software wird in Python geschrieben und in mehrere Module aufgeteilt. Die Module sind:
- config: Konfiguration der Software (Angaben zur KI, Projektpfaden, etc.)
- main: Hauptmodul, das die Benutzeroberfläche bereitstellt und die Benutzereingaben verarbeitet, sowie ermittelt, ob das Projekt existiert und welche Artefakte bereits erstellt wurden.
- ai: Ruft die KI-Agenten auf (zu Beginn den Projektleiter), und koordiniert sie.
- ai/base: Basisklasse für die KI-Agenten.
- ai/project_manager: Projektleiter, der die KI-Agenten koordiniert.
- ai/requirements_manager: Anforderungsmanager, der die Anforderungsdefinition erstellt.
- ai/architect: Architekt, der die Architekturspezifikation erstellt.
- ai/developer: Entwickler, der die Modulanforderungen, Spezifikationen, Quellcode und Testfälle erstellt.
- ai/tester: Tester, der die Testpläne erstellt.
- ai/reviewer: Reviewer, der die Traceability und die Konsistenz der Artefakte sicherstellt.
- files: Liest und schreibt die Artefakte in Dateien.