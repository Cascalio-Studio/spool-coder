#!/usr/bin/env python
"""
Unit test for the startup screen functionality
"""

import sys
import os
import unittest
from PyQt6.QtWidgets import QApplication
from PyQt6.QtCore import Qt, QTimer

# Add src to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', 'src'))

class TestStartupScreen(unittest.TestCase):
    """Test suite for startup screen"""
    
    @classmethod
    def setUpClass(cls):
        """Set up test class with QApplication"""
        if not QApplication.instance():
            cls.app = QApplication(sys.argv)
        else:
            cls.app = QApplication.instance()
    
    def test_startup_screen_creation(self):
        """Test that startup screen can be created with tasks"""
        from src.ui.components.startup_screen import StartupScreen
        
        test_tasks = [
            ("Loading Configuration", None),
            ("Initializing UI", None),
            ("Setting up NFC Services", None),
            ("Ready", None)
        ]
        
        startup = StartupScreen(test_tasks)
        self.assertIsNotNone(startup)
        self.assertEqual(len(startup.initialization_tasks), 4)
    
    def test_startup_screen_signals(self):
        """Test that startup screen has required signals"""
        from src.ui.components.startup_screen import StartupScreen
        
        startup = StartupScreen()
        self.assertTrue(hasattr(startup, 'startup_complete'))
    
    def test_default_tasks(self):
        """Test that default tasks are created when none provided"""
        from src.ui.components.startup_screen import StartupScreen
        
        startup = StartupScreen()
        self.assertGreater(len(startup.initialization_tasks), 0)

if __name__ == "__main__":
    unittest.main()
