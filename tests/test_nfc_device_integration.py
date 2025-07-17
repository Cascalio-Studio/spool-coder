"""
Integration test for NFCDevice with minimum-length payload
"""

import pytest
import sys
import os

# Add src directory to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from services.nfc.device import NFCDevice
from services.nfc.decoder import NFCDecoder
from models.filament import FilamentSpool


class TestNFCDeviceIntegration:
    """
    Test suite for NFCDevice integration with minimum-length payload decoding
    """
    
    def test_nfc_device_decode_minimum_payload(self):
        """
        Test that NFCDevice can decode minimum-length payload using the decoder
        """
        device = NFCDevice()
        device.connect()
        
        # Get minimum payload
        min_payload = NFCDecoder.get_minimum_valid_payload()
        
        # Decode using device
        decoded_spool = device.decode_tag_data(min_payload)
        
        # Verify successful decoding
        assert decoded_spool is not None, "Device should decode minimum payload"
        assert isinstance(decoded_spool, FilamentSpool), "Should return FilamentSpool"
        
        # Verify basic fields
        assert decoded_spool.type == "PLA"
        assert decoded_spool.color == "#000"
        assert decoded_spool.density == 1
        assert decoded_spool.diameter == 1
    
    def test_nfc_device_raw_read_integration(self):
        """
        Test full integration: read raw data and decode it
        """
        device = NFCDevice()
        device.connect()
        
        # Read raw data (simulated)
        raw_data = device.read_tag_raw()
        assert raw_data is not None, "Should read raw data"
        
        # Decode the raw data
        decoded_spool = device.decode_tag_data(raw_data)
        assert decoded_spool is not None, "Should decode raw data"
        assert isinstance(decoded_spool, FilamentSpool), "Should return FilamentSpool"
        
        # Verify this is the simulated data from device.py
        assert decoded_spool.name == "Bambu PLA"
        assert decoded_spool.type == "PLA"
        assert decoded_spool.manufacturer == "Bambulab"