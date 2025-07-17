"""
Tests for NFC spool tag decoding functionality
"""

import sys
import os

# Add src to path so we can import modules
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from models.filament import FilamentSpool  # noqa: E402
from services.nfc.decoder import decode_nfc_payload  # noqa: E402


class TestNFCDecoder:
    """Test cases for NFC decoder functionality"""

    def test_decode_pla_spool_tag(self):
        """
        Test: Decode PLA Spool Tag

        Purpose: Verify decoding of standard PLA spool tag data.
        Input: Raw NFC payload from PLA spool.
        Expected Output:
        - Decoded material = 'PLA'
        - Correct spool info extracted
        """
        # Raw NFC payload representing a PLA spool (simplified hex format)
        # This simulates the actual NFC data that would be read from a
        # BambuLab PLA spool
        raw_nfc_payload = bytes.fromhex(
            "504C41"          # "PLA" material type
            "FF0000"          # Red color (hex)
            "0834"            # Nozzle temp 2100 (210°C encoded as 2100/10)
            "003C"            # Bed temp 60°C
            "00F0"            # Remaining length 240m
            "03E8"            # Remaining weight 1000g
            "42616D6275"      # "Bambu" manufacturer (ASCII)
        )

        # Call the decoding function
        decoded_spool = decode_nfc_payload(raw_nfc_payload)

        # Verify decoded data
        assert decoded_spool is not None, \
            "Decoder should return a FilamentSpool object"
        assert isinstance(decoded_spool, FilamentSpool), \
            "Should return FilamentSpool instance"

        # Verify material type is correctly decoded as PLA
        assert decoded_spool.type == "PLA", \
            f"Expected material 'PLA', got '{decoded_spool.type}'"

        # Verify other spool info is correctly extracted
        assert decoded_spool.nozzle_temp == 210, \
            f"Expected nozzle temp 210, got {decoded_spool.nozzle_temp}"
        assert decoded_spool.bed_temp == 60, \
            f"Expected bed temp 60, got {decoded_spool.bed_temp}"
        assert decoded_spool.remaining_length == 240, \
            f"Expected length 240, got {decoded_spool.remaining_length}"
        assert decoded_spool.remaining_weight == 1000, \
            f"Expected weight 1000, got {decoded_spool.remaining_weight}"
        assert decoded_spool.color == "#FF0000", \
            f"Expected color #FF0000, got {decoded_spool.color}"
        assert "Bambu" in decoded_spool.manufacturer, \
            f"Expected manufacturer to contain 'Bambu', " \
            f"got '{decoded_spool.manufacturer}'"

    def test_decode_invalid_payload(self):
        """Test decoder handles invalid payloads gracefully"""
        # Test with empty payload
        result = decode_nfc_payload(b"")
        assert result is None, "Empty payload should return None"

        # Test with malformed payload
        result = decode_nfc_payload(b"invalid")
        assert result is None, "Invalid payload should return None"

    def test_decode_none_payload(self):
        """Test decoder handles None input gracefully"""
        result = decode_nfc_payload(None)
        assert result is None, "None payload should return None"
