"""
Tests for the WriteView UI component
"""
import unittest
from unittest.mock import patch, MagicMock
from PyQt6.QtWidgets import QApplication, QMessageBox
import sys

# Create a QApplication instance for tests
app = QApplication.instance()
if not app:
    app = QApplication(sys.argv)

from src.ui.views.write_view import WriteView
from src.models.filament import FilamentSpool
from src.services.nfc.device import NFCDevice

class TestWriteView(unittest.TestCase):
    """Test cases for the WriteView class"""
    
    def setUp(self):
        """Set up test cases"""
        # Mock the NFCDevice
        self.mock_nfc_device = MagicMock(spec=NFCDevice)
        
        # Create a sample FilamentSpool for testing
        self.test_spool = FilamentSpool(
            name="Test PLA",
            type="PLA",
            color="#00FF00",
            manufacturer="TestMaker",
            density=1.24,
            diameter=1.75,
            nozzle_temp=210,
            bed_temp=60,
            remaining_length=240,
            remaining_weight=1000
        )
        
        # Create WriteView instance for testing
        self.view = WriteView()
        # Replace the nfc_device with our mock after creation
        self.view.nfc_device = self.mock_nfc_device
        # Enable testing mode to skip timer delays
        self.view._testing_mode = True
    
    def tearDown(self):
        """Clean up after each test"""
        self.view.deleteLater()
    
    def test_init(self):
        """Test initialization of WriteView"""
        # Test if UI components are created
        self.assertIsNotNone(self.view.title_label)
        self.assertIsNotNone(self.view.back_button)
        self.assertIsNotNone(self.view.connect_button)
        self.assertIsNotNone(self.view.write_button)
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
    
    def test_on_write_clicked_success(self):
        """Test write button click with successful write"""
        # Mock successful connection and write
        self.mock_nfc_device.is_connected.return_value = True
        self.mock_nfc_device.write_tag.return_value = True
        
        # Prepare form data
        with patch.object(self.view.filament_detail_widget, 'get_form_data', return_value=self.test_spool):
            # Call the write method
            with patch('PyQt6.QtWidgets.QMessageBox.information') as mock_info:
                self.view.on_write_clicked()
                
                # Check if write_tag method was called
                self.mock_nfc_device.write_tag.assert_called_once()
                
                # Check if success message was shown
                mock_info.assert_called_once()
                
                # Check that the status label is not empty (contains some success message)
                self.assertNotEqual(self.view.status_label.text(), "")
    
    def test_on_write_clicked_not_connected(self):
        """Test write button click when not connected"""
        # Mock not connected
        self.mock_nfc_device.is_connected.return_value = False
        
        # Call the write method
        with patch('PyQt6.QtWidgets.QMessageBox.warning') as mock_warning:
            self.view.on_write_clicked()
            
            # Check if write_tag method was not called
            self.mock_nfc_device.write_tag.assert_not_called()
            
            # Check if warning message was shown
            mock_warning.assert_called_once()
    
    def test_on_write_clicked_write_failure(self):
        """Test write button click with failed write"""
        # Mock connected but failed write
        self.mock_nfc_device.is_connected.return_value = True
        self.mock_nfc_device.write_tag.return_value = False
        
        # Prepare form data
        with patch.object(self.view.filament_detail_widget, 'get_form_data', return_value=self.test_spool):
            # Call the write method
            with patch('PyQt6.QtWidgets.QMessageBox.warning') as mock_warning:
                self.view.on_write_clicked()
                
                # Check if write_tag method was called
                self.mock_nfc_device.write_tag.assert_called_once()
                
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
        self.assertTrue(self.view.write_button.isEnabled())
        
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
        self.assertFalse(self.view.write_button.isEnabled())
        
        # Check that status label is updated (not empty)
        self.assertNotEqual(self.view.status_label.text(), "")
    
    def test_on_back_clicked(self):
        """Test back button click"""
        # Mock the parent() method to return a MainWindow mock
        from src.ui.views.main_window import MainWindow
        mock_main_window = MagicMock(spec=MainWindow)
        mock_main_window.show_home = MagicMock()
        
        # Patch the parent method to return our mock
        with patch.object(self.view, 'parent', return_value=mock_main_window):
            # Call back button click
            self.view.on_back_clicked()
            
            # Check if show_home was called
            mock_main_window.show_home.assert_called_once()

if __name__ == "__main__":
    unittest.main()
