"""
Test for minimum-length NFC tag decoding
"""

import pytest
import sys
import os

# Add src directory to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from services.nfc.decoder import NFCDecoder
from models.filament import FilamentSpool


class TestMinimumLengthNFCTag:
    """
    Test suite for minimum-length valid NFC tag decoding
    """
    
    def test_minimum_length_payload_decoding(self):
        """
        Test: Verify decoding works with minimum-length valid NFC tag
        
        Purpose: Verify decoding works with minimum-length valid NFC tag.
        Input: Shortest valid NFC payload according to spec.
        Expected Output:
        - Decoding succeeds
        - All required fields populated
        """
        # Get minimum-length valid payload
        payload = NFCDecoder.get_minimum_valid_payload()
        
        # Verify payload is actually minimal (should be quite short)
        assert len(payload) < 200, f"Payload too long for minimum: {len(payload)} bytes"
        
        # Call decoding function with minimum-length payload
        decoded_spool = NFCDecoder.decode_payload(payload)
        
        # Verify decoding succeeds
        assert decoded_spool is not None, "Decoding should succeed for minimum valid payload"
        assert isinstance(decoded_spool, FilamentSpool), "Should return FilamentSpool object"
        
        # Verify all required fields are populated
        assert decoded_spool.name is not None, "Name should be populated"
        assert decoded_spool.type is not None and decoded_spool.type != "", "Type should be populated"
        assert decoded_spool.color is not None and decoded_spool.color != "", "Color should be populated"
        assert decoded_spool.manufacturer is not None, "Manufacturer should be populated"
        assert decoded_spool.density is not None, "Density should be populated"
        assert decoded_spool.diameter is not None, "Diameter should be populated"
        assert decoded_spool.nozzle_temp is not None, "Nozzle temp should be populated"
        assert decoded_spool.bed_temp is not None, "Bed temp should be populated"
        assert decoded_spool.remaining_length is not None, "Remaining length should be populated"
        assert decoded_spool.remaining_weight is not None, "Remaining weight should be populated"
        
        # Verify minimum valid values are as expected
        assert decoded_spool.name == "", "Name should be minimal empty string"
        assert decoded_spool.type == "PLA", "Type should be 'PLA'"
        assert decoded_spool.color == "#000", "Color should be minimal '#000'"
        assert decoded_spool.manufacturer == "", "Manufacturer should be minimal empty string"
        assert decoded_spool.density == 1, "Density should be 1"
        assert decoded_spool.diameter == 1, "Diameter should be 1"
        assert decoded_spool.nozzle_temp == 0, "Nozzle temp should be 0"
        assert decoded_spool.bed_temp == 0, "Bed temp should be 0"
        assert decoded_spool.remaining_length == 0, "Remaining length should be 0"
        assert decoded_spool.remaining_weight == 0, "Remaining weight should be 0"
    
    def test_payload_length_is_truly_minimal(self):
        """
        Test that the minimum payload is actually minimal by verifying 
        any shorter valid payload is impossible
        """
        payload = NFCDecoder.get_minimum_valid_payload()
        
        # Verify this is a reasonably short payload
        assert len(payload) < 200, f"Minimum payload should be under 200 bytes, got {len(payload)}"
        
        # Decode the payload to ensure it's valid
        decoded = NFCDecoder.decode_payload(payload)
        assert decoded is not None, "Minimum payload should decode successfully"
        
        # Check that the payload contains all required fields
        payload_str = payload.decode('utf-8')
        for field in NFCDecoder.REQUIRED_FIELDS.keys():
            assert field in payload_str, f"Required field '{field}' should be in payload"
    
    def test_invalid_payloads_fail_decoding(self):
        """
        Test that invalid or incomplete payloads fail decoding gracefully
        """
        # Test empty payload
        assert NFCDecoder.decode_payload(b"") is None
        
        # Test invalid JSON
        assert NFCDecoder.decode_payload(b"invalid json") is None
        
        # Test missing required field
        incomplete_payload = b'{"name":"A","type":"PLA"}'  # Missing other required fields
        assert NFCDecoder.decode_payload(incomplete_payload) is None
        
        # Test wrong data types
        wrong_types_payload = b'{"name":123,"type":"PLA","color":"#FFF","manufacturer":"B","density":"wrong","diameter":1.0,"nozzle_temp":0,"bed_temp":0,"remaining_length":0,"remaining_weight":0}'
        assert NFCDecoder.decode_payload(wrong_types_payload) is None
    
    def test_roundtrip_encoding_decoding(self):
        """
        Test that a decoded minimum payload can be converted back to dict and maintains data integrity
        """
        payload = NFCDecoder.get_minimum_valid_payload()
        decoded_spool = NFCDecoder.decode_payload(payload)
        
        assert decoded_spool is not None
        
        # Convert back to dict
        spool_dict = decoded_spool.to_dict()
        
        # Verify all data is preserved
        assert spool_dict["name"] == ""
        assert spool_dict["type"] == "PLA"
        assert spool_dict["color"] == "#000"
        assert spool_dict["manufacturer"] == ""
        assert spool_dict["density"] == 1
        assert spool_dict["diameter"] == 1
        assert spool_dict["nozzle_temp"] == 0
        assert spool_dict["bed_temp"] == 0
        assert spool_dict["remaining_length"] == 0
        assert spool_dict["remaining_weight"] == 0