# NFC Malformed Data Handling

This document describes the robust error handling implemented for NFC payload decoding in the spool-coder application.

## Overview

The application now handles malformed NFC tag data gracefully to ensure:
- **No crashes** when encountering invalid or corrupted NFC data
- **Proper logging** of parsing errors for debugging
- **Graceful degradation** with sensible defaults when possible

## Components

### NFCPayloadDecoder (`src/services/nfc/decoder.py`)

The main decoder class that handles various payload formats:

- **Dictionary payloads**: Direct field validation with type checking
- **String payloads**: JSON or hex string decoding
- **Binary payloads**: Simulated BambuLab binary format parsing

#### Error Handling Features

1. **Field Validation**:
   - Type conversion (string ↔ number)
   - Range validation (temperatures, densities, etc.)
   - String length limits with truncation
   - Default value substitution for invalid fields

2. **Payload Format Handling**:
   - Automatic format detection (dict/string/binary)
   - Multiple fallback strategies for string payloads
   - Binary structure validation with corruption handling

3. **Logging**:
   - Detailed error messages for each validation failure
   - Warning messages for out-of-range values
   - Info messages for successful operations

### Enhanced NFCDevice (`src/services/nfc/device.py`)

Updated to use the robust decoder with comprehensive error handling:

- Uses `NFCPayloadDecoder` for all tag reading operations
- Logs connection, read, and write operations
- Returns `None` instead of crashing on errors
- Validates data before writing to tags

## Error Scenarios Handled

### 1. Payload Format Errors
- **None/null payloads**: Raises `NFCDecodingError`
- **Empty dictionaries**: Returns defaults for all fields
- **Invalid JSON**: Attempts hex decoding, then fails gracefully
- **Invalid hex strings**: Proper error messages and logging
- **Unexpected types**: Clear error messages for unsupported types

### 2. Data Validation Errors
- **Invalid data types**: Automatic type conversion where possible
- **Out-of-range values**: Uses defaults with warning logs
- **Oversized strings**: Truncates to maximum allowed length
- **Missing fields**: Fills with appropriate default values

### 3. Binary Format Errors
- **Too short payloads**: Clear minimum size requirements
- **Corrupted structure**: Extracts what's possible, defaults for rest
- **Invalid magic numbers**: Logs warning but continues processing

## Usage Examples

### Basic Usage
```python
from services.nfc import NFCDevice, NFCDecodingError

device = NFCDevice()
device.connect()

try:
    data = device.read_tag()  # Never crashes, returns None on error
    if data:
        print(f"Read filament: {data['name']}")
    else:
        print("No valid data found")
except Exception as e:
    print(f"Unexpected error: {e}")  # Should not happen with malformed data

device.disconnect()
```

### Direct Decoder Usage
```python
from services.nfc import NFCPayloadDecoder, NFCDecodingError

decoder = NFCPayloadDecoder()

# This will not crash, will use defaults
malformed_data = {"name": "Test", "nozzle_temp": "not_a_number"}
try:
    result = decoder.decode_payload(malformed_data)
    print(f"Decoded: {result['name']}, temp: {result['nozzle_temp']}")
except NFCDecodingError as e:
    print(f"Decoding failed: {e}")
```

## Logging Configuration

The decoder uses Python's standard logging module. To see detailed error messages:

```python
import logging
logging.basicConfig(level=logging.WARNING)

# or for more detailed debugging:
logging.getLogger('services.nfc').setLevel(logging.DEBUG)
```

## Testing

Run the comprehensive test suite to verify malformed data handling:

```bash
# Run unit tests for malformed payloads
python test_malformed_nfc.py

# Run integration tests demonstrating end-to-end handling
python integration_test.py
```

## Default Values

When fields cannot be validated, the following defaults are used:

| Field | Default Value | Type |
|-------|---------------|------|
| name | "Unknown Filament" | string |
| type | "PLA" | string |
| color | "#FFFFFF" | string |
| manufacturer | "Unknown" | string |
| density | 1.24 | float |
| diameter | 1.75 | float |
| nozzle_temp | 200 | int |
| bed_temp | 60 | int |
| remaining_length | 0 | float |
| remaining_weight | 0 | float |

## Validation Rules

### String Fields
- **Maximum lengths**: name (64), type (16), color (7), manufacturer (32)
- **Truncation**: Oversized strings are truncated with warning log
- **Type conversion**: Non-strings are converted to string representation

### Numeric Fields
- **Temperature ranges**: nozzle_temp (150-350°C), bed_temp (0-150°C)
- **Material ranges**: density (0.5-5.0 g/cm³), diameter (1.0-3.0 mm)
- **Weight/length**: remaining values must be non-negative
- **Type conversion**: String numbers are converted to appropriate numeric types

### Special Cases
- **NaN/Infinite values**: Replaced with defaults
- **Negative values**: For weight/length fields, replaced with 0
- **Missing fields**: Filled with appropriate defaults

This robust error handling ensures that the application remains stable and usable even when encountering corrupted or malformed NFC tag data, meeting the requirements specified in issue #13.