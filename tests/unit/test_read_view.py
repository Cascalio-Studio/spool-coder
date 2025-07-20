"""
Tests for the ReadView UI component
"""
import unittest
from unittest.mock import patch, MagicMock
from PyQt6.QtWidgets import QApplication, QMessageBox
import sys

# Create a QApplication instance for tests
app = QApplication.instance()
if not app:
    app = QApplication(sys.argv)

from src.ui.views.read_view import ReadView
from src.models.filament import FilamentSpool
from src.services.nfc.device import NFCDevice

class TestReadView(unittest.TestCase):
    """Test cases for the ReadView class"""
    
    def setUp(self):
        """Set up test cases"""
        # Mock the NFCDevice
        self.mock_nfc_device = MagicMock(spec=NFCDevice)
        
        # Create a sample FilamentSpool for testing
        self.test_spool_data = {
            "name": "Test PLA",
            "type": "PLA",
            "color": "#00FF00",
            "manufacturer": "TestMaker",
            "density": 1.24,
            "diameter": 1.75,
            "nozzle_temp": 210,
            "bed_temp": 60,
            "remaining_length": 240,
            "remaining_weight": 1000
        }
        
        # Create ReadView instance for testing
        with patch('src.services.nfc.device.NFCDevice', return_value=self.mock_nfc_device):
            self.view = ReadView()
    
    def tearDown(self):
        """Clean up after each test"""
        self.view.deleteLater()
    
    def test_init(self):
        """Test initialization of ReadView"""
        # Test if UI components are created
        self.assertIsNotNone(self.view.title_label)
        self.assertIsNotNone(self.view.back_button)
        self.assertIsNotNone(self.view.connect_button)
        self.assertIsNotNone(self.view.read_button)
        self.assertIsNotNone(self.view.status_label)
        self.assertIsNotNone(self.view.filament_detail_widget)
        
        # Test if NFCDevice is created
        self.assertIsNotNone(self.view.nfc_device)
        
    def test_on_connect_clicked_success(self):
        """Test connect button click with successful connection"""
        # Mock successful connection
        self.mock_nfc_device.connect.return_value = True
        self.mock_nfc_device.is_connected.return_value = True
        
        # Call the connect method
        with patch.object(self.view, 'update_ui') as mock_update_ui:
            self.view.on_connect_clicked()
            
            # Check if connect method was called
            self.mock_nfc_device.connect.assert_called_once()
            
            # Check if UI was updated
            mock_update_ui.assert_called_once()
    
    def test_on_connect_clicked_failure(self):
        """Test connect button click with failed connection"""
        # Mock failed connection
        self.mock_nfc_device.connect.return_value = False
        self.mock_nfc_device.is_connected.return_value = False
        
        # Mock QMessageBox.warning
        with patch('PyQt6.QtWidgets.QMessageBox.warning') as mock_warning:
            self.view.on_connect_clicked()
            
            # Check if connect method was called
            self.mock_nfc_device.connect.assert_called_once()
            
            # Check if warning message was shown
            mock_warning.assert_called_once()
    
    def test_on_read_clicked_success(self):
        """Test read button click with successful read"""
        # Mock successful connection and read
        self.mock_nfc_device.is_connected.return_value = True
        self.mock_nfc_device.read_tag.return_value = self.test_spool_data
        
        # Call the read method
        with patch.object(self.view.filament_detail_widget, 'fill_form') as mock_fill_form:
            self.view.on_read_clicked()
            
            # Check if read_tag method was called
            self.mock_nfc_device.read_tag.assert_called_once()
            
            # Check if form was filled
            mock_fill_form.assert_called_once()
            
            # Check that status label is updated (not empty)
            self.assertNotEqual(self.view.status_label.text(), "")
    
    def test_on_read_clicked_not_connected(self):
        """Test read button click when not connected"""
        # Mock not connected
        self.mock_nfc_device.is_connected.return_value = False
        
        # Call the read method
        with patch('PyQt6.QtWidgets.QMessageBox.warning') as mock_warning:
            self.view.on_read_clicked()
            
            # Check if read_tag method was not called
            self.mock_nfc_device.read_tag.assert_not_called()
            
            # Check if warning message was shown
            mock_warning.assert_called_once()
    
    def test_on_read_clicked_read_failure(self):
        """Test read button click with failed read"""
        # Mock connected but failed read
        self.mock_nfc_device.is_connected.return_value = True
        self.mock_nfc_device.read_tag.return_value = None
        
        # Call the read method
        with patch('PyQt6.QtWidgets.QMessageBox.warning') as mock_warning:
            self.view.on_read_clicked()
            
            # Check if read_tag method was called
            self.mock_nfc_device.read_tag.assert_called_once()
            
            # Check if warning message was shown
            mock_warning.assert_called_once()
    
    def test_update_ui_connected(self):
        """Test UI update when connected"""
        # Mock connected
        self.mock_nfc_device.is_connected.return_value = True
        
        # Update UI
        self.view.update_ui()
        
        # Check button states
        self.assertFalse(self.view.connect_button.isEnabled())
        self.assertTrue(self.view.read_button.isEnabled())
        
        # Check that status label is updated (not empty)
        self.assertNotEqual(self.view.status_label.text(), "")
    
    def test_update_ui_disconnected(self):
        """Test UI update when disconnected"""
        # Mock disconnected
        self.mock_nfc_device.is_connected.return_value = False
        
        # Update UI
        self.view.update_ui()
        
        # Check button states
        self.assertTrue(self.view.connect_button.isEnabled())
        self.assertFalse(self.view.read_button.isEnabled())
        
        # Check that status label is updated (not empty)
        self.assertNotEqual(self.view.status_label.text(), "")

if __name__ == "__main__":
    unittest.main()
