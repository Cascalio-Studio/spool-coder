#!/usr/bin/env python
"""
Security demonstration script for NFC unauthorized access
This script demonstrates the security features implemented for Issue #4
"""

import sys
import os

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from services.nfc.device import NFCDevice
from services.auth.authorization import get_auth_service

def main():
    """
    Demonstrate security functionality
    """
    print("=== Security Test: Unauthorized NFC Access ===\n")
    
    # Create NFC device
    nfc_device = NFCDevice()
    nfc_device.connect()
    auth_service = get_auth_service()
    
    print("1. Testing unauthorized read access...")
    print(f"   - Current authorization status: {auth_service.is_authorized()}")
    print("   - Attempting to read NFC data without authorization...")
    
    read_result = nfc_device.read_tag()
    if read_result is None:
        print("   ✓ ACCESS DENIED - Unauthorized read was properly blocked")
    else:
        print("   ✗ SECURITY BREACH - Unauthorized read was allowed!")
    
    print("\n2. Testing unauthorized write access...")
    test_data = {"name": "Test Filament", "type": "PLA"}
    print("   - Attempting to write NFC data without authorization...")
    
    write_result = nfc_device.write_tag(test_data)
    if write_result is False:
        print("   ✓ ACCESS DENIED - Unauthorized write was properly blocked")
    else:
        print("   ✗ SECURITY BREACH - Unauthorized write was allowed!")
    
    print("\n3. Testing authorized access (control test)...")
    print("   - Authenticating user...")
    auth_result = auth_service.authenticate_user("admin", "admin123")
    
    if auth_result:
        print("   ✓ Authentication successful")
        print(f"   - Current authorization status: {auth_service.is_authorized()}")
        print("   - Current user:", auth_service.get_current_user())
        
        print("   - Attempting authorized read...")
        read_result = nfc_device.read_tag()
        if read_result is not None:
            print("   ✓ Authorized read successful")
            print(f"   - Read data: {read_result.get('name', 'Unknown')} ({read_result.get('type', 'Unknown')})")
        else:
            print("   ✗ Authorized read failed unexpectedly")
        
        print("   - Attempting authorized write...")
        write_result = nfc_device.write_tag(test_data)
        if write_result is True:
            print("   ✓ Authorized write successful")
        else:
            print("   ✗ Authorized write failed unexpectedly")
    else:
        print("   ✗ Authentication failed")
    
    print("\n4. Testing authorization revocation...")
    auth_service.revoke_authorization()
    print("   - Authorization revoked")
    print(f"   - Current authorization status: {auth_service.is_authorized()}")
    
    read_result = nfc_device.read_tag()
    if read_result is None:
        print("   ✓ Access properly denied after revocation")
    else:
        print("   ✗ Access still allowed after revocation - Security issue!")
    
    nfc_device.disconnect()
    
    print("\n=== Security Test Complete ===")
    print("Expected behavior:")
    print("- Unauthorized access attempts should be denied")
    print("- Security events should be logged (check console output above)")
    print("- Authorized access should work normally")
    print("- Access should be denied after authorization revocation")

if __name__ == "__main__":
    main()