"""
Tests for NFC Driver Initialization

This test suite validates the NFC driver initialization functionality
as specified in issue #5.
"""

import pytest
import unittest.mock as mock
from unittest.mock import patch, MagicMock
import sys
import os

# Add src to path for testing
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from services.nfc import NFCDevice, NFCManager


class TestNFCDriverInitialization:
    """
    Test suite for NFC driver initialization functionality
    """
    
    def setup_method(self):
        """
        Setup test environment before each test
        """
        self.nfc_device = None
        self.nfc_manager = None
    
    def teardown_method(self):
        """
        Cleanup after each test
        """
        if self.nfc_device:
            try:
                self.nfc_device.disconnect()
            except:
                pass
        if self.nfc_manager:
            try:
                self.nfc_manager.shutdown()
            except:
                pass
    
    def test_detect_supported_devices_no_devices(self):
        """
        Test: Device detection when no devices are connected
        """
        with patch('serial.tools.list_ports.comports', return_value=[]):
            devices = NFCDevice.detect_supported_devices()
            assert devices == []
    
    @patch('serial.tools.list_ports.comports')
    def test_detect_supported_devices_with_nfc_device(self, mock_comports):
        """
        Test: Device detection with supported NFC device connected
        """
        # Mock ein NFC-Gerät
        mock_port = MagicMock()
        mock_port.device = '/dev/ttyUSB0'
        mock_port.description = 'PN532 NFC Reader'
        mock_port.manufacturer = 'NFC Corp'
        mock_port.vid = 0x1234
        mock_port.pid = 0x5678
        
        mock_comports.return_value = [mock_port]
        
        devices = NFCDevice.detect_supported_devices()
        
        assert len(devices) == 1
        assert devices[0]['port'] == '/dev/ttyUSB0'
        assert 'PN532' in devices[0]['description']
        assert devices[0]['manufacturer'] == 'NFC Corp'
    
    @patch('serial.Serial')
    def test_nfc_device_initialization_success(self, mock_serial):
        """
        Test: Successful NFC device initialization
        """
        # Mock serielle Verbindung
        mock_serial_instance = MagicMock()
        mock_serial_instance.is_open = True
        mock_serial_instance.readline.return_value = b'OK:SPOOL_CODER_NFC_V1\n'
        mock_serial.return_value = mock_serial_instance
        
        self.nfc_device = NFCDevice('/dev/ttyUSB0')
        
        # Test Initialisierung
        result = self.nfc_device.initialize_driver()
        
        assert result is True
        assert self.nfc_device.is_connected() is True
        assert self.nfc_device.get_last_error() is None
        
        # Test Geräteinformationen
        device_info = self.nfc_device.get_device_info()
        assert device_info is not None
        assert device_info['id'] == 'SPOOL_CODER_NFC_V1'
        assert device_info['port'] == '/dev/ttyUSB0'
        assert device_info['status'] == 'connected'
    
    def test_nfc_device_initialization_no_port(self):
        """
        Test: NFC device initialization without port specification
        """
        with patch.object(NFCDevice, 'detect_supported_devices', return_value=[]):
            self.nfc_device = NFCDevice()
            
            result = self.nfc_device.initialize_driver()
            
            assert result is False
            assert 'Keine unterstützten NFC-Geräte gefunden' in self.nfc_device.get_last_error()
    
    @patch('serial.Serial')
    def test_nfc_device_connection_failure(self, mock_serial):
        """
        Test: NFC device connection failure
        """
        import serial
        mock_serial.side_effect = serial.SerialException("Port not available")
        
        self.nfc_device = NFCDevice('/dev/ttyUSB0')
        
        result = self.nfc_device.connect()
        
        assert result is False
        assert self.nfc_device.is_connected() is False
        assert 'Serielle Verbindung fehlgeschlagen' in self.nfc_device.get_last_error()
    
    @patch('serial.Serial')
    def test_nfc_device_identification_fallback(self, mock_serial):
        """
        Test: NFC device identification with fallback for unknown devices
        """
        # Mock serielle Verbindung ohne PING-Antwort
        mock_serial_instance = MagicMock()
        mock_serial_instance.is_open = True
        mock_serial_instance.readline.return_value = b'ERROR:UNKNOWN_COMMAND\n'
        mock_serial.return_value = mock_serial_instance
        
        self.nfc_device = NFCDevice('/dev/ttyUSB0')
        
        result = self.nfc_device.initialize_driver()
        
        # Sollte trotzdem erfolgreich sein (Fallback)
        assert result is True
        assert self.nfc_device.is_connected() is True
        
        device_info = self.nfc_device.get_device_info()
        assert device_info['id'] == 'UNKNOWN_NFC_DEVICE'
        assert device_info['protocol_version'] == 'unknown'
    
    @patch.object(NFCDevice, 'detect_supported_devices')
    def test_nfc_manager_initialization_success(self, mock_detect):
        """
        Test: Successful NFC manager initialization
        """
        # Mock erkannte Geräte
        mock_detect.return_value = [
            {'port': '/dev/ttyUSB0', 'description': 'PN532 NFC Reader'}
        ]
        
        with patch.object(NFCDevice, 'initialize_driver', return_value=True):
            with patch.object(NFCDevice, 'is_connected', return_value=True):
                with patch.object(NFCDevice, 'get_device_info', return_value={
                    'id': 'TEST_NFC_DEVICE',
                    'port': '/dev/ttyUSB0',
                    'status': 'connected'
                }):
                    self.nfc_manager = NFCManager()
                    
                    result = self.nfc_manager.initialize()
                    
                    assert result is True
                    assert self.nfc_manager.is_initialized() is True
                    assert self.nfc_manager.get_last_error() is None
    
    def test_nfc_manager_initialization_failure(self):
        """
        Test: NFC manager initialization failure
        """
        with patch.object(NFCDevice, 'initialize_driver', return_value=False):
            with patch.object(NFCDevice, 'get_last_error', return_value='Test error'):
                self.nfc_manager = NFCManager()
                
                result = self.nfc_manager.initialize()
                
                assert result is False
                assert self.nfc_manager.is_initialized() is False
                assert 'Test error' in self.nfc_manager.get_last_error()
    
    def test_nfc_manager_device_detection(self):
        """
        Test: NFC manager device detection
        """
        mock_devices = [
            {'port': '/dev/ttyUSB0', 'description': 'PN532 NFC Reader'},
            {'port': '/dev/ttyUSB1', 'description': 'ACR122U USB NFC Reader'}
        ]
        
        with patch.object(NFCDevice, 'detect_supported_devices', return_value=mock_devices):
            self.nfc_manager = NFCManager()
            
            devices = self.nfc_manager.get_detected_devices()
            
            assert len(devices) == 2
            assert devices[0]['port'] == '/dev/ttyUSB0'
            assert devices[1]['port'] == '/dev/ttyUSB1'
    
    def test_nfc_manager_shutdown(self):
        """
        Test: NFC manager proper shutdown
        """
        self.nfc_manager = NFCManager()
        
        # Erstelle ein Mock-Gerät und setze es als current_device
        mock_device = MagicMock()
        self.nfc_manager.current_device = mock_device
        self.nfc_manager.initialization_status = True
        
        self.nfc_manager.shutdown()
        
        # Verifiziere, dass disconnect auf dem Gerät aufgerufen wurde
        mock_device.disconnect.assert_called_once()
        assert self.nfc_manager.current_device is None
        assert self.nfc_manager.initialization_status is False


class TestNFCDriverIntegration:
    """
    Integration tests for the complete NFC driver initialization flow
    """
    
    def test_full_initialization_flow_simulation(self):
        """
        Test: Complete initialization flow simulation
        
        Simulates the complete flow as described in issue #5:
        1. Start application (represented by NFCManager creation)
        2. Trigger NFC driver initialization routine
        3. Verify hardware detection and identification
        4. Ensure no errors are reported
        """
        # Schritt 1: Application start simulation
        nfc_manager = NFCManager()
        assert nfc_manager is not None
        
        # Mock-Setup für erfolgreiche Initialisierung
        mock_devices = [
            {
                'port': '/dev/ttyUSB0',
                'description': 'Spool-Coder NFC Reader v1.0',
                'manufacturer': 'Cascalio-Studio',
                'vid': 0x1234,
                'pid': 0x5678
            }
        ]
        
        with patch.object(NFCDevice, 'detect_supported_devices', return_value=mock_devices):
            with patch('serial.Serial') as mock_serial:
                # Mock erfolgreiche serielle Verbindung
                mock_serial_instance = MagicMock()
                mock_serial_instance.is_open = True
                mock_serial_instance.readline.return_value = b'OK:SPOOL_CODER_NFC_V1\n'
                mock_serial.return_value = mock_serial_instance
                
                # Schritt 2: Trigger NFC driver initialization
                result = nfc_manager.initialize()
                
                # Schritt 3: Verify hardware detection and identification
                assert result is True, "NFC-Initialisierung sollte erfolgreich sein"
                assert nfc_manager.is_initialized() is True, "NFC-Manager sollte initialisiert sein"
                
                device_info = nfc_manager.get_device_info()
                assert device_info is not None, "Geräteinformationen sollten verfügbar sein"
                assert device_info['id'] == 'SPOOL_CODER_NFC_V1', "Gerät sollte korrekt identifiziert werden"
                assert device_info['status'] == 'connected', "Gerät sollte verbunden sein"
                
                # Schritt 4: Ensure no errors are reported
                assert nfc_manager.get_last_error() is None, "Es sollten keine Fehler aufgetreten sein"
        
        # Cleanup
        nfc_manager.shutdown()


if __name__ == '__main__':
    pytest.main([__file__, '-v'])