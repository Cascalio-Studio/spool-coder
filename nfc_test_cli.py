#!/usr/bin/env python
"""
Windows Application Test CLI for NFC Raw Data Reading

This provides a command-line interface to test the NFC raw data reading functionality
as specified in the test requirements.

Purpose: Confirm NFC reader can acquire raw payload data from tag.
Input: Present valid BambuLab spool tag to the reader.
Expected Output: Raw NFC payload (byte stream) is returned
"""

import sys
import os

# Add src directory to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from services.nfc.device import NFCDevice


def main():
    """
    Main function for the Windows application test.
    
    Steps:
    1. Start the Windows application.
    2. Trigger NFC read operation.
    """
    print("Spool-Coder NFC Raw Data Test")
    print("=" * 40)
    print("Purpose: Confirm NFC reader can acquire raw payload data from tag")
    print("Input: Present valid BambuLab spool tag to the reader")
    print()
    
    # Initialize NFC device
    print("Initializing NFC device...")
    nfc_device = NFCDevice()
    
    # Main loop
    while True:
        print("\nCommands:")
        print("1. Read NFC tag (parsed data)")
        print("2. Read raw NFC data (byte stream)")
        print("3. Check device status")
        print("4. Exit")
        
        choice = input("\nEnter command (1-4): ").strip()
        
        if choice == '1':
            read_parsed_data(nfc_device)
        elif choice == '2':
            read_raw_data(nfc_device)
        elif choice == '3':
            check_device_status(nfc_device)
        elif choice == '4':
            break
        else:
            print("Invalid choice. Please enter 1-4.")
    
    # Cleanup
    if nfc_device.is_connected():
        nfc_device.disconnect()
    print("\nExiting application...")


def read_parsed_data(nfc_device):
    """
    Read and display parsed NFC tag data.
    """
    print("\n--- Reading NFC Tag (Parsed Data) ---")
    
    if not nfc_device.is_connected():
        print("Connecting to NFC device...")
        if not nfc_device.connect():
            print("❌ Failed to connect to NFC device")
            return
        print("✓ Connected to NFC device")
    
    print("Please present BambuLab spool tag to the reader...")
    print("Reading tag data...")
    
    data = nfc_device.read_tag()
    
    if data:
        print("✅ Tag read successfully!")
        print("\nParsed data:")
        for key, value in data.items():
            print(f"  {key}: {value}")
    else:
        print("❌ Failed to read tag data")
    
    print("Disconnecting from device...")
    nfc_device.disconnect()


def read_raw_data(nfc_device):
    """
    Read and display raw NFC data (byte stream).
    This is the main test function for the requirements.
    """
    print("\n--- Reading Raw NFC Data (Byte Stream) ---")
    print("This tests the requirement: 'Raw NFC payload (byte stream) is returned'")
    
    if not nfc_device.is_connected():
        print("Connecting to NFC device...")
        if not nfc_device.connect():
            print("❌ Failed to connect to NFC device")
            return
        print("✓ Connected to NFC device")
    
    print("Please present valid BambuLab spool tag to the reader...")
    print("Triggering NFC read operation for raw data...")
    
    raw_data = nfc_device.read_raw_data()
    
    if raw_data:
        print("✅ Raw NFC payload acquired successfully!")
        print(f"\nRaw payload information:")
        print(f"  Data type: {type(raw_data).__name__}")
        print(f"  Data length: {len(raw_data)} bytes")
        
        # Display hex dump of first and last bytes
        print(f"\nHex dump (first 32 bytes):")
        hex_data = raw_data[:32].hex().upper()
        for i in range(0, len(hex_data), 16):
            line = hex_data[i:i+16]
            spaced_line = ' '.join(line[j:j+2] for j in range(0, len(line), 2))
            print(f"  {i//2:04X}: {spaced_line}")
        
        if len(raw_data) > 32:
            print(f"\nHex dump (last 32 bytes):")
            hex_data = raw_data[-32:].hex().upper()
            for i in range(0, len(hex_data), 16):
                line = hex_data[i:i+16]
                spaced_line = ' '.join(line[j:j+2] for j in range(0, len(line), 2))
                offset = len(raw_data) - 32 + i//2
                print(f"  {offset:04X}: {spaced_line}")
        
        # Try to extract readable content
        print(f"\nContent analysis:")
        try:
            # Look for JSON content
            json_start = raw_data.find(b'{')
            json_end = raw_data.rfind(b'}')
            
            if json_start != -1 and json_end != -1:
                json_data = raw_data[json_start:json_end+1]
                decoded_json = json_data.decode('utf-8', errors='ignore')
                print(f"  Found JSON data: {decoded_json[:100]}...")
            else:
                print("  No JSON data found in payload")
                
            # Check for BambuLab identifiers
            content = raw_data.decode('utf-8', errors='ignore')
            if 'Bambu' in content:
                print("  ✓ Contains BambuLab identifier")
            if 'PLA' in content or 'ABS' in content or 'PETG' in content:
                print("  ✓ Contains filament type identifier")
                
        except Exception as e:
            print(f"  Content analysis failed: {e}")
        
        print(f"\n🎉 TEST REQUIREMENT MET:")
        print(f"✅ Raw NFC payload (byte stream) has been successfully returned")
        
    else:
        print("❌ Failed to read raw NFC data")
    
    print("Disconnecting from device...")
    nfc_device.disconnect()


def check_device_status(nfc_device):
    """
    Check and display device connection status.
    """
    print("\n--- Device Status ---")
    
    if nfc_device.is_connected():
        print("✓ Device is connected")
    else:
        print("❌ Device is not connected")
        print("Attempting to connect...")
        
        if nfc_device.connect():
            print("✓ Successfully connected to device")
        else:
            print("❌ Failed to connect to device")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nOperation cancelled by user")
    except Exception as e:
        print(f"\nUnexpected error: {e}")
        sys.exit(1)