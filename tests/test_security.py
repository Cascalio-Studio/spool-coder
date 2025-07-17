"""
Test security functionality for unauthorized NFC access
"""

import pytest
import sys
import os
from unittest.mock import patch, MagicMock

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from services.nfc.device import NFCDevice
from services.auth.authorization import AuthorizationService, get_auth_service
from services.auth.security_logger import SecurityLogger, get_security_logger


class TestUnauthorizedNFCAccess:
    """
    Test suite for unauthorized NFC access security
    """
    
    def setup_method(self):
        """Setup for each test method"""
        # Reset authorization state
        auth_service = get_auth_service()
        auth_service.revoke_authorization()
        
        # Create fresh NFC device
        self.nfc_device = NFCDevice()
        self.nfc_device.connect()
    
    def teardown_method(self):
        """Cleanup after each test method"""
        if hasattr(self, 'nfc_device'):
            self.nfc_device.disconnect()
    
    def test_unauthorized_read_access_denied(self):
        """
        Test: Unauthorized NFC read access should be denied
        Expected: Access denied, returns None
        """
        # Ensure not authorized
        auth_service = get_auth_service()
        assert not auth_service.is_authorized()
        
        # Attempt to read NFC data without authorization
        result = self.nfc_device.read_tag()
        
        # Verify access was denied
        assert result is None, "Unauthorized read access should return None"
    
    def test_unauthorized_write_access_denied(self):
        """
        Test: Unauthorized NFC write access should be denied
        Expected: Access denied, returns False
        """
        # Ensure not authorized
        auth_service = get_auth_service()
        assert not auth_service.is_authorized()
        
        # Sample data to write
        test_data = {
            "name": "Test Filament",
            "type": "PLA",
            "color": "#FF0000"
        }
        
        # Attempt to write NFC data without authorization
        result = self.nfc_device.write_tag(test_data)
        
        # Verify access was denied
        assert result is False, "Unauthorized write access should return False"
    
    @patch('services.auth.security_logger.logging.getLogger')
    def test_unauthorized_access_logged(self, mock_get_logger):
        """
        Test: Unauthorized access attempts should be logged
        Expected: Security events are logged
        """
        # Setup mock logger
        mock_logger = MagicMock()
        mock_get_logger.return_value = mock_logger
        
        # Create a fresh security logger instance with mocked logger
        from services.auth.security_logger import SecurityLogger
        security_logger = SecurityLogger()
        security_logger.logger = mock_logger
        
        # Patch the NFC device to use our mock logger
        self.nfc_device.security_logger = security_logger
        
        # Ensure not authorized
        auth_service = get_auth_service()
        assert not auth_service.is_authorized()
        
        # Attempt unauthorized read
        self.nfc_device.read_tag()
        
        # Verify security logging occurred
        assert mock_logger.warning.called, "Security warning should have been logged"
        
        # Check the warning calls for unauthorized access
        warning_calls = mock_logger.warning.call_args_list
        unauthorized_logs = [
            call for call in warning_calls
            if 'UNAUTHORIZED ACCESS ATTEMPT' in str(call[0][0])
        ]
        
        assert len(unauthorized_logs) > 0, "Should have logged unauthorized access attempt"
    
    @patch('services.auth.security_logger.logging.getLogger')
    def test_access_denied_logged(self, mock_get_logger):
        """
        Test: Access denied events should be logged
        Expected: Access denied events are logged
        """
        # Setup mock logger
        mock_logger = MagicMock()
        mock_get_logger.return_value = mock_logger
        
        # Create a fresh security logger instance with mocked logger
        from services.auth.security_logger import SecurityLogger
        security_logger = SecurityLogger()
        security_logger.logger = mock_logger
        
        # Patch the NFC device to use our mock logger
        self.nfc_device.security_logger = security_logger
        
        # Ensure not authorized
        auth_service = get_auth_service()
        assert not auth_service.is_authorized()
        
        # Attempt unauthorized write
        test_data = {"name": "Test"}
        self.nfc_device.write_tag(test_data)
        
        # Verify access denied logging occurred
        assert mock_logger.warning.called, "Security warning should have been logged"
        
        # Check the warning calls for access denied
        warning_calls = mock_logger.warning.call_args_list
        access_denied_logs = [
            call for call in warning_calls
            if 'ACCESS DENIED' in str(call[0][0])
        ]
        
        assert len(access_denied_logs) > 0, "Should have logged access denied event"
    
    def test_authorized_access_allowed(self):
        """
        Test: Authorized access should be allowed (control test)
        Expected: Access granted when properly authorized
        """
        # Authenticate user
        auth_service = get_auth_service()
        auth_result = auth_service.authenticate_user("admin", "admin123")
        assert auth_result is True, "Authentication should succeed"
        assert auth_service.is_authorized(), "Should be authorized after authentication"
        
        # Attempt authorized read
        result = self.nfc_device.read_tag()
        assert result is not None, "Authorized read access should return data"
        assert isinstance(result, dict), "Read result should be a dictionary"
        
        # Attempt authorized write
        test_data = {"name": "Test Filament", "type": "PLA"}
        write_result = self.nfc_device.write_tag(test_data)
        assert write_result is True, "Authorized write access should succeed"
    
    def test_issue_4_unauthorized_nfc_access_requirements(self):
        """
        Test for Issue #4: Security (Unauthorized NFC Access)
        
        Purpose: Verify denial of unauthorized NFC data access.
        Input: Attempt unauthorized NFC data access via the application.
        Steps: 1. Attempt to access NFC data without authorization.
        Expected Output: - Access denied, - Security event logged
        """
        # Setup: Ensure not authorized (per step 1)
        auth_service = get_auth_service()
        auth_service.revoke_authorization()  # Ensure clean state
        assert not auth_service.is_authorized(), "Should start unauthorized"
        
        # Create mock logger to capture security events
        from unittest.mock import MagicMock
        mock_logger = MagicMock()
        original_logger = self.nfc_device.security_logger.logger
        self.nfc_device.security_logger.logger = mock_logger
        
        try:
            # Step 1: Attempt to access NFC data without authorization
            read_result = self.nfc_device.read_tag()
            write_result = self.nfc_device.write_tag({"test": "data"})
            
            # Expected Output 1: Access denied
            assert read_result is None, "Read access should be denied (return None)"
            assert write_result is False, "Write access should be denied (return False)"
            
            # Expected Output 2: Security event logged
            assert mock_logger.warning.called, "Security events should be logged"
            
            # Verify specific security log messages
            warning_calls = [str(call) for call in mock_logger.warning.call_args_list]
            
            # Check for unauthorized access attempt logs
            unauthorized_logs = [log for log in warning_calls if 'UNAUTHORIZED ACCESS ATTEMPT' in log]
            assert len(unauthorized_logs) >= 1, "Should log unauthorized access attempts"
            
            # Check for access denied logs
            access_denied_logs = [log for log in warning_calls if 'ACCESS DENIED' in log]
            assert len(access_denied_logs) >= 1, "Should log access denied events"
            
            print("✓ Issue #4 Requirements Met:")
            print("  - Unauthorized access denied ✓")
            print("  - Security events logged ✓")
            
        finally:
            # Restore original logger
            self.nfc_device.security_logger.logger = original_logger
    
    def test_authorization_service_functionality(self):
        """
        Test: Authorization service basic functionality
        Expected: Proper authentication and authorization state management
        """
        auth_service = get_auth_service()
        
        # Initially not authorized
        assert not auth_service.is_authorized()
        assert auth_service.get_current_user() is None
        
        # Invalid credentials should fail
        result = auth_service.authenticate_user("wrong", "credentials")
        assert result is False
        assert not auth_service.is_authorized()
        
        # Valid credentials should succeed
        result = auth_service.authenticate_user("admin", "admin123")
        assert result is True
        assert auth_service.is_authorized()
        assert auth_service.get_current_user() == "admin"
        
        # Revoking authorization should work
        auth_service.revoke_authorization()
        assert not auth_service.is_authorized()
        assert auth_service.get_current_user() is None


if __name__ == "__main__":
    # Run the tests
    pytest.main([__file__, "-v"])