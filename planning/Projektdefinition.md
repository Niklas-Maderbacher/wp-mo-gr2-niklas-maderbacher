---
title: HealthLog
name: Niklas Maderbacher
date: 20.11.2025
---

# HealthLog

## Projektbeschreibung

Entwicklung des `HealthLog` Programms zur täglichen Eintragen von bestimmten Gesundheitsdaten wie erledigte `Aktivitäten`, die durchschnittliche `Tagesstimmung` und die Anzahl der Stunden an `Schlaft`. Diese Daten werden gesammelt, um visualisiert und (opt.) verarbeitet zu werden.

Tagesaktuelle Daten werden nach erfolgreichem Einloggen/Registrieren auf dem Dashboard visualisiert und können erweitert oder abgeändert werden.
Bei der aktuellen Stimmung kann zwischen `sehr gut`, `gut`, `mittelmäßig`, `schlecht` und `sehr schlacht` gewählt werden.
Bie der Anzahl der Stunden an Schlaf kann zwischen `0 Stunden 0 Minuten` und `24 Stunden 0 Minuten` gewählt werden.

Die eingegebenen Daten werden mittels Tabellenform visualisiert, wobei für jedes Datum (einz. Daten) eine eigenständige Tabelle existiert, wobei in der Aktivitätentabelle spezifisch gesucht werden kann: Kategorie der Aktivität filtert, nach einem Schlüsselwort im Namen der Aktivität suchen oder zeitlich aufsteigend oder absteigend sortieren.

Der Administrator hat Einsicht in alle Benutzer und deren Daten mittels Tabellenform, wobei für jedes Datum (einz. Daten) eine eigenständige Tabelle existiert, in der nach `Nutzername oder Aktivität gefiltert` werden kann.

### Optional

Daten, die innerhalb der letzten Woche (7 Tage) gesammelt wurden, werden mittels eines Diagrammes visualisiert:
- `Aktivitäten`: Anzahl der Aktivitäten in der letzten Woche, durchschnittliche Aktivitäten pro Tag und ein Balkendiagramm mit Anzahl der Aktivitäten an einem Tag
- `Stimmung`: Druchschnittliche Stimmung in der letzten Woche und ein linien Diagram mit Anzahl der Stunden an einem Tag
- `Schlaf`: Durchschnittliche Stundne an Schlaf in der letzten Woche und ein Balkendiagramm mit Anzahl der Stunden an Schlaf an einem Tag

## Use-Cases

### Use-Case 1 - Registrierung

1. User öffnet die Website
2. System zeigt Eingabefelder für den Login
3. User betätigt <Noch kein Kontro?> Knopf
4. System zeigt Registrierungsfelder
5. User trägt `user123@user123.com` in Email-Feld ein
6. User trägt `User123` in Username-Feld ein
7. User trägt `Kennwort1` in Passwort-Feld ein
8. User betätigt <Registrieren> Knopf
9. System validiert die Eingaben <br>
    a. System akzeptiert Eingagaben
    b. System meldet `Angegebene Email ist keine Email` und bittet um erneute Eingabe
    c. System meldet `Username existiert bereits` und bittet um erneute Eingabe
    d. System meldet `Email existiert bereits` und bittet um erneute Eingabe
10. System speichert die Daten und leitet User an Login weiter

### Use-Case 2 - Anmeldung

1. User öffnet die Website
2. System zeigt Eingabefelder für den Login
3. User trägt `user123@user123.com` in Email-Feld ein
4. User trägt `Kennwort1` in Passwort-Feld ein
5. User betätigt <Login> Knopf
6. System validiert die Eingaben
    a. System akzeptiert die Eingaben
    b. System meldet `Email oder Passwort sind falsch` und bittet um erneute Eingabe
7. System leitet User an Dashboard weiter

### Use-Case 3 - Abmeldung

1. User betätigt <Logout> Knopf
2. System akzeptiert die Anfrage und leitet User an <Login> weiter

### Use-Case 4 - Durchschnittliche Tagesstimmung eintragen

1. User betätigt <Tagesübersicht> Reiter
2. User betätigt das <Dropdown Menü> der Tagesstimmung
3. User wählt Tagesstimmung `gut` aus
4. User betätigt <speichern> Knopf
5. System speichert die Daten und aktualisiert das Dashboard

### Use-Case 5 - Durchschnittliche Tagesstimmung bearbeiten

1. User betätigt <Tagesübersicht> Reiter
2. User betätigt das <Dropdown Menü> der Tagesstimmung
3. User wählt neue Tagesstimmung aus
4. System validiert die Eingaben
    a. System akzeptiert die Eingaben
    b. System erkennt selbe Eingabe wie bereits vorhanden (opt.) und blockiert <speichern> Knopf
5. User betätigt <speichern> Knopf
6. System speichert die Daten und aktualisiert das Dashboard

### Use-Case 6 - Anzahl der Stunden an Schalf eintragen

1. User betätigt <Tagesübersicht> Reiter
2. User trägt `8` in das Stunden Feld ein  
3. User trägt `47` in das Minuten Feld ein
4. User betätigt <speichern> Knopf
5. System validiert die Eingabe
    a. System akzeptiert die Eingabe
    b. System meldet `Stunden Wert nicht kleiner 0 und größer 24` und bittet um erneute Eingabe
    c. System meldet `Minuten Wert nicht kleiner 0 und größer 60` und bittet um erneute Eingabe
6. System speichert die Daten und aktualisiert das Dashboard

### Use-Case 7 - Anzahl der Stunden bearbeiten

1. User betätigt <Tagesübersicht> Reiter
2. User ersetzt vorhandenen Wert im Stunden Feld mit `6`
3. User ersetzt vorhandenen Wert im Minuten Feld mit `7`
4. User betätigt <speichern> Knopf
5. System validiert die Eingabe
    a. System akzeptiert die Eingabe
    b. System meldet `Stunden Wert nicht kleiner 0 und größer 24` und bittet um erneute Eingabe
    c. System meldet `Minuten Wert nicht kleiner 0 und größer 60` und bittet um erneute Eingabe
6. System speichert die Daten und aktualisiert das Dashboard

### Use-Case 8 - Aktivität eintragen

1. User betätigt <Tagesübersicht> Reiter
2. User betätigt <neue Aktivität anlegen> Knopf
3. System zeigt Eingabefelder für Aktivitäten
4. User trägt `Laufen im Wald` im Namens-Feld ein
5. User wählt `Laufen` als Kategorie aus
6. User trägt `1:20` in das Dauer-Feld ein
7. User betätigt <speichern> Knopf
8. System validiert die Eingabe
    a. System akzeptiert die Eingabe
    b. System meldet `Name der Aktivität zu lang`
    c. System meldet `Dauer bitte im HH:MM Format eintragen`
9. System speichert die Daten und aktualisiert das Dashboard

### Use-Case 9 - Aktivität bearbeiten

1. User betätigt <Tagesübersicht> Reiter
2. User betätigt den <bearbeiten> Knopf neben einer Aktivität
3. System zeigt Eingabefelder für Aktivitäten
4. User ändert `Laufen im Wald` zu `PoE2 spielen` im Namens-Feld ein
5. User ändert `Laufen` zu `Zocken` als Kategorie aus
6. User ändert `1:20` zu `12:30` in das Dauer-Feld ein
7. User betätigt <speichern> Knopf
8. System validiert die Eingabe
    a. System akzeptiert die Eingabe
    b. System meldet `Name der Aktivität zu lang`
    c. System meldet `Dauer bitte im HH:MM Format eintragen`
    d. System erkennt selbe Eingabe wie bereits vorhanden (opt.) und blockiert <speichern> Knopf
9. System speichert die Daten und aktualisiert das Dashboard

### Use-Case 10 - Tagesübersicht anzeigen

1. User betätigt <Tagesübersicht> Reiter
2. User sieht seine aktuelle Stimmung
3. User sieht seine Anzahl an Stunden
4. User sieht seine Aktivitäten

### Use-Case 11 - Alle Tagesstimmungen anzeigen

1. User betätigt <Tagesstimmungen> Reiter
2. User sieht alle eingetragenen Tagesstimmungen von sich
3. (opt.) Druchschnittliche Stimmung in der letzten Woche und ein linien Diagram mit Anzahl der Stunden an einem Tag

### Use-Case 12 - Alle Anzahl der Stunden an Schlaf anzeigen

1. User betätigt <Schlaf> Reiter
2. User sieht alle eingetragenen Anzahl der Stunden von sich
3. (opt.) Durchschnittliche Stunden an Schlaf in der letzten Woche und ein Balkendiagramm mit Anzahl der Stunden an Schlaf an einem Tag

### Use-Case 13 - Alle Aktivitäten anzeigen

1. User betätigt <Aktivität> Reiter
2. User sieht alle eingetragenen Aktivitäten von sich
3. (opt.) Anzahl der Aktivitäten in der letzten Woche, durchschnittliche Aktivitäten pro Tag und ein Balkendiagramm mit Anzahl der Aktivitäten an einem Tag
