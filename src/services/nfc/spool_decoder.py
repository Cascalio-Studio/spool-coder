"""
Spool decoder module for parsing NFC tag data from BambuLab filament spools.
Handles decoding of all known spool types with robust error handling.
"""

import json
import logging
from typing import Optional, Dict, Any
from ...models.filament import FilamentSpool

logger = logging.getLogger(__name__)


class SpoolDecoder:
    """
    Decoder for BambuLab filament spool NFC tag data.
    Supports all documented spool types with validation and error handling.
    """
    
    # Supported spool types with their expected properties
    SUPPORTED_SPOOL_TYPES = {
        "PLA": {"min_temp": 180, "max_temp": 230, "min_bed": 0, "max_bed": 80},
        "PETG": {"min_temp": 230, "max_temp": 270, "min_bed": 70, "max_bed": 90},
        "ABS": {"min_temp": 240, "max_temp": 280, "min_bed": 80, "max_bed": 110},
        "TPU": {"min_temp": 200, "max_temp": 240, "min_bed": 30, "max_bed": 70},
        "ASA": {"min_temp": 240, "max_temp": 280, "min_bed": 80, "max_bed": 110},
        "WOOD": {"min_temp": 190, "max_temp": 230, "min_bed": 45, "max_bed": 80},
        "CARBON_FIBER": {"min_temp": 250, "max_temp": 290, "min_bed": 60, "max_bed": 90},
        "METAL_FILLED": {"min_temp": 240, "max_temp": 280, "min_bed": 70, "max_bed": 100},
        "SUPPORT": {"min_temp": 180, "max_temp": 220, "min_bed": 30, "max_bed": 60},
        "PVA": {"min_temp": 190, "max_temp": 230, "min_bed": 45, "max_bed": 80},
    }
    
    def __init__(self):
        """Initialize the spool decoder."""
        self.validation_enabled = True
    
    def decode(self, payload: Optional[str]) -> Optional[FilamentSpool]:
        """
        Decode NFC tag payload data into a FilamentSpool object.
        
        Args:
            payload: Raw payload string from NFC tag (JSON format expected)
            
        Returns:
            FilamentSpool object if decoding successful, None otherwise
            
        Raises:
            None - All errors are handled gracefully and logged
        """
        if not payload:
            logger.warning("Empty or None payload provided")
            return None
            
        try:
            # Parse JSON payload
            if isinstance(payload, str):
                data = json.loads(payload)
            elif isinstance(payload, dict):
                data = payload
            else:
                logger.error(f"Unsupported payload type: {type(payload)}")
                return None
                
        except json.JSONDecodeError as e:
            logger.error(f"Invalid JSON payload: {e}")
            return None
        except Exception as e:
            logger.error(f"Unexpected error parsing payload: {e}")
            return None
            
        # Validate and normalize the data
        normalized_data = self._normalize_data(data)
        if not normalized_data:
            return None
            
        # Validate spool type
        if not self._validate_spool_type(normalized_data):
            logger.warning(f"Unknown or invalid spool type: {normalized_data.get('type', 'unknown')}")
            # Continue with decoding even for unknown types
            
        # Create FilamentSpool object
        try:
            spool = FilamentSpool.from_dict(normalized_data)
            logger.info(f"Successfully decoded {spool.type} spool: {spool.name}")
            return spool
        except Exception as e:
            logger.error(f"Failed to create FilamentSpool from data: {e}")
            return None
    
    def _normalize_data(self, data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """
        Normalize and validate the payload data.
        
        Args:
            data: Raw payload data dictionary
            
        Returns:
            Normalized data dictionary or None if validation fails
        """
        if not isinstance(data, dict):
            logger.error("Payload data must be a dictionary")
            return None
            
        normalized = {}
        
        # Required fields with defaults
        required_fields = {
            "name": "",
            "type": "PLA",
            "manufacturer": "Unknown"
        }
        
        # Optional fields with defaults
        optional_fields = {
            "color": "#FFFFFF",
            "density": 1.24,
            "diameter": 1.75,
            "nozzle_temp": 200,
            "bed_temp": 60,
            "remaining_length": 240.0,
            "remaining_weight": 1000.0
        }
        
        # Copy required fields
        for field, default in required_fields.items():
            if field in data:
                normalized[field] = data[field]
            else:
                normalized[field] = default
                logger.warning(f"Missing required field '{field}', using default: {default}")
        
        # Copy optional fields
        for field, default in optional_fields.items():
            if field in data:
                normalized[field] = data[field]
            else:
                normalized[field] = default
        
        # Normalize spool type (case insensitive)
        if normalized["type"]:
            normalized["type"] = normalized["type"].upper()
        
        # Validate data types and ranges
        if not self._validate_field_types(normalized):
            return None
            
        return normalized
    
    def _validate_spool_type(self, data: Dict[str, Any]) -> bool:
        """
        Validate that the spool type is known and supported.
        
        Args:
            data: Normalized payload data
            
        Returns:
            True if spool type is supported, False otherwise
        """
        spool_type = data.get("type", "").upper()
        return spool_type in self.SUPPORTED_SPOOL_TYPES
    
    def _validate_field_types(self, data: Dict[str, Any]) -> bool:
        """
        Validate field types and value ranges.
        
        Args:
            data: Normalized payload data
            
        Returns:
            True if all validations pass, False otherwise
        """
        try:
            # Validate string fields
            string_fields = ["name", "type", "manufacturer", "color"]
            for field in string_fields:
                if not isinstance(data.get(field), str):
                    if data.get(field) is not None:
                        data[field] = str(data[field])
                    else:
                        logger.error(f"Field '{field}' must be a string")
                        return False
            
            # Validate numeric fields
            numeric_fields = {
                "density": (0.1, 10.0),
                "diameter": (1.0, 3.0),
                "nozzle_temp": (100, 400),
                "bed_temp": (0, 150),
                "remaining_length": (0, 1000),
                "remaining_weight": (0, 5000)
            }
            
            for field, (min_val, max_val) in numeric_fields.items():
                value = data.get(field)
                if value is not None:
                    try:
                        data[field] = float(value)
                        if not (min_val <= data[field] <= max_val):
                            logger.warning(f"Field '{field}' value {data[field]} outside expected range [{min_val}, {max_val}]")
                    except (ValueError, TypeError):
                        logger.error(f"Field '{field}' must be numeric")
                        return False
            
            # Validate color format
            color = data.get("color", "")
            if color and not self._validate_color_format(color):
                logger.warning(f"Invalid color format: {color}, using default")
                data["color"] = "#FFFFFF"
            
            # Validate temperature ranges for known spool types
            if self.validation_enabled:
                self._validate_temperatures(data)
            
            return True
            
        except Exception as e:
            logger.error(f"Validation error: {e}")
            return False
    
    def _validate_color_format(self, color: str) -> bool:
        """
        Validate hex color format.
        
        Args:
            color: Color string to validate
            
        Returns:
            True if valid hex color, False otherwise
        """
        if not color.startswith("#"):
            return False
        if len(color) != 7:
            return False
        
        hex_part = color[1:]
        return all(c in "0123456789ABCDEFabcdef" for c in hex_part)
    
    def _validate_temperatures(self, data: Dict[str, Any]) -> bool:
        """
        Validate temperature ranges for specific spool types.
        
        Args:
            data: Normalized payload data
            
        Returns:
            True if temperatures are reasonable for the spool type
        """
        spool_type = data.get("type", "").upper()
        if spool_type not in self.SUPPORTED_SPOOL_TYPES:
            return True  # Skip validation for unknown types
        
        type_specs = self.SUPPORTED_SPOOL_TYPES[spool_type]
        nozzle_temp = data.get("nozzle_temp", 0)
        bed_temp = data.get("bed_temp", 0)
        
        # Check nozzle temperature
        if not (type_specs["min_temp"] <= nozzle_temp <= type_specs["max_temp"]):
            logger.warning(f"Nozzle temperature {nozzle_temp}°C unusual for {spool_type} "
                         f"(expected: {type_specs['min_temp']}-{type_specs['max_temp']}°C)")
        
        # Check bed temperature  
        if not (type_specs["min_bed"] <= bed_temp <= type_specs["max_bed"]):
            logger.warning(f"Bed temperature {bed_temp}°C unusual for {spool_type} "
                         f"(expected: {type_specs['min_bed']}-{type_specs['max_bed']}°C)")
        
        return True
    
    def get_supported_types(self) -> list:
        """
        Get list of supported spool types.
        
        Returns:
            List of supported spool type strings
        """
        return list(self.SUPPORTED_SPOOL_TYPES.keys())
    
    def set_validation_enabled(self, enabled: bool):
        """
        Enable or disable strict validation.
        
        Args:
            enabled: Whether to enable strict validation
        """
        self.validation_enabled = enabled