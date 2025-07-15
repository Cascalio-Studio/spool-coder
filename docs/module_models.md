# Model-Module Dokumentation

Dieses Dokument beschreibt die Model-Module des Spool-Coder-Projekts, die für die Datenhaltung und -modellierung verantwortlich sind.

## Übersicht

Die Model-Module sind in `src/models/` organisiert und definieren die Datenstrukturen, die von der Anwendung verwendet werden.

## Filament-Modell

### FilamentSpool

**Datei**: `src/models/filament.py`

Die `FilamentSpool`-Klasse repräsentiert eine Filamentspule mit NFC-Daten.

#### Attribute:

- **name**: Name des Filaments
- **type**: Filament-Typ (z.B. PLA, PETG, ABS)
- **color**: Farbe als Hex-Code
- **manufacturer**: Hersteller des Filaments
- **density**: Dichte des Materials in g/cm³
- **diameter**: Durchmesser des Filaments in mm
- **nozzle_temp**: Empfohlene Düsentemperatur in °C
- **bed_temp**: Empfohlene Betttemperatur in °C
- **remaining_length**: Verbleibende Filamentlänge in m
- **remaining_weight**: Verbleibendes Gewicht in g

#### Methoden:

- **to_dict()**: Konvertiert die Filamentspule in ein Dictionary für die NFC-Codierung
- **from_dict(data)**: Erstellt eine Filamentspule aus einem Dictionary (Klassenmethode)

#### Beispiel:

```python
from models import FilamentSpool

# Erstellen einer neuen Filamentspule
spool = FilamentSpool(
    name="Mein PLA",
    type="PLA",
    color="#FF0000",
    manufacturer="BambuLab",
    density=1.24,
    diameter=1.75,
    nozzle_temp=210,
    bed_temp=60,
    remaining_length=240,
    remaining_weight=1000
)

# Konvertieren zu Dictionary für NFC
data = spool.to_dict()

# Erstellen aus Dictionary
spool2 = FilamentSpool.from_dict(data)
```

## Datenfluss

Die Modelle werden in folgenden Szenarien verwendet:

1. **Lesen von NFC-Spulen**: Daten werden vom NFC-Gerät gelesen und in ein `FilamentSpool`-Objekt konvertiert.
2. **Anzeigen von Daten**: Die Daten werden in der UI angezeigt, typischerweise durch `FilamentDetailWidget`.
3. **Bearbeiten von Daten**: Der Benutzer kann die Attribute bearbeiten.
4. **Schreiben auf NFC-Spulen**: Die bearbeiteten Daten werden wieder in ein Dictionary konvertiert und auf die NFC-Spule geschrieben.

## Erweiterungsmöglichkeiten

Das Modell kann in Zukunft um weitere Attribute erweitert werden, beispielsweise:

- **extrusion_multiplier**: Multiplikator für die Extrusion
- **chamber_temp**: Empfohlene Kammertemperatur
- **batch_number**: Chargennummer des Filaments
- **production_date**: Produktionsdatum
- **expiration_date**: Ablaufdatum/Haltbarkeit
