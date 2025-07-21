#!/usr/bin/env python
"""
Haupteintrittspunkt für die Spool-Coder Anwendung
"""

import sys
import os
from PyQt6.QtWidgets import QApplication
from PyQt6.QtCore import Qt
from src.ui.views.main_window import MainWindow
from src.ui.components.startup_screen import StartupManager

def initialize_nfc_services():
    """Initialize NFC services and check device availability"""
    try:
        # Import and initialize NFC services
        from src.services.nfc.device import NFCDevice
        from src.services.nfc.bambu_algorithm import BambuLabNFCDecoder
        
        # Test device detection (in simulation mode if no hardware)
        nfc_device = NFCDevice()
        decoder = BambuLabNFCDecoder()
        
        # Additional initialization can be added here
        return True
    except Exception as e:
        print(f"NFC service initialization warning: {e}")
        return False

def initialize_ui_components():
    """Initialize UI components and themes"""
    try:
        # Pre-load UI components
        from src.ui.views import read_view, write_view, demo_view, info_view
        from src.ui.dialogs import nfc_device_dialog
        from src.ui.components import filament_detail_widget
        return True
    except Exception as e:
        print(f"UI component initialization warning: {e}")
        return False

def initialize_configuration():
    """Initialize application configuration"""
    try:
        # Set up environment variables and configuration
        if not os.getenv("SIMULATION_MODE"):
            os.environ["SIMULATION_MODE"] = "True"
        
        # Additional configuration setup
        return True
    except Exception as e:
        print(f"Configuration initialization warning: {e}")
        return False

def get_initialization_tasks():
    """Get the list of initialization tasks for the startup screen"""
    return [
        ("Configuration", initialize_configuration),
        ("UI Components", initialize_ui_components),
        ("NFC Services", initialize_nfc_services),
        ("Bambu Algorithm", lambda: __import__('src.services.nfc.bambu_algorithm', fromlist=[''])),
        ("Python Environment", lambda: sys.version_info),
        ("Application Ready", None)
    ]

def main():
    """
    Hauptfunktion zum Starten der Anwendung
    """    # Create QApplication
    app = QApplication(sys.argv)
    app.setApplicationName("Spool-Coder")
    app.setOrganizationName("Cascalio-Studio")
    
    # Set application icon (if available)
    # app.setWindowIcon(QIcon("path/to/icon.png"))
    
    # Note: In PyQt6, high DPI scaling is enabled by default
    # No need to manually set AA_EnableHighDpiScaling or AA_UseHighDpiPixmaps
    
    # Create startup manager with initialization tasks
    startup_manager = StartupManager(
        app=app,
        main_window_class=MainWindow,
        initialization_tasks=get_initialization_tasks()
    )
    
    # Start the application with startup screen
    startup_manager.start_application()
    
    # Run the application
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
