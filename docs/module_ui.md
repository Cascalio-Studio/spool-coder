# UI-Module Dokumentation

Dieses Dokument beschreibt die UI-Module des Spool-Coder-Projekts, die für die grafische Benutzeroberfläche verantwortlich sind.

## Übersicht

Die UI-Module sind in `src/ui/` organisiert und folgen einer strukturierten Aufteilung:

- **views/**: Enthält die Hauptansichten der Anwendung
- **components/**: Wiederverwendbare UI-Komponenten
- **assets/**: Bilder, Icons und andere Ressourcen

## Hauptansichten (views)

### MainWindow

**Datei**: `src/ui/views/main_window.py`

Die `MainWindow`-Klasse dient als Hauptfenster der Anwendung und ist für die Navigation zwischen verschiedenen Ansichten zuständig.

#### Schlüsselfunktionen:

- **setup_menu()**: Erstellt die Menüleiste mit Optionen für Datei, Ansicht und Hilfe.
- **create_menu_buttons()**: Erstellt die Hauptnavigationsbuttons für die verschiedenen Funktionen.
- **show_home()**: Zeigt die Startseite an.
- **show_read_view()**: Wechselt zur Ansicht zum Auslesen von NFC-Spulen.
- **show_write_view()**: Wechselt zur Ansicht zum Programmieren von NFC-Spulen.
- **show_info()**: Zeigt die Info-Seite an.

### ReadView

**Datei**: `src/ui/views/read_view.py`

Die `ReadView`-Klasse ist für die Ansicht zum Auslesen von NFC-Spulen verantwortlich.

#### Schlüsselfunktionen:

- **start_reading()**: Startet den Lesevorgang für eine NFC-Spule.
- **connect_device()**: Verbindet mit dem NFC-Lesegerät.
- **reading_completed()**: Wird aufgerufen, wenn der Lesevorgang abgeschlossen ist.

### WriteView

**Datei**: `src/ui/views/write_view.py`

Die `WriteView`-Klasse bietet eine Oberfläche zum Programmieren von NFC-Spulen mit benutzerdefinierten Daten.

#### Schlüsselfunktionen:

- **start_writing()**: Startet den Schreibvorgang für eine NFC-Spule.
- **writing_completed()**: Wird aufgerufen, wenn der Schreibvorgang abgeschlossen ist.

### InfoView

**Datei**: `src/ui/views/info_view.py`

Die `InfoView`-Klasse zeigt Informationen über die Anwendung, eine Anleitung und Lizenzdetails an.

## Komponenten (components)

### FilamentDetailWidget

**Datei**: `src/ui/components/filament_detail.py`

Das `FilamentDetailWidget` ist eine wiederverwendbare UI-Komponente zur Anzeige und Bearbeitung von Filament-Spulendaten.

#### Schlüsselfunktionen:

- **set_data()**: Setzt die anzuzeigenden Filamentdaten.
- **get_data()**: Gibt die aktuellen Daten zurück.
- **select_color()**: Öffnet einen Farbauswahldialog für die Filamentfarbe.

## UI-Fluss

1. Die Anwendung startet mit der `MainWindow`-Klasse, die den Startbildschirm anzeigt.
2. Benutzer können über Menü oder Hauptbuttons zu verschiedenen Funktionen navigieren:
   - "Spule auslesen" lädt die `ReadView`
   - "Spule programmieren" lädt die `WriteView`
   - "Info" lädt die `InfoView`
3. Jede Ansicht enthält einen "Zurück"-Button, der zur Startseite zurückkehrt.

## Styling

Die Anwendung verwendet benutzerdefiniertes CSS-Styling für Buttons und andere UI-Elemente, um ein konsistentes und ansprechendes Erscheinungsbild zu gewährleisten.
