#!/usr/bin/env python
"""
Test: Read Raw NFC Data

Purpose: Confirm NFC reader can acquire raw payload data from tag.
Input: Present valid BambuLab spool tag to the reader.
Expected Output: Raw NFC payload (byte stream) is returned

Related to: #1
"""

import sys
import os

# Add src directory to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from services.nfc.device import NFCDevice


def test_nfc_raw_data_reading():
    """
    Test that NFC reader can acquire raw payload data from a BambuLab spool tag.
    
    Steps:
    1. Initialize NFC device
    2. Connect to the device
    3. Trigger NFC read operation for raw data
    4. Verify raw payload (byte stream) is returned
    """
    print("=== Test: Read Raw NFC Data ===")
    print("Purpose: Confirm NFC reader can acquire raw payload data from tag")
    print()
    
    # Step 1: Initialize NFC device
    print("Step 1: Initializing NFC device...")
    nfc_device = NFCDevice()
    assert nfc_device is not None, "Failed to initialize NFC device"
    print("✓ NFC device initialized successfully")
    
    # Step 2: Connect to the device
    print("\nStep 2: Connecting to NFC device...")
    connection_successful = nfc_device.connect()
    assert connection_successful, "Failed to connect to NFC device"
    assert nfc_device.is_connected(), "Device reports as not connected"
    print("✓ Successfully connected to NFC device")
    
    # Step 3: Trigger NFC read operation for raw data
    print("\nStep 3: Reading raw NFC payload data...")
    print("(Simulating: Present valid BambuLab spool tag to the reader)")
    
    raw_data = nfc_device.read_raw_data()
    
    # Step 4: Verify raw payload (byte stream) is returned
    print("\nStep 4: Validating raw payload data...")
    
    # Check that raw data was returned
    assert raw_data is not None, "No raw data returned from NFC device"
    print("✓ Raw data returned from NFC device")
    
    # Check that it's bytes
    assert isinstance(raw_data, bytes), f"Expected bytes, got {type(raw_data)}"
    print("✓ Raw data is byte stream as expected")
    
    # Check that it contains data
    assert len(raw_data) > 0, "Raw data is empty"
    print(f"✓ Raw data contains {len(raw_data)} bytes")
    
    # Display raw payload information
    print(f"\n--- Raw NFC Payload Data ---")
    print(f"Data length: {len(raw_data)} bytes")
    print(f"First 16 bytes (hex): {raw_data[:16].hex().upper()}")
    print(f"Last 16 bytes (hex): {raw_data[-16:].hex().upper()}")
    
    # Verify it contains expected BambuLab data patterns
    # The simulated data should contain JSON-like structure
    try:
        # Look for common patterns in BambuLab spool data
        data_str = raw_data.decode('utf-8', errors='ignore')
        assert 'Bambu' in data_str, "Expected BambuLab identifier in raw data"
        assert 'PLA' in data_str, "Expected filament type in raw data"
        print("✓ Raw data contains expected BambuLab spool patterns")
    except UnicodeDecodeError:
        # If it's pure binary data, check for header patterns
        assert raw_data[0:4] == bytes([0x01, 0x02, 0x03, 0x04]), "Expected NFC header pattern"
        print("✓ Raw data contains expected NFC header pattern")
    
    # Cleanup
    nfc_device.disconnect()
    print("✓ Disconnected from NFC device")
    
    print(f"\n=== TEST PASSED ===")
    print("✅ NFC reader successfully acquired raw payload data from tag")
    print("✅ Raw NFC payload (byte stream) was returned as expected")
    
    return True


def test_nfc_device_error_handling():
    """
    Test error handling when device is not connected.
    """
    print("\n=== Test: Error Handling ===")
    
    nfc_device = NFCDevice()
    
    # Try to read without connecting
    raw_data = nfc_device.read_raw_data()
    assert raw_data is None, "Expected None when device not connected"
    print("✓ Proper error handling when device not connected")
    
    return True


if __name__ == "__main__":
    print("Starting NFC Raw Data Reading Tests...")
    print("=" * 50)
    
    try:
        # Run the main test
        test_nfc_raw_data_reading()
        
        # Run error handling test
        test_nfc_device_error_handling()
        
        print("\n" + "=" * 50)
        print("🎉 ALL TESTS PASSED!")
        print("NFC reader can successfully acquire raw payload data from BambuLab spool tags.")
        
    except AssertionError as e:
        print(f"\n❌ TEST FAILED: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"\n💥 UNEXPECTED ERROR: {e}")
        sys.exit(1)