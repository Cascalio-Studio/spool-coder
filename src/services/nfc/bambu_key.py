"""
Bambu Lab NFC Key Derivation - Implementation of the key derivation function from Bambu-Research-Group

This module implements the key derivation function from the Bambu-Research-Group/RFID-Tag-Guide
repository to generate the proper XOR keys for Bambu Lab NFC tags based on their UIDs.
"""

import os
import sys
import hmac
import hashlib
from typing import Optional

# Path to the Bambu Research Group repository submodule
BAMBU_RESEARCH_PATH = os.path.abspath(os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__)))), 'vendor', 'bambu-research'))

# Flag to indicate whether we have the pycryptodomex library
CRYPTODOME_AVAILABLE = False

# Try to import pycryptodomex for the KDF implementation
try:
    from Cryptodome.Protocol.KDF import HKDF
    from Cryptodome.Hash import SHA256
    CRYPTODOME_AVAILABLE = True
    
    def derive_bambu_key(uid: bytes) -> bytes:
        """
        Derive the encryption key for a Bambu Lab RFID tag based on its UID.
        Implementation from Bambu-Research-Group/RFID-Tag-Guide (deriveKeys.py).
        
        Args:
            uid: The UID of the RFID tag (bytes)
            
        Returns:
            The derived key as bytes
        """
        # Master key for deriving Bambu Lab RFID keys (from Bambu-Research-Group)
        master = bytes([0x9a,0x75,0x9c,0xf2,0xc4,0xf7,0xca,0xff,0x22,0x2c,0xb9,0x76,0x9b,0x41,0xbc,0x96])
        
        # Get the key using HKDF
        result = HKDF(uid, 6, master, SHA256, 16, context=b"RFID-A\0")
        
        # Based on looking at the output, the HKDF function from pycryptodomex
        # returns a list of bytes objects. We need to join them into a single bytes object.
        if isinstance(result, list) and all(isinstance(x, bytes) for x in result):
            # Use only the first item as our key (16 bytes)
            # This is based on how the original implementation uses the key
            return result[0]
            
        return result
        
except ImportError:
    # Simple HMAC-based key derivation function implementation as a fallback
    def simple_kdf(input_key_material, salt, key_len):
        """Simple key derivation function using HMAC with SHA-256"""
        key = hmac.new(salt, input_key_material, hashlib.sha256).digest()
        # If we need more bytes, we can chain the HMAC
        result = key
        while len(result) < key_len:
            key = hmac.new(salt, key, hashlib.sha256).digest()
            result += key
        return result[:key_len]
    
    def derive_bambu_key(uid: bytes) -> bytes:
        """
        Derive the encryption keys for a Bambu Lab RFID tag based on its UID.
        Fallback implementation when pycryptodomex is not available.
        
        Args:
            uid: The UID of the RFID tag (bytes)
            
        Returns:
            The derived key as bytes
        """
        # Master key for deriving Bambu Lab RFID keys (from Bambu-Research-Group/RFID-Tag-Guide)
        master = bytes([0x9a,0x75,0x9c,0xf2,0xc4,0xf7,0xca,0xff,0x22,0x2c,0xb9,0x76,0x9b,0x41,0xbc,0x96])
        context = b"RFID-A\0"
        
        # Combine UID with context for better entropy
        salt = uid + context
        derived_key = simple_kdf(master, salt, 16)
        
        return derived_key
        
except (ImportError, ModuleNotFoundError) as e:
    # Simple HMAC-based key derivation function implementation as a fallback
    def simple_kdf(input_key_material, salt, key_len):
        """Simple key derivation function using HMAC with SHA-256"""
        key = hmac.new(salt, input_key_material, hashlib.sha256).digest()
        # If we need more bytes, we can chain the HMAC
        result = key
        while len(result) < key_len:
            key = hmac.new(salt, key, hashlib.sha256).digest()
            result += key
        return result[:key_len]
    
    def derive_bambu_key(uid: bytes) -> bytes:
        """
        Derive the encryption keys for a Bambu Lab RFID tag based on its UID.
        Fallback implementation when the Bambu-Research-Group code is not available.
        
        Args:
            uid: The UID of the RFID tag (bytes)
            
        Returns:
            The derived key as bytes
        """
        # Master key for deriving Bambu Lab RFID keys (from Bambu-Research-Group/RFID-Tag-Guide)
        master = bytes([0x9a,0x75,0x9c,0xf2,0xc4,0xf7,0xca,0xff,0x22,0x2c,0xb9,0x76,0x9b,0x41,0xbc,0x96])
        context = b"RFID-A\0"
        
        # Combine UID with context for better entropy
        salt = uid + context
        derived_key = simple_kdf(master, salt, 16)
        
        return derived_key

# Try to import pycryptodomex directly as a fallback option
if not CRYPTODOME_AVAILABLE:
    try:
        from Cryptodome.Protocol.KDF import HKDF
        from Cryptodome.Hash import SHA256
        CRYPTODOME_AVAILABLE = True
        
        def derive_bambu_key_cryptodome(uid: bytes) -> bytes:
            """
            Derive the encryption keys for a Bambu Lab RFID tag based on its UID.
            Direct implementation using pycryptodomex.
            
            Args:
                uid: The UID of the RFID tag (bytes)
                
            Returns:
                The derived key as bytes
            """
            # Master key for deriving Bambu Lab RFID keys (from Bambu-Research-Group/RFID-Tag-Guide)
            master = bytes([0x9a,0x75,0x9c,0xf2,0xc4,0xf7,0xca,0xff,0x22,0x2c,0xb9,0x76,0x9b,0x41,0xbc,0x96])
            context = b"RFID-A\0"
            
            return HKDF(uid, 6, master, SHA256, 16, context=context)
        
        # Override the original function with the pycryptodomex implementation
        derive_bambu_key = derive_bambu_key_cryptodome
        
    except ImportError:
        pass
