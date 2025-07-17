"""
NFC payload decoder for BambuLab filament spools.
Handles decoding of binary NFC data into structured filament information.
"""
import struct
import json
from typing import Dict, Optional, Union, List


class NFCDecoder:
    """
    Decoder for BambuLab NFC filament spool data.
    Supports multiple payload formats and data structures.
    """
    
    # Sample NFC payload formats based on BambuLab filament spools
    # These are representative structures that might be found on actual spools
    PAYLOAD_FORMATS = {
        'bambu_v1': {
            'header': b'\x42\x4D\x42',  # "BMB" header
            'format': '<3s32s32s16sffHHff',  # little-endian format
            'fields': ['header', 'name', 'type', 'color', 'density', 'diameter', 
                      'nozzle_temp', 'bed_temp', 'remaining_length', 'remaining_weight']
        },
        'bambu_v2': {
            'header': b'\x42\x4D\x42\x32',  # "BMB2" header
            'format': '<4s32s32s16s32sffHHffI',  # extended format with manufacturer
            'fields': ['header', 'name', 'type', 'color', 'manufacturer', 'density', 
                      'diameter', 'nozzle_temp', 'bed_temp', 'remaining_length', 
                      'remaining_weight', 'serial_number']
        }
    }
    
    def __init__(self):
        """Initialize the NFC decoder."""
        self.decode_count = 0
        
    def detect_format(self, payload: bytes) -> Optional[str]:
        """
        Detect the format of an NFC payload.
        
        Args:
            payload (bytes): Raw NFC payload data
            
        Returns:
            str: Format identifier or None if unrecognized
        """
        if len(payload) < 4:
            return None
            
        if payload.startswith(b'\x42\x4D\x42\x32'):  # BMB2
            return 'bambu_v2'
        elif payload.startswith(b'\x42\x4D\x42'):  # BMB
            return 'bambu_v1'
        
        return None
    
    def decode_payload(self, payload: bytes) -> Optional[Dict]:
        """
        Decode a single NFC payload into structured data.
        
        Args:
            payload (bytes): Raw NFC payload data
            
        Returns:
            dict: Decoded filament data or None if decoding fails
        """
        self.decode_count += 1
        
        try:
            format_type = self.detect_format(payload)
            if not format_type:
                return None
                
            format_info = self.PAYLOAD_FORMATS[format_type]
            
            # Ensure payload is long enough for the expected format
            expected_size = struct.calcsize(format_info['format'])
            if len(payload) < expected_size:
                return None
                
            # Unpack the binary data
            unpacked_data = struct.unpack(format_info['format'], payload[:expected_size])
            
            # Create structured dictionary
            result = {}
            for i, field in enumerate(format_info['fields']):
                value = unpacked_data[i]
                
                # Clean up string fields
                if isinstance(value, bytes):
                    if field == 'header':
                        continue  # Skip header in result
                    value = value.decode('utf-8').rstrip('\x00')
                
                result[field] = value
            
            return result
            
        except (struct.error, UnicodeDecodeError, IndexError) as e:
            # Payload could not be decoded
            return None
    
    def batch_decode(self, payloads: List[bytes]) -> List[Optional[Dict]]:
        """
        Decode a batch of NFC payloads.
        
        Args:
            payloads (List[bytes]): List of raw NFC payload data
            
        Returns:
            List[Optional[Dict]]: List of decoded filament data (None for failed decodes)
        """
        results = []
        for payload in payloads:
            result = self.decode_payload(payload)
            results.append(result)
        return results
    
    def get_decode_count(self) -> int:
        """Get the total number of decode operations performed."""
        return self.decode_count
    
    def reset_count(self):
        """Reset the decode counter."""
        self.decode_count = 0


def generate_sample_payload(format_type: str = 'bambu_v1', **kwargs) -> bytes:
    """
    Generate a sample NFC payload for testing purposes.
    
    Args:
        format_type (str): Payload format type
        **kwargs: Field values to override defaults
        
    Returns:
        bytes: Generated NFC payload
    """
    if format_type not in NFCDecoder.PAYLOAD_FORMATS:
        raise ValueError(f"Unknown format type: {format_type}")
    
    format_info = NFCDecoder.PAYLOAD_FORMATS[format_type]
    
    # Default values
    defaults = {
        'bambu_v1': {
            'header': b'\x42\x4D\x42',
            'name': b'Bambu PLA Basic',
            'type': b'PLA',
            'color': b'#FF0000',
            'density': 1.24,
            'diameter': 1.75,
            'nozzle_temp': 210,
            'bed_temp': 60,
            'remaining_length': 240.0,
            'remaining_weight': 1000.0
        },
        'bambu_v2': {
            'header': b'\x42\x4D\x42\x32',
            'name': b'Bambu PLA Basic',
            'type': b'PLA',
            'color': b'#FF0000',
            'manufacturer': b'Bambulab',
            'density': 1.24,
            'diameter': 1.75,
            'nozzle_temp': 210,
            'bed_temp': 60,
            'remaining_length': 240.0,
            'remaining_weight': 1000.0,
            'serial_number': 12345
        }
    }
    
    # Merge with provided kwargs
    values = defaults[format_type].copy()
    for key, value in kwargs.items():
        if key in values:
            if isinstance(values[key], bytes) and isinstance(value, str):
                values[key] = value.encode('utf-8')
            else:
                values[key] = value
    
    # Ensure string fields are properly padded/truncated
    for field in format_info['fields']:
        if field in values and isinstance(values[field], bytes):
            if field == 'name':
                values[field] = values[field][:32].ljust(32, b'\x00')
            elif field == 'type':
                values[field] = values[field][:32].ljust(32, b'\x00')
            elif field == 'color':
                values[field] = values[field][:16].ljust(16, b'\x00')
            elif field == 'manufacturer':
                values[field] = values[field][:32].ljust(32, b'\x00')
    
    # Pack the data
    field_values = [values[field] for field in format_info['fields']]
    return struct.pack(format_info['format'], *field_values)