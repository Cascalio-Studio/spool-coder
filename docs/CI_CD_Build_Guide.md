# CI/CD and Build Documentation

This document explains the Continuous Integration/Continuous Deployment (CI/CD) setup for SpoolCoder and how to build the application for distribution.

## Overview

The SpoolCoder project uses GitHub Actions for automated testing and building Windows executables whenever code is pushed to the main branch.

## CI/CD Pipeline

### Automated Workflow (`.github/workflows/build-and-test.yml`)

The CI/CD pipeline consists of three main jobs:

#### 1. **Test Job** (`test`)
- **Runs on:** Ubuntu Latest
- **Python versions:** 3.9, 3.10, 3.11, 3.12, 3.13
- **Purpose:** Ensure code quality and functionality across Python versions

**Steps:**
1. Install system dependencies for PyQt6
2. Install Python dependencies
3. Run comprehensive test suite with coverage
4. Upload coverage reports to Codecov

#### 2. **Build Windows Executable** (`build-windows`)
- **Runs on:** Windows Latest
- **Triggered:** Only on pushes to `main` branch
- **Dependencies:** Requires `test` job to pass first

**Steps:**
1. Install dependencies and PyInstaller
2. Run tests on Windows platform
3. Build standalone Windows executable using our build script
4. Test the created executable
5. Create versioned release artifacts
6. Upload as GitHub artifacts (retained for 90 days)

#### 3. **Build Notification** (`build-notification`)
- **Purpose:** Provide build status summary
- **Runs:** Always, regardless of other job outcomes

### Trigger Events

The pipeline runs on:
- **Push to `main` or `develop` branches** → Full test + build
- **Pull requests to `main`** → Tests only
- **Release publication** → Full test + build + release assets

## Local Building

### Quick Build (Windows)

Use the provided batch script:

```bash
# Run from project root
build_windows.bat
```

This script will:
1. Install dependencies
2. Run tests
3. Clean previous builds
4. Create `SpoolCoder.exe` in the `dist/` folder

### Cross-Platform Build

Use the Python build script for more control:

```bash
# Basic build
python build.py

# Debug build with console output
python build.py --debug

# Directory distribution instead of single file
python build.py --onedir

# Skip tests (faster build)
python build.py --skip-tests

# Skip cleaning (incremental build)
python build.py --skip-clean
```

### Manual PyInstaller Build

For advanced users who want to customize the build:

```bash
# Install PyInstaller
pip install pyinstaller

# Basic build command
pyinstaller --name SpoolCoder --windowed --onefile src/main.py

# Full build with all assets
pyinstaller SpoolCoder.spec
```

## Build Outputs

### Files Created

After a successful build, you'll find:

```
dist/
├── SpoolCoder.exe                 # Main executable (Windows)
├── RELEASE_NOTES.md              # Build information
└── build-info.txt                # Version details
```

### Executable Features

The built executable includes:
- ✅ All Python dependencies bundled
- ✅ PyQt6 GUI framework
- ✅ UI assets and icons
- ✅ Vendor libraries (Bambu research)
- ✅ Documentation files
- ✅ No external dependencies required

## Distribution

### GitHub Artifacts

Every successful build on `main` creates:
- **Artifact Name:** `SpoolCoder-Windows-Build`
- **Contains:** Executable + release notes
- **Retention:** 90 days
- **Download:** Available from GitHub Actions tab

### Releases

For official releases:
1. Create a Git tag: `git tag v1.0.0`
2. Push the tag: `git push origin v1.0.0`
3. Create a GitHub release from the tag
4. The workflow will automatically attach the executable

### Manual Distribution

The standalone executable can be distributed directly:
- **No installer required**
- **No Python installation needed**
- **Single file deployment**
- **Compatible with Windows 10/11**

## System Requirements

### Development Environment
- Python 3.9+ 
- PyQt6
- Git
- Windows/Linux/macOS

### Runtime (End Users)
- **Windows:** Windows 10/11 (64-bit)
- **macOS:** macOS 10.14+ (if building for Mac)
- **Linux:** Modern Linux distribution with X11

## Troubleshooting

### Common Build Issues

1. **"Tests failed"**
   - Ensure all dependencies are installed
   - Check that PyQt6 works in headless mode
   - Run tests manually: `python -m pytest tests/ -v`

2. **"PyInstaller failed"**
   - Clear build cache: `rm -rf build dist *.spec`
   - Check for missing imports in the spec file
   - Try debug build: `python build.py --debug`

3. **"Executable won't start"**
   - Check Windows Defender/antivirus
   - Try console build to see error messages
   - Verify all assets are included

### Build Performance

- **Single file builds:** Slower startup, easier distribution
- **Directory builds:** Faster startup, multiple files
- **Debug builds:** Helpful for troubleshooting
- **Release builds:** Optimized for distribution

## Security Considerations

### Code Signing (Optional)

For production releases, consider code signing:

```bash
# Windows (requires certificate)
signtool sign /f certificate.p12 /p password dist/SpoolCoder.exe
```

### Antivirus Detection

Some antivirus software may flag PyInstaller executables:
- Submit to antivirus vendors for whitelisting
- Consider code signing
- Build on clean systems
- Use VirusTotal for verification

---

*This documentation is maintained alongside the codebase and updated with each release.*
