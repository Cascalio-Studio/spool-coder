"""
Tests for the MainWindow UI component
"""
import unittest
from unittest.mock import patch, MagicMock
from PyQt6.QtWidgets import QApplication, QStackedWidget, QPushButton, QLabel
from PyQt6.QtGui import QAction
import sys

# Create a QApplication instance for tests
app = QApplication.instance()
if not app:
    app = QApplication(sys.argv)

from src.ui.views.main_window import MainWindow
from src.ui.views.read_view import ReadView
from src.ui.views.write_view import WriteView
from src.ui.views.info_view import InfoView

class TestMainWindow(unittest.TestCase):
    """Test cases for the MainWindow class"""
    
    def setUp(self):
        """Set up test cases"""
        # Create MainWindow instance for testing
        self.main_window = MainWindow()
    
    def tearDown(self):
        """Clean up after each test"""
        self.main_window.close()
    
    def test_init(self):
        """Test initialization of MainWindow"""
        # Test window title
        self.assertEqual(self.main_window.windowTitle(), "Spool-Coder - Bambulab NFC Tool")
        
        # Test central widget exists
        self.assertIsNotNone(self.main_window.central_widget)
        
        # Test if status bar exists
        self.assertIsNotNone(self.main_window.statusBar)
        
        # Test window size (angepasst an neue Mindestgröße)
        self.assertGreaterEqual(self.main_window.minimumSize().width(), 700)
        self.assertGreaterEqual(self.main_window.minimumSize().height(), 550)
        
    def test_ui_components(self):
        """Test UI components of MainWindow"""
        # Check if main layout exists
        self.assertIsNotNone(self.main_window.main_layout)
        
        # Check if buttons are created
        buttons = [widget for widget in self.main_window.findChildren(QPushButton)]
        self.assertGreater(len(buttons), 0, "No buttons found in main window")
        
        # Check if labels are created
        labels = [widget for widget in self.main_window.findChildren(QLabel)]
        self.assertGreater(len(labels), 0, "No labels found in main window")
    
    def test_menu_actions(self):
        """Test menu actions"""
        # Check if menu bar exists (access the menuBar property directly)
        self.assertIsNotNone(self.main_window.menuBar)
        
        # Find QActions in the menu
        actions = [action for action in self.main_window.findChildren(QAction)]
        self.assertGreater(len(actions), 0, "No menu actions found")

if __name__ == "__main__":
    unittest.main()
