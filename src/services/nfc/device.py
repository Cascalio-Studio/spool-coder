"""
Basis-Klasse für die NFC-Kommunikation mit dem Gerät
"""

import time
import random
from typing import Dict, Optional, Tuple

from src.models.filament import FilamentSpool
from src.services.nfc.bambu_algorithm import BambuLabNFCEncoder, BambuLabNFCDecoder

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
        self.encoder = BambuLabNFCEncoder()
        self.decoder = BambuLabNFCDecoder()
    
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
        Liest Daten von einem NFC-Tag und konvertiert sie in ein FilamentSpool-Objekt
        
        Returns:
            dict: Die gelesenen Daten oder None bei Fehler
        """
        if not self.connected:
            return None
            
        try:
            # In einer realen Implementierung würden wir hier die NFC-Daten lesen
            # Für die Simulation verwenden wir simulierte NFC-Tag-Daten
            
            time.sleep(0.5)  # Simuliere Lesezeit
            
            # Simuliere ein erfolgreiches oder fehlgeschlagenes Lesen
            if random.random() > 0.1:  # 90% Erfolgsrate
                # Simuliere Rohdaten von einem NFC-Tag
                raw_data = self._simulate_read_raw_tag_data()
                
                # Decodiere die Daten mit dem Bambu Lab NFC Decoder
                decoded_data = self.decoder.decode_tag_data(raw_data)
                
                if decoded_data:
                    # Konvertiere die decodierten Daten in ein sauberes Format für FilamentSpool
                    spool_data = decoded_data["spool_data"]
                    
                    # Bereite die Daten für den FilamentSpool vor
                    filament_data = {
                        "name": spool_data["name"],
                        "type": spool_data["type"],
                        "color": spool_data["color"],
                        "manufacturer": spool_data["manufacturer"],
                        "density": spool_data["density"],
                        "diameter": spool_data["diameter"],
                        "nozzle_temp": spool_data["nozzle_temp"],
                        "bed_temp": spool_data["bed_temp"],
                        "remaining_length": spool_data["remaining_length"],
                        "remaining_weight": spool_data["remaining_weight"]
                    }
                    
                    return filament_data
            
            # Wenn hier angekommen, ist das Lesen fehlgeschlagen
            return None
                
        except Exception as e:
            print(f"Fehler beim Lesen des NFC-Tags: {str(e)}")
            return None
    
    def write_tag(self, data):
        """
        Schreibt Daten auf ein NFC-Tag
        
        Args:
            data (dict): Die zu schreibenden Daten oder ein FilamentSpool-Objekt
            
        Returns:
            bool: True bei erfolgreichem Schreiben, False sonst
        """
        if not self.connected:
            return False
        
        try:
            # Konvertiere FilamentSpool-Objekt zu einem Dictionary, falls nötig
            if hasattr(data, 'to_dict'):
                data_dict = data.to_dict()
            else:
                data_dict = data
                
            # Bereite die Daten für den Bambu Lab NFC Encoder vor
            tag_data = {
                "version": 1,
                "flags": "000000",
                "spool_data": {
                    "type": data_dict.get("type", "PLA"),
                    "color": data_dict.get("color", "#FFFFFF"),
                    "diameter": float(data_dict.get("diameter", 1.75)),
                    "nozzle_temp": int(data_dict.get("nozzle_temp", 220)),
                    "bed_temp": int(data_dict.get("bed_temp", 60)),
                    "density": float(data_dict.get("density", 1.24)),
                    "remaining_length": float(data_dict.get("remaining_length", 240.0)),
                    "remaining_weight": float(data_dict.get("remaining_weight", 1000.0)),
                    "manufacturer": data_dict.get("manufacturer", ""),
                    "name": data_dict.get("name", "")
                },
                "manufacturing_info": {
                    "serial": f"SC{int(time.time())}", # Generiere eine eindeutige Seriennummer
                    "date": int(time.time()) # Aktuelles Datum als Unix-Timestamp
                }
            }
            
            # Codiere die Daten mit dem Bambu Lab NFC Encoder
            encoded_data = self.encoder.encode_tag_data(tag_data)
            
            # In einer realen Implementierung würden wir hier die NFC-Daten schreiben
            # Für die Simulation verwenden wir eine verzögerte Antwort
            time.sleep(1.0)  # Simuliere Schreibzeit
            
            # Simuliere ein erfolgreiches oder fehlgeschlagenes Schreiben
            return random.random() > 0.1  # 90% Erfolgsrate
                
        except Exception as e:
            print(f"Fehler beim Schreiben des NFC-Tags: {str(e)}")
            return False
            
    def _simulate_read_raw_tag_data(self):
        """
        Simuliert das Lesen von Rohdaten von einem NFC-Tag für Testzwecke
        
        Returns:
            bytes: Simulierte Rohdaten eines NFC-Tags
        """
        # Wir verwenden die encode_tag_data Methode, um gültige Beispieldaten zu erstellen
        tag_data = {
            "version": 1,
            "flags": "000000",
            "spool_data": {
                "type": "PLA",
                "color": "#" + "".join([format(random.randint(0, 255), '02X') for _ in range(3)]),
                "diameter": 1.75,
                "nozzle_temp": random.randint(190, 230),
                "bed_temp": random.randint(50, 70),
                "density": 1.24,
                "remaining_length": random.uniform(200, 250),
                "remaining_weight": random.uniform(800, 1000),
                "manufacturer": "Bambu Lab",
                "name": random.choice([
                    "PLA Matte", "PLA Silk", "PLA Basic", 
                    "PETG", "ABS", "TPU"
                ])
            },
            "manufacturing_info": {
                "serial": f"BL{random.randint(10000, 99999)}",
                "date": int(time.time()) - random.randint(0, 30000000)
            }
        }
        
        # Erstelle encodierte Daten
        return self.encoder.encode_tag_data(tag_data)
