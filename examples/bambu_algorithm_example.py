#!/usr/bin/env python
"""
Example script demonstrating the use of the Bambu Lab NFC algorithm
"""

import sys
import os
import json
import base64
from src.services.nfc.bambu_algorithm import BambuLabNFCEncoder, BambuLabNFCDecoder, SAMPLE_TAG_DATA
from src.models.filament import FilamentSpool


def test_algorithm():
    """Test the basic functionality of the algorithm"""
    print("Testing Bambu Lab NFC algorithm...")
    
    # Create encoder and decoder instances
    encoder = BambuLabNFCEncoder()
    decoder = BambuLabNFCDecoder()
    
    # Encode the sample data
    print("Encoding sample data...")
    encoded = encoder.encode_tag_data(SAMPLE_TAG_DATA)
    
    # Print out a sample of the encoded data
    print(f"Encoded data (first 32 bytes): {encoded[:32].hex()}")
    print(f"Total encoded data size: {len(encoded)} bytes")
    
    # Save the encoded data to a file in base64 format
    base64_data = base64.b64encode(encoded).decode('ascii')
    with open("sample_tag.b64", "w") as f:
        f.write(base64_data)
    print("Sample tag data saved to 'sample_tag.b64'")
    
    # Decode the data
    print("\nDecoding data...")
    decoded = decoder.decode_tag_data(encoded)
    
    if decoded:
        print("Successfully decoded data:")
        print(json.dumps(decoded, indent=2))
        
        # Check key fields
        print("\nKey fields verification:")
        spool_data = decoded["spool_data"]
        print(f"Type: {spool_data['type']}")
        print(f"Color: {spool_data['color']}")
        print(f"Diameter: {spool_data['diameter']} mm")
        print(f"Density: {spool_data['density']} g/cm³")
        print(f"Nozzle Temp: {spool_data['nozzle_temp']}°C")
        print(f"Bed Temp: {spool_data['bed_temp']}°C")
        print(f"Remaining Length: {spool_data['remaining_length']} m")
        print(f"Remaining Weight: {spool_data['remaining_weight']} g")
        print(f"Manufacturer: {spool_data['manufacturer']}")
        print(f"Name: {spool_data['name']}")
        
        # Create FilamentSpool object from decoded data
        print("\nCreating FilamentSpool object from decoded data...")
        spool = FilamentSpool(
            name=spool_data["name"],
            type=spool_data["type"],
            color=spool_data["color"],
            manufacturer=spool_data["manufacturer"],
            density=spool_data["density"],
            diameter=spool_data["diameter"],
            nozzle_temp=spool_data["nozzle_temp"],
            bed_temp=spool_data["bed_temp"],
            remaining_length=spool_data["remaining_length"],
            remaining_weight=spool_data["remaining_weight"]
        )
        
        print("FilamentSpool object created successfully!")
        print(f"Name: {spool.name}, Type: {spool.type}, Color: {spool.color}")
    else:
        print("Failed to decode tag data!")


def test_data_corruption():
    """Test the algorithm's ability to detect data corruption"""
    print("Testing data corruption detection...")
    
    # Create encoder and decoder instances
    encoder = BambuLabNFCEncoder()
    decoder = BambuLabNFCDecoder()
    
    # Encode the sample data
    encoded = encoder.encode_tag_data(SAMPLE_TAG_DATA)
    
    # Corrupt the data in various ways
    corruptions = [
        ("Header corruption", bytearray(encoded[:]), 0, 0x99),
        ("Data corruption", bytearray(encoded[:]), 100, 0x99),
        ("Checksum corruption", bytearray(encoded[:]), 512, 0x99)
    ]
    
    for name, data, pos, val in corruptions:
        # Apply corruption
        data[pos] = val
        
        # Try to decode
        result = decoder.decode_tag_data(bytes(data))
        
        if result is None:
            print(f"✅ {name} detected successfully!")
        else:
            print(f"❌ {name} not detected!")


if __name__ == "__main__":
    # Add the project root to the Python path
    project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    if project_root not in sys.path:
        sys.path.append(project_root)
    
    print("Bambu Lab NFC Algorithm Example")
    print("================================\n")
    
    test_algorithm()
    print("\n")
    test_data_corruption()
