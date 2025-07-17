# Spool-Coder Testumgebung

Diese Testumgebung enthält Unit-Tests für alle Komponenten der Spool-Coder Anwendung.

## Teststruktur

Die Tests sind wie folgt organisiert:

- `tests/unit/`: Enthält alle Unit-Tests
  - `test_filament_model.py`: Tests für die FilamentSpool-Modellklasse
  - `test_nfc_device.py`: Tests für die NFCDevice-Serviceklasse
  - `test_main_window.py`: Tests für das MainWindow
  - `test_filament_detail_widget.py`: Tests für das FilamentDetailWidget
  - `test_read_view.py`: Tests für die ReadView
  - `test_write_view.py`: Tests für die WriteView
- `tests/test_suite.py`: Testsuite, die alle Tests zusammenfasst

## Tests ausführen

### Alle Tests ausführen

Um alle verfügbaren Tests auszuführen:

```bash
python -m tests.test_suite
```

### Einzelne Testdatei ausführen

Um einzelne Tests auszuführen (funktioniert zuverlässig für Modell- und Service-Tests):

```bash
python -m unittest tests.unit.test_filament_model
python -m unittest tests.unit.test_nfc_device
```

### Bestimmten Test ausführen

Um einen bestimmten Test auszuführen:

```bash
python -m unittest tests.unit.test_filament_model.TestFilamentSpool.test_init
```

### Hinweis zu UI-Tests

Die UI-Tests können möglicherweise Fehler verursachen, wenn PyQt6 nicht richtig installiert ist oder wenn die Komponenten in der Anwendung geändert wurden. Wenn Sie UI-Tests ausführen möchten, stellen Sie sicher, dass PyQt6 installiert ist:

```bash
pip install PyQt6
```

## Testabdeckung

Die Tests decken folgende Bereiche ab:

### Modelle
- **FilamentSpool**: Initialisierung, Konvertierung von/zu Dictionary

### Services
- **NFCDevice**: Verbindungsaufbau, Lesen und Schreiben von NFC-Tags

### UI-Komponenten
- **MainWindow**: Navigation zwischen verschiedenen Views
- **FilamentDetailWidget**: Formularsteuerung, Datenkonvertierung
- **ReadView**: NFC-Verbindung, Lesen von Tags, UI-Updates
- **WriteView**: NFC-Verbindung, Schreiben von Tags, UI-Updates

## Abhängigkeiten für Tests

Die Tests verwenden:
- `unittest`: Standard Python-Testframework
- `unittest.mock`: Mock-Objekte für externe Abhängigkeiten

## Hinweis zu UI-Tests

Die UI-Tests erfordern eine QApplication-Instanz. Diese wird in den Testdateien erstellt:

```python
app = QApplication.instance()
if not app:
    app = QApplication(sys.argv)
```

Wenn die Tests im Headless-Modus ausgeführt werden sollen, muss möglicherweise ein virtueller X-Server verwendet werden.
