"""
Basis-Klasse für die NFC-Kommunikation mit dem Gerät
"""

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
    
    def read_tag_with_error_handling(self):
        """
        Liest Daten von einem NFC-Tag mit expliziter Fehlerbehandlung
        
        Returns:
            tuple: (data, error_message) where data is dict or None, 
                  error_message is string or None
        """
        if not self.connected:
            return None, "ERROR:NO_DEVICE"
            
        # Hier würde der echte NFC-Lesevorgang stehen
        # Simulation verschiedener Szenarien:
        
        try:
            # Simulation eines erfolgreichen Lesevorgangs
            data = {
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
            
            # Validiere die gelesenen Daten
            if not isinstance(data, dict):
                return None, "ERROR:INVALID_DATA"
                
            # Prüfe auf erforderliche Mindestdaten
            if not data:
                return None, "ERROR:NO_TAG"
                
            return data, None
            
        except Exception as e:
            # Behandle verschiedene Fehlertypen
            if "timeout" in str(e).lower():
                return None, "ERROR:READ_TIMEOUT"
            elif "corrupt" in str(e).lower():
                return None, "ERROR:INVALID_DATA"
            else:
                return None, "ERROR:READ_FAILED"
    
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
