"""
Test for decoding ABS spool tag data
"""

import unittest
import sys
import os

# Add src directory to Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from services.nfc.decoder import SpoolTagDecoder
from models.filament import FilamentSpool


class TestABSSpoolTagDecoding(unittest.TestCase):
    """
    Test decoding of ABS spool tag data
    """
    
    def setUp(self):
        """Set up test fixtures"""
        self.decoder = SpoolTagDecoder()
    
    def test_decode_abs_spool_tag(self):
        """
        Test: Decode ABS Spool Tag
        
        Purpose: Test decoding of ABS spool tag data.
        Input: Raw NFC payload from ABS spool.
        Steps:
        1. Call decoding function/module with ABS payload.
        Expected Output:
        - Decoded material = 'ABS'
        - Correct spool info extracted
        """
        # Step 1: Create sample ABS payload
        abs_payload = SpoolTagDecoder.create_sample_abs_payload()
        
        # Step 1: Call decoding function with ABS payload
        decoded_spool = SpoolTagDecoder.decode_spool_data(abs_payload)
        
        # Verify decoding was successful
        self.assertIsNotNone(decoded_spool, "Decoding should return a FilamentSpool object")
        self.assertIsInstance(decoded_spool, FilamentSpool, "Result should be a FilamentSpool instance")
        
        # Expected Output: Decoded material = 'ABS'
        self.assertEqual(decoded_spool.type, 'ABS', "Decoded material should be 'ABS'")
        
        # Expected Output: Correct spool info extracted
        self.assertEqual(decoded_spool.manufacturer, 'Bambulab', "Manufacturer should be 'Bambulab'")
        self.assertEqual(decoded_spool.name, 'Bambu ABS', "Name should be 'Bambu ABS'")
        self.assertEqual(decoded_spool.density, 1.04, "ABS density should be 1.04 g/cm³")
        self.assertEqual(decoded_spool.diameter, 1.75, "Diameter should be 1.75 mm")
        self.assertEqual(decoded_spool.nozzle_temp, 240, "Nozzle temperature should be 240°C for ABS")
        self.assertEqual(decoded_spool.bed_temp, 80, "Bed temperature should be 80°C for ABS")
        
        # Verify color was decoded correctly (FF6432 = RGB(255,100,50))
        self.assertEqual(decoded_spool.color, '#FF6432', "Color should be decoded correctly")
        
        # Verify weight was decoded correctly
        self.assertEqual(decoded_spool.remaining_weight, 1000, "Remaining weight should be 1000g")
    
    def test_decode_abs_from_hex_string(self):
        """
        Test decoding ABS payload from hex string format
        """
        # Create hex string representation of ABS payload
        abs_payload = SpoolTagDecoder.create_sample_abs_payload()
        hex_payload = abs_payload.hex()
        
        # Decode from hex string
        decoded_spool = SpoolTagDecoder.decode_spool_data(hex_payload)
        
        # Verify ABS material was decoded correctly
        self.assertIsNotNone(decoded_spool)
        self.assertEqual(decoded_spool.type, 'ABS')
        self.assertEqual(decoded_spool.nozzle_temp, 240)
        self.assertEqual(decoded_spool.bed_temp, 80)
    
    def test_decode_invalid_payload(self):
        """
        Test handling of invalid payloads
        """
        # Test with empty payload
        result = SpoolTagDecoder.decode_spool_data(b'')
        self.assertIsNone(result, "Empty payload should return None")
        
        # Test with too short payload
        result = SpoolTagDecoder.decode_spool_data(b'\x02\x01')
        self.assertIsNone(result, "Too short payload should return None")
        
        # Test with invalid hex string
        result = SpoolTagDecoder.decode_spool_data("invalid_hex")
        self.assertIsNone(result, "Invalid hex string should return None")
    
    def test_abs_material_properties(self):
        """
        Test that ABS material properties are correctly set
        """
        abs_payload = SpoolTagDecoder.create_sample_abs_payload()
        decoded_spool = SpoolTagDecoder.decode_spool_data(abs_payload)
        
        # ABS specific properties
        self.assertEqual(decoded_spool.type, 'ABS')
        self.assertGreaterEqual(decoded_spool.nozzle_temp, 230, "ABS nozzle temp should be >= 230°C")
        self.assertLessEqual(decoded_spool.nozzle_temp, 260, "ABS nozzle temp should be <= 260°C")
        self.assertGreaterEqual(decoded_spool.bed_temp, 70, "ABS bed temp should be >= 70°C")
        self.assertLessEqual(decoded_spool.bed_temp, 100, "ABS bed temp should be <= 100°C")
        self.assertEqual(decoded_spool.density, 1.04, "ABS density should be 1.04 g/cm³")


if __name__ == '__main__':
    unittest.main()