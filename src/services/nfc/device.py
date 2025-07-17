"""
Basis-Klasse für die NFC-Kommunikation mit dem Gerät
"""

import logging
from typing import Optional, Dict, Any
from .decoder import NFCPayloadDecoder, NFCDecodingError

# Configure logger
logger = logging.getLogger(__name__)

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
        self.decoder = NFCPayloadDecoder()
        self.logger = logging.getLogger(f"{__name__}.{self.__class__.__name__}")
        
        # Configure logging for NFC operations
        self._setup_logging()
    
    def _setup_logging(self):
        """Setup logging configuration for NFC operations"""
        # Ensure we have a handler for NFC operations
        if not self.logger.handlers:
            handler = logging.StreamHandler()
            formatter = logging.Formatter(
                '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
            )
            handler.setFormatter(formatter)
            self.logger.addHandler(handler)
            self.logger.setLevel(logging.INFO)
    
    def connect(self):
        """
        Stellt eine Verbindung zum Gerät her
        
        Returns:
            bool: True bei erfolgreicher Verbindung, False sonst
        """
        try:
            self.logger.info(f"Attempting to connect to NFC device on port: {self.port}")
            # Hier würde der Code zur Verbindungsherstellung stehen
            # Simulation einer erfolgreichen Verbindung
            self.connected = True
            self.logger.info("NFC device connected successfully")
            return True
        except Exception as e:
            self.logger.error(f"Failed to connect to NFC device: {e}")
            self.connected = False
            return False
    
    def disconnect(self):
        """
        Trennt die Verbindung zum Gerät
        """
        if self.connected:
            try:
                self.logger.info("Disconnecting from NFC device")
                # Hier würde der Code zur Verbindungstrennung stehen
                self.connected = False
                self.logger.info("NFC device disconnected successfully")
            except Exception as e:
                self.logger.error(f"Error during disconnect: {e}")
                self.connected = False
    
    def is_connected(self):
        """
        Überprüft, ob eine Verbindung besteht
        
        Returns:
            bool: True wenn verbunden, False sonst
        """
        return self.connected
    
    def read_tag(self) -> Optional[Dict[str, Any]]:
        """
        Liest Daten von einem NFC-Tag mit robuster Fehlerbehandlung
        
        Returns:
            dict: Die gelesenen und decodierten Daten oder None bei Fehler
        """
        if not self.connected:
            self.logger.error("Cannot read tag: device not connected")
            return None
        
        try:
            self.logger.info("Starting NFC tag read operation")
            
            # Hier würde der Code zum Lesen des NFC-Tags stehen
            # Simulation verschiedener Payload-Typen für Testing
            raw_payload = self._simulate_tag_read()
            
            if raw_payload is None:
                self.logger.warning("No tag detected or read failed")
                return None
            
            # Verwende den robusten Decoder
            decoded_data = self.decoder.decode_payload(raw_payload)
            
            if decoded_data:
                self.logger.info("NFC tag read and decoded successfully")
                return decoded_data
            else:
                self.logger.error("Failed to decode NFC payload")
                return None
                
        except NFCDecodingError as e:
            self.logger.error(f"NFC decoding failed: {e}")
            return None
        except Exception as e:
            self.logger.error(f"Unexpected error during tag read: {e}")
            return None
    
    def _simulate_tag_read(self) -> Optional[Any]:
        """
        Simuliert das Lesen verschiedener Payload-Typen
        Wird in der echten Implementierung durch tatsächliches Hardware-Interface ersetzt
        """
        # Für die Simulation verwenden wir verschiedene Payload-Typen
        import random
        
        payloads = [
            # Normal dict payload
            {
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
            },
            # JSON string payload
            '{"name": "PETG Clear", "type": "PETG", "nozzle_temp": 230, "bed_temp": 80}',
            # Binary payload simulation
            b'\x46\x4D\x4C\x42\xD2\x00\x3C\x00\x00\x00\x9F?\x00\x00\xE0?PLA Basic\x00',
        ]
        
        return random.choice(payloads)
    
    def write_tag(self, data: Dict[str, Any]) -> bool:
        """
        Schreibt Daten auf ein NFC-Tag
        
        Args:
            data (dict): Die zu schreibenden Daten
            
        Returns:
            bool: True bei erfolgreichem Schreiben, False sonst
        """
        if not self.connected:
            self.logger.error("Cannot write tag: device not connected")
            return False
        
        try:
            self.logger.info("Starting NFC tag write operation")
            
            # Validiere die Daten vor dem Schreiben
            if not isinstance(data, dict) or not data:
                self.logger.error("Invalid data for writing: must be non-empty dictionary")
                return False
            
            # Verwende den Decoder zur Validierung der Daten
            validated_data = self.decoder.decode_payload(data)
            if not validated_data:
                self.logger.error("Data validation failed before writing")
                return False
            
            # Hier würde der Code zum Schreiben des NFC-Tags stehen
            # Simulation eines erfolgreichen Schreibvorgangs
            self.logger.info("NFC tag write operation completed successfully")
            return True
            
        except NFCDecodingError as e:
            self.logger.error(f"Data validation failed before writing: {e}")
            return False
        except Exception as e:
            self.logger.error(f"Unexpected error during tag write: {e}")
            return False
    
    def read_raw_tag(self) -> Optional[bytes]:
        """
        Liest rohe Daten von einem NFC-Tag ohne Dekodierung
        
        Returns:
            bytes: Rohe Tag-Daten oder None bei Fehler
        """
        if not self.connected:
            self.logger.error("Cannot read raw tag: device not connected")
            return None
        
        try:
            self.logger.info("Reading raw NFC tag data")
            # Hier würde der Code zum Lesen der rohen Tag-Daten stehen
            # Simulation
            return b'\x46\x4D\x4C\x42\xD2\x00\x3C\x00\x00\x00\x9F?\x00\x00\xE0?PLA Basic\x00'
        except Exception as e:
            self.logger.error(f"Failed to read raw tag data: {e}")
            return None
