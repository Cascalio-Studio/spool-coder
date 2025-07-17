"""
Basis-Klasse für die NFC-Kommunikation mit dem Gerät
"""

from .decoder import NFCDecoder


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
    
    def read_tag_raw(self):
        """
        Liest rohe Daten von einem NFC-Tag
        
        Returns:
            bytes: Die rohen Daten oder None bei Fehler
        """
        if not self.connected:
            return None
            
        # Hier würde der Code zum Lesen der rohen NFC-Tag-Daten stehen
        # Simulation von rohen Daten basierend auf den simulierten gelesenen Daten
        simulated_data = self.read_tag()
        if simulated_data:
            import json
            return json.dumps(simulated_data, separators=(',', ':')).encode('utf-8')
        return None
    
    def decode_tag_data(self, raw_data):
        """
        Dekodiert rohe NFC-Tag-Daten in eine FilamentSpool
        
        Args:
            raw_data (bytes): Rohe NFC-Tag-Daten
            
        Returns:
            FilamentSpool: Dekodierte Filamentspule oder None bei Fehler
        """
        return NFCDecoder.decode_payload(raw_data)
    
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
