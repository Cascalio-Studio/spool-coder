# Installation Guide

This guide describes the installation and setup of the Spool-Coder software.

## System Requirements

- Windows, macOS, or Linux
- Python 3.8 or higher
- USB port for the NFC reader device (when used)

## Python Installation

If Python is not already installed:

### Windows

1. Visit [python.org](https://www.python.org/downloads/)
2. Download the latest Python version for Windows
3. Run the installer and check the option "Add Python to PATH"
4. Verify the installation with the command `python --version` in the command prompt

### macOS

1. Visit [python.org](https://www.python.org/downloads/)
2. Download the latest Python version for macOS
3. Run the installer
4. Verify the installation with the command `python3 --version` in the terminal

### Linux

Most Linux distributions have Python pre-installed. If not:

```bash
# Ubuntu/Debian
sudo apt update
sudo apt install python3 python3-pip

# Fedora
sudo dnf install python3 python3-pip

# Arch Linux
sudo pacman -S python python-pip
```

## Installing Spool-Coder

### Installation from the Repository

1. Clone the repository:

```bash
git clone https://github.com/Cascalio-Studio/spool-coder.git
cd spool-coder
```

2. Install the dependencies:

```bash
pip install -e .
```

Or alternatively with requirements.txt:

```bash
pip install -r requirements.txt
```

### Installation for Developers

For developers who want to work on the project:

```bash
pip install -e ".[dev]"
```

This installs additional development tools like pytest, black, flake8, etc.

## Connecting the NFC Reader Device

> Note: The NFC reader device is still under development. This guide will be updated when the device is available.

1. Connect the NFC reader device to a free USB port on your computer
2. Wait until the operating system has recognized the device
3. Make note of the COM port (Windows) or device path (Linux/macOS) where the device is available

## Starting the Application

After successful installation, the application can be started as follows:

### As an Installed Package

If you installed the application with `pip install -e .`:

```bash
spool-coder
```

### Directly from the Source Code

```bash
cd spool-coder
python src/main.py
```

## Troubleshooting

### Python Not Found

Make sure Python is installed correctly and is in your PATH:

- Windows: Open Control Panel > System > Advanced System Settings > Environment Variables and check if the Python installation path is included in the PATH variable
- macOS/Linux: Run `which python3` to check if Python is installed correctly

### PyQt6 Not Found

If you encounter issues with PyQt6:

```bash
pip install PyQt6
```

### NFC Reader Device Not Recognized

1. Check the USB connection
2. Windows: Check the Device Manager to ensure the device was recognized
3. Linux: Run `dmesg | grep tty` after connecting the device to find the device path
4. Make sure you have the necessary permissions to access serial ports:
   - Windows: Run as administrator
   - Linux: Add your user to the `dialout` group: `sudo usermod -a -G dialout $USER` and then restart
