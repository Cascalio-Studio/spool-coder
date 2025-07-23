# CI/CD Fixes für Ubuntu 24.04 (Noble)

## Problem
Die GitHub Actions CI/CD-Pipeline schlug fehl wegen veralteter Ubuntu-Paketnamen in Ubuntu 24.04.

## Fehlgeschlagene Pakete
- `libgl1-mesa-glx` → `libgl1-mesa-dev`
- `libgconf-2-4` → entfernt (deprecated)
- `libasound2` → `libasound2t64`

## Angewendete Fixes

### 1. Aktualisierte Paketnamen
```yaml
- libgl1-mesa-glx → libgl1-mesa-dev
- libasound2 → libasound2t64
- Entfernte veraltete Pakete: libgconf-2-4
- Entfernte Duplikate
```

### 2. Verbesserte Xvfb-Konfiguration
```yaml
- Explizites Xvfb-Setup für GUI-Tests
- Korrekte Display-Variable
- Startup-Verzögerung für Stabilität
```

### 3. Bereinigte Abhängigkeiten
- Entfernte doppelte Einträge
- Fokus auf essenzielle Pakete für PyQt6
- Hinzugefügtes `xvfb` für virtuelle Display-Tests

## Getestete Umgebung
- Ubuntu 24.04 LTS (Noble)
- Python 3.12, 3.13
- PyQt6
- pytest mit Coverage

## Erwartetes Ergebnis
- ✅ Erfolgreiche Paketinstallation
- ✅ Funktionierende GUI-Tests im Headless-Modus
- ✅ Coverage-Berichte
- ✅ Windows-Build bei Main-Branch
