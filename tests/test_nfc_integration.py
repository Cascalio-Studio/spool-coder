"""
Integration tests for NFC device and decoding workflow.

These tests validate the end-to-end NFC reading and decoding process
to ensure the integration between device reading and payload decoding
works correctly.
"""

import pytest
from src.services.nfc.device import NFCDevice
from src.models.filament import FilamentSpool
from tests.test_data import BAMBU_PLA_BASIC, BAMBU_PETG_BASIC


@pytest.mark.integration
class TestNFCDeviceIntegration:
    """
    Integration tests for NFC device reading and payload decoding.
    """

    def test_nfc_device_read_and_decode_workflow(self):
        """
        Test the complete workflow of connecting device, reading tag, and decoding data.
        
        This simulates the actual user workflow and ensures the integration 
        between NFCDevice and FilamentSpool decoding works correctly.
        """
        # Arrange: Create NFC device
        device = NFCDevice()
        
        # Act: Connect and read (simulated)
        assert device.connect() == True, "Device should connect successfully"
        assert device.is_connected() == True, "Device should report as connected"
        
        # Read tag data
        tag_data = device.read_tag()
        assert tag_data is not None, "Should read tag data successfully"
        
        # Decode the data
        spool = FilamentSpool.from_dict(tag_data)
        assert spool is not None, "Should decode spool data successfully"
        assert isinstance(spool, FilamentSpool), "Should return FilamentSpool instance"
        
        # Verify decoded data makes sense
        assert spool.name != "", "Spool should have a name"
        assert spool.type in ["PLA", "PETG", "ABS", "ASA", "TPU", "PC", "PA-CF"], "Should be valid filament type"
        assert spool.nozzle_temp > 0, "Should have valid nozzle temperature"
        assert spool.bed_temp >= 0, "Should have valid bed temperature"
        assert spool.remaining_weight >= 0, "Should have valid remaining weight"
        
        # Clean up
        device.disconnect()
        assert device.is_connected() == False, "Device should be disconnected"

    def test_multiple_read_cycles(self):
        """
        Test multiple read cycles to ensure device and decoding remain stable.
        
        This tests for memory leaks or state issues in repeated operations.
        """
        device = NFCDevice()
        
        for i in range(5):
            # Connect, read, decode, disconnect cycle
            assert device.connect() == True, f"Device should connect on cycle {i}"
            
            tag_data = device.read_tag()
            assert tag_data is not None, f"Should read data on cycle {i}"
            
            spool = FilamentSpool.from_dict(tag_data)
            assert spool is not None, f"Should decode data on cycle {i}"
            
            device.disconnect()
            assert device.is_connected() == False, f"Device should disconnect on cycle {i}"

    def test_device_state_management(self):
        """
        Test that device state is managed correctly during operations.
        """
        device = NFCDevice()
        
        # Initial state
        assert device.is_connected() == False, "Device should start disconnected"
        
        # Reading without connection should return None
        tag_data = device.read_tag()
        assert tag_data is None, "Should not read data when disconnected"
        
        # Connect and verify state
        assert device.connect() == True, "Should connect successfully"
        assert device.is_connected() == True, "Should report connected"
        
        # Now reading should work
        tag_data = device.read_tag()
        assert tag_data is not None, "Should read data when connected"
        
        # Disconnect and verify state
        device.disconnect()
        assert device.is_connected() == False, "Should report disconnected after disconnect"


@pytest.mark.integration  
class TestEndToEndDecoding:
    """
    End-to-end tests that simulate real user scenarios.
    """

    def test_complete_user_read_workflow(self):
        """
        Simulate complete user workflow: connect device -> read spool -> display data.
        
        This test represents the typical user interaction with the application.
        """
        # Step 1: User starts the application and connects to NFC device
        device = NFCDevice()
        connection_success = device.connect()
        assert connection_success, "User should be able to connect to NFC device"
        
        # Step 2: User places spool on reader and initiates read
        tag_data = device.read_tag()
        assert tag_data is not None, "User should get tag data from spool"
        
        # Step 3: Application decodes the data for display
        spool = FilamentSpool.from_dict(tag_data)
        assert spool is not None, "Application should decode spool data"
        
        # Step 4: User sees decoded information
        display_data = spool.to_dict()
        assert "name" in display_data, "Display should include filament name"
        assert "type" in display_data, "Display should include filament type"
        assert "nozzle_temp" in display_data, "Display should include nozzle temperature"
        assert "bed_temp" in display_data, "Display should include bed temperature"
        assert "remaining_weight" in display_data, "Display should include remaining weight"
        
        # Step 5: User disconnects
        device.disconnect()
        assert not device.is_connected(), "User should be able to disconnect"

    def test_error_recovery_workflow(self):
        """
        Test error recovery scenarios in the end-to-end workflow.
        """
        device = NFCDevice()
        
        # Scenario 1: Connection fails initially but succeeds on retry
        # (Simulated - in real implementation, connection always succeeds)
        assert device.connect() == True, "Should eventually connect"
        
        # Scenario 2: Read succeeds after device is connected
        tag_data = device.read_tag()
        assert tag_data is not None, "Should read data after successful connection"
        
        # Scenario 3: Decoding handles any format variations gracefully
        spool = FilamentSpool.from_dict(tag_data)
        assert spool is not None, "Should handle any valid tag format"
        
        device.disconnect()

    def test_data_consistency_across_operations(self):
        """
        Test that data remains consistent across multiple operations.
        """
        device = NFCDevice()
        device.connect()
        
        # Read the same tag multiple times
        readings = []
        for _ in range(3):
            tag_data = device.read_tag()
            readings.append(tag_data)
        
        # All readings should be identical (for simulated data)
        for reading in readings[1:]:
            assert reading == readings[0], "Multiple reads should return consistent data"
        
        # All decodings should produce identical spools
        spools = [FilamentSpool.from_dict(reading) for reading in readings]
        for spool in spools[1:]:
            assert spool.to_dict() == spools[0].to_dict(), "Decoded spools should be identical"
        
        device.disconnect()