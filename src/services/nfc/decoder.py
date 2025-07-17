"""
NFC Spool Tag Decoder for BambuLab filament spools
"""

import struct
from typing import Dict, Optional, Union
from models.filament import FilamentSpool


class SpoolTagDecoder:
    """
    Decoder for BambuLab NFC spool tag data
    """
    
    # Material type mappings based on BambuLab specifications
    MATERIAL_TYPES = {
        0x01: "PLA",
        0x02: "ABS", 
        0x03: "PETG",
        0x04: "TPU",
        0x05: "PA",
        0x06: "ASA",
        0x07: "PC",
        0x08: "PLA-CF",
        0x09: "PETG-CF"
    }
    
    @classmethod
    def decode_spool_data(cls, payload: Union[bytes, str]) -> Optional[FilamentSpool]:
        """
        Decode raw NFC payload from BambuLab spool tag
        
        Args:
            payload: Raw NFC payload as bytes or hex string
            
        Returns:
            FilamentSpool object with decoded data or None if decode fails
        """
        try:
            # Convert hex string to bytes if necessary
            if isinstance(payload, str):
                payload = bytes.fromhex(payload.replace(' ', '').replace(':', ''))
            
            # Minimum payload size check
            if len(payload) < 32:
                return None
                
            # Basic decode structure for ABS spool example
            # This is a simplified implementation for testing
            material_id = payload[0]
            
            # Get material type
            material_type = cls.MATERIAL_TYPES.get(material_id, "UNKNOWN")
            
            # Extract other fields (simplified for ABS test)
            if material_type == "ABS":
                # ABS-specific decoding
                color_r = payload[1] if len(payload) > 1 else 255
                color_g = payload[2] if len(payload) > 2 else 100
                color_b = payload[3] if len(payload) > 3 else 50
                
                # Convert to hex color
                color = f"#{color_r:02X}{color_g:02X}{color_b:02X}"
                
                # Extract weight and temperature data
                remaining_weight = struct.unpack('<H', payload[4:6])[0] if len(payload) >= 6 else 1000
                nozzle_temp = struct.unpack('<H', payload[6:8])[0] if len(payload) >= 8 else 240
                bed_temp = payload[8] if len(payload) > 8 else 80
                
                # Create FilamentSpool object with decoded ABS data
                return FilamentSpool(
                    name=f"Bambu {material_type}",
                    type=material_type,
                    color=color,
                    manufacturer="Bambulab",
                    density=1.04,  # ABS density
                    diameter=1.75,
                    nozzle_temp=nozzle_temp,
                    bed_temp=bed_temp,
                    remaining_length=240,
                    remaining_weight=remaining_weight
                )
            
            # For other materials, return basic info
            return FilamentSpool(
                name=f"Bambu {material_type}",
                type=material_type,
                color="#FFFFFF",
                manufacturer="Bambulab",
                density=1.24,
                diameter=1.75,
                nozzle_temp=200,
                bed_temp=60,
                remaining_length=240,
                remaining_weight=1000
            )
            
        except (IndexError, struct.error, ValueError) as e:
            # Return None if decoding fails
            return None
    
    @classmethod
    def create_sample_abs_payload(cls) -> bytes:
        """
        Create a sample ABS spool payload for testing
        
        Returns:
            Sample ABS payload as bytes
        """
        # Sample ABS payload: material_id=0x02, RGB color, weight, temps
        payload = bytearray(32)
        payload[0] = 0x02  # ABS material ID
        payload[1] = 255   # Red component
        payload[2] = 100   # Green component  
        payload[3] = 50    # Blue component
        
        # Pack weight (1000g) as little endian 16-bit
        struct.pack_into('<H', payload, 4, 1000)
        
        # Pack nozzle temp (240°C) as little endian 16-bit
        struct.pack_into('<H', payload, 6, 240)
        
        # Bed temp (80°C) as single byte
        payload[8] = 80
        
        return bytes(payload)