# Benutzerhandbuch

Dieses Benutzerhandbuch erklärt die Verwendung der Spool-Coder Software zum Auslesen und Umprogrammieren von NFC-Spulen für Bambulab Filament Rollen.

## Inhaltsverzeichnis

1. [Starten der Anwendung](#starten-der-anwendung)
2. [Hauptmenü](#hauptmenü)
3. [Spule auslesen](#spule-auslesen)
4. [Spule programmieren](#spule-programmieren)
5. [Einstellungen](#einstellungen)
6. [Info-Bereich](#info-bereich)
7. [Tipps und Tricks](#tipps-und-tricks)
8. [Fehlerbehebung](#fehlerbehebung)

## Starten der Anwendung

Nach der Installation (siehe [Installationsanleitung](installation.md)) kann die Anwendung wie folgt gestartet werden:

```bash
# Wenn als Paket installiert
spool-coder

# Oder direkt aus dem Quellcode
python src/main.py
```

Nach dem Start wird der Hauptbildschirm angezeigt.

## Hauptmenü

Das Hauptmenü bietet Zugriff auf alle Funktionen der Anwendung:

![Hauptmenü](images/main_menu.png) *(Hinweis: Screenshot wird später hinzugefügt)*

Folgende Optionen stehen zur Verfügung:

- **Spule auslesen**: Liest die Daten einer Bambulab Filament Rolle aus
- **Spule programmieren**: Programmiert eine Spule mit benutzerdefinierten Daten
- **Einstellungen**: Konfigurationsmöglichkeiten für die Anwendung
- **Info**: Informationen über die Software

Zusätzlich finden Sie am oberen Rand der Anwendung eine Menüleiste mit den Kategorien **Datei**, **Ansicht** und **Hilfe**.

## Spule auslesen

Um eine Filamentspule auszulesen:

1. Klicken Sie im Hauptmenü auf **Spule auslesen**
2. Verbinden Sie das NFC-Lesegerät mit Ihrem Computer (falls nicht bereits geschehen)
3. Platzieren Sie die Filamentspule auf dem NFC-Lesegerät
4. Klicken Sie auf den Button **Auslesen**
5. Warten Sie, bis der Lesevorgang abgeschlossen ist

Nach erfolgreichem Auslesen werden die Daten der Filamentspule angezeigt:
- Name des Filaments
- Typ (PLA, PETG, etc.)
- Farbe
- Hersteller
- Technische Daten (Dichte, Durchmesser, Temperaturen)
- Verbleibende Menge (Länge und Gewicht)

Um zum Hauptmenü zurückzukehren, klicken Sie auf den Button **Zurück**.

## Spule programmieren

Um eine Filamentspule zu programmieren:

1. Klicken Sie im Hauptmenü auf **Spule programmieren**
2. Bearbeiten Sie die Filamentdaten nach Wunsch:
   - Name
   - Typ
   - Farbe (Klicken Sie auf "..." für die Farbauswahl)
   - Hersteller
   - Technische Daten
   - Verbleibende Menge
3. Verbinden Sie das NFC-Lesegerät mit Ihrem Computer (falls nicht bereits geschehen)
4. Platzieren Sie die zu programmierende Filamentspule auf dem NFC-Lesegerät
5. Klicken Sie auf den Button **Programmieren**
6. Bestätigen Sie den Schreibvorgang im angezeigten Dialog
7. Warten Sie, bis der Programmiervorgang abgeschlossen ist

Nach erfolgreichem Programmieren wird eine Bestätigungsmeldung angezeigt.

Um zum Hauptmenü zurückzukehren, klicken Sie auf den Button **Zurück**.

## Einstellungen

Die Einstellungen ermöglichen die Konfiguration der Anwendung (Funktion wird in einer zukünftigen Version implementiert).

## Info-Bereich

Der Info-Bereich enthält:

1. **Über**: Allgemeine Informationen über die Software wie Version und Copyright
2. **Anleitung**: Eine Kurzanleitung zur Verwendung der Software
3. **Lizenz**: Informationen zur Softwarelizenz

Um zum Hauptmenü zurückzukehren, klicken Sie auf den Button **Zurück**.

## Tipps und Tricks

- **Farbauswahl**: Beim Programmieren können Sie mit dem "..."-Button neben dem Farbfeld einen Farbwähler öffnen
- **Standardwerte**: Wenn Sie eine Spule neu programmieren, werden sinnvolle Standardwerte vorgeschlagen
- **Geräteverbindung**: Die Anwendung versucht automatisch, eine Verbindung zum NFC-Lesegerät herzustellen

## Fehlerbehebung

### Gerät wird nicht erkannt

- Überprüfen Sie, ob das NFC-Lesegerät korrekt angeschlossen ist
- Versuchen Sie, das USB-Kabel abzuziehen und wieder anzuschließen
- Starten Sie die Anwendung neu

### Lese-/Schreibfehler

- Stellen Sie sicher, dass die Spule korrekt auf dem Lesegerät positioniert ist
- Bewegen Sie die Spule nicht während des Lese-/Schreibvorgangs
- Versuchen Sie es erneut mit einer langsameren Bewegung der Spule zum Lesegerät
