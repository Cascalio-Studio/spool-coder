"""
Test the key derivation function imported from the Bambu-Research-Group repository.
"""

import sys
import os
import binascii

# Add the src directory to the path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), 'src')))

# Import our key derivation module
from src.services.nfc.bambu_key import derive_bambu_key, CRYPTODOME_AVAILABLE
from src.services.nfc.bambu_algorithm import BambuLabNFCEncoder, BambuLabNFCDecoder

def test_key_derivation():
    print("Testing Bambu key derivation...")
    
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
    test_key_derivation()
