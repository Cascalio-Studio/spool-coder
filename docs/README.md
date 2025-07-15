# Spool-Coder Documentation

This documentation describes the "Spool-Coder" software, an application for reading and reprogramming NFC spools for Bambulab filament rolls.

## Table of Contents

1. [Introduction](#introduction)
2. [Installation](#installation)
3. [Usage](#usage)
4. [Architecture](#architecture)
5. [Modules](#modules)
6. [Development](#development)

## Introduction

Spool-Coder is a Python-based application with a graphical user interface that enables reading and reprogramming NFC spools for Bambulab filament rolls. The software communicates with a specialized NFC reader device and provides a user-friendly interface for these tasks.

## Installation

### Prerequisites

- Python 3.8 or higher
- PyQt6
- Additional dependencies (see `requirements.txt` or `setup.py`)

### Installation from Source

```bash
git clone https://github.com/Cascalio-Studio/spool-coder.git
cd spool-coder
pip install -e .
```

## Usage

After installation, the application can be started as follows:

```bash
python src/main.py
```

Or if installed:

```bash
spool-coder
```

### Features

- **Read Spool**: Reads the data from a Bambulab filament roll.
- **Program Spool**: Allows customizing and writing data to a filament NFC spool.
- **Settings**: Configuration options for the application.
- **Info**: Information about the software and instructions for use.

## Architecture

The application follows a modular structure with clear separation between user interface, business logic, and device interaction:

- **UI Layer**: Implemented with PyQt6, provides the graphical user interface.
- **Model Layer**: Contains the data models for filament spools and other required entities.
- **Service Layer**: Handles communication with the NFC device and other services.

## Modules

See the subpages for detailed documentation of individual modules:

- [UI Modules](module_ui.md)
- [Model Modules](module_models.md)
- [Service Modules](module_services.md)

## Development

### Code Conventions

- The code follows the [PEP 8](https://www.python.org/dev/peps/pep-0008/) Style Guide for Python Code.
- Docstrings are written in Google style.

### Tests

Unit tests can be run with pytest:

```bash
pytest tests/
```
