#!/usr/bin/env python
"""
Haupteintrittspunkt für die Spool-Coder Anwendung
"""

import sys
from PyQt6.QtWidgets import QApplication
from ui.views.main_window import MainWindow

def main():
    """
    Hauptfunktion zum Starten der Anwendung
    """
    app = QApplication(sys.argv)
    app.setApplicationName("Spool-Coder")
    app.setOrganizationName("Cascalio-Studio")
    
    window = MainWindow()
    window.show()
    
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
