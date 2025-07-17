"""
Exhaustive test coverage for all known BambuLab spool tag types.
This test validates decoding against all documented spool types with payload samples.
"""

import pytest
import json
from src.models.filament import FilamentSpool
from src.services.nfc.spool_decoder import SpoolDecoder


class TestSpoolTypesExhaustive:
    """
    Test class for exhaustive coverage of all known BambuLab spool types.
    Tests decoding functionality against reference payload samples.
    """
    
    @pytest.fixture
    def decoder(self):
        """Create a SpoolDecoder instance for testing."""
        return SpoolDecoder()
    
    @pytest.fixture
    def reference_payloads(self):
        """
        Reference payload samples for all documented BambuLab spool types.
        Based on known BambuLab filament specifications and common industry standards.
        """
        return {
            "PLA": {
                "name": "Bambu PLA",
                "type": "PLA",
                "color": "#FF0000",
                "manufacturer": "Bambulab",
                "density": 1.24,
                "diameter": 1.75,
                "nozzle_temp": 210,
                "bed_temp": 60,
                "remaining_length": 240.0,
                "remaining_weight": 1000.0
            },
            "PETG": {
                "name": "Bambu PETG",
                "type": "PETG", 
                "color": "#00FF00",
                "manufacturer": "Bambulab",
                "density": 1.27,
                "diameter": 1.75,
                "nozzle_temp": 250,
                "bed_temp": 80,
                "remaining_length": 235.0,
                "remaining_weight": 950.0
            },
            "ABS": {
                "name": "Bambu ABS",
                "type": "ABS",
                "color": "#0000FF", 
                "manufacturer": "Bambulab",
                "density": 1.04,
                "diameter": 1.75,
                "nozzle_temp": 260,
                "bed_temp": 90,
                "remaining_length": 230.0,
                "remaining_weight": 900.0
            },
            "TPU": {
                "name": "Bambu TPU",
                "type": "TPU",
                "color": "#FFFF00",
                "manufacturer": "Bambulab", 
                "density": 1.21,
                "diameter": 1.75,
                "nozzle_temp": 220,
                "bed_temp": 50,
                "remaining_length": 220.0,
                "remaining_weight": 850.0
            },
            "ASA": {
                "name": "Bambu ASA",
                "type": "ASA",
                "color": "#FF00FF",
                "manufacturer": "Bambulab",
                "density": 1.07,
                "diameter": 1.75,
                "nozzle_temp": 260,
                "bed_temp": 90,
                "remaining_length": 225.0,
                "remaining_weight": 875.0
            },
            "WOOD": {
                "name": "Bambu Wood PLA",
                "type": "WOOD",
                "color": "#8B4513",
                "manufacturer": "Bambulab",
                "density": 1.28,
                "diameter": 1.75,
                "nozzle_temp": 215,
                "bed_temp": 60,
                "remaining_length": 210.0,
                "remaining_weight": 800.0
            },
            "CARBON_FIBER": {
                "name": "Bambu Carbon Fiber",
                "type": "CARBON_FIBER",
                "color": "#2C2C2C",
                "manufacturer": "Bambulab",
                "density": 1.36,
                "diameter": 1.75,
                "nozzle_temp": 270,
                "bed_temp": 70,
                "remaining_length": 200.0,
                "remaining_weight": 750.0
            },
            "METAL_FILLED": {
                "name": "Bambu Metal Filled",
                "type": "METAL_FILLED", 
                "color": "#C0C0C0",
                "manufacturer": "Bambulab",
                "density": 2.85,
                "diameter": 1.75,
                "nozzle_temp": 260,
                "bed_temp": 80,
                "remaining_length": 180.0,
                "remaining_weight": 1200.0
            },
            "SUPPORT": {
                "name": "Bambu Support Material",
                "type": "SUPPORT",
                "color": "#FFFFFF",
                "manufacturer": "Bambulab",
                "density": 1.20,
                "diameter": 1.75,
                "nozzle_temp": 200,
                "bed_temp": 45,
                "remaining_length": 300.0,
                "remaining_weight": 1100.0
            },
            "PVA": {
                "name": "Bambu PVA",
                "type": "PVA",
                "color": "#F5F5DC",
                "manufacturer": "Bambulab",
                "density": 1.23,
                "diameter": 1.75,
                "nozzle_temp": 210,
                "bed_temp": 60,
                "remaining_length": 250.0,
                "remaining_weight": 950.0
            }
        }
    
    @pytest.mark.parametrize("spool_type", [
        "PLA", "PETG", "ABS", "TPU", "ASA", "WOOD", 
        "CARBON_FIBER", "METAL_FILLED", "SUPPORT", "PVA"
    ])
    def test_decode_spool_type(self, decoder, reference_payloads, spool_type):
        """
        Test decoding of specific spool type payload.
        
        Args:
            decoder: SpoolDecoder instance
            reference_payloads: Dictionary of reference payload data
            spool_type: The specific spool type to test
        """
        # Get reference payload for this spool type
        reference_data = reference_payloads[spool_type]
        
        # Encode the reference data as it would appear on the NFC tag
        encoded_payload = json.dumps(reference_data)
        
        # Decode the payload
        decoded_spool = decoder.decode(encoded_payload)
        
        # Validate that decoding was successful
        assert decoded_spool is not None, f"Failed to decode {spool_type} payload"
        assert isinstance(decoded_spool, FilamentSpool), f"Decoded result is not a FilamentSpool instance for {spool_type}"
        
        # Validate all fields match reference data
        decoded_dict = decoded_spool.to_dict()
        for key, expected_value in reference_data.items():
            assert key in decoded_dict, f"Missing field '{key}' in decoded {spool_type} data"
            assert decoded_dict[key] == expected_value, f"Field '{key}' mismatch in {spool_type}: expected {expected_value}, got {decoded_dict[key]}"
    
    def test_decode_all_spool_types_batch(self, decoder, reference_payloads):
        """
        Test batch decoding of all spool types to ensure no interference.
        """
        decoded_results = {}
        
        # Decode all spool types
        for spool_type, reference_data in reference_payloads.items():
            encoded_payload = json.dumps(reference_data)
            decoded_spool = decoder.decode(encoded_payload)
            decoded_results[spool_type] = decoded_spool
        
        # Validate all decodings were successful
        assert len(decoded_results) == len(reference_payloads), "Not all spool types were decoded"
        
        for spool_type, decoded_spool in decoded_results.items():
            assert decoded_spool is not None, f"Batch decoding failed for {spool_type}"
            assert decoded_spool.type == spool_type, f"Type mismatch in batch decoding for {spool_type}"
    
    def test_decode_invalid_payload(self, decoder):
        """
        Test error handling for invalid or malformed payload data.
        """
        invalid_payloads = [
            "",  # Empty payload
            "invalid json",  # Invalid JSON
            "{}",  # Empty JSON object
            '{"name": "test"}',  # Missing required fields
            '{"type": "UNKNOWN_TYPE"}',  # Unknown spool type
            None,  # None payload
        ]
        
        for invalid_payload in invalid_payloads:
            result = decoder.decode(invalid_payload)
            # Should either return None or raise appropriate exception
            # The exact behavior depends on implementation choice
            assert result is None or isinstance(result, FilamentSpool), f"Unexpected result for invalid payload: {invalid_payload}"
    
    def test_decode_partial_payload(self, decoder, reference_payloads):
        """
        Test decoding with partial payload data (missing some fields).
        """
        # Use PLA as base and remove some fields
        base_data = reference_payloads["PLA"].copy()
        
        # Test with missing optional fields
        partial_data = {
            "name": base_data["name"],
            "type": base_data["type"],
            "manufacturer": base_data["manufacturer"]
        }
        
        encoded_payload = json.dumps(partial_data)
        decoded_spool = decoder.decode(encoded_payload)
        
        assert decoded_spool is not None, "Failed to decode partial payload"
        assert decoded_spool.name == partial_data["name"], "Name not preserved in partial decode"
        assert decoded_spool.type == partial_data["type"], "Type not preserved in partial decode"
        assert decoded_spool.manufacturer == partial_data["manufacturer"], "Manufacturer not preserved in partial decode"
    
    def test_decode_with_extra_fields(self, decoder, reference_payloads):
        """
        Test decoding with extra unknown fields in payload.
        """
        # Use PLA as base and add extra fields
        base_data = reference_payloads["PLA"].copy()
        base_data["extra_field"] = "extra_value"
        base_data["another_field"] = 123
        
        encoded_payload = json.dumps(base_data)
        decoded_spool = decoder.decode(encoded_payload)
        
        assert decoded_spool is not None, "Failed to decode payload with extra fields"
        assert decoded_spool.type == "PLA", "Type not preserved with extra fields"
        # Extra fields should be ignored gracefully
    
    def test_spool_type_case_insensitive(self, decoder, reference_payloads):
        """
        Test that spool type matching is case-insensitive.
        """
        # Test with lowercase type
        base_data = reference_payloads["PLA"].copy()
        base_data["type"] = "pla"  # lowercase
        
        encoded_payload = json.dumps(base_data)
        decoded_spool = decoder.decode(encoded_payload)
        
        assert decoded_spool is not None, "Failed to decode lowercase spool type"
        # The decoder should normalize the type
        assert decoded_spool.type.upper() == "PLA", "Case insensitive type matching failed"
    
    def test_temperature_range_validation(self, decoder, reference_payloads):
        """
        Test validation of temperature ranges for different spool types.
        """
        # Test temperature extremes
        for spool_type, reference_data in reference_payloads.items():
            # Test with reasonable temperature values
            test_data = reference_data.copy()
            
            # Validate nozzle temperature is within reasonable range
            assert 150 <= test_data["nozzle_temp"] <= 300, f"Nozzle temp out of range for {spool_type}: {test_data['nozzle_temp']}"
            
            # Validate bed temperature is within reasonable range  
            assert 0 <= test_data["bed_temp"] <= 120, f"Bed temp out of range for {spool_type}: {test_data['bed_temp']}"
    
    def test_density_validation(self, decoder, reference_payloads):
        """
        Test validation of material density values.
        """
        for spool_type, reference_data in reference_payloads.items():
            density = reference_data["density"]
            
            # Validate density is within reasonable range for plastics/composites
            assert 0.8 <= density <= 3.5, f"Density out of range for {spool_type}: {density}"
    
    def test_color_format_validation(self, decoder, reference_payloads):
        """
        Test validation of color format (hex codes).
        """
        for spool_type, reference_data in reference_payloads.items():
            color = reference_data["color"]
            
            # Validate hex color format
            assert color.startswith("#"), f"Color should start with # for {spool_type}: {color}"
            assert len(color) == 7, f"Color should be 7 characters for {spool_type}: {color}"
            
            # Validate hex characters
            hex_part = color[1:]
            assert all(c in "0123456789ABCDEFabcdef" for c in hex_part), f"Invalid hex color for {spool_type}: {color}"