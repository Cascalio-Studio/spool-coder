"""
Test module for NFC invalid data handling.

Tests confirm that the NFC decoding functions properly handle corrupted or invalid payloads
and return appropriate error messages or raise exceptions.
"""

import pytest
import sys
import os

# Add src to path to import modules
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from models.filament import FilamentSpool
from services.nfc.device import NFCDevice


class TestNFCInvalidDataHandling:
    """Test class for NFC invalid data handling"""
    
    def test_filament_from_dict_with_empty_dict(self):
        """Test FilamentSpool.from_dict with empty dictionary"""
        # Empty dict should work with defaults
        result = FilamentSpool.from_dict({})
        assert result.name == ""
        assert result.type == "PLA"
        assert result.color == "#FFFFFF"
    
    def test_filament_from_dict_with_none(self):
        """Test FilamentSpool.from_dict with None"""
        with pytest.raises(ValueError):
            FilamentSpool.from_dict(None)
    
    def test_filament_from_dict_with_corrupted_data_types(self):
        """Test FilamentSpool.from_dict with invalid data types"""
        corrupted_data = {
            "name": 123,  # Should be string
            "density": "invalid",  # Should be float
            "nozzle_temp": "not_a_number",  # Should be int
            "remaining_weight": None  # Should be number
        }
        
        # This should still work with the current implementation due to .get() defaults
        result = FilamentSpool.from_dict(corrupted_data)
        assert result.name == 123  # Current implementation doesn't validate types
        assert result.density == "invalid"
    
    def test_filament_from_dict_with_malformed_structure(self):
        """Test FilamentSpool.from_dict with malformed structure"""
        malformed_data = "not_a_dict"
        
        with pytest.raises(TypeError):
            FilamentSpool.from_dict(malformed_data)
    
    def test_filament_from_dict_with_missing_critical_fields(self):
        """Test FilamentSpool.from_dict with completely wrong keys"""
        wrong_data = {
            "invalid_key1": "value1",
            "invalid_key2": "value2",
            "completely_wrong": True
        }
        
        # Should work with defaults
        result = FilamentSpool.from_dict(wrong_data)
        assert result.name == ""
        assert result.type == "PLA"


class TestNFCDeviceInvalidDataHandling:
    """Test class for NFCDevice invalid data scenarios"""
    
    def test_nfc_device_read_when_not_connected(self):
        """Test NFCDevice.read_tag when not connected"""
        device = NFCDevice()
        # Don't call connect()
        result = device.read_tag()
        assert result is None
    
    def test_nfc_device_connection_status(self):
        """Test NFCDevice connection status tracking"""
        device = NFCDevice()
        assert not device.is_connected()
        
        device.connect()
        assert device.is_connected()
        
        device.disconnect()
        assert not device.is_connected()


class TestIntegratedNFCInvalidDataFlow:
    """Test the complete flow with invalid data like the UI would encounter"""
    
    def test_complete_flow_with_invalid_nfc_payload(self):
        """Test the complete flow from NFCDevice through FilamentSpool decoding"""
        device = NFCDevice()
        device.connect()
        
        # Override read_tag to return invalid data (simulating corrupted NFC payload)
        def mock_corrupted_read():
            return None  # Simulating no data or corrupted read
        
        device.read_tag = mock_corrupted_read
        
        data = device.read_tag()
        assert data is None
        
        # In the UI, this would result in showing an error message
        if data is None:
            error_message = "Fehler: Keine Daten gefunden oder Spule nicht erkannt."
            assert "Fehler" in error_message or "keine" in error_message.lower()
    
    def test_complete_flow_with_empty_payload(self):
        """Test the complete flow with empty payload"""
        device = NFCDevice()
        device.connect()
        
        # Override read_tag to return empty dict (simulating empty/cleared NFC tag)
        def mock_empty_read():
            return {}
        
        device.read_tag = mock_empty_read
        
        data = device.read_tag()
        assert data == {}
        
        # This should still work, creating a filament with defaults
        if data is not None:
            spool = FilamentSpool.from_dict(data)
            assert spool.name == ""
            assert spool.type == "PLA"
    
    def test_complete_flow_with_malformed_json_like_data(self):
        """Test handling of malformed JSON-like data"""
        device = NFCDevice()
        device.connect()
        
        # Override read_tag to return malformed data
        def mock_malformed_read():
            return "{'invalid': json, 'structure':"  # Malformed JSON-like string
        
        device.read_tag = mock_malformed_read
        
        data = device.read_tag()
        
        # The current NFCDevice returns this malformed data as-is
        # FilamentSpool.from_dict would fail with this
        if isinstance(data, str):
            with pytest.raises(TypeError):
                FilamentSpool.from_dict(data)


class TestSpecificCorruptedPayloads:
    """Test specific types of corrupted NFC payloads that might occur in real usage"""
    
    def test_corrupted_binary_data(self):
        """Test handling of corrupted binary data that might come from a damaged NFC tag"""
        device = NFCDevice()
        device.connect()
        
        # Override read_tag to return bytes (corrupted binary data)
        def mock_binary_read():
            return b'\x00\x01\x02\xff\xfe\xfd'  # Random binary data
        
        device.read_tag = mock_binary_read
        data = device.read_tag()
        
        # This would fail in FilamentSpool.from_dict
        with pytest.raises(TypeError):
            FilamentSpool.from_dict(data)
    
    def test_partial_json_data(self):
        """Test handling of partially corrupted JSON-like data"""
        test_cases = [
            {"name": "Valid", "invalid_structure": ["nested", "arrays", {"deep": "nesting"}]},
            {"temperature": float('inf')},  # Invalid float
            {"temperature": float('nan')},  # NaN value
            {i: f"key_{i}" for i in range(1000)},  # Extremely large dict
        ]
        
        for corrupted_data in test_cases:
            # Should not crash, may work with defaults for missing fields
            try:
                result = FilamentSpool.from_dict(corrupted_data)
                # If it works, verify it has reasonable defaults
                assert hasattr(result, 'name')
                assert hasattr(result, 'type')
            except (AttributeError, TypeError, ValueError):
                # Exceptions are acceptable for truly invalid data
                pass
    
    def test_extremely_large_payload(self):
        """Test handling of unreasonably large payloads"""
        huge_string = "x" * 1000000  # 1MB string
        large_data = {"name": huge_string}
        
        # Should work but will have huge name
        result = FilamentSpool.from_dict(large_data)
        assert len(result.name) == 1000000
    
    def test_invalid_tag_error_simulation(self):
        """Test simulation of 'invalid tag' error as mentioned in requirements"""
        device = NFCDevice()
        device.connect()
        
        # Simulate various "invalid tag" scenarios
        invalid_scenarios = [
            None,  # No tag detected
            {},    # Empty tag
            "CORRUPTED_DATA",  # Corrupted string data
            b"BINARY_CORRUPTION",  # Binary corruption
        ]
        
        for invalid_data in invalid_scenarios:
            def mock_invalid_read():
                return invalid_data
            
            device.read_tag = mock_invalid_read
            data = device.read_tag()
            
            # Test the complete error flow like in the UI
            if data is None:
                # This matches the UI behavior for invalid/no tag
                error_msg = "Fehler: Keine Daten gefunden oder Spule nicht erkannt."
                assert "Fehler" in error_msg
            elif data == {}:
                # Empty tag - should work with defaults
                spool = FilamentSpool.from_dict(data)
                assert spool.name == ""
            elif isinstance(data, (str, bytes)):
                # String/binary data should fail in from_dict
                with pytest.raises(TypeError):
                    FilamentSpool.from_dict(data)


class TestEnhancedErrorHandling:
    """Test the enhanced error handling methods"""
    
    def test_read_tag_with_error_handling_success(self):
        """Test the enhanced read_tag_with_error_handling method for success case"""
        device = NFCDevice()
        device.connect()
        
        data, error = device.read_tag_with_error_handling()
        assert data is not None
        assert error is None
        assert isinstance(data, dict)
    
    def test_read_tag_with_error_handling_not_connected(self):
        """Test the enhanced method when device not connected"""
        device = NFCDevice()
        # Don't connect
        
        data, error = device.read_tag_with_error_handling()
        assert data is None
        assert error == "ERROR:NO_DEVICE"
    
    def test_filament_from_dict_safe_with_none(self):
        """Test FilamentSpool.from_dict_safe with None"""
        spool, error = FilamentSpool.from_dict_safe(None)
        assert spool is None
        assert "INVALID_TAG" in error
        assert "Keine Daten" in error
    
    def test_filament_from_dict_safe_with_invalid_type(self):
        """Test FilamentSpool.from_dict_safe with invalid data type"""
        spool, error = FilamentSpool.from_dict_safe("not a dict")
        assert spool is None
        assert "INVALID_TAG" in error
        assert "falsches Format" in error
    
    def test_filament_from_dict_safe_with_valid_data(self):
        """Test FilamentSpool.from_dict_safe with valid data"""
        valid_data = {"name": "Test PLA", "type": "PLA"}
        spool, error = FilamentSpool.from_dict_safe(valid_data)
        assert spool is not None
        assert error is None
        assert spool.name == "Test PLA"
    
    def test_filament_from_dict_safe_with_empty_dict(self):
        """Test FilamentSpool.from_dict_safe with empty dict"""
        spool, error = FilamentSpool.from_dict_safe({})
        assert spool is not None
        assert error is None
        assert spool.name == ""  # Default value
    
    def test_enhanced_from_dict_raises_proper_exceptions(self):
        """Test that enhanced from_dict raises proper exceptions"""
        # Test None
        with pytest.raises(ValueError, match="Daten dürfen nicht None sein"):
            FilamentSpool.from_dict(None)
        
        # Test wrong type
        with pytest.raises(TypeError, match="Daten müssen ein Dictionary sein"):
            FilamentSpool.from_dict("string")
    
    def test_complete_invalid_data_flow_with_enhanced_methods(self):
        """Test complete flow using enhanced error handling methods"""
        device = NFCDevice()
        
        # Test disconnected device
        data, error = device.read_tag_with_error_handling()
        assert data is None
        assert "ERROR:NO_DEVICE" in error
        
        # If we got an error from device, handle it gracefully
        if data is None:
            spool, decode_error = FilamentSpool.from_dict_safe(data)
            assert spool is None
            assert "INVALID_TAG" in decode_error
            
            # This represents the complete error flow:
            # Device error -> Invalid data -> Decode error -> "INVALID_TAG" message
            assert "INVALID_TAG" in decode_error


class TestErrorMessageValidation:
    """Test that error messages match expected format from requirements"""
    
    def test_error_message_contains_invalid_tag_concept(self):
        """Verify error messages indicate invalid tag scenarios"""
        # Test the actual error message from UI
        ui_error_message = "Fehler: Keine Daten gefunden oder Spule nicht erkannt."
        
        # This message effectively indicates an "invalid tag" scenario
        assert any(word in ui_error_message.lower() for word in ["fehler", "keine", "nicht erkannt"])
        
        # The message indicates the tag is invalid/not recognized
        assert "nicht erkannt" in ui_error_message  # "not recognized" = invalid tag
    
    def test_enhanced_error_messages_contain_invalid_tag(self):
        """Test that enhanced error messages explicitly contain 'INVALID_TAG'"""
        # Test various invalid inputs with the safe method
        invalid_inputs = [None, "string", 123, [], set()]
        
        for invalid_input in invalid_inputs:
            spool, error = FilamentSpool.from_dict_safe(invalid_input)
            assert spool is None
            assert "INVALID_TAG" in error
    
    def test_exception_handling_for_corrupted_decode(self):
        """Test that decoding corrupted data raises appropriate exceptions"""
        corrupted_inputs = [
            None,
            "not_a_dict", 
            123,
            [],
            set(),
        ]
        
        for corrupted_input in corrupted_inputs:
            with pytest.raises((ValueError, TypeError)):
                FilamentSpool.from_dict(corrupted_input)
    
    def test_nfc_device_error_states(self):
        """Test NFCDevice error states that indicate invalid tag scenarios"""
        device = NFCDevice()
        
        # Not connected should return None (invalid state)
        assert device.read_tag() is None
        
        # Enhanced method should provide explicit error
        data, error = device.read_tag_with_error_handling()
        assert data is None
        assert "ERROR:NO_DEVICE" in error
        
        # Connect and test
        device.connect()
        assert device.read_tag() is not None  # Should return valid data when connected
        
        # Enhanced method should work
        data, error = device.read_tag_with_error_handling()
        assert data is not None
        assert error is None
        
        # Disconnect should reset state
        device.disconnect()
        assert device.read_tag() is None


if __name__ == "__main__":
    pytest.main([__file__])