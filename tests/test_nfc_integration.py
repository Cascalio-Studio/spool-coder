"""
Integration test for NFCDevice with SpoolDecoder.
Tests the integration between the device reading and spool decoding.
"""

import pytest
from src.services.nfc.device import NFCDevice
from src.models.filament import FilamentSpool


class TestNFCDeviceIntegration:
    """Test NFCDevice integration with SpoolDecoder."""
    
    @pytest.fixture
    def device(self):
        """Create an NFCDevice instance for testing."""
        device = NFCDevice()
        device.connect()  # Simulate connection
        return device
    
    def test_read_tag_returns_filament_spool(self, device):
        """Test that read_tag returns a properly decoded FilamentSpool object."""
        result = device.read_tag()
        
        assert result is not None, "read_tag should return a FilamentSpool object"
        assert isinstance(result, FilamentSpool), "Result should be a FilamentSpool instance"
        assert result.name == "Bambu PLA", "Name should match simulated data"
        assert result.type == "PLA", "Type should match simulated data"
        assert result.manufacturer == "Bambulab", "Manufacturer should match simulated data"
    
    def test_write_tag_accepts_filament_spool(self, device):
        """Test that write_tag accepts FilamentSpool objects."""
        # Create a test spool
        test_spool = FilamentSpool(
            name="Test Spool",
            type="PETG",
            manufacturer="Test Corp"
        )
        
        # Write should succeed
        result = device.write_tag(test_spool)
        assert result is True, "write_tag should succeed with FilamentSpool object"
    
    def test_write_tag_accepts_dict(self, device):
        """Test that write_tag still accepts dictionary data."""
        test_data = {
            "name": "Test Dict Spool",
            "type": "ABS",
            "manufacturer": "Dict Corp"
        }
        
        result = device.write_tag(test_data)
        assert result is True, "write_tag should succeed with dict object"
    
    def test_disconnected_device_behavior(self):
        """Test behavior when device is not connected."""
        device = NFCDevice()
        # Don't connect the device
        
        assert device.read_tag() is None, "Disconnected device should return None on read"
        assert device.write_tag({}) is False, "Disconnected device should return False on write"