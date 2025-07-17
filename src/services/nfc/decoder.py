"""
NFC payload decoder for BambuLab filament spool tags
"""

import json
from typing import Dict, Optional, Any
from models.filament import FilamentSpool


class NFCDecoder:
    """
    Decoder for NFC payload data from BambuLab filament spools
    """
    
    # Required fields for a valid filament spool
    REQUIRED_FIELDS = {
        'name': str,
        'type': str, 
        'color': str,
        'manufacturer': str,
        'density': (int, float),
        'diameter': (int, float),
        'nozzle_temp': int,
        'bed_temp': int,
        'remaining_length': (int, float),
        'remaining_weight': (int, float)
    }
    
    @classmethod
    def decode_payload(cls, payload: bytes) -> Optional[FilamentSpool]:
        """
        Decode NFC payload bytes into a FilamentSpool object
        
        Args:
            payload (bytes): Raw NFC payload data
            
        Returns:
            FilamentSpool: Decoded filament spool object or None if decoding fails
        """
        try:
            # Convert bytes to string
            payload_str = payload.decode('utf-8')
            
            # Parse JSON data
            data = json.loads(payload_str)
            
            # Validate required fields
            if not cls._validate_data(data):
                return None
                
            # Create FilamentSpool from validated data
            return FilamentSpool.from_dict(data)
            
        except (UnicodeDecodeError, json.JSONDecodeError, ValueError) as e:
            return None
    
    @classmethod
    def _validate_data(cls, data: Dict[str, Any]) -> bool:
        """
        Validate that the data contains all required fields with correct types
        
        Args:
            data (dict): Parsed JSON data
            
        Returns:
            bool: True if data is valid, False otherwise
        """
        if not isinstance(data, dict):
            return False
            
        for field, expected_type in cls.REQUIRED_FIELDS.items():
            if field not in data:
                return False
                
            value = data[field]
            if not isinstance(value, expected_type):
                return False
                
        return True
    
    @classmethod
    def get_minimum_valid_payload(cls) -> bytes:
        """
        Generate the minimum-length valid NFC payload for testing
        
        Returns:
            bytes: Minimum valid payload as bytes
        """
        # Minimum data with shortest possible values but all required fields
        min_data = {
            "name": "",  # Empty string is shortest
            "type": "PLA",  # Standard short type
            "color": "#000",  # Shorter than #FFF
            "manufacturer": "",  # Empty string is shortest
            "density": 1,  # Integer is shorter than 1.0
            "diameter": 1,  # Integer is shorter than 1.0
            "nozzle_temp": 0,  # Minimum temperature
            "bed_temp": 0,  # Minimum temperature
            "remaining_length": 0,  # Minimum length
            "remaining_weight": 0  # Minimum weight
        }
        
        # Convert to compact JSON (no spaces)
        json_str = json.dumps(min_data, separators=(',', ':'))
        return json_str.encode('utf-8')