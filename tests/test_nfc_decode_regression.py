"""
Regression tests for NFC decode functionality.

This module contains tests to ensure that previously passing NFC payloads 
continue to decode correctly after code changes.

Purpose: Confirm previous passing NFC payloads still decode correctly 
after code updates.

Related to issue #3: Validate and Test NFC Decoding Module
"""

import pytest
from src.models.filament import FilamentSpool
from tests.test_data import ALL_VALID_PAYLOADS, INVALID_PAYLOADS


class TestNFCDecodeRegression:
    """
    Regression tests for NFC payload decoding to ensure previously 
    passing cases continue to work after code changes.
    """

    @pytest.mark.parametrize("payload_name,payload_data", ALL_VALID_PAYLOADS)
    def test_valid_payloads_decode_successfully(self, payload_name, payload_data):
        """
        Test that all known valid NFC payloads decode successfully.
        
        This is the core regression test that ensures all previously 
        working BambuLab filament spool configurations continue to 
        decode correctly.
        
        Args:
            payload_name (str): Descriptive name of the test case
            payload_data (dict): NFC payload data to decode
        """
        # Act: Attempt to decode the payload
        try:
            decoded_spool = FilamentSpool.from_dict(payload_data)
        except Exception as e:
            pytest.fail(f"Failed to decode valid payload '{payload_name}': {e}")
        
        # Assert: Verify the decoding was successful and data is preserved
        assert decoded_spool is not None, f"Decoded spool should not be None for {payload_name}"
        assert isinstance(decoded_spool, FilamentSpool), f"Should return FilamentSpool instance for {payload_name}"
        
        # Verify all expected attributes are present and correct
        assert decoded_spool.name == payload_data.get("name", ""), f"Name mismatch for {payload_name}"
        assert decoded_spool.type == payload_data.get("type", "PLA"), f"Type mismatch for {payload_name}"
        assert decoded_spool.color == payload_data.get("color", "#FFFFFF"), f"Color mismatch for {payload_name}"
        assert decoded_spool.manufacturer == payload_data.get("manufacturer", ""), f"Manufacturer mismatch for {payload_name}"
        assert decoded_spool.density == payload_data.get("density", 1.24), f"Density mismatch for {payload_name}"
        assert decoded_spool.diameter == payload_data.get("diameter", 1.75), f"Diameter mismatch for {payload_name}"
        assert decoded_spool.nozzle_temp == payload_data.get("nozzle_temp", 200), f"Nozzle temp mismatch for {payload_name}"
        assert decoded_spool.bed_temp == payload_data.get("bed_temp", 60), f"Bed temp mismatch for {payload_name}"
        assert decoded_spool.remaining_length == payload_data.get("remaining_length", 240), f"Remaining length mismatch for {payload_name}"
        assert decoded_spool.remaining_weight == payload_data.get("remaining_weight", 1000), f"Remaining weight mismatch for {payload_name}"

    @pytest.mark.parametrize("payload_name,payload_data", ALL_VALID_PAYLOADS)
    def test_roundtrip_encoding_decoding(self, payload_name, payload_data):
        """
        Test that encoding and then decoding produces the same data.
        
        This ensures the decode process is symmetric with encoding 
        and no data is lost in the round-trip process.
        
        Args:
            payload_name (str): Descriptive name of the test case
            payload_data (dict): NFC payload data to test
        """
        # Act: Decode then encode then decode again
        original_spool = FilamentSpool.from_dict(payload_data)
        encoded_data = original_spool.to_dict()
        roundtrip_spool = FilamentSpool.from_dict(encoded_data)
        
        # Assert: Verify round-trip preserves all data
        assert original_spool.name == roundtrip_spool.name, f"Name changed in roundtrip for {payload_name}"
        assert original_spool.type == roundtrip_spool.type, f"Type changed in roundtrip for {payload_name}"
        assert original_spool.color == roundtrip_spool.color, f"Color changed in roundtrip for {payload_name}"
        assert original_spool.manufacturer == roundtrip_spool.manufacturer, f"Manufacturer changed in roundtrip for {payload_name}"
        assert original_spool.density == roundtrip_spool.density, f"Density changed in roundtrip for {payload_name}"
        assert original_spool.diameter == roundtrip_spool.diameter, f"Diameter changed in roundtrip for {payload_name}"
        assert original_spool.nozzle_temp == roundtrip_spool.nozzle_temp, f"Nozzle temp changed in roundtrip for {payload_name}"
        assert original_spool.bed_temp == roundtrip_spool.bed_temp, f"Bed temp changed in roundtrip for {payload_name}"
        assert original_spool.remaining_length == roundtrip_spool.remaining_length, f"Remaining length changed in roundtrip for {payload_name}"
        assert original_spool.remaining_weight == roundtrip_spool.remaining_weight, f"Remaining weight changed in roundtrip for {payload_name}"

    def test_bambu_pla_basic_specific_values(self):
        """
        Test specific decoding of the most common Bambu PLA Basic configuration.
        
        This test validates the exact expected values for the standard 
        BambuLab PLA Basic filament to catch any regression in the 
        most commonly used configuration.
        """
        # Arrange: Use the standard Bambu PLA Basic payload
        from tests.test_data import BAMBU_PLA_BASIC
        
        # Act: Decode the payload
        spool = FilamentSpool.from_dict(BAMBU_PLA_BASIC)
        
        # Assert: Verify exact expected values
        assert spool.name == "Bambu PLA Basic"
        assert spool.type == "PLA"
        assert spool.color == "#FFFFFF"
        assert spool.manufacturer == "Bambulab"
        assert spool.density == 1.24
        assert spool.diameter == 1.75
        assert spool.nozzle_temp == 210
        assert spool.bed_temp == 60
        assert spool.remaining_length == 240
        assert spool.remaining_weight == 1000

    def test_high_temperature_filaments_decode(self):
        """
        Test that high-temperature filaments (PC, PA-CF) decode correctly.
        
        These filaments have higher temperature requirements and ensure 
        the decoding works for the full temperature range.
        """
        from tests.test_data import BAMBU_PC_BASIC, BAMBU_PA_CF
        
        # Test PC filament
        pc_spool = FilamentSpool.from_dict(BAMBU_PC_BASIC)
        assert pc_spool.nozzle_temp == 300
        assert pc_spool.bed_temp == 100
        assert pc_spool.type == "PC"
        
        # Test PA-CF filament  
        pa_cf_spool = FilamentSpool.from_dict(BAMBU_PA_CF)
        assert pa_cf_spool.nozzle_temp == 320
        assert pa_cf_spool.bed_temp == 90
        assert pa_cf_spool.type == "PA-CF"

    def test_extreme_remaining_amounts_decode(self):
        """
        Test that spools with extreme remaining amounts (nearly empty, full) decode correctly.
        
        This validates edge cases for remaining weight and length values.
        """
        from tests.test_data import BAMBU_PLA_NEARLY_EMPTY, BAMBU_PETG_FULL
        
        # Test nearly empty spool
        empty_spool = FilamentSpool.from_dict(BAMBU_PLA_NEARLY_EMPTY)
        assert empty_spool.remaining_length == 5
        assert empty_spool.remaining_weight == 20
        
        # Test full spool
        full_spool = FilamentSpool.from_dict(BAMBU_PETG_FULL)
        assert full_spool.remaining_length == 330
        assert full_spool.remaining_weight == 1000

    def test_all_filament_types_supported(self):
        """
        Test that all major BambuLab filament types can be decoded.
        
        This ensures regression coverage for all supported filament types.
        """
        expected_types = {"PLA", "PETG", "PETG-HF", "ABS", "ASA", "TPU", "PC", "PA-CF"}
        decoded_types = set()
        
        for payload_name, payload_data in ALL_VALID_PAYLOADS:
            spool = FilamentSpool.from_dict(payload_data)
            decoded_types.add(spool.type)
        
        # Verify all expected types are covered
        missing_types = expected_types - decoded_types
        assert len(missing_types) == 0, f"Missing filament types in test coverage: {missing_types}"

    def test_color_format_preservation(self):
        """
        Test that color hex codes are preserved correctly during decoding.
        """
        test_colors = ["#FFFFFF", "#000000", "#FF0000", "#00FF00", "#0000FF", "#800080"]
        
        for payload_name, payload_data in ALL_VALID_PAYLOADS:
            if payload_data["color"] in test_colors:
                spool = FilamentSpool.from_dict(payload_data)
                assert spool.color == payload_data["color"], f"Color not preserved for {payload_name}"
                assert spool.color.startswith("#"), f"Color should start with # for {payload_name}"
                assert len(spool.color) == 7, f"Color should be 7 characters for {payload_name}"


class TestNFCDecodeErrorHandling:
    """
    Tests for error handling with malformed or invalid NFC payloads.
    
    These tests ensure robust error handling for corrupted or invalid data.
    """

    @pytest.mark.parametrize("payload_name,invalid_payload", INVALID_PAYLOADS)
    def test_invalid_payloads_handle_gracefully(self, payload_name, invalid_payload):
        """
        Test that invalid payloads are handled gracefully without crashing.
        
        The system should either use default values or raise appropriate 
        exceptions rather than crashing.
        
        Args:
            payload_name (str): Descriptive name of the invalid test case
            invalid_payload (dict): Invalid payload data to test
        """
        try:
            # Act: Attempt to decode invalid payload
            spool = FilamentSpool.from_dict(invalid_payload)
            
            # If decoding succeeds, verify it used reasonable defaults
            assert spool is not None, f"Should not return None for {payload_name}"
            assert isinstance(spool, FilamentSpool), f"Should return FilamentSpool for {payload_name}"
            
            # Verify defaults are applied for missing/invalid data
            if "name" not in invalid_payload:
                assert spool.name == "", f"Should use empty string default for missing name in {payload_name}"
            
        except (TypeError, ValueError, KeyError) as e:
            # Expected exceptions for invalid data - this is acceptable behavior
            assert str(e), f"Exception should have a meaningful message for {payload_name}"
        except Exception as e:
            # Unexpected exceptions should cause test failure
            pytest.fail(f"Unexpected exception type for {payload_name}: {type(e).__name__}: {e}")

    def test_none_payload_handling(self):
        """
        Test that None payload is handled appropriately.
        """
        with pytest.raises((TypeError, AttributeError)):
            FilamentSpool.from_dict(None)

    def test_empty_dict_handling(self):
        """
        Test that empty dictionary uses all default values.
        """
        spool = FilamentSpool.from_dict({})
        
        # Verify all defaults are applied
        assert spool.name == ""
        assert spool.type == "PLA"
        assert spool.color == "#FFFFFF"
        assert spool.manufacturer == ""
        assert spool.density == 1.24
        assert spool.diameter == 1.75
        assert spool.nozzle_temp == 200
        assert spool.bed_temp == 60
        assert spool.remaining_length == 240
        assert spool.remaining_weight == 1000