# NFC-Protokoll Dokumentation

Diese Dokumentation beschreibt das Protokoll zur Kommunikation mit dem NFC-Lesegerät für die Spool-Coder Anwendung.

> **Hinweis**: Diese Dokumentation ist vorläufig, da das tatsächliche NFC-Lesegerät noch entwickelt wird. Die Details werden aktualisiert, sobald das Gerät fertiggestellt ist.

## Übersicht

Das NFC-Protokoll definiert die Kommunikation zwischen der Spool-Coder Software und dem NFC-Lesegerät, das zum Auslesen und Programmieren von Bambulab Filament-Spulen verwendet wird.

## Verbindung

Die Verbindung zum NFC-Lesegerät erfolgt über eine serielle Schnittstelle (USB).

### Verbindungsparameter

- **Baudrate**: 115200
- **Datenbits**: 8
- **Parität**: Keine
- **Stopbits**: 1
- **Flusskontrolle**: Keine

### Verbindungsaufbau

1. Software sucht nach verfügbaren seriellen Ports
2. Verbindung wird mit den oben genannten Parametern hergestellt
3. Software sendet einen Ping-Befehl, um die Geräteverbindung zu überprüfen
4. Gerät antwortet mit Identifikationsinformationen

## Befehlssatz

Die Kommunikation basiert auf einem Befehlssatz aus ASCII-Zeichenketten.

### Befehlsformat

```
<BEFEHL>:<PARAMETER>;<PARAMETER>;...\n
```

Beispiel:
```
READ\n
```

### Antwortformat

```
<STATUS>:<DATEN>\n
```

Status kann sein:
- `OK`: Befehl erfolgreich ausgeführt
- `ERROR`: Fehler bei der Ausführung des Befehls

Beispiel:
```
OK:{"name":"Bambu PLA","type":"PLA","color":"#FF0000"}\n
```

### Verfügbare Befehle

#### PING

Prüft, ob das Gerät verbunden ist.

**Befehl**:
```
PING\n
```

**Antwort**:
```
OK:SPOOL_CODER_NFC_V1\n
```

#### READ

Liest Daten von einer NFC-Spule.

**Befehl**:
```
READ\n
```

**Antwort (Erfolg)**:
```
OK:<JSON-Daten>\n
```

**Antwort (Fehler)**:
```
ERROR:NO_TAG\n
```

#### WRITE

Schreibt Daten auf eine NFC-Spule.

**Befehl**:
```
WRITE:<JSON-Daten>\n
```

**Antwort (Erfolg)**:
```
OK:WRITE_COMPLETE\n
```

**Antwort (Fehler)**:
```
ERROR:NO_TAG\n
ERROR:WRITE_FAILED\n
```

#### FORMAT

Formatiert eine NFC-Spule.

**Befehl**:
```
FORMAT\n
```

**Antwort (Erfolg)**:
```
OK:FORMAT_COMPLETE\n
```

**Antwort (Fehler)**:
```
ERROR:NO_TAG\n
ERROR:FORMAT_FAILED\n
```

## Datenformat

Die Daten werden im JSON-Format übertragen.

### Beispiel für Filament-Daten

```json
{
  "name": "Bambu PLA",
  "type": "PLA",
  "color": "#FF0000",
  "manufacturer": "Bambulab",
  "density": 1.24,
  "diameter": 1.75,
  "nozzle_temp": 210,
  "bed_temp": 60,
  "remaining_length": 240,
  "remaining_weight": 1000
}
```

## Fehlerbehandlung

### Timeouts

- Verbindungs-Timeout: 5 Sekunden
- Befehlsausführungs-Timeout: 10 Sekunden

### Neuverbindung

Bei Verbindungsabbrüchen versucht die Software automatisch, die Verbindung wiederherzustellen.

### Fehlercodes

- `NO_TAG`: Keine NFC-Spule gefunden
- `READ_FAILED`: Fehler beim Lesen der Spulendaten
- `WRITE_FAILED`: Fehler beim Schreiben der Spulendaten
- `FORMAT_FAILED`: Fehler beim Formatieren der Spule
- `INVALID_DATA`: Ungültige Daten für den Schreibvorgang
- `UNKNOWN_ERROR`: Unbekannter Fehler

## Implementierung

### Beispielcode für den Leseprozess

```python
import serial
import json
import time

def read_nfc_tag(port="/dev/ttyUSB0"):
    try:
        # Verbindung herstellen
        ser = serial.Serial(
            port=port,
            baudrate=115200,
            bytesize=serial.EIGHTBITS,
            parity=serial.PARITY_NONE,
            stopbits=serial.STOPBITS_ONE,
            timeout=5
        )
        
        # Verbindung prüfen
        ser.write(b"PING\n")
        response = ser.readline().decode('utf-8').strip()
        if not response.startswith("OK:"):
            ser.close()
            return None, "Gerät antwortet nicht korrekt"
        
        # Lesebefehl senden
        ser.write(b"READ\n")
        response = ser.readline().decode('utf-8').strip()
        
        # Verbindung schließen
        ser.close()
        
        # Antwort auswerten
        if response.startswith("OK:"):
            data_json = response[3:]  # "OK:" entfernen
            data = json.loads(data_json)
            return data, None
        elif response.startswith("ERROR:"):
            error_code = response[6:]  # "ERROR:" entfernen
            return None, f"Fehler: {error_code}"
        else:
            return None, "Unbekannte Antwort vom Gerät"
            
    except serial.SerialException as e:
        return None, f"Verbindungsfehler: {str(e)}"
    except json.JSONDecodeError:
        return None, "Ungültiges Datenformat"
    except Exception as e:
        return None, f"Unerwarteter Fehler: {str(e)}"
```

## Zukünftige Erweiterungen

- Verschlüsselung der übertragenen Daten
- Verbesserte Fehlerbehandlung und Wiederherstellung
- Unterstützung für mehrere NFC-Protokolle
- Firmware-Updates über die Anwendung
