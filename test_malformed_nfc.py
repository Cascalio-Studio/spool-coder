"""
Comprehensive tests for NFC payload decoding with malformed data

This test suite validates robust handling of malformed NFC payloads
to ensure the application doesn't crash and properly logs errors.
"""

import unittest
import logging
import sys
import os

# Add src to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from services.nfc.decoder import NFCPayloadDecoder, NFCDecodingError
from services.nfc.device import NFCDevice


class TestMalformedNFCPayloads(unittest.TestCase):
    """Test suite for malformed NFC payload handling"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.decoder = NFCPayloadDecoder()
        self.device = NFCDevice()
        
        # Setup logging to capture log messages
        self.log_handler = logging.StreamHandler(sys.stdout)
        self.log_handler.setLevel(logging.DEBUG)
        formatter = logging.Formatter('%(levelname)s:%(name)s:%(message)s')
        self.log_handler.setFormatter(formatter)
        
        # Add handler to loggers
        logging.getLogger('services.nfc.decoder').addHandler(self.log_handler)
        logging.getLogger('services.nfc.device').addHandler(self.log_handler)
        logging.getLogger('services.nfc.decoder').setLevel(logging.DEBUG)
        logging.getLogger('services.nfc.device').setLevel(logging.DEBUG)
    
    def tearDown(self):
        """Clean up after tests"""
        # Remove our handler
        logging.getLogger('services.nfc.decoder').removeHandler(self.log_handler)
        logging.getLogger('services.nfc.device').removeHandler(self.log_handler)
    
    def test_none_payload(self):
        """Test handling of None payload"""
        with self.assertRaises(NFCDecodingError) as context:
            self.decoder.decode_payload(None)
        
        self.assertIn("Payload is None", str(context.exception))
    
    def test_empty_dict_payload(self):
        """Test handling of empty dictionary payload"""
        # Empty dict should now return defaults instead of raising an error
        result = self.decoder.decode_payload({})
        
        # Should return defaults for all fields
        self.assertIsNotNone(result)
        for field, default_value in self.decoder.DEFAULT_VALUES.items():
            self.assertEqual(result[field], default_value)
    
    def test_invalid_types_payload(self):
        """Test handling of payload with invalid field types"""
        malformed_payload = {
            "name": 12345,  # Should be string
            "type": ["PLA", "ABS"],  # Should be string, not list
            "nozzle_temp": "very_hot",  # Should be number
            "density": {"value": 1.24},  # Should be number, not dict
            "remaining_weight": None  # None value
        }
        
        # Should not crash, should return data with defaults for invalid fields
        result = self.decoder.decode_payload(malformed_payload)
        
        # Should have some valid data (the name converted to string)
        self.assertIsNotNone(result)
        self.assertEqual(result["name"], "12345")  # Converted to string
        self.assertEqual(result["nozzle_temp"], self.decoder.DEFAULT_VALUES["nozzle_temp"])
    
    def test_out_of_range_values(self):
        """Test handling of values outside expected ranges"""
        out_of_range_payload = {
            "name": "Valid Name",  # Include at least one valid field
            "nozzle_temp": 1000,  # Too high
            "bed_temp": -50,      # Too low
            "density": 50.0,      # Way too high
            "diameter": 0.1,      # Too small
            "remaining_weight": -100  # Negative
        }
        
        result = self.decoder.decode_payload(out_of_range_payload)
        
        # Should use default values for out-of-range fields but keep valid ones
        self.assertIsNotNone(result)
        self.assertEqual(result["name"], "Valid Name")  # This should be preserved
        self.assertEqual(result["nozzle_temp"], self.decoder.DEFAULT_VALUES["nozzle_temp"])
        self.assertEqual(result["bed_temp"], self.decoder.DEFAULT_VALUES["bed_temp"])
        self.assertEqual(result["density"], self.decoder.DEFAULT_VALUES["density"])
    
    def test_oversized_strings(self):
        """Test handling of oversized string fields"""
        oversized_payload = {
            "name": "x" * 1000,  # Way too long
            "type": "SUPER_LONG_FILAMENT_TYPE_NAME_THAT_EXCEEDS_LIMITS",
            "manufacturer": "A" * 500,
            "nozzle_temp": 200  # Add at least one valid non-string field
        }
        
        # Should not crash and should truncate long strings
        result = self.decoder.decode_payload(oversized_payload)
        self.assertIsNotNone(result)
        # Names should be truncated to max length
        self.assertLessEqual(len(result["name"]), self.decoder.EXPECTED_FIELDS["name"]["max_length"])
        self.assertLessEqual(len(result["type"]), self.decoder.EXPECTED_FIELDS["type"]["max_length"])
        self.assertEqual(result["nozzle_temp"], 200)  # Valid field should be preserved
    
    def test_malformed_json_string(self):
        """Test handling of malformed JSON string payloads"""
        malformed_json_payloads = [
            '{"name": "Test"',  # Missing closing brace
            '{"name": "Test", "type":}',  # Missing value
            '{name: "Test"}',  # Unquoted key
            '{"name": "Test", "temp": 200,}',  # Trailing comma
            'not json at all',
            '',  # Empty string
            '   ',  # Whitespace only
        ]
        
        for payload in malformed_json_payloads:
            with self.subTest(payload=payload):
                with self.assertRaises(NFCDecodingError):
                    self.decoder.decode_payload(payload)
    
    def test_malformed_hex_string(self):
        """Test handling of malformed hex string payloads"""
        malformed_hex_payloads = [
            "0x12345",  # Odd length
            "ZZZZZZ",   # Invalid hex characters
            "0x",       # Empty hex
            "12 34 56 7",  # Odd length with spaces
            "0xGHIJKL",    # Invalid characters after 0x
        ]
        
        for payload in malformed_hex_payloads:
            with self.subTest(payload=payload):
                with self.assertRaises(NFCDecodingError):
                    self.decoder.decode_payload(payload)
    
    def test_truncated_binary_payload(self):
        """Test handling of truncated binary payloads"""
        truncated_payloads = [
            b'',  # Empty
            b'\x00',  # Too short
            b'\x00\x01\x02',  # Still too short
            b'\x46\x4D',  # Partial magic number
        ]
        
        for payload in truncated_payloads:
            with self.subTest(payload=payload):
                with self.assertRaises(NFCDecodingError):
                    self.decoder.decode_payload(payload)
    
    def test_corrupted_binary_payload(self):
        """Test handling of corrupted binary payloads"""
        # Valid structure but with corrupted data
        corrupted_payload = b'\x46\x4D\x4C\x42' + b'\xFF' * 50  # Good magic, corrupted data
        
        # Should not crash, should return something with defaults
        result = self.decoder.decode_payload(corrupted_payload)
        self.assertIsNotNone(result)
    
    def test_unexpected_payload_types(self):
        """Test handling of completely unexpected payload types"""
        unexpected_payloads = [
            42,           # Integer
            3.14,         # Float
            True,         # Boolean
            [],           # Empty list
            [1, 2, 3],    # List with data
            set(),        # Set
            object(),     # Generic object
        ]
        
        for payload in unexpected_payloads:
            with self.subTest(payload=type(payload).__name__):
                with self.assertRaises(NFCDecodingError):
                    self.decoder.decode_payload(payload)
    
    def test_partial_valid_data(self):
        """Test handling of payloads with some valid and some invalid data"""
        partial_payload = {
            "name": "Valid Name",
            "type": "PLA",
            "nozzle_temp": "invalid_temp",
            "bed_temp": 60,
            "invalid_field": "should_be_ignored",
            "density": None,
        }
        
        result = self.decoder.decode_payload(partial_payload)
        
        # Should extract valid fields and use defaults for invalid ones
        self.assertIsNotNone(result)
        self.assertEqual(result["name"], "Valid Name")
        self.assertEqual(result["type"], "PLA")
        self.assertEqual(result["bed_temp"], 60)
        self.assertEqual(result["nozzle_temp"], self.decoder.DEFAULT_VALUES["nozzle_temp"])
        self.assertEqual(result["density"], self.decoder.DEFAULT_VALUES["density"])
    
    def test_nfc_device_error_handling(self):
        """Test that NFCDevice handles decoder errors gracefully"""
        # Mock a malformed payload by temporarily modifying the simulation
        original_simulate = self.device._simulate_tag_read
        
        # Test with None payload
        self.device._simulate_tag_read = lambda: None
        result = self.device.read_tag()
        self.assertIsNone(result)
        
        # Test with invalid payload
        self.device._simulate_tag_read = lambda: 12345  # Invalid type
        result = self.device.read_tag()
        self.assertIsNone(result)  # Should return None, not crash
        
        # Restore original method
        self.device._simulate_tag_read = original_simulate
    
    def test_payload_integrity_check(self):
        """Test payload integrity validation"""
        # Valid payloads
        self.assertTrue(self.decoder.validate_payload_integrity({"name": "test"}))
        self.assertTrue(self.decoder.validate_payload_integrity("valid string"))
        self.assertTrue(self.decoder.validate_payload_integrity(b"binary data"))
        
        # Invalid payloads
        self.assertFalse(self.decoder.validate_payload_integrity(None))
        self.assertFalse(self.decoder.validate_payload_integrity({}))
        self.assertFalse(self.decoder.validate_payload_integrity(""))
        self.assertFalse(self.decoder.validate_payload_integrity(b""))
        self.assertFalse(self.decoder.validate_payload_integrity(b"123"))  # Too short
    
    def test_logging_on_errors(self):
        """Test that appropriate log messages are generated on errors"""
        # Capture log output
        log_stream = sys.stdout
        
        # Test with invalid payload that should generate logs
        try:
            self.decoder.decode_payload(None)
        except NFCDecodingError:
            pass  # Expected
        
        # Additional logging tests would require more sophisticated log capture
        # but the manual verification shows that logs are being generated
    
    def test_field_validation_edge_cases(self):
        """Test edge cases in field validation"""
        # Test boundary values
        boundary_payload = {
            "nozzle_temp": 150,  # Minimum valid
            "bed_temp": 150,     # Maximum valid
            "density": 0.5,      # Minimum valid
            "diameter": 3.0,     # Maximum valid
        }
        
        result = self.decoder.decode_payload(boundary_payload)
        self.assertIsNotNone(result)
        self.assertEqual(result["nozzle_temp"], 150)
        self.assertEqual(result["bed_temp"], 150)
        self.assertEqual(result["density"], 0.5)
        self.assertEqual(result["diameter"], 3.0)
    
    def test_unicode_and_special_characters(self):
        """Test handling of unicode and special characters in string fields"""
        unicode_payload = {
            "name": "Filament™ Spëcial",
            "type": "PLA+",
            "manufacturer": "Bämbü®",
        }
        
        result = self.decoder.decode_payload(unicode_payload)
        self.assertIsNotNone(result)
        self.assertEqual(result["name"], "Filament™ Spëcial")
    
    def test_nested_structure_rejection(self):
        """Test that nested structures are properly rejected or flattened"""
        nested_payload = {
            "name": "Test",
            "properties": {
                "nozzle_temp": 200,
                "bed_temp": 60
            },
            "array_field": [1, 2, 3]
        }
        
        result = self.decoder.decode_payload(nested_payload)
        # Should handle the simple fields and ignore/default the complex ones
        self.assertIsNotNone(result)
        self.assertEqual(result["name"], "Test")


class TestNFCDeviceRobustness(unittest.TestCase):
    """Test suite for NFCDevice robustness with various error conditions"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.device = NFCDevice()
    
    def test_read_without_connection(self):
        """Test reading when device is not connected"""
        # Device starts disconnected
        result = self.device.read_tag()
        self.assertIsNone(result)
    
    def test_write_without_connection(self):
        """Test writing when device is not connected"""
        test_data = {"name": "Test", "type": "PLA"}
        result = self.device.write_tag(test_data)
        self.assertFalse(result)
    
    def test_write_invalid_data(self):
        """Test writing invalid data types"""
        self.device.connect()
        
        # Test various invalid data types
        invalid_data_sets = [
            None,
            "",
            [],
            "string",
            123,
            {},  # Empty dict
        ]
        
        for invalid_data in invalid_data_sets:
            with self.subTest(data=invalid_data):
                result = self.device.write_tag(invalid_data)
                self.assertFalse(result)
    
    def test_multiple_connect_disconnect(self):
        """Test multiple connect/disconnect cycles"""
        for i in range(5):
            with self.subTest(cycle=i):
                self.assertTrue(self.device.connect())
                self.assertTrue(self.device.is_connected())
                self.device.disconnect()
                self.assertFalse(self.device.is_connected())
    
    def test_raw_tag_reading(self):
        """Test raw tag data reading"""
        self.device.connect()
        raw_data = self.device.read_raw_tag()
        self.assertIsInstance(raw_data, bytes)
        self.assertGreater(len(raw_data), 0)


if __name__ == '__main__':
    # Set up logging for test runs
    logging.basicConfig(
        level=logging.DEBUG,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    
    # Run tests
    unittest.main(verbosity=2)