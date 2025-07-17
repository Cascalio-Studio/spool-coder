"""
NFC Payload Decoder for BambuLab Filament Spools

This module provides robust decoding of NFC tag data from BambuLab filament spools,
with comprehensive error handling for malformed or corrupted data.
"""

import logging
import struct
from typing import Dict, Optional, Union, Any

# Configure logger for NFC decoding
logger = logging.getLogger(__name__)


class NFCDecodingError(Exception):
    """Exception raised when NFC payload decoding fails"""
    pass


class NFCPayloadDecoder:
    """
    Robust decoder for BambuLab filament spool NFC payloads
    
    Handles various payload formats and provides comprehensive error handling
    for malformed or corrupted data.
    """
    
    # Expected field sizes and types for validation
    EXPECTED_FIELDS = {
        'name': {'type': str, 'max_length': 64},
        'type': {'type': str, 'max_length': 16},
        'color': {'type': str, 'max_length': 7},  # Hex color code
        'manufacturer': {'type': str, 'max_length': 32},
        'density': {'type': float, 'min': 0.5, 'max': 5.0},
        'diameter': {'type': float, 'min': 1.0, 'max': 3.0},
        'nozzle_temp': {'type': int, 'min': 150, 'max': 350},
        'bed_temp': {'type': int, 'min': 0, 'max': 150},
        'remaining_length': {'type': float, 'min': 0, 'max': 10000},
        'remaining_weight': {'type': float, 'min': 0, 'max': 5000}
    }
    
    DEFAULT_VALUES = {
        'name': 'Unknown Filament',
        'type': 'PLA',
        'color': '#FFFFFF',
        'manufacturer': 'Unknown',
        'density': 1.24,
        'diameter': 1.75,
        'nozzle_temp': 200,
        'bed_temp': 60,
        'remaining_length': 0,
        'remaining_weight': 0
    }
    
    def __init__(self):
        """Initialize the NFC payload decoder"""
        self.logger = logging.getLogger(f"{__name__}.{self.__class__.__name__}")
    
    def decode_payload(self, payload: Union[bytes, str, dict]) -> Optional[Dict[str, Any]]:
        """
        Decode an NFC payload with robust error handling
        
        Args:
            payload: Raw NFC payload data (bytes, hex string, or dict)
            
        Returns:
            Dictionary with decoded filament data, or None if decoding fails
            
        Raises:
            NFCDecodingError: When payload is completely invalid
        """
        try:
            if payload is None:
                self.logger.error("Received None payload")
                raise NFCDecodingError("Payload is None")
            
            # Handle different payload types
            if isinstance(payload, dict):
                return self._decode_dict_payload(payload)
            elif isinstance(payload, str):
                return self._decode_string_payload(payload)
            elif isinstance(payload, bytes):
                return self._decode_bytes_payload(payload)
            else:
                self.logger.error(f"Unsupported payload type: {type(payload)}")
                raise NFCDecodingError(f"Unsupported payload type: {type(payload)}")
                
        except NFCDecodingError:
            # Re-raise NFCDecodingError as-is
            raise
        except Exception as e:
            self.logger.error(f"Unexpected error during payload decoding: {e}")
            raise NFCDecodingError(f"Unexpected decoding error: {e}")
    
    def _decode_dict_payload(self, payload: dict) -> Dict[str, Any]:
        """
        Decode a dictionary payload with validation and error handling
        
        Args:
            payload: Dictionary containing filament data
            
        Returns:
            Validated and cleaned filament data
        """
        self.logger.debug(f"Decoding dictionary payload with {len(payload)} fields")
        
        if not isinstance(payload, dict):
            raise NFCDecodingError("Payload is not a dictionary")
        
        result = {}
        errors = []
        
        # Process each expected field
        for field_name, field_spec in self.EXPECTED_FIELDS.items():
            try:
                raw_value = payload.get(field_name)
                validated_value = self._validate_field(field_name, raw_value, field_spec)
                result[field_name] = validated_value
            except Exception as e:
                self.logger.warning(f"Field '{field_name}' validation failed: {e}")
                errors.append(f"{field_name}: {e}")
                result[field_name] = self.DEFAULT_VALUES[field_name]
        
        # Log validation errors if any
        if errors:
            self.logger.warning(f"Payload validation errors: {'; '.join(errors)}")
        
        # Check if we have any valid data (at least one field that isn't all defaults)
        # Allow some fields to be valid even if others failed
        valid_fields = sum(1 for field in self.EXPECTED_FIELDS.keys() 
                          if result[field] != self.DEFAULT_VALUES[field])
        
        # Only fail if absolutely no useful data was extracted
        if valid_fields == 0 and len(payload) > 0:
            # If we have some input data but extracted nothing useful, that's an error
            # But if we can extract at least something, we should return it
            total_provided_fields = len([k for k in payload.keys() 
                                       if k in self.EXPECTED_FIELDS])
            if total_provided_fields > 0:
                self.logger.error("No valid fields found in payload despite having input data")
                raise NFCDecodingError("No valid fields found in payload")
        
        self.logger.info(f"Successfully decoded payload with {valid_fields}/{len(self.EXPECTED_FIELDS)} valid fields")
        return result
    
    def _decode_string_payload(self, payload: str) -> Dict[str, Any]:
        """
        Decode a string payload (hex or JSON format)
        
        Args:
            payload: String representation of NFC data
            
        Returns:
            Decoded filament data
        """
        self.logger.debug(f"Decoding string payload: {payload[:50]}...")
        
        if not payload or not isinstance(payload, str):
            raise NFCDecodingError("Invalid string payload")
        
        payload = payload.strip()
        
        # Try to decode as JSON first
        try:
            import json
            data = json.loads(payload)
            return self._decode_dict_payload(data)
        except json.JSONDecodeError:
            self.logger.debug("Payload is not valid JSON, trying hex decoding")
        
        # Try to decode as hex string
        try:
            # Remove common hex prefixes and clean up
            clean_payload = payload.replace('0x', '').replace(' ', '').replace('-', '')
            if len(clean_payload) % 2 != 0:
                raise ValueError("Odd-length hex string")
            
            bytes_payload = bytes.fromhex(clean_payload)
            return self._decode_bytes_payload(bytes_payload)
        except ValueError as e:
            self.logger.error(f"Failed to decode hex string: {e}")
            raise NFCDecodingError(f"Invalid hex string format: {e}")
    
    def _decode_bytes_payload(self, payload: bytes) -> Dict[str, Any]:
        """
        Decode a binary payload (simulated BambuLab format)
        
        Args:
            payload: Binary NFC payload data
            
        Returns:
            Decoded filament data
        """
        self.logger.debug(f"Decoding binary payload of {len(payload)} bytes")
        
        if not payload or len(payload) == 0:
            raise NFCDecodingError("Empty binary payload")
        
        # For demonstration, we'll implement a simple binary format
        # In reality, this would need to match the actual BambuLab format
        try:
            # Check minimum payload size
            if len(payload) < 10:
                raise NFCDecodingError(f"Payload too short: {len(payload)} bytes (minimum 10)")
            
            # Simple format simulation: first 4 bytes are magic number
            magic = struct.unpack('<I', payload[:4])[0]
            if magic != 0x424C4D46:  # "BLMF" (BambuLab Material Format)
                self.logger.warning(f"Unexpected magic number: 0x{magic:08X}")
            
            # Extract basic data with error handling
            result = self.DEFAULT_VALUES.copy()
            
            try:
                # Simulate extracting temperature data
                if len(payload) >= 8:
                    temps = struct.unpack('<HH', payload[4:8])
                    result['nozzle_temp'] = self._validate_field('nozzle_temp', temps[0], 
                                                               self.EXPECTED_FIELDS['nozzle_temp'])
                    result['bed_temp'] = self._validate_field('bed_temp', temps[1], 
                                                            self.EXPECTED_FIELDS['bed_temp'])
            except (struct.error, ValueError) as e:
                self.logger.warning(f"Failed to extract temperature data: {e}")
            
            try:
                # Simulate extracting material data
                if len(payload) >= 16:
                    material_data = struct.unpack('<ff', payload[8:16])
                    result['density'] = self._validate_field('density', material_data[0], 
                                                           self.EXPECTED_FIELDS['density'])
                    result['diameter'] = self._validate_field('diameter', material_data[1], 
                                                            self.EXPECTED_FIELDS['diameter'])
            except (struct.error, ValueError) as e:
                self.logger.warning(f"Failed to extract material data: {e}")
            
            # Try to extract string data
            try:
                if len(payload) > 16:
                    string_data = payload[16:].decode('utf-8', errors='ignore').rstrip('\x00')
                    if string_data:
                        # Simple parsing: assume name is first part
                        parts = string_data.split('\x00')
                        if parts[0]:
                            result['name'] = self._validate_field('name', parts[0], 
                                                                self.EXPECTED_FIELDS['name'])
            except Exception as e:
                self.logger.warning(f"Failed to extract string data: {e}")
            
            self.logger.info("Successfully decoded binary payload")
            return result
            
        except struct.error as e:
            self.logger.error(f"Binary payload structure error: {e}")
            raise NFCDecodingError(f"Invalid binary format: {e}")
        except Exception as e:
            self.logger.error(f"Unexpected error in binary decoding: {e}")
            raise NFCDecodingError(f"Binary decoding failed: {e}")
    
    def _validate_field(self, field_name: str, value: Any, spec: Dict[str, Any]) -> Any:
        """
        Validate a field value according to its specification
        
        Args:
            field_name: Name of the field
            value: Raw field value
            spec: Field specification with type and constraints
            
        Returns:
            Validated and potentially converted value
            
        Raises:
            ValueError: If validation fails
        """
        if value is None:
            raise ValueError("Value is None")
        
        expected_type = spec['type']
        
        # Type conversion and validation
        try:
            if expected_type == str:
                str_value = str(value)
                max_length = spec.get('max_length', 1000)
                if len(str_value) > max_length:
                    # Truncate instead of failing
                    self.logger.warning(f"String truncated from {len(str_value)} to {max_length} characters")
                    str_value = str_value[:max_length]
                return str_value
            
            elif expected_type == int:
                int_value = int(float(value))  # Handle string numbers
                min_val = spec.get('min', float('-inf'))
                max_val = spec.get('max', float('inf'))
                if not (min_val <= int_value <= max_val):
                    self.logger.warning(f"Value {int_value} out of range [{min_val}, {max_val}], using default")
                    raise ValueError(f"Value {int_value} not in range [{min_val}, {max_val}]")
                return int_value
            
            elif expected_type == float:
                float_value = float(value)
                # Check for NaN or infinite values
                if not (float_value == float_value and float_value != float('inf') and float_value != float('-inf')):
                    raise ValueError(f"Invalid float value: {float_value}")
                min_val = spec.get('min', float('-inf'))
                max_val = spec.get('max', float('inf'))
                if not (min_val <= float_value <= max_val):
                    self.logger.warning(f"Value {float_value} out of range [{min_val}, {max_val}], using default")
                    raise ValueError(f"Value {float_value} not in range [{min_val}, {max_val}]")
                return float_value
            
            else:
                raise ValueError(f"Unsupported field type: {expected_type}")
                
        except (ValueError, TypeError) as e:
            raise ValueError(f"Type conversion failed: {e}")
    
    def validate_payload_integrity(self, payload: Any) -> bool:
        """
        Check if a payload has basic integrity without full decoding
        
        Args:
            payload: Raw payload to check
            
        Returns:
            True if payload seems valid, False otherwise
        """
        try:
            if payload is None:
                return False
            
            if isinstance(payload, dict):
                return len(payload) > 0
            elif isinstance(payload, str):
                return len(payload.strip()) > 0
            elif isinstance(payload, bytes):
                return len(payload) >= 4  # Minimum size for any valid payload
            else:
                return False
                
        except Exception:
            return False