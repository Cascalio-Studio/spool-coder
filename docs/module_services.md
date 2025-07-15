# Service-Module Dokumentation

Dieses Dokument beschreibt die Service-Module des Spool-Coder-Projekts, die für die Kommunikation mit dem NFC-Lesegerät und andere Dienste verantwortlich sind.

## Übersicht

Die Service-Module sind in `src/services/` organisiert und bieten Funktionalitäten für die Interaktion mit Hardware und externe Dienste.

## NFC-Dienste

### NFCDevice

**Datei**: `src/services/nfc/device.py`

Die `NFCDevice`-Klasse ist für die Kommunikation mit dem NFC-Lesegerät verantwortlich.

#### Attribute:

- **port**: Der serielle Port für die Verbindung (z.B. 'COM3' unter Windows)
- **connected**: Status der Verbindung zum Gerät

#### Methoden:

- **connect()**: Stellt eine Verbindung zum Gerät her
- **disconnect()**: Trennt die Verbindung zum Gerät
- **is_connected()**: Überprüft, ob eine Verbindung besteht
- **read_tag()**: Liest Daten von einem NFC-Tag
- **write_tag(data)**: Schreibt Daten auf ein NFC-Tag

#### Beispiel:

```python
from services.nfc import NFCDevice

# Gerät erstellen
device = NFCDevice(port="COM3")

# Verbindung herstellen
if device.connect():
    # Daten lesen
    data = device.read_tag()
    
    if data:
        # Daten verarbeiten
        print(f"Gelesen: {data}")
    
    # Neue Daten schreiben
    new_data = {
        "name": "Mein PLA",
        "type": "PLA",
        "color": "#FF0000",
        "manufacturer": "BambuLab",
        "density": 1.24,
        "diameter": 1.75,
        "nozzle_temp": 210,
        "bed_temp": 60,
        "remaining_length": 240,
        "remaining_weight": 1000
    }
    
    success = device.write_tag(new_data)
    print(f"Schreiben {'erfolgreich' if success else 'fehlgeschlagen'}")
    
    # Verbindung trennen
    device.disconnect()
```

## Kommunikationsprotokoll

Aktuell ist die Implementierung des `NFCDevice` eine Simulation. Das tatsächliche Kommunikationsprotokoll mit dem NFC-Lesegerät wird implementiert, sobald das Gerät verfügbar ist.

Das erwartete Protokoll wird wahrscheinlich folgendes umfassen:

1. **Verbindungsaufbau**: Serielle Verbindung mit dem Gerät herstellen
2. **Befehle senden**: Befehle zum Lesen oder Schreiben von Tags
3. **Antworten empfangen**: Daten oder Statusmeldungen vom Gerät
4. **Fehlerbehandlung**: Behandlung von Timeout, Verbindungsabbrüchen oder Fehlermeldungen

## Erweiterungsmöglichkeiten

Die Service-Module können in Zukunft um weitere Funktionalitäten erweitert werden:

### Geräte-Management

- **Automatische Geräteerkennung**
- **Geräteauswahl**, wenn mehrere Geräte verfügbar sind
- **Firmware-Updates** für das NFC-Lesegerät

### Erweiterte NFC-Funktionen

- **Formatierung von NFC-Tags**
- **Verschlüsselung** der auf den Tags gespeicherten Daten
- **Backup und Wiederherstellung** von Tag-Daten
- **Verifikation** nach dem Schreiben
