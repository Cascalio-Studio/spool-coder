#!/usr/bin/env python3
"""
Spool-Coder Main Application Entry Point

This is the main entry point for the Spool-Coder application.
It initializes the GUI and starts the application.
"""

import sys
import os

# Add the src directory to the Python path
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))

from PyQt6.QtWidgets import QApplication
from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtGui import QIcon

from ui.views.main_window import MainWindow
from ui.components.startup_screen import StartupManager


def setup_application():
    """Setup the QApplication with proper settings"""
    # Enable high DPI support
    QApplication.setHighDpiScaleFactorRoundingPolicy(
        Qt.HighDpiScaleFactorRoundingPolicy.PassThrough
    )
    
    app = QApplication(sys.argv)
    app.setApplicationName("Spool-Coder")
    app.setApplicationVersion("0.1.1")
    app.setOrganizationName("Cascalio Studio")
    app.setOrganizationDomain("cascalio.studio")
    
    # Set application icon if available
    try:
        icon_path = os.path.join(os.path.dirname(__file__), '..', 'ui', 'assets', 'logo_startup.svg')
        if os.path.exists(icon_path):
            app.setWindowIcon(QIcon(icon_path))
    except Exception as e:
        print(f"Could not load application icon: {e}")
    
    return app


def get_initialization_tasks():
    """Define initialization tasks for the startup screen"""
    def init_nfc_services():
        """Initialize NFC services"""
        try:
            from services.nfc.device import NFCDevice
            # Initialize NFC device detection
            pass
        except ImportError as e:
            print(f"NFC services not available: {e}")
    
    def init_bambu_algorithm():
        """Initialize Bambu Lab algorithm"""
        try:
            from services.nfc.bambu_algorithm import BambuAlgorithm
            # Initialize algorithm components
            pass
        except ImportError as e:
            print(f"Bambu algorithm not available: {e}")
    
    def init_ui_components():
        """Initialize UI components"""
        try:
            from ui.views.main_window import MainWindow
            # Pre-load UI components
            pass
        except ImportError as e:
            print(f"UI components not fully available: {e}")
    
    return [
        ("Python Environment", lambda: None),
        ("UI Components", init_ui_components),
        ("NFC Services", init_nfc_services),
        ("Bambu Algorithm", init_bambu_algorithm),
        ("Configuration", lambda: None),
        ("Application Ready", lambda: None)
    ]


def main():
    """Main application entry point"""
    try:
        # Setup Qt Application
        app = setup_application()
        
        # Get initialization tasks
        init_tasks = get_initialization_tasks()
        
        # Create startup manager
        startup_manager = StartupManager(
            app=app,
            main_window_class=MainWindow,
            initialization_tasks=init_tasks
        )
        
        # Start the application with startup screen
        startup_manager.start_application()
        
        # Run the application
        sys.exit(app.exec())
        
    except Exception as e:
        print(f"Critical error starting application: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
