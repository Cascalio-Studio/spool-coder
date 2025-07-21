"""
Tests for the NFCDevice service
"""
import unittest
from unittest.mock import patch, MagicMock
from src.services.nfc.device import NFCDevice

class TestNFCDevice(unittest.TestCase):
    """Test cases for the NFCDevice class"""
    
    def setUp(self):
        """Set up test cases"""
        # Create an NFC device for testing
        self.device = NFCDevice(port="TEST_PORT")
        # Enable testing mode to ensure consistent behavior
        self.device._testing_mode = True
        
        # Sample data for testing
        self.test_data = {
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
    
    def test_init(self):
        """Test initialization of NFCDevice"""
        self.assertEqual(self.device.port, "TEST_PORT")
        self.assertFalse(self.device.connected)
    
    def test_connect_disconnect(self):
        """Test connect and disconnect methods"""
        # Test connect
        result = self.device.connect()
        self.assertTrue(result)
        self.assertTrue(self.device.connected)
        
        # Test disconnect
        self.device.disconnect()
        self.assertFalse(self.device.connected)
    
    def test_is_connected(self):
        """Test is_connected method"""
        self.assertFalse(self.device.is_connected())
        
        self.device.connected = True
        self.assertTrue(self.device.is_connected())
        
        self.device.connected = False
        self.assertFalse(self.device.is_connected())
    
    def test_read_tag_when_not_connected(self):
        """Test reading a tag when not connected"""
        self.device.connected = False
        result = self.device.read_tag()
        self.assertIsNone(result)
    
    def test_read_tag_when_connected(self):
        """Test reading a tag when connected"""
        self.device.connected = True
        result = self.device.read_tag()
        
        # Since this is a simulation, we should get a dictionary back
        self.assertIsNotNone(result)
        self.assertIsInstance(result, dict)
        
        # Check if required keys are present
        self.assertIn("name", result)
        self.assertIn("type", result)
        self.assertIn("color", result)
        self.assertIn("manufacturer", result)
    
    def test_write_tag_when_not_connected(self):
        """Test writing a tag when not connected"""
        self.device.connected = False
        result = self.device.write_tag(self.test_data)
        self.assertFalse(result)
    
    def test_write_tag_when_connected(self):
        """Test writing a tag when connected"""
        self.device.connected = True
        result = self.device.write_tag(self.test_data)
        
        # Since this is a simulation, we should get True
        self.assertTrue(result)

if __name__ == "__main__":
    unittest.main()
