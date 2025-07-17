"""
Basis-Klasse für die NFC-Kommunikation mit dem Gerät
"""

import serial
import serial.tools.list_ports
import usb.core
import usb.util

class NFCDevice:
    """
    Basisklasse zur Kommunikation mit dem NFC-Lesegerät
    """
    
    def __init__(self, port=None):
        """
        Initialisiert die Verbindung zum NFC-Lesegerät
        
        Args:
            port (str): Der serielle Port für die Verbindung (z.B. 'COM3' unter Windows)
        """
        self.port = port
        self.connected = False
    
    def connect(self):
        """
        Stellt eine Verbindung zum Gerät her
        
        Returns:
            bool: True bei erfolgreicher Verbindung, False sonst
        """
        try:
            # Versuche NFC-Gerät über verschiedene Methoden zu finden
            if self._detect_nfc_device():
                self.connected = True
                return True
        except Exception:
            pass
        
        # Kein Gerät gefunden
        self.connected = False
        return False
    
    def _detect_nfc_device(self):
        """
        Versucht ein NFC-Gerät zu erkennen
        
        Returns:
            bool: True wenn ein Gerät gefunden wurde, False sonst
        """
        # Suche nach bekannten NFC-Lesegeräten über USB
        if self._detect_usb_nfc_devices():
            return True
            
        # Suche nach seriellen NFC-Geräten
        if self._detect_serial_nfc_devices():
            return True
            
        return False
    
    def _detect_usb_nfc_devices(self):
        """
        Sucht nach NFC-Geräten über USB
        
        Returns:
            bool: True wenn ein USB-NFC-Gerät gefunden wurde
        """
        try:
            # Bekannte NFC-Reader Vendor/Product IDs
            nfc_devices = [
                (0x072f, 0x2200),  # Advanced Card Systems Ltd. ACR122U
                (0x04e6, 0x5816),  # SCM Microsystems Inc. SCL3711
                (0x04e6, 0x5591),  # SCM Microsystems Inc. SCL011
                (0x08e6, 0x3437),  # Gemalto Prox-PU/CU
                (0x0471, 0x0055),  # Philips JCOP41V221
                (0x04cc, 0x0531),  # ST Microelectronics
                (0x04cc, 0x2533),  # ST Microelectronics
                (0x1fd3, 0x0608),  # A-Data Technology Co. NFC Reader
            ]
            
            for vendor_id, product_id in nfc_devices:
                device = usb.core.find(idVendor=vendor_id, idProduct=product_id)
                if device is not None:
                    return True
                    
            return False
        except Exception:
            return False
    
    def _detect_serial_nfc_devices(self):
        """
        Sucht nach NFC-Geräten über serielle Schnittstellen
        
        Returns:
            bool: True wenn ein serielles NFC-Gerät gefunden wurde
        """
        try:
            # Liste alle verfügbaren seriellen Ports auf
            ports = serial.tools.list_ports.comports()
            
            for port in ports:
                # Bekannte NFC-Reader Descriptions/Hardware IDs
                if port.description and any(keyword in port.description.lower() for keyword in 
                    ['nfc', 'acr122', 'pn532', 'mfrc522', 'scl3711']):
                    return True
                    
                if port.hwid and any(keyword in port.hwid.lower() for keyword in 
                    ['072f', '04e6', '08e6', '0471', '04cc', '1fd3']):
                    return True
                    
            return False
        except Exception:
            return False
    
    def disconnect(self):
        """
        Trennt die Verbindung zum Gerät
        """
        if self.connected:
            # Hier würde der Code zur Verbindungstrennung stehen
            self.connected = False
    
    def is_connected(self):
        """
        Überprüft, ob eine Verbindung besteht
        
        Returns:
            bool: True wenn verbunden, False sonst
        """
        return self.connected
    
    def read_tag(self):
        """
        Liest Daten von einem NFC-Tag
        
        Returns:
            dict: Die gelesenen Daten oder None bei Fehler
        """
        if not self.connected:
            return None
            
        # Hier würde der Code zum Lesen des NFC-Tags stehen
        # Simulation gelesener Daten
        return {
            "name": "Bambu PLA",
            "type": "PLA",
            "color": "#FF0000",
            "manufacturer": "Bambulab",
            "density": 1.24,
            "diameter": 1.75,
            "nozzle_temp": 210,
            "bed_temp": 60,
            "remaining_length": 240,
            "remaining_weight": 1000
        }
    
    def write_tag(self, data):
        """
        Schreibt Daten auf ein NFC-Tag
        
        Args:
            data (dict): Die zu schreibenden Daten
            
        Returns:
            bool: True bei erfolgreichem Schreiben, False sonst
        """
        if not self.connected:
            return False
            
        # Hier würde der Code zum Schreiben des NFC-Tags stehen
        # Simulation eines erfolgreichen Schreibvorgangs
        return True
