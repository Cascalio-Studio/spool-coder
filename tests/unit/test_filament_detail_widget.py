"""
Tests for the FilamentDetailWidget UI component
"""
import unittest
from unittest.mock import patch, MagicMock
from PyQt6.QtWidgets import QApplication
from PyQt6.QtGui import QColor
import sys

# Create a QApplication instance for tests
app = QApplication.instance()
if not app:
    app = QApplication(sys.argv)

from src.ui.components.filament_detail_widget import FilamentDetailWidget
from src.models.filament import FilamentSpool

class TestFilamentDetailWidget(unittest.TestCase):
    """Test cases for the FilamentDetailWidget class"""
    
    def setUp(self):
        """Set up test cases"""
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
        
        # Create FilamentDetailWidget instance for testing
        self.widget = FilamentDetailWidget()
    
    def tearDown(self):
        """Clean up after each test"""
        self.widget.deleteLater()
    
    def test_init(self):
        """Test initialization of FilamentDetailWidget"""
        # Test if all form fields are created
        self.assertIsNotNone(self.widget.name_edit)
        self.assertIsNotNone(self.widget.type_combo)
        self.assertIsNotNone(self.widget.color_button)
        self.assertIsNotNone(self.widget.manufacturer_edit)
        self.assertIsNotNone(self.widget.density_spin)
        self.assertIsNotNone(self.widget.diameter_combo)
        self.assertIsNotNone(self.widget.nozzle_temp_spin)
        self.assertIsNotNone(self.widget.bed_temp_spin)
        self.assertIsNotNone(self.widget.remaining_length_spin)
        self.assertIsNotNone(self.widget.remaining_weight_spin)
        
    def test_fill_form(self):
        """Test filling the form with FilamentSpool data"""
        self.widget.fill_form(self.test_spool)
        
        # Check if form fields are filled with correct data
        self.assertEqual(self.widget.name_edit.text(), "Test PLA")
        self.assertEqual(self.widget.type_combo.currentText(), "PLA")
        self.assertEqual(self.widget.manufacturer_edit.text(), "TestMaker")
        self.assertEqual(self.widget.density_spin.value(), 1.24)
        self.assertEqual(self.widget.diameter_combo.currentText(), "1.75")
        self.assertEqual(self.widget.nozzle_temp_spin.value(), 210)
        self.assertEqual(self.widget.bed_temp_spin.value(), 60)
        self.assertEqual(self.widget.remaining_length_spin.value(), 240)
        self.assertEqual(self.widget.remaining_weight_spin.value(), 1000)
        
        # Check color button
        color = QColor(self.test_spool.color)
        button_color = self.widget.color_button.palette().button().color()
        self.assertEqual(button_color.name(), color.name())
    
    def test_get_form_data(self):
        """Test getting form data as FilamentSpool"""
        # Fill the form first
        self.widget.fill_form(self.test_spool)
        
        # Get the data
        result_spool = self.widget.get_form_data()
        
        # Check if result spool has correct data
        self.assertEqual(result_spool.name, "Test PLA")
        self.assertEqual(result_spool.type, "PLA")
        self.assertEqual(result_spool.color, "#00ff00")  # Color may be normalized to lowercase
        self.assertEqual(result_spool.manufacturer, "TestMaker")
        self.assertEqual(result_spool.density, 1.24)
        self.assertEqual(result_spool.diameter, 1.75)
        self.assertEqual(result_spool.nozzle_temp, 210)
        self.assertEqual(result_spool.bed_temp, 60)
        self.assertEqual(result_spool.remaining_length, 240)
        self.assertEqual(result_spool.remaining_weight, 1000)
    
    def test_clear_form(self):
        """Test clearing the form"""
        # Fill the form first
        self.widget.fill_form(self.test_spool)
        
        # Clear the form
        self.widget.clear_form()
        
        # Check if form is cleared
        self.assertEqual(self.widget.name_edit.text(), "")
        self.assertEqual(self.widget.manufacturer_edit.text(), "")
        self.assertEqual(self.widget.density_spin.value(), 1.0)  # Default value
        self.assertEqual(self.widget.nozzle_temp_spin.value(), 200)  # Default value
        self.assertEqual(self.widget.bed_temp_spin.value(), 60)  # Default value
        self.assertEqual(self.widget.remaining_length_spin.value(), 0)  # Default value
        self.assertEqual(self.widget.remaining_weight_spin.value(), 0)  # Default value

if __name__ == "__main__":
    unittest.main()
