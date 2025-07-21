"""
Unit test for the key derivation function from the Bambu-Research-Group repository.
"""

import sys
import os
import binascii
import unittest

# Add the src directory to the path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'src')))

class TestKeyDerivation(unittest.TestCase):
    """Test suite for key derivation functionality"""
    
    def setUp(self):
        """Set up test fixtures"""
        # Import our key derivation module
        from src.services.nfc.bambu_key import derive_bambu_key, CRYPTODOME_AVAILABLE
        from src.services.nfc.bambu_algorithm import BambuLabNFCEncoder, BambuLabNFCDecoder
        
        self.derive_bambu_key = derive_bambu_key
        self.CRYPTODOME_AVAILABLE = CRYPTODOME_AVAILABLE
        self.BambuLabNFCEncoder = BambuLabNFCEncoder
        self.BambuLabNFCDecoder = BambuLabNFCDecoder
    
    def test_key_derivation_basic(self):
        """Test basic key derivation functionality"""
        # Sample UID
        uid = bytes.fromhex("11223344")
        
        # Derive key
        key = self.derive_bambu_key(uid)
        
        self.assertIsInstance(key, bytes)
        self.assertGreater(len(key), 0)
        self.assertEqual(uid.hex().upper(), "11223344")
    
    def test_cryptodome_availability(self):
        """Test that pycryptodomex is available"""
        self.assertTrue(self.CRYPTODOME_AVAILABLE, "pycryptodomex should be available")
    
    def test_encoder_decoder_consistency(self):
        """Test that encoder and decoder use consistent keys"""
        uid = bytes.fromhex("11223344")
        
        encoder = self.BambuLabNFCEncoder(tag_uid=uid)
        decoder = self.BambuLabNFCDecoder(tag_uid=uid)
        
        # Keys should be the same
        self.assertEqual(encoder._xor_key, decoder._xor_key)
    
    def test_different_uids_different_keys(self):
        """Test that different UIDs produce different keys"""
        uid1 = bytes.fromhex("11223344")
        uid2 = bytes.fromhex("44332211")
        
        key1 = self.derive_bambu_key(uid1)
        key2 = self.derive_bambu_key(uid2)
        
        self.assertNotEqual(key1, key2)
    
    def test_bambu_example_uid(self):
        """Test with the example UID from the Bambu research"""
        uid = bytes.fromhex("75886B1D")
        key = self.derive_bambu_key(uid)
        
        # This should match the first key from the original deriveKeys.py
        expected_start = "6E5B0EC6EF7C"
        actual_key_hex = key.hex().upper()
        
        self.assertTrue(actual_key_hex.startswith(expected_start),
                       f"Expected key to start with {expected_start}, got {actual_key_hex}")

if __name__ == "__main__":
    unittest.main()
