# NFC Decode Regression Testing

This document describes the regression testing setup for the NFC decode functionality in the spool-coder application.

## Purpose

The NFC decode regression tests ensure that previously passing NFC payloads continue to decode correctly after code changes. This prevents regressions in the core functionality that could break support for existing BambuLab filament spools.

## Test Coverage

### Valid Payload Tests (`test_nfc_decode_regression.py`)

The regression test suite includes comprehensive coverage of:

#### Filament Types
- **PLA**: Basic, Matte, Silk variants
- **PETG**: Basic and High-Flow (HF) variants  
- **ABS**: Standard configuration
- **ASA**: UV-resistant filament
- **TPU**: Flexible filament (95A shore hardness)
- **PC**: Polycarbonate high-temperature filament
- **PA-CF**: Carbon fiber reinforced nylon

#### Temperature Ranges
- Low temperature: TPU (230°C nozzle, 50°C bed)
- Standard temperature: PLA (210°C nozzle, 60°C bed)  
- High temperature: PC (300°C nozzle, 100°C bed)
- Extreme temperature: PA-CF (320°C nozzle, 90°C bed)

#### Spool States
- Full new spools (1000g, 330m)
- Partially used spools (various amounts)
- Nearly empty spools (20g, 5m)

#### Color Variations
- Standard colors (white, black, red, green, blue)
- Custom colors (purple, grey, yellow)
- Hex color code format validation

### Error Handling Tests

#### Invalid Payload Scenarios
- Missing required fields (name, type, etc.)
- Invalid data types (string instead of number)
- Negative values (weight, length)
- Empty payloads
- Corrupted color formats
- None/null payloads

### Integration Tests (`test_nfc_integration.py`)

#### Device Integration
- NFC device connection/disconnection cycles
- Tag reading workflow
- State management validation
- Multiple read cycle stability

#### End-to-End Workflows
- Complete user read workflow simulation
- Error recovery scenarios
- Data consistency validation

## Running the Tests

### All Tests
```bash
python -m pytest tests/ -v
```

### Regression Tests Only
```bash
python -m pytest tests/test_nfc_decode_regression.py -v
```

### Integration Tests Only
```bash
python -m pytest tests/test_nfc_integration.py -v
```

### With Coverage Report
```bash
python -m pytest tests/ --cov=src --cov-report=html
```

## Test Data

Test data is centralized in `tests/test_data.py` and includes:

- `ALL_VALID_PAYLOADS`: 13 different valid filament configurations
- `INVALID_PAYLOADS`: 5 different invalid/malformed scenarios

### Sample Valid Payload
```python
BAMBU_PLA_BASIC = {
    "name": "Bambu PLA Basic",
    "type": "PLA", 
    "color": "#FFFFFF",
    "manufacturer": "Bambulab",
    "density": 1.24,
    "diameter": 1.75,
    "nozzle_temp": 210,
    "bed_temp": 60,
    "remaining_length": 240,
    "remaining_weight": 1000
}
```

## Expected Results

All tests should pass with the current implementation:

- **38 test cases** in the regression test suite
- **6 test cases** in the integration test suite  
- **100% pass rate** for valid payloads
- **Graceful handling** of invalid payloads (no crashes)

## Continuous Integration

These tests should be run:

1. **Before any changes** to the NFC decoding logic
2. **After any changes** to ensure no regressions
3. **In CI/CD pipelines** for pull requests
4. **Before releases** as part of the validation process

## Adding New Test Cases

When adding support for new filament types or configurations:

1. Add sample payload data to `tests/test_data.py`
2. Add the payload to `ALL_VALID_PAYLOADS` list
3. Run tests to ensure the new payload decodes correctly
4. Update this documentation with the new filament type

## Troubleshooting

### Test Failures
If regression tests fail after code changes:

1. **Check error messages** for specific payload that failed
2. **Verify the changes** didn't alter expected default values
3. **Update test expectations** if the changes are intentional
4. **Fix the decoding logic** if the failure indicates a bug

### Adding New Error Cases
When adding new validation logic:

1. Add corresponding invalid payload to `INVALID_PAYLOADS`
2. Ensure the test verifies the expected error behavior
3. Document the new validation requirement

## References

- [Bambu Research Group RFID Tag Guide](https://github.com/Bambu-Research-Group/RFID-Tag-Guide)
- Issue #3: Validate and Test NFC Decoding Module
- Issue #14: Test: Regression (NFC Decode)