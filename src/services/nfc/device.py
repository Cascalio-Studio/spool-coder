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
    
    def read_raw_data(self):
        """
        Liest rohe NFC-Daten von einem Tag als Byte-Stream
        
        Returns:
            bytes: Die rohen NFC-Daten oder None bei Fehler
        """
        if not self.connected:
            return None
            
        # Hier würde der Code zum Lesen der rohen NFC-Daten stehen
        # Simulation einer typischen BambuLab Spool NFC Payload
        # Basierend auf bekannten NFC-Datenstrukturen für Filament-Spulen
        raw_payload = bytearray([
            # NFC Header (simuliert)
            0x01, 0x02, 0x03, 0x04,  # UID/Header
            
            # JSON-Daten als UTF-8 Bytes (simuliert BambuLab Format)
            0x7B, 0x22, 0x6E, 0x61, 0x6D, 0x65, 0x22, 0x3A, 0x22,  # {"name":"
            0x42, 0x61, 0x6D, 0x62, 0x75, 0x20, 0x50, 0x4C, 0x41,  # Bambu PLA
            0x22, 0x2C, 0x22, 0x74, 0x79, 0x70, 0x65, 0x22, 0x3A,  # ","type":
            0x22, 0x50, 0x4C, 0x41, 0x22, 0x2C, 0x22, 0x63, 0x6F,  # "PLA","co
            0x6C, 0x6F, 0x72, 0x22, 0x3A, 0x22, 0x23, 0x46, 0x46,  # lor":"#FF
            0x30, 0x30, 0x30, 0x30, 0x22, 0x2C, 0x22, 0x6D, 0x61,  # 0000","ma
            0x6E, 0x75, 0x66, 0x61, 0x63, 0x74, 0x75, 0x72, 0x65,  # nufacture
            0x72, 0x22, 0x3A, 0x22, 0x42, 0x61, 0x6D, 0x62, 0x75,  # r":"Bambu
            0x6C, 0x61, 0x62, 0x22, 0x2C, 0x22, 0x64, 0x65, 0x6E,  # lab","den
            0x73, 0x69, 0x74, 0x79, 0x22, 0x3A, 0x31, 0x2E, 0x32,  # sity":1.2
            0x34, 0x2C, 0x22, 0x64, 0x69, 0x61, 0x6D, 0x65, 0x74,  # 4,"diamet
            0x65, 0x72, 0x22, 0x3A, 0x31, 0x2E, 0x37, 0x35, 0x2C,  # er":1.75,
            0x22, 0x6E, 0x6F, 0x7A, 0x7A, 0x6C, 0x65, 0x5F, 0x74,  # "nozzle_t
            0x65, 0x6D, 0x70, 0x22, 0x3A, 0x32, 0x31, 0x30, 0x2C,  # emp":210,
            0x22, 0x62, 0x65, 0x64, 0x5F, 0x74, 0x65, 0x6D, 0x70,  # "bed_temp
            0x22, 0x3A, 0x36, 0x30, 0x2C, 0x22, 0x72, 0x65, 0x6D,  # ":60,"rem
            0x61, 0x69, 0x6E, 0x69, 0x6E, 0x67, 0x5F, 0x6C, 0x65,  # aining_le
            0x6E, 0x67, 0x74, 0x68, 0x22, 0x3A, 0x32, 0x34, 0x30,  # ngth":240
            0x2C, 0x22, 0x72, 0x65, 0x6D, 0x61, 0x69, 0x6E, 0x69,  # ,"remaini
            0x6E, 0x67, 0x5F, 0x77, 0x65, 0x69, 0x67, 0x68, 0x74,  # ng_weight
            0x22, 0x3A, 0x31, 0x30, 0x30, 0x30, 0x7D,              # ":1000}
            
            # NFC Footer/Checksum (simuliert)
            0xFF, 0xFE, 0xFD, 0xFC
        ])
        
        return bytes(raw_payload)
    
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
