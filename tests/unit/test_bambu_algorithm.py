"""
Tests for the BambuLab NFC algorithm
"""
import unittest
import base64
from src.services.nfc.bambu_algorithm import BambuLabNFCEncoder, BambuLabNFCDecoder, SAMPLE_TAG_DATA


class TestBambuLabNFCAlgorithm(unittest.TestCase):
    """Test cases for the BambuLab NFC algorithm"""
    
    def setUp(self):
        """Set up the test case"""
        # Use consistent UID for both encoder and decoder
        self.test_uid = b'\xaa\x55\xcc\x33'
        self.encoder = BambuLabNFCEncoder(tag_uid=self.test_uid)
        self.decoder = BambuLabNFCDecoder()
        self.test_data = SAMPLE_TAG_DATA.copy()
    
    def test_encoder_creates_valid_data(self):
        """Test that the encoder creates a valid data structure"""
        encoded = self.encoder.encode_tag_data(self.test_data)
        
        # Check that the data is not empty
        self.assertIsNotNone(encoded)
        self.assertGreater(len(encoded), 0)
        
        # Check that the data starts with the correct header
        self.assertEqual(encoded[:4], BambuLabNFCDecoder.TAG_HEADER)
    
    def test_encode_decode_roundtrip(self):
        """Test that encoding and then decoding preserves the original data"""
        # Encode the test data
        encoded = self.encoder.encode_tag_data(self.test_data)
        
        # Decode it back
        decoded = self.decoder.decode_tag_data(encoded, tag_uid=self.test_uid)
        
        # Verify the data was preserved
        self.assertIsNotNone(decoded)
        
        # Check spool data fields
        original = self.test_data["spool_data"]
        result = decoded["spool_data"]
        
        self.assertEqual(result["type"], original["type"])
        self.assertEqual(result["color"], original["color"])
        self.assertAlmostEqual(result["diameter"], original["diameter"], places=2)
        self.assertEqual(result["nozzle_temp"], original["nozzle_temp"])
        self.assertEqual(result["bed_temp"], original["bed_temp"])
        self.assertAlmostEqual(result["density"], original["density"], places=3)
        self.assertAlmostEqual(result["remaining_length"], original["remaining_length"], places=1)
        self.assertLessEqual(abs(result["remaining_weight"] - original["remaining_weight"]), 1)  # Allow small rounding differences
        self.assertEqual(result["manufacturer"], original["manufacturer"])
        self.assertEqual(result["name"], original["name"])
        
        # Check manufacturing info
        original_mfg = self.test_data["manufacturing_info"]
        result_mfg = decoded["manufacturing_info"]
        
        self.assertEqual(result_mfg["serial"], original_mfg["serial"])
        self.assertEqual(result_mfg["date"], original_mfg["date"])
    
    def test_data_corruption_detection(self):
        """Test that corrupted data is detected"""
        # Encode the test data
        encoded = self.encoder.encode_tag_data(self.test_data)
        
        # Corrupt the data by changing a byte in the middle
        corrupted = bytearray(encoded)
        corrupted[100] = (corrupted[100] + 1) % 256
        
        # Decoding should fail (return None)
        result = self.decoder.decode_tag_data(bytes(corrupted))
        self.assertIsNone(result)
        
        # But the original should still decode correctly
        result_original = self.decoder.decode_tag_data(encoded, tag_uid=self.test_uid)
        self.assertIsNotNone(result_original)
    
    def test_header_validation(self):
        """Test that the header is correctly validated"""
        # Encode the test data
        encoded = self.encoder.encode_tag_data(self.test_data)
        
        # Corrupt the header
        corrupted = bytearray(encoded)
        corrupted[0] = (corrupted[0] + 1) % 256  # Change the first byte of the header
        
        # Decoding should fail
        result = self.decoder.decode_tag_data(bytes(corrupted))
        self.assertIsNone(result)
    
    def test_various_filament_types(self):
        """Test encoding and decoding various filament types"""
        filament_types = ["PLA", "PETG", "ABS", "TPU", "ASA"]
        
        for filament_type in filament_types:
            # Update test data with this filament type
            self.test_data["spool_data"]["type"] = filament_type
            
            # Encode and decode
            encoded = self.encoder.encode_tag_data(self.test_data)
            decoded = self.decoder.decode_tag_data(encoded, tag_uid=self.test_uid)
            
            # Verify the filament type was preserved
            self.assertEqual(decoded["spool_data"]["type"], filament_type)
    
    def test_base64_encoding_decoding(self):
        """Test base64 encoding and decoding of tag data"""
        # Encode the test data
        encoded = self.encoder.encode_tag_data(self.test_data)
        
        # Convert to base64 (useful for storing in databases or transferring)
        base64_data = base64.b64encode(encoded).decode('ascii')
        self.assertIsNotNone(base64_data)
        
        # Decode from base64
        decoded_bytes = base64.b64decode(base64_data)
        self.assertEqual(decoded_bytes, encoded)
        
        # Parse the decoded data
        result = self.decoder.decode_tag_data(decoded_bytes, tag_uid=self.test_uid)
        self.assertIsNotNone(result)
        self.assertEqual(result["spool_data"]["name"], self.test_data["spool_data"]["name"])


if __name__ == '__main__':
    unittest.main()
