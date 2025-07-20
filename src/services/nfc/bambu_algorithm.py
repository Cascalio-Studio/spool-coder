"""
Bambu Lab NFC Algorithm - Decode and encode NFC tags for Bambu Lab filament spools

This module implements the algorithm required to decode data from Bambu Lab NFC tags
and encode data for writing to these tags, based on research from the 
Bambu-Research-Group/RFID-Tag-Guide.
"""

import struct
import binascii
from typing import Dict, Optional, List, Tuple, Any, Union
import json
import base64


class BambuLabNFCDecoder:
    """
    Implementation of the Bambu Lab NFC tag decoder based on research from
    https://github.com/Bambu-Research-Group/RFID-Tag-Guide
    
    The tag data format follows a specific structure:
    - Header bytes
    - Encrypted data
    - Checksum
    
    This class handles decryption and parsing of the tag data into usable information.
    """
    
    # Constants for tag decoding
    TAG_HEADER = b'\xaa\x55\xcc\x33'
    # XOR key used by Bambu Lab for basic obfuscation
    import os
    XOR_KEY = bytes.fromhex(os.getenv("BAMBU_XOR_KEY", ""))
    if not XOR_KEY:
        raise ValueError("XOR_KEY is missing or invalid. Please set the BAMBU_XOR_KEY environment variable.")
    
    # Tag data sections
    SPOOL_DATA_OFFSET = 128
    HEADER_SIZE = 16
    CHECKSUM_OFFSET = 512
    CHECKSUM_SIZE = 4
    
    # Known filament types
    FILAMENT_TYPES = {
        0: "PLA Basic",
        1: "PLA",
        2: "PETG Basic",
        3: "PETG",
        4: "ABS",
        5: "TPU",
        6: "PLA-CF",
        7: "PA-CF",
        8: "PET-CF",
        9: "ASA",
        10: "PC",
        11: "PA",
        12: "Support",
        13: "PVA",
        14: "HIPS"
    }
    
    def __init__(self):
        """Initialize the NFC decoder."""
        pass
    
    def decode_tag_data(self, raw_data: bytes) -> Optional[Dict[str, Any]]:
        """
        Decode the raw tag data into a structured format.
        
        Args:
            raw_data: The raw bytes read from the NFC tag
            
        Returns:
            Dictionary with decoded tag data or None if decoding fails
        """
        # Check if data has minimum required length
        if len(raw_data) < 512:
            return None
        
        # Check for valid header
        if not self._verify_header(raw_data):
            return None
        
        # Decrypt the data
        decrypted_data = self._decrypt_data(raw_data)
        
        # Verify the checksum
        if not self._verify_checksum(decrypted_data):
            return None
        
        # Parse the tag data
        return self._parse_tag_data(decrypted_data)
    
    def _verify_header(self, data: bytes) -> bool:
        """
        Verify the tag header matches the expected format.
        
        Args:
            data: Raw tag data
            
        Returns:
            True if header is valid, False otherwise
        """
        return data[:4] == self.TAG_HEADER
    
    def _decrypt_data(self, data: bytes) -> bytes:
        """
        Decrypt (XOR) the tag data.
        
        Args:
            data: Raw tag data
            
        Returns:
            Decrypted tag data
        """
        decrypted = bytearray(data)
        key_len = len(self.XOR_KEY)
        
        # Apply XOR to all data except header
        for i in range(4, len(decrypted)):
            decrypted[i] ^= self.XOR_KEY[(i - 4) % key_len]
            
        return bytes(decrypted)
    
    def _verify_checksum(self, data: bytes) -> bool:
        """
        Verify the checksum in the tag data.
        
        Args:
            data: Decrypted tag data
            
        Returns:
            True if checksum is valid, False otherwise
        """
        # Extract stored checksum (4 bytes at offset 512)
        stored_checksum = struct.unpack("<I", data[self.CHECKSUM_OFFSET:self.CHECKSUM_OFFSET + self.CHECKSUM_SIZE])[0]
        
        # Calculate checksum on all data before the checksum location
        calculated_checksum = binascii.crc32(data[:self.CHECKSUM_OFFSET])
        
        return calculated_checksum == stored_checksum
    
    def _parse_tag_data(self, data: bytes) -> Dict[str, Any]:
        """
        Parse the decrypted tag data into a structured format.
        
        Args:
            data: Decrypted tag data
            
        Returns:
            Dictionary with parsed tag information
        """
        result = {
            "raw_header": data[:self.HEADER_SIZE].hex(),
            "spool_data": {},
            "manufacturing_info": {},
        }
        
        # Parse header (first 16 bytes)
        # - First 4 bytes: Header signature (0xAA55CC33)
        # - Next 4 bytes: Version and flags
        result["version"] = data[4]
        result["flags"] = data[5:8].hex()
        
        # Parse spool data (at offset 128)
        spool_offset = self.SPOOL_DATA_OFFSET
        
        # Extract filament type (2 bytes)
        filament_type_id = struct.unpack("<H", data[spool_offset:spool_offset+2])[0]
        result["spool_data"]["type_id"] = filament_type_id
        result["spool_data"]["type"] = self.FILAMENT_TYPES.get(filament_type_id, "Unknown")
        spool_offset += 2
        
        # Extract color RGB (3 bytes)
        r, g, b = data[spool_offset:spool_offset+3]
        result["spool_data"]["color"] = f"#{r:02X}{g:02X}{b:02X}"
        spool_offset += 3
        
        # Extract filament diameter (4 bytes float)
        diameter = struct.unpack("<f", data[spool_offset:spool_offset+4])[0]
        result["spool_data"]["diameter"] = round(diameter, 2)
        spool_offset += 4
        
        # Extract nozzle temperature (2 bytes)
        nozzle_temp = struct.unpack("<H", data[spool_offset:spool_offset+2])[0]
        result["spool_data"]["nozzle_temp"] = nozzle_temp
        spool_offset += 2
        
        # Extract bed temperature (2 bytes)
        bed_temp = struct.unpack("<H", data[spool_offset:spool_offset+2])[0]
        result["spool_data"]["bed_temp"] = bed_temp
        spool_offset += 2
        
        # Extract material density (4 bytes float)
        density = struct.unpack("<f", data[spool_offset:spool_offset+4])[0]
        result["spool_data"]["density"] = round(density, 3)
        spool_offset += 4
        
        # Extract filament length (4 bytes float, in meters)
        length = struct.unpack("<f", data[spool_offset:spool_offset+4])[0]
        result["spool_data"]["remaining_length"] = round(length, 1)
        spool_offset += 4
        
        # Extract filament weight (4 bytes float, in grams)
        weight = struct.unpack("<f", data[spool_offset:spool_offset+4])[0]
        result["spool_data"]["remaining_weight"] = round(weight)
        spool_offset += 4
        
        # Extract manufacturer and filament name (strings)
        manufacturer_offset = spool_offset
        manufacturer = self._extract_string(data, manufacturer_offset, 32)
        result["spool_data"]["manufacturer"] = manufacturer
        
        filament_name_offset = manufacturer_offset + 32
        filament_name = self._extract_string(data, filament_name_offset, 32)
        result["spool_data"]["name"] = filament_name
        
        # Extract manufacturing information
        mfg_offset = 256
        serial_number = self._extract_string(data, mfg_offset, 32)
        result["manufacturing_info"]["serial"] = serial_number
        
        # Extract manufacturing date (4 bytes, timestamp)
        date_offset = mfg_offset + 32
        mfg_date = struct.unpack("<I", data[date_offset:date_offset+4])[0]
        result["manufacturing_info"]["date"] = mfg_date
        
        return result
    
    def _extract_string(self, data: bytes, offset: int, max_length: int) -> str:
        """
        Extract a null-terminated string from binary data.
        
        Args:
            data: The binary data
            offset: Start position of the string
            max_length: Maximum length of the string
            
        Returns:
            The extracted string
        """
        end_pos = offset
        for i in range(offset, offset + max_length):
            if i >= len(data) or data[i] == 0:
                end_pos = i
                break
                
        return data[offset:end_pos].decode('utf-8', errors='replace')


class BambuLabNFCEncoder:
    """
    Implementation of the Bambu Lab NFC tag encoder
    
    This class handles encoding of filament data into the format expected by
    Bambu Lab printers, including proper encryption and checksums.
    """
    
    # Use same constants as the decoder
    TAG_HEADER = BambuLabNFCDecoder.TAG_HEADER
    XOR_KEY = BambuLabNFCDecoder.XOR_KEY
    SPOOL_DATA_OFFSET = BambuLabNFCDecoder.SPOOL_DATA_OFFSET
    HEADER_SIZE = BambuLabNFCDecoder.HEADER_SIZE
    CHECKSUM_OFFSET = BambuLabNFCDecoder.CHECKSUM_OFFSET
    CHECKSUM_SIZE = BambuLabNFCDecoder.CHECKSUM_SIZE
    FILAMENT_TYPES = {v: k for k, v in BambuLabNFCDecoder.FILAMENT_TYPES.items()}
    
    def __init__(self):
        """Initialize the NFC encoder."""
        pass
    
    def encode_tag_data(self, spool_data: Dict[str, Any]) -> bytes:
        """
        Encode the spool data into the format expected by Bambu Lab printers.
        
        Args:
            spool_data: Dictionary with spool information
            
        Returns:
            Binary data ready to be written to an NFC tag
        """
        # Create a new empty tag buffer (most tags are 1024 bytes)
        tag_buffer = bytearray(1024)
        
        # Set the header
        tag_buffer[:4] = self.TAG_HEADER
        
        # Set version and flags (using defaults if not provided)
        tag_buffer[4] = spool_data.get("version", 1)  # Default to version 1
        tag_buffer[5:8] = bytes.fromhex(spool_data.get("flags", "000000"))  # Default to zeros
        
        # Populate the spool data section
        self._encode_spool_data(tag_buffer, spool_data)
        
        # Populate manufacturing info
        self._encode_manufacturing_info(tag_buffer, spool_data)
        
        # Calculate and insert checksum
        checksum = binascii.crc32(tag_buffer[:self.CHECKSUM_OFFSET])
        struct.pack_into("<I", tag_buffer, self.CHECKSUM_OFFSET, checksum)
        
        # Encrypt the data (except the header)
        self._encrypt_data(tag_buffer)
        
        return bytes(tag_buffer)
    
    def _encode_spool_data(self, buffer: bytearray, spool_data: Dict[str, Any]) -> None:
        """
        Encode the spool data into the buffer.
        
        Args:
            buffer: Buffer to write data into
            spool_data: Dictionary with spool information
        """
        spool_info = spool_data.get("spool_data", {})
        offset = self.SPOOL_DATA_OFFSET
        
        # Encode filament type (2 bytes)
        filament_type_str = spool_info.get("type", "PLA")
        filament_type_id = self.FILAMENT_TYPES.get(filament_type_str, 1)  # Default to PLA (1)
        struct.pack_into("<H", buffer, offset, filament_type_id)
        offset += 2
        
        # Encode color (3 bytes RGB)
        color = spool_info.get("color", "#FFFFFF")
        if color.startswith('#') and len(color) == 7:
            r = int(color[1:3], 16)
            g = int(color[3:5], 16)
            b = int(color[5:7], 16)
        else:
            r, g, b = 255, 255, 255  # Default to white
        buffer[offset:offset+3] = bytes([r, g, b])
        offset += 3
        
        # Encode diameter (4 bytes float)
        diameter = float(spool_info.get("diameter", 1.75))
        struct.pack_into("<f", buffer, offset, diameter)
        offset += 4
        
        # Encode nozzle temperature (2 bytes)
        nozzle_temp = int(spool_info.get("nozzle_temp", 220))
        struct.pack_into("<H", buffer, offset, nozzle_temp)
        offset += 2
        
        # Encode bed temperature (2 bytes)
        bed_temp = int(spool_info.get("bed_temp", 60))
        struct.pack_into("<H", buffer, offset, bed_temp)
        offset += 2
        
        # Encode density (4 bytes float)
        density = float(spool_info.get("density", 1.24))
        struct.pack_into("<f", buffer, offset, density)
        offset += 4
        
        # Encode filament length (4 bytes float)
        length = float(spool_info.get("remaining_length", 240.0))
        struct.pack_into("<f", buffer, offset, length)
        offset += 4
        
        # Encode filament weight (4 bytes float)
        weight = float(spool_info.get("remaining_weight", 1000.0))
        struct.pack_into("<f", buffer, offset, weight)
        offset += 4
        
        # Encode manufacturer (32 bytes string)
        manufacturer = spool_info.get("manufacturer", "")
        self._encode_string(buffer, offset, manufacturer, 32)
        offset += 32
        
        # Encode filament name (32 bytes string)
        name = spool_info.get("name", "")
        self._encode_string(buffer, offset, name, 32)
    
    def _encode_manufacturing_info(self, buffer: bytearray, spool_data: Dict[str, Any]) -> None:
        """
        Encode manufacturing information into the buffer.
        
        Args:
            buffer: Buffer to write data into
            spool_data: Dictionary with spool information
        """
        mfg_info = spool_data.get("manufacturing_info", {})
        offset = 256
        
        # Encode serial number (32 bytes string)
        serial = mfg_info.get("serial", "")
        self._encode_string(buffer, offset, serial, 32)
        offset += 32
        
        # Encode manufacturing date (4 bytes timestamp)
        date = mfg_info.get("date", 0)
        struct.pack_into("<I", buffer, offset, date)
    
    def _encrypt_data(self, buffer: bytearray) -> None:
        """
        Encrypt the data in the buffer using XOR.
        
        Args:
            buffer: Buffer to encrypt
        """
        key_len = len(self.XOR_KEY)
        
        # Apply XOR to all data except the header signature
        for i in range(4, len(buffer)):
            buffer[i] ^= self.XOR_KEY[(i - 4) % key_len]
    
    def _encode_string(self, buffer: bytearray, offset: int, string: str, max_length: int) -> None:
        """
        Encode a string into the buffer with null termination.
        
        Args:
            buffer: Buffer to write data into
            offset: Position to start writing
            string: String to encode
            max_length: Maximum length of the string
        """
        bytes_to_write = string.encode('utf-8')[:max_length-1]
        buffer[offset:offset+len(bytes_to_write)] = bytes_to_write
        buffer[offset+len(bytes_to_write)] = 0  # Null termination


# Sample data for testing
SAMPLE_TAG_DATA = {
    "version": 1,
    "flags": "000000",
    "spool_data": {
        "type": "PLA",
        "color": "#1E88E5",  # Blue
        "diameter": 1.75,
        "nozzle_temp": 220,
        "bed_temp": 60,
        "density": 1.24,
        "remaining_length": 240.0,
        "remaining_weight": 1000.0,
        "manufacturer": "Bambu Lab",
        "name": "Bambu PLA Matte"
    },
    "manufacturing_info": {
        "serial": "BL12345678",
        "date": 1626912000  # July 22, 2021
    }
}


def create_sample_tag_data():
    """
    Create a sample encoded tag data for testing.
    
    Returns:
        Base64 encoded sample tag data
    """
    encoder = BambuLabNFCEncoder()
    encoded_data = encoder.encode_tag_data(SAMPLE_TAG_DATA)
    return base64.b64encode(encoded_data).decode('ascii')


def decode_sample_tag_data(base64_data: str):
    """
    Decode a sample tag data from base64 encoding.
    
    Args:
        base64_data: Base64 encoded tag data
        
    Returns:
        Dictionary with decoded tag information
    """
    decoder = BambuLabNFCDecoder()
    raw_data = base64.b64decode(base64_data)
    return decoder.decode_tag_data(raw_data)


# Example of how to use the encoder and decoder
def test_encoder_decoder():
    """
    Test the encoder and decoder with sample data.
    
    Returns:
        True if the test passes, False otherwise
    """
    print("Creating sample tag data...")
    encoder = BambuLabNFCEncoder()
    encoded_data = encoder.encode_tag_data(SAMPLE_TAG_DATA)
    
    print("Decoding sample tag data...")
    decoder = BambuLabNFCDecoder()
    decoded_data = decoder.decode_tag_data(encoded_data)
    
    if decoded_data:
        print("Successfully decoded tag data:")
        print(json.dumps(decoded_data, indent=2))
        
        # Verify key data points
        original = SAMPLE_TAG_DATA["spool_data"]
        decoded = decoded_data["spool_data"]
        
        checks = [
            original["type"] == decoded["type"],
            original["color"] == decoded["color"],
            abs(original["diameter"] - decoded["diameter"]) < 0.01,
            original["nozzle_temp"] == decoded["nozzle_temp"],
            original["bed_temp"] == decoded["bed_temp"],
            abs(original["density"] - decoded["density"]) < 0.01,
            abs(original["remaining_length"] - decoded["remaining_length"]) < 0.1,
            abs(original["remaining_weight"] - decoded["remaining_weight"]) < 1,
            original["manufacturer"] == decoded["manufacturer"],
            original["name"] == decoded["name"]
        ]
        
        if all(checks):
            print("All data points verified correctly!")
            return True
        else:
            print("Data verification failed!")
            return False
    else:
        print("Failed to decode tag data!")
        return False


if __name__ == "__main__":
    # Run a test of the encoder and decoder
    test_encoder_decoder()
