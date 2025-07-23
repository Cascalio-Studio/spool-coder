# CI/CD Fixes für Ubuntu 24.04 (Noble)

## Problem
Die GitHub Actions CI/CD-Pipeline schlug fehl wegen:
1. Veralteter Ubuntu-Paketnamen in Ubuntu 24.04
2. Nicht-existierender PyQt6-SVG-Abhängigkeit

## Fehlgeschlagene Pakete & Dependencies

### Ubuntu-Pakete
- `libgl1-mesa-glx` → `libgl1-mesa-dev`
- `libgconf-2-4` → entfernt (deprecated)
- `libasound2` → `libasound2t64`

### Python-Pakete
- `PyQt6-Qt6-SVG` → entfernt (falscher Paketname)
- `PyQt6-SVG` → entfernt (nicht existent, SVG ist in PyQt6 enthalten)

## Angewendete Fixes

### 1. Aktualisierte Ubuntu-Paketnamen
```yaml
- libgl1-mesa-glx → libgl1-mesa-dev
- libasound2 → libasound2t64
- Entfernte veraltete Pakete: libgconf-2-4
- Entfernte Duplikate
```

### 2. Bereinige Python-Dependencies
```txt
# Entfernt (nicht existent):
# PyQt6-Qt6-SVG>=6.2.0
# PyQt6-SVG>=6.2.0

# SVG-Unterstützung ist in PyQt6>=6.2.0 enthalten
PyQt6>=6.2.0  # Enthält QtSvg-Module
```

### 3. Vereinfachte CI/CD-Installation
```yaml
# Vorher: Komplizierte Multi-Step-Installation
# Nachher: Einfache requirements.txt Installation
pip install -r requirements.txt
```

### 4. Verbesserte Xvfb-Konfiguration
```yaml
- Explizites Xvfb-Setup für GUI-Tests
- Korrekte Display-Variable
- Startup-Verzögerung für Stabilität
```

## Getestete Funktionalität
- ✅ PyQt6.QtSvg Import funktioniert
- ✅ StartupScreen mit SVG-Logo lädt korrekt
- ✅ Alle lokalen Tests bestehen
- ✅ Build-Prozess mit PyInstaller funktioniert

## Erwartetes Ergebnis
- ✅ Erfolgreiche Paketinstallation
- ✅ Funktionierende GUI-Tests im Headless-Modus
- ✅ SVG-Unterstützung ohne separate Pakete
- ✅ Coverage-Berichte
- ✅ Windows-Build bei Main-Branch
