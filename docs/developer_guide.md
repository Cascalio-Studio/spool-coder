# Entwicklerdokumentation

Diese Dokumentation richtet sich an Entwickler, die am Spool-Coder Projekt mitarbeiten oder den Code verstehen und erweitern möchten.

## Projekt-Setup

### Entwicklungsumgebung einrichten

1. Klonen Sie das Repository:

```bash
git clone https://github.com/Cascalio-Studio/spool-coder.git
cd spool-coder
```

2. Installieren Sie die Entwicklungsabhängigkeiten:

```bash
pip install -e ".[dev]"
```

3. Einrichten einer virtuellen Umgebung (optional, aber empfohlen):

```bash
# Mit venv
python -m venv venv
source venv/bin/activate  # Unter Windows: venv\Scripts\activate

# Oder mit conda
conda create -n spool-coder python=3.8
conda activate spool-coder
```

### Projektstruktur

```
spool-coder/
│
├── docs/               # Dokumentation
│
├── src/                # Quellcode
│   ├── core/           # Kernfunktionalität
│   ├── models/         # Datenmodelle
│   ├── services/       # Dienste (NFC, etc.)
│   │   └── nfc/        # NFC-Gerätesteuerung
│   ├── ui/             # Benutzeroberfläche
│   │   ├── assets/     # Bilder, Icons, etc.
│   │   ├── components/ # Wiederverwendbare UI-Komponenten
│   │   └── views/      # Hauptansichten
│   ├── utils/          # Hilfsfunktionen
│   └── main.py         # Haupteintrittspunkt
│
├── tests/              # Tests
│   ├── unit/           # Unit-Tests
│   └── integration/    # Integrationstests
│
├── .github/            # GitHub-spezifische Dateien
│   └── workflows/      # GitHub Actions Workflows
│
├── scripts/            # Build- und Hilfsskripte
├── setup.py            # Paketdefinition
├── requirements.txt    # Abhängigkeiten
├── LICENSE             # Lizenzinformationen
└── README.md           # Projektbeschreibung
```

## Entwicklungsrichtlinien

### Codestandards

- Befolgen Sie [PEP 8](https://www.python.org/dev/peps/pep-0008/) für Python-Code
- Schreiben Sie Docstrings im Google-Stil
- Verwenden Sie aussagekräftige Variablen- und Funktionsnamen
- Fügen Sie Typhinweise (Type Hints) hinzu, wo immer möglich

### Commit-Konventionen

Verwenden Sie aussagekräftige Commit-Nachrichten, die dem folgenden Format folgen:

```
<typ>(<bereich>): <beschreibung>

[optional körper]

[optional fußzeile]
```

Typen:
- feat: Neue Funktionen
- fix: Fehlerbehebungen
- docs: Nur Dokumentationsänderungen
- style: Änderungen, die nicht den Code beeinflussen (Formatierung, etc.)
- refactor: Code-Änderungen, die weder Funktionen hinzufügen noch Fehler beheben
- test: Hinzufügen oder Korrigieren von Tests
- chore: Änderungen an Build-Prozessen oder Hilfswerkzeugen

Beispiel:
```
feat(ui): Implementiere Filament-Detail-Ansicht

- Fügt ein neues Widget zur Anzeige von Filament-Details hinzu
- Implementiert Bearbeitungsmodus für das Widget
- Integriert Farbauswahl-Funktionalität
```

## Implementierungsdetails

### UI-Framework

Die Benutzeroberfläche ist mit PyQt6 implementiert. PyQt ist ein leistungsstarkes Framework für die Erstellung plattformübergreifender Anwendungen mit Python.

Wichtige Klassen:
- `QMainWindow`: Basisklasse für das Hauptfenster
- `QWidget`: Basisklasse für alle UI-Elemente
- `QVBoxLayout`, `QHBoxLayout`: Layout-Manager
- `QStackedWidget`: Ermöglicht das Wechseln zwischen verschiedenen Ansichten

### Datenmodelle

Die Anwendung verwendet einfache Klassen zur Repräsentation von Daten. Die Hauptklasse ist `FilamentSpool`, die alle Informationen über eine Filamentspule enthält.

### NFC-Kommunikation

Die NFC-Kommunikation wird über die `NFCDevice`-Klasse im `services.nfc`-Modul abgewickelt. Diese Klasse stellt eine abstrakte Schnittstelle für die Kommunikation mit dem NFC-Lesegerät bereit.

> Hinweis: Die aktuelle Implementierung ist eine Simulation, da das tatsächliche Gerät noch entwickelt wird. Die konkrete Hardware-Kommunikation muss implementiert werden, sobald das Gerät verfügbar ist.

## Tests

### Unit-Tests

Unit-Tests befinden sich im Verzeichnis `tests/unit/` und können mit pytest ausgeführt werden:

```bash
pytest tests/unit/
```

### Integrationstests

Integrationstests befinden sich im Verzeichnis `tests/integration/` und können ebenfalls mit pytest ausgeführt werden:

```bash
pytest tests/integration/
```

## Erweiterungen und Beiträge

### Funktionen hinzufügen

1. Identifizieren Sie den geeigneten Ort für Ihren Code
2. Implementieren Sie die Funktionalität
3. Fügen Sie Tests hinzu
4. Aktualisieren Sie die Dokumentation
5. Erstellen Sie einen Pull Request

### Pull Request-Prozess

1. Forken Sie das Repository
2. Erstellen Sie einen Feature-Branch
3. Implementieren Sie Ihre Änderungen
4. Führen Sie alle Tests aus
5. Reichen Sie einen Pull Request ein

## Veröffentlichung

### Version erhöhen

1. Aktualisieren Sie die Versionsnummer in `setup.py`
2. Aktualisieren Sie die Versionsnummer in `src/__init__.py`
3. Erstellen Sie ein neues Tag für die Version

### Build erstellen

Um ein ausführbares Programm zu erstellen, kann PyInstaller verwendet werden:

```bash
pip install pyinstaller
pyinstaller --name spool-coder --onefile --windowed src/main.py
```

Die ausführbare Datei wird im `dist/`-Verzeichnis erstellt.
