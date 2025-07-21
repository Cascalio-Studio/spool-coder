#!/usr/bin/env python
"""
Visual test for the startup screen layout
"""

import sys
from PyQt6.QtWidgets import QApplication
from PyQt6.QtCore import QTimer
from src.ui.components.startup_screen import StartupScreen

def show_startup_screen_test():
    """Show the startup screen for a few seconds for visual verification"""
    app = QApplication(sys.argv)
    
    # Create startup screen with test tasks that will show progress
    startup = StartupScreen([
        ("Configuration", lambda: None),
        ("UI Components", lambda: None), 
        ("NFC Services", lambda: None),
        ("Bambu Algorithm", lambda: None),
        ("Testing Layout", lambda: None),
        ("Finalizing", lambda: None)
    ])
    
    print("Showing startup screen with progress animation...")
    print("You should see:")
    print("- Larger window (500x400)")
    print("- Properly sized logo (80x80)")
    print("- Clear, readable text")
    print("- Visible progress bar")
    print("- Status text updates")
    print("- Good spacing between elements")
    
    def close_after_delay():
        print("Visual test completed!")
        startup.close()
        app.quit()
    
    # Show the startup screen with actual progress
    startup.show_and_initialize()
    
    # Close after 8 seconds to see full progress
    QTimer.singleShot(8000, close_after_delay)
    
    app.exec()

if __name__ == "__main__":
    show_startup_screen_test()
