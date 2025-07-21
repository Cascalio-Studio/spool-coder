@echo off
REM Build script for SpoolCoder Windows executable
REM This script creates a standalone Windows executable using PyInstaller

echo ================================================
echo Building SpoolCoder Windows Executable
echo ================================================

REM Check if Python is available
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH
    pause
    exit /b 1
)

REM Check if we're in the right directory
if not exist "src\main.py" (
    echo ERROR: main.py not found. Please run this script from the project root directory.
    pause
    exit /b 1
)

echo Step 1: Installing/updating dependencies...
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
python -m pip install pyinstaller

echo.
echo Step 2: Running tests to ensure everything works...
python -m pytest tests/ -v
if errorlevel 1 (
    echo ERROR: Tests failed. Please fix issues before building.
    pause
    exit /b 1
)

echo.
echo Step 3: Cleaning previous builds...
if exist "build" rmdir /s /q "build"
if exist "dist" rmdir /s /q "dist"
if exist "SpoolCoder.spec" del "SpoolCoder.spec"

echo.
echo Step 4: Building executable...
pyinstaller --name SpoolCoder ^
    --windowed ^
    --onefile ^
    --add-data "src/ui/assets;src/ui/assets" ^
    --add-data "vendor;vendor" ^
    --add-data "docs;docs" ^
    --hidden-import=PyQt6.QtCore ^
    --hidden-import=PyQt6.QtWidgets ^
    --hidden-import=PyQt6.QtGui ^
    --hidden-import=PyQt6.QtSvg ^
    --hidden-import=PyQt6.QtSvgWidgets ^
    --collect-all=PyQt6 ^
    --exclude-module=pytest ^
    --exclude-module=tests ^
    src/main.py

if errorlevel 1 (
    echo ERROR: Build failed!
    pause
    exit /b 1
)

echo.
echo Step 5: Testing executable...
if exist "dist\SpoolCoder.exe" (
    echo ✅ SUCCESS: SpoolCoder.exe created successfully!
    echo Location: %CD%\dist\SpoolCoder.exe
    
    for %%I in ("dist\SpoolCoder.exe") do (
        echo Size: %%~zI bytes
        echo Created: %%~tI
    )
    
    echo.
    echo You can now run the executable from: dist\SpoolCoder.exe
    echo.
    
    REM Ask if user wants to test run the executable
    set /p test_run="Do you want to test run the executable now? (y/n): "
    if /i "%test_run%"=="y" (
        echo Starting SpoolCoder...
        start "" "dist\SpoolCoder.exe"
    )
) else (
    echo ❌ ERROR: SpoolCoder.exe was not created!
    echo Check the build output above for errors.
)

echo.
echo Build process completed.
pause
