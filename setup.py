from setuptools import setup, find_packages

setup(
    name="spool-coder",
    version="0.1.0",
    description="Software zum Auslesen und Umprogrammieren von NFC Spulen für Bambulab Filament Rollen",
    author="Cascalio-Studio",
    author_email="your-email@example.com",  # Ersetzen Sie dies durch Ihre E-Mail-Adresse
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    python_requires=">=3.8",
    install_requires=[
        "pyserial",  # Für die serielle Kommunikation mit dem NFC-Gerät
        "PyQt6",     # Für die GUI
        "pynfc",     # Für NFC-Funktionalität (möglicherweise benötigt)
        "pyusb",     # Für USB-Kommunikation
        "pillow",    # Für Bildverarbeitung in der UI
    ],
    extras_require={
        "dev": [
            "pytest",
            "pytest-cov",
            "black",
            "flake8",
            "mypy",
        ],
        "docs": [
            "sphinx",
            "sphinx-rtd-theme",
        ],
    },
    entry_points={
        "console_scripts": [
            "spool-coder=main:main",
        ],
    },
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: End Users/Desktop",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Topic :: Utilities",
    ],
)
