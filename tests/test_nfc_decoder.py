"""
Unit tests for NFC decoder functionality.
Tests the basic decoding capabilities of the NFC module.
"""
import pytest
from services.nfc.device import NFCDevice
from services.nfc.decoder import NFCDecoder, generate_sample_payload


class TestNFCDecoder:
    """Unit tests for NFC decoder."""
    
    def test_decoder_initialization(self):
        """Test that decoder initializes correctly."""
        decoder = NFCDecoder()
        assert decoder.get_decode_count() == 0
    
    def test_format_detection(self):
        """Test payload format detection."""
        decoder = NFCDecoder()
        
        # Test bambu_v1 format
        payload_v1 = generate_sample_payload('bambu_v1')
        assert decoder.detect_format(payload_v1) == 'bambu_v1'
        
        # Test bambu_v2 format
        payload_v2 = generate_sample_payload('bambu_v2')
        assert decoder.detect_format(payload_v2) == 'bambu_v2'
        
        # Test unknown format
        unknown_payload = b'\x12\x34\x56\x78' + b'\x00' * 100
        assert decoder.detect_format(unknown_payload) is None
        
        # Test too short payload
        short_payload = b'\x42'
        assert decoder.detect_format(short_payload) is None
    
    def test_successful_decode_v1(self):
        """Test successful decoding of bambu_v1 format."""
        decoder = NFCDecoder()
        
        payload = generate_sample_payload(
            'bambu_v1',
            name='Test PLA',
            type='PLA',
            color='#FF0000',
            remaining_weight=500
        )
        
        result = decoder.decode_payload(payload)
        
        assert result is not None
        assert result['name'] == 'Test PLA'
        assert result['type'] == 'PLA'
        assert result['color'] == '#FF0000'
        assert result['remaining_weight'] == 500.0
        assert decoder.get_decode_count() == 1
    
    def test_successful_decode_v2(self):
        """Test successful decoding of bambu_v2 format."""
        decoder = NFCDecoder()
        
        payload = generate_sample_payload(
            'bambu_v2',
            name='Test PETG',
            type='PETG',
            manufacturer='Bambulab',
            color='#00FF00',
            serial_number=98765
        )
        
        result = decoder.decode_payload(payload)
        
        assert result is not None
        assert result['name'] == 'Test PETG'
        assert result['type'] == 'PETG'
        assert result['manufacturer'] == 'Bambulab'
        assert result['color'] == '#00FF00'
        assert result['serial_number'] == 98765
        assert decoder.get_decode_count() == 1
    
    def test_failed_decode_corrupted_payload(self):
        """Test handling of corrupted payload."""
        decoder = NFCDecoder()
        
        # Corrupted payload (too short)
        corrupted_payload = b'\x42\x4D\x42' + b'\x00' * 10
        result = decoder.decode_payload(corrupted_payload)
        
        assert result is None
        assert decoder.get_decode_count() == 1
    
    def test_batch_decode(self):
        """Test batch decoding functionality."""
        decoder = NFCDecoder()
        
        payloads = [
            generate_sample_payload('bambu_v1', name='Payload 1'),
            generate_sample_payload('bambu_v2', name='Payload 2'),
            generate_sample_payload('bambu_v1', name='Payload 3')
        ]
        
        results = decoder.batch_decode(payloads)
        
        assert len(results) == 3
        assert all(result is not None for result in results)
        assert results[0]['name'] == 'Payload 1'
        assert results[1]['name'] == 'Payload 2'
        assert results[2]['name'] == 'Payload 3'
        assert decoder.get_decode_count() == 3


class TestNFCDevice:
    """Unit tests for NFC device."""
    
    def test_device_initialization(self):
        """Test device initialization."""
        device = NFCDevice()
        assert not device.is_connected()
        assert device.port is None
    
    def test_device_connection(self):
        """Test device connection."""
        device = NFCDevice(port='COM3')
        assert device.port == 'COM3'
        
        result = device.connect()
        assert result is True
        assert device.is_connected()
        
        device.disconnect()
        assert not device.is_connected()
    
    def test_read_tag(self):
        """Test reading NFC tag data."""
        device = NFCDevice()
        
        # Should return None when not connected
        result = device.read_tag()
        assert result is None
        
        # Should return data when connected
        device.connect()
        result = device.read_tag()
        
        assert result is not None
        assert isinstance(result, dict)
        assert 'name' in result
        assert 'type' in result
    
    def test_decode_payload(self):
        """Test payload decoding through device."""
        device = NFCDevice()
        device.connect()
        
        payload = generate_sample_payload('bambu_v1', name='Device Test')
        result = device.decode_payload(payload)
        
        assert result is not None
        assert result['name'] == 'Device Test'
    
    def test_batch_decode_through_device(self):
        """Test batch decoding through device."""
        device = NFCDevice()
        device.connect()
        
        payloads = [
            generate_sample_payload('bambu_v1', name=f'Batch Test {i}')
            for i in range(10)
        ]
        
        results = device.batch_decode(payloads)
        
        assert len(results) == 10
        assert all(result is not None for result in results)
        for i, result in enumerate(results):
            assert result['name'] == f'Batch Test {i}'