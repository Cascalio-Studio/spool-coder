"""
Basis-Klasse für die NFC-Kommunikation mit dem Gerät
"""
from .decoder import NFCDecoder, generate_sample_payload

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
        self.decoder = NFCDecoder()
    
    def connect(self):
        """
        Stellt eine Verbindung zum Gerät her
        
        Returns:
            bool: True bei erfolgreicher Verbindung, False sonst
        """
        # Hier würde der Code zur Verbindungsherstellung stehen
        # Simulation einer erfolgreichen Verbindung
        self.connected = True
        return True
    
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
        # Für Tests verwenden wir simulierte Payload-Daten
        sample_payload = generate_sample_payload('bambu_v1')
        decoded_data = self.decoder.decode_payload(sample_payload)
        
        return decoded_data
    
    def read_tag_raw(self):
        """
        Liest rohe Binärdaten von einem NFC-Tag
        
        Returns:
            bytes: Die rohen Daten oder None bei Fehler
        """
        if not self.connected:
            return None
            
        # Hier würde der Code zum Lesen der rohen NFC-Tag-Daten stehen
        # Für Tests verwenden wir simulierte Payload-Daten
        return generate_sample_payload('bambu_v1')
    
    def decode_payload(self, payload):
        """
        Dekodiert rohe NFC-Payload-Daten
        
        Args:
            payload (bytes): Rohe NFC-Payload-Daten
            
        Returns:
            dict: Dekodierte Daten oder None bei Fehler
        """
        return self.decoder.decode_payload(payload)
    
    def batch_decode(self, payloads):
        """
        Dekodiert eine Liste von NFC-Payloads
        
        Args:
            payloads (list): Liste von rohen NFC-Payload-Daten
            
        Returns:
            list: Liste von dekodierten Daten
        """
        return self.decoder.batch_decode(payloads)
    
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
