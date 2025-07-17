"""
NFC Payload Decoder for BambuLab Spool Tags

This module provides functionality to decode raw NFC payload data from
BambuLab filament spool tags and convert it into FilamentSpool objects.
"""

from models.filament import FilamentSpool


def decode_nfc_payload(raw_payload):
    """
    Decode raw NFC payload data from a BambuLab spool tag.

    This is a simplified decoder implementation that handles basic PLA
    spool data. The payload format is assumed to be:
    - Bytes 0-2: Material type (ASCII, e.g., "PLA")
    - Bytes 3-5: Color (RGB hex, e.g., 0xFF0000 for red)
    - Bytes 6-7: Nozzle temperature * 10 (e.g., 2100 for 210°C)
    - Bytes 8-9: Bed temperature (e.g., 60 for 60°C)
    - Bytes 10-11: Remaining length in meters
    - Bytes 12-13: Remaining weight in grams
    - Bytes 14+: Manufacturer name (ASCII)

    Args:
        raw_payload (bytes): Raw NFC payload data

    Returns:
        FilamentSpool: Decoded filament spool object, or None if decoding
                      fails
    """
    if not raw_payload or len(raw_payload) < 14:
        return None

    try:
        # Decode material type (first 3 bytes as ASCII)
        material_bytes = raw_payload[0:3]
        material_type = material_bytes.decode('ascii').rstrip('\x00')

        # Decode color (next 3 bytes as RGB hex)
        color_r = raw_payload[3]
        color_g = raw_payload[4]
        color_b = raw_payload[5]
        color = f"#{color_r:02X}{color_g:02X}{color_b:02X}"

        # Decode nozzle temperature (2 bytes, big endian, divided by 10)
        nozzle_temp_raw = (raw_payload[6] << 8) | raw_payload[7]
        nozzle_temp = nozzle_temp_raw // 10

        # Decode bed temperature (2 bytes, big endian)
        bed_temp = (raw_payload[8] << 8) | raw_payload[9]

        # Decode remaining length (2 bytes, big endian)
        remaining_length = (raw_payload[10] << 8) | raw_payload[11]

        # Decode remaining weight (2 bytes, big endian)
        remaining_weight = (raw_payload[12] << 8) | raw_payload[13]

        # Decode manufacturer (remaining bytes as ASCII)
        manufacturer = ""
        if len(raw_payload) > 14:
            manufacturer_bytes = raw_payload[14:]
            manufacturer = (manufacturer_bytes.decode('ascii')
                            .rstrip('\x00'))

        # Create and return FilamentSpool object
        return FilamentSpool(
            name=(f"{manufacturer} {material_type}"
                  if manufacturer else material_type),
            type=material_type,
            color=color,
            manufacturer=manufacturer,
            density=1.24,  # Default PLA density
            diameter=1.75,  # Standard diameter
            nozzle_temp=nozzle_temp,
            bed_temp=bed_temp,
            remaining_length=remaining_length,
            remaining_weight=remaining_weight
        )

    except (UnicodeDecodeError, IndexError, ValueError):
        # Return None if any decoding error occurs
        return None
