# Bambu Lab NFC Algorithm

This module provides an implementation of the algorithm needed to decode and encode data from Bambu Lab filament spool NFC tags.

## Overview

Bambu Lab 3D printers use NFC-tagged filament spools for automatic material detection and tracking. This implementation allows the Spool-Coder application to:

1. Read and decode data from original Bambu Lab filament spools
2. Encode and write data to blank NFC tags to create compatible spools

The implementation is based on research from [Bambu-Research-Group/RFID-Tag-Guide](https://github.com/Bambu-Research-Group/RFID-Tag-Guide).

## Key Features

- Decoding of Bambu Lab NFC tag data format
- Encoding of compatible data for writing to blank NFC tags
- Checksum validation to ensure data integrity
- Support for all Bambu Lab filament types
- Error detection for data corruption

## Tag Data Structure

The NFC tag data uses the following structure:

- Header: `0xAA55CC33` (4 bytes)
- Version and flags (4 bytes)
- Encrypted data sections:
  - Spool data (starting at offset 128):
    - Filament type (2 bytes)
    - Color RGB (3 bytes)
    - Diameter (4 bytes, float)
    - Nozzle temperature (2 bytes)
    - Bed temperature (2 bytes)
    - Material density (4 bytes, float)
    - Remaining length (4 bytes, float)
    - Remaining weight (4 bytes, float)
    - Manufacturer name (32 bytes, string)
    - Filament name (32 bytes, string)
  - Manufacturing information (starting at offset 256):
    - Serial number (32 bytes, string)
    - Manufacturing date (4 bytes, timestamp)
- Checksum (4 bytes, CRC32 at offset 512)

## Usage

### Decoding NFC Tag Data

```python
from services.nfc.bambu_algorithm import BambuLabNFCDecoder

# Create a decoder instance
decoder = BambuLabNFCDecoder()

# Decode raw tag data
raw_data = ... # bytes from NFC tag
decoded_data = decoder.decode_tag_data(raw_data)

if decoded_data:
    # Access decoded information
    filament_type = decoded_data["spool_data"]["type"]
    color = decoded_data["spool_data"]["color"]
    diameter = decoded_data["spool_data"]["diameter"]
    remaining_weight = decoded_data["spool_data"]["remaining_weight"]
else:
    # Decoding failed (invalid tag or corrupted data)
    print("Failed to decode tag data")
```

### Encoding NFC Tag Data

```python
from services.nfc.bambu_algorithm import BambuLabNFCEncoder

# Create an encoder instance
encoder = BambuLabNFCEncoder()

# Prepare data to encode
spool_data = {
    "version": 1,
    "flags": "000000",
    "spool_data": {
        "type": "PLA",
        "color": "#1E88E5",
        "diameter": 1.75,
        "nozzle_temp": 220,
        "bed_temp": 60,
        "density": 1.24,
        "remaining_length": 240.0,
        "remaining_weight": 1000.0,
        "manufacturer": "My Brand",
        "name": "My Custom PLA"
    },
    "manufacturing_info": {
        "serial": "CUSTOM123456",
        "date": 1689598000  # Unix timestamp
    }
}

# Encode the data
encoded_data = encoder.encode_tag_data(spool_data)

# Write encoded_data to NFC tag
```

## Testing

The algorithm includes unit tests to verify correct functionality. Run the tests with:

```
python -m unittest tests.unit.test_bambu_algorithm
```

## Example

An example script is included to demonstrate the use of the algorithm:

```
python -m examples.bambu_algorithm_example
```

This will generate a sample tag data file and demonstrate encoding and decoding.

## Supported Filament Types

The following filament types are recognized:

- PLA Basic (0)
- PLA (1)
- PETG Basic (2)
- PETG (3)
- ABS (4)
- TPU (5)
- PLA-CF (6)
- PA-CF (7)
- PET-CF (8)
- ASA (9)
- PC (10)
- PA (11)
- Support (12)
- PVA (13)
- HIPS (14)
