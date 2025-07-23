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
        self.assertEqual(uid.hex(), "11223344")
    
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

def test_key_derivation():
    """Legacy function for backwards compatibility"""
    # Import required modules
    from src.services.nfc.bambu_key import derive_bambu_key, CRYPTODOME_AVAILABLE
    from src.services.nfc.bambu_algorithm import BambuLabNFCEncoder, BambuLabNFCDecoder
    
    # Sample UID
    uid = bytes.fromhex("11223344")
    
    # Derive key
    key = derive_bambu_key(uid)
    
    print(f"UID: {uid.hex()}")
    print(f"Derived key: {key.hex()}")
    print(f"Using pycryptodomex: {CRYPTODOME_AVAILABLE}")
    
    # Also test the encoder and decoder with the derived key
    print("\nTesting encoder and decoder with derived key...")
    encoder = BambuLabNFCEncoder(tag_uid=uid)
    decoder = BambuLabNFCDecoder(tag_uid=uid)
    
    # Check that they're using the same key
    print(f"Encoder key: {encoder._xor_key.hex()}")
    print(f"Decoder key: {decoder._xor_key.hex()}")
    
    # Now test a full encoding/decoding cycle using the derived key
    print("\nTesting full encode/decode cycle with derived key...")
    from src.services.nfc.bambu_algorithm import SAMPLE_TAG_DATA
    
    # Encode some data
    encoded_data = encoder.encode_tag_data(SAMPLE_TAG_DATA)
    
    # Decode it back
    decoded_data = decoder.decode_tag_data(encoded_data)
    
    # Verify it worked
    if decoded_data:
        print("Successfully decoded tag data with derived key!")
        print(f"Filament type: {decoded_data['spool_data']['type']}")
        print(f"Manufacturer: {decoded_data['spool_data']['manufacturer']}")
        print(f"Name: {decoded_data['spool_data']['name']}")
    else:
        print("Failed to decode tag data with derived key!")
    
    return key

if __name__ == "__main__":
    # Run tests if called directly
    if len(sys.argv) > 1 and sys.argv[1] == "test":
        test_key_derivation()
    else:
        unittest.main()
