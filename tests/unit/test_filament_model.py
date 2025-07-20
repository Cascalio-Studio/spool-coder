"""
Tests for the FilamentSpool model
"""
import unittest
from src.models.filament import FilamentSpool

class TestFilamentSpool(unittest.TestCase):
    """Test cases for the FilamentSpool class"""
    
    def setUp(self):
        """Set up test cases"""
        # Create a sample FilamentSpool for testing
        self.test_spool = FilamentSpool(
            name="Test PLA",
            type="PLA",
            color="#FF0000",
            manufacturer="TestMaker",
            density=1.24,
            diameter=1.75,
            nozzle_temp=210,
            bed_temp=60,
            remaining_length=240,
            remaining_weight=1000
        )
        
        # Sample data dictionary
        self.test_data = {
            "name": "Test PETG",
            "type": "PETG",
            "color": "#0000FF",
            "manufacturer": "TestMaker",
            "density": 1.27,
            "diameter": 1.75,
            "nozzle_temp": 230,
            "bed_temp": 80,
            "remaining_length": 235,
            "remaining_weight": 950
        }
    
    def test_init(self):
        """Test initialization of FilamentSpool"""
        self.assertEqual(self.test_spool.name, "Test PLA")
        self.assertEqual(self.test_spool.type, "PLA")
        self.assertEqual(self.test_spool.color, "#FF0000")
        self.assertEqual(self.test_spool.manufacturer, "TestMaker")
        self.assertEqual(self.test_spool.density, 1.24)
        self.assertEqual(self.test_spool.diameter, 1.75)
        self.assertEqual(self.test_spool.nozzle_temp, 210)
        self.assertEqual(self.test_spool.bed_temp, 60)
        self.assertEqual(self.test_spool.remaining_length, 240)
        self.assertEqual(self.test_spool.remaining_weight, 1000)
    
    def test_to_dict(self):
        """Test conversion of FilamentSpool to dictionary"""
        spool_dict = self.test_spool.to_dict()
        
        # Check if all expected keys are present
        self.assertIn("name", spool_dict)
        self.assertIn("type", spool_dict)
        self.assertIn("color", spool_dict)
        self.assertIn("manufacturer", spool_dict)
        self.assertIn("density", spool_dict)
        self.assertIn("diameter", spool_dict)
        self.assertIn("nozzle_temp", spool_dict)
        self.assertIn("bed_temp", spool_dict)
        self.assertIn("remaining_length", spool_dict)
        self.assertIn("remaining_weight", spool_dict)
        
        # Check if values match
        self.assertEqual(spool_dict["name"], "Test PLA")
        self.assertEqual(spool_dict["type"], "PLA")
        self.assertEqual(spool_dict["color"], "#FF0000")
    
    def test_from_dict(self):
        """Test creation of FilamentSpool from dictionary"""
        spool = FilamentSpool.from_dict(self.test_data)
        
        self.assertEqual(spool.name, "Test PETG")
        self.assertEqual(spool.type, "PETG")
        self.assertEqual(spool.color, "#0000FF")
        self.assertEqual(spool.manufacturer, "TestMaker")
        self.assertEqual(spool.density, 1.27)
        self.assertEqual(spool.diameter, 1.75)
        self.assertEqual(spool.nozzle_temp, 230)
        self.assertEqual(spool.bed_temp, 80)
        self.assertEqual(spool.remaining_length, 235)
        self.assertEqual(spool.remaining_weight, 950)
    
    def test_from_dict_with_missing_values(self):
        """Test creation of FilamentSpool from incomplete dictionary"""
        # Dictionary with missing values
        incomplete_data = {
            "name": "Minimal PLA",
            "type": "PLA"
        }
        
        spool = FilamentSpool.from_dict(incomplete_data)
        
        # Check that specified values are used
        self.assertEqual(spool.name, "Minimal PLA")
        self.assertEqual(spool.type, "PLA")
        
        # Check that default values are used for missing keys
        self.assertEqual(spool.color, "#FFFFFF")  # Default from from_dict
        self.assertEqual(spool.manufacturer, "")   # Default from from_dict
        self.assertEqual(spool.density, 1.24)      # Default from from_dict
        self.assertEqual(spool.diameter, 1.75)     # Default from from_dict

if __name__ == "__main__":
    unittest.main()
