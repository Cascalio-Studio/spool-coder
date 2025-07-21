#!/usr/bin/env python
"""
Unit test for startup screen components functionality
"""

import sys
import os
import unittest
from PyQt6.QtWidgets import QApplication
from PyQt6.QtCore import QTimer

# Add src to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', 'src'))

class TestStartupComponents(unittest.TestCase):
    """Test suite for startup screen components"""
    
    @classmethod
    def setUpClass(cls):
        """Set up test class with QApplication"""
        if not QApplication.instance():
            cls.app = QApplication(sys.argv)
        else:
            cls.app = QApplication.instance()
    
    def test_startup_imports(self):
        """Test that startup screen components can be imported"""
        try:
            from src.ui.components.startup_screen import StartupManager, StartupScreen
            from src.ui.views.main_window import MainWindow
            self.assertTrue(True, "All imports successful")
        except ImportError as e:
            self.fail(f"Import failed: {e}")
    
    def test_startup_manager_creation(self):
        """Test StartupManager can be created"""
        from src.ui.components.startup_screen import StartupManager
        from src.ui.views.main_window import MainWindow
        
        startup_manager = StartupManager(
            app=self.app,
            main_window_class=MainWindow,
            initialization_tasks=[("Test Task", None)]
        )
        self.assertIsNotNone(startup_manager)
    
    def test_startup_screen_creation(self):
        """Test StartupScreen can be created"""
        from src.ui.components.startup_screen import StartupScreen
        
        startup_screen = StartupScreen([("Test Task", None)])
        self.assertIsNotNone(startup_screen)
        self.assertEqual(startup_screen.width(), 500)
        self.assertEqual(startup_screen.height(), 400)

def test_startup_functionality():
    """Legacy function for backwards compatibility"""
    unittest.main()

if __name__ == "__main__":
    unittest.main()
