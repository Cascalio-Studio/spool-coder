"""
Basis-Klasse für die NFC-Kommunikation mit dem Gerät
"""

import time
import random
import logging
from typing import Dict, Optional, Tuple, Any, Union
import os

from src.models.filament import FilamentSpool
from src.services.nfc.bambu_algorithm import BambuLabNFCEncoder, BambuLabNFCDecoder

# Konfiguriere Logging
logger = logging.getLogger('nfc_device')
logging.basicConfig(level=logging.INFO)

# Flag zur Steuerung des Simulationsmodus
SIMULATION_MODE = os.getenv('SIMULATION_MODE', 'True').lower() == 'true'  # Standardmäßig True, falls nicht gesetzt
logger.info(f"SIMULATION_MODE konfiguriert als {'True' if SIMULATION_MODE else 'False'} über Umgebungsvariable.")

# Import nfcpy Bibliothek, falls verfügbar
NFC_AVAILABLE = False
try:
    import nfc
    NFC_AVAILABLE = True
    logger.info("NFC-Bibliothek erfolgreich geladen.")
except ImportError:
    logger.warning("NFC-Bibliothek nicht gefunden. Verwende Simulationsmodus.")
    SIMULATION_MODE = True

class NFCDevice:
    """
    Klasse zur Kommunikation mit dem NFC-Lesegerät
    
    Unterstützt sowohl simulierte NFC-Kommunikation für Tests als auch
    echte Hardware-Kommunikation mit NFC-Geräten über die nfcpy-Bibliothek.
    """
    
    def __init__(self, port=None, simulation=None):
        """
        Initialisiert die Verbindung zum NFC-Lesegerät
        
        Args:
            port (str): Der USB-Path oder die Geräte-ID (z.B. 'usb:04e6:5591')
                        Bei None wird automatisch nach verfügbaren Geräten gesucht.
            simulation (bool): Überschreibt das globale SIMULATION_MODE Flag
        """
        self.port = port
        self.connected = False
        self.clf = None  # NFC ContactLess Frontend
        self.tag = None  # Aktueller NFC-Tag
        self.encoder = BambuLabNFCEncoder()
        self.decoder = BambuLabNFCDecoder()
        
        # Simulationsmodus bestimmen
        self.simulation_mode = simulation if simulation is not None else SIMULATION_MODE
        
        if self.simulation_mode:
            logger.info("NFCDevice läuft im Simulationsmodus.")
        else:
            if not NFC_AVAILABLE:
                logger.error("Echtgeräte-Modus aktiviert, aber NFC-Bibliothek nicht verfügbar!")
                raise ImportError("Die NFC-Bibliothek konnte nicht importiert werden.")
            logger.info("NFCDevice läuft im Echtgeräte-Modus.")
    
    def connect(self):
        """
        Stellt eine Verbindung zum NFC-Gerät her
        
        Returns:
            bool: True bei erfolgreicher Verbindung, False sonst
        """
        # Simulationsmodus
        if self.simulation_mode:
            logger.info("Simulation: Verbindung zum NFC-Gerät hergestellt.")
            self.connected = True
            return True
            
        # Echtgeräte-Modus
        try:
            # Gerätestring für nfcpy erstellen
            device = self.port if self.port else ''
            
            # Verbindung zum NFC-Gerät herstellen
            self.clf = nfc.ContactlessFrontend(device)
            if not self.clf:
                logger.error("Konnte keine Verbindung zum NFC-Gerät herstellen.")
                return False
                
            logger.info(f"Verbindung zu NFC-Gerät hergestellt: {self.clf.device}")
            self.connected = True
            return True
        except Exception as e:
            logger.error(f"Fehler beim Verbinden mit NFC-Gerät: {e}")
            self.connected = False
            return False
    
    def disconnect(self):
        """
        Trennt die Verbindung zum Gerät
        """
        if not self.connected:
            return
            
        # Simulationsmodus
        if self.simulation_mode:
            logger.info("Simulation: Verbindung zum NFC-Gerät getrennt.")
            self.connected = False
            return
            
        # Echtgeräte-Modus
        try:
            if self.clf:
                self.clf.close()
                logger.info("Verbindung zum NFC-Gerät getrennt.")
            self.clf = None
            self.tag = None
            self.connected = False
        except Exception as e:
            logger.error(f"Fehler beim Trennen der Verbindung: {e}")
    
    def is_connected(self):
        """
        Überprüft, ob eine Verbindung besteht
        
        Returns:
            bool: True wenn verbunden, False sonst
        """
        return self.connected
    
    def _connect_to_tag(self, timeout=5.0):
        """
        Wartet auf die Erkennung eines NFC-Tags
        
        Args:
            timeout (float): Timeout in Sekunden
            
        Returns:
            bool: True wenn ein Tag gefunden wurde, False sonst
        """
        if self.simulation_mode:
            # Im Simulationsmodus immer erfolgreich nach kurzer Verzögerung
            time.sleep(0.5)
            return True
            
        # Im Echtgeräte-Modus
        if not self.clf:
            logger.error("Keine Verbindung zum NFC-Gerät.")
            return False
            
        try:
            # Warte auf einen Tag mit NTAG/MIFARE Unterstützung
            self.tag = self.clf.connect(rdwr={'on-connect': lambda tag: False},
                                      iterations=int(timeout*10),
                                      interval=0.1)
            return self.tag is not None
        except Exception as e:
            logger.error(f"Fehler beim Verbinden mit dem Tag: {e}")
            return False
    
    def read_tag(self):
        """
        Liest Daten von einem NFC-Tag und konvertiert sie in ein FilamentSpool-Objekt
        
        Returns:
            dict: Die gelesenen Daten oder None bei Fehler
        """
        if not self.connected:
            logger.error("Nicht mit NFC-Gerät verbunden.")
            return None
            
        try:
            # Simulationsmodus
            if self.simulation_mode:
                time.sleep(0.5)  # Simuliere Lesezeit
                
                # Simuliere ein erfolgreiches oder fehlgeschlagenes Lesen
                if random.random() > SIMULATION_FAILURE_RATE:  # 90% Erfolgsrate
                    # Simuliere Rohdaten von einem NFC-Tag
                    raw_data = self._simulate_read_raw_tag_data()
                    logger.info("Simulation: NFC-Tag erfolgreich gelesen.")
                else:
                    logger.warning("Simulation: Fehler beim Lesen des NFC-Tags.")
                    return None
            
            # Echtgeräte-Modus
            else:
                # Verbinde mit Tag
                logger.info("Warte auf NFC-Tag...")
                if not self._connect_to_tag():
                    logger.warning("Kein NFC-Tag gefunden.")
                    return None
                    
                logger.info(f"NFC-Tag gefunden: {self.tag}")
                
                # Lese die Daten vom Tag
                if hasattr(self.tag, 'ndef') and self.tag.ndef:
                    # NDEF-formatierter Tag
                    raw_data = self._read_ndef_tag()
                else:
                    # Nicht-NDEF Tag (Direktes Lesen)
                    raw_data = self._read_raw_tag()
                
                if not raw_data:
                    logger.warning("Konnte keine Daten vom Tag lesen.")
                    return None
                    
                logger.info(f"Rohdaten vom Tag gelesen: {len(raw_data)} Bytes")
            
            # Decodiere die Daten mit dem Bambu Lab NFC Decoder
            decoded_data = self.decoder.decode_tag_data(raw_data)
            
            if decoded_data:
                logger.info("Bambu Lab NFC-Tag erfolgreich decodiert.")
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
            else:
                logger.warning("Tag-Daten konnten nicht als Bambu Lab Format erkannt werden.")
                return None
                
        except Exception as e:
            logger.error(f"Fehler beim Lesen des NFC-Tags: {str(e)}")
            return None
    
    def _read_ndef_tag(self):
        """
        Liest Daten von einem NDEF-formatierten Tag
        
        Returns:
            bytes: Die gelesenen Daten oder None bei Fehler
        """
        try:
            if not self.tag or not self.tag.ndef:
                return None
                
            # Lese NDEF-Nachricht
            for record in self.tag.ndef.records:
                # Suche nach dem ersten Record mit dem Bambu Lab Datenformat
                if record.type == "application/octet-stream" or record.type == "text/plain":
                    return record.data
                
            return None
        except Exception as e:
            logger.error(f"Fehler beim Lesen des NDEF-Tags: {e}")
            return None
    
    def _read_raw_tag(self):
        """
        Liest Rohdaten von einem nicht-NDEF Tag
        
        Returns:
            bytes: Die gelesenen Daten oder None bei Fehler
        """
        try:
            if not self.tag:
                return None
                
            # Je nach Tag-Typ unterschiedliche Lese-Methoden
            if hasattr(self.tag, 'read'):
                # NTAG21x oder ähnlicher Tag
                # Lese die ersten 540 Bytes (ausreichend für Bambu Lab Format)
                data = bytearray()
                for i in range(0, 135):  # 135 Blöcke à 4 Bytes = 540 Bytes
                    try:
                        block_data = self.tag.read(i)
                        if block_data:
                            data.extend(block_data)
                        else:
                            break
                    except Exception:
                        break
                
                return bytes(data)
            else:
                logger.error(f"Unbekannter Tag-Typ: {type(self.tag)}")
                return None
                
        except Exception as e:
            logger.error(f"Fehler beim Lesen des Raw-Tags: {e}")
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
            logger.error("Nicht mit NFC-Gerät verbunden.")
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
            logger.info(f"Daten für NFC-Tag codiert: {len(encoded_data)} Bytes")
            
            # Simulationsmodus
            if self.simulation_mode:
                time.sleep(1.0)  # Simuliere Schreibzeit
                # Simuliere ein erfolgreiches oder fehlgeschlagenes Schreiben
                success = random.random() > 0.1  # 90% Erfolgsrate
                if success:
                    logger.info("Simulation: Daten erfolgreich auf NFC-Tag geschrieben.")
                else:
                    logger.warning("Simulation: Fehler beim Schreiben auf den NFC-Tag.")
                return success
            
            # Echtgeräte-Modus
            else:
                # Verbinde mit Tag
                logger.info("Warte auf NFC-Tag zum Schreiben...")
                if not self._connect_to_tag():
                    logger.warning("Kein NFC-Tag gefunden.")
                    return False
                    
                logger.info(f"NFC-Tag gefunden: {self.tag}")
                
                # Schreibe die Daten auf den Tag
                if hasattr(self.tag, 'ndef') and self.tag.ndef:
                    # NDEF-formatierter Tag
                    success = self._write_ndef_tag(encoded_data)
                else:
                    # Nicht-NDEF Tag (Direktes Schreiben)
                    success = self._write_raw_tag(encoded_data)
                
                return success
                
        except Exception as e:
            logger.error(f"Fehler beim Schreiben des NFC-Tags: {str(e)}")
            return False
    
    def _write_ndef_tag(self, data):
        """
        Schreibt Daten auf einen NDEF-formatierten Tag
        
        Args:
            data (bytes): Die zu schreibenden Daten
            
        Returns:
            bool: True bei erfolgreichem Schreiben, False sonst
        """
        if not NFC_AVAILABLE or not self.tag or not self.tag.ndef:
            return False
            
        try:
            import nfc.ndef
            
            # Erstelle NDEF-Nachricht mit den Daten
            record = nfc.ndef.Record(type="application/octet-stream", data=data)
            message = nfc.ndef.Message([record])
            
            # Schreibe NDEF-Nachricht auf den Tag
            self.tag.ndef.records = message
            
            logger.info("Daten erfolgreich auf NDEF-Tag geschrieben.")
            return True
        except Exception as e:
            logger.error(f"Fehler beim Schreiben des NDEF-Tags: {e}")
            return False
    
    def _write_raw_tag(self, data):
        """
        Schreibt Rohdaten auf einen nicht-NDEF Tag
        
        Args:
            data (bytes): Die zu schreibenden Daten
            
        Returns:
            bool: True bei erfolgreichem Schreiben, False sonst
        """
        try:
            if not self.tag:
                return False
                
            # Je nach Tag-Typ unterschiedliche Schreib-Methoden
            if hasattr(self.tag, 'write'):
                # NTAG21x oder ähnlicher Tag
                # Schreibe die Daten blockweise (je 4 Bytes)
                for i in range(0, min(len(data) // 4, 135)):  # Max 135 Blöcke schreiben
                    block_data = data[i*4:i*4+4]
                    # Fülle Block auf 4 Bytes auf, falls nötig
                    if len(block_data) < 4:
                        block_data = block_data + bytes([0] * (4 - len(block_data)))
                    
                    try:
                        self.tag.write(block_data, i)
                    except Exception as e:
                        logger.error(f"Fehler beim Schreiben von Block {i}: {e}")
                        return False
                
                logger.info(f"Daten erfolgreich auf Raw-Tag geschrieben ({len(data)} Bytes).")
                return True
            else:
                logger.error(f"Unbekannter Tag-Typ: {type(self.tag)}")
                return False
                
        except Exception as e:
            logger.error(f"Fehler beim Schreiben des Raw-Tags: {e}")
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
        
    @staticmethod
    def list_available_devices():
        """
        Listet alle verfügbaren NFC-Geräte auf
        
        Returns:
            list: Liste der verfügbaren NFC-Geräte
        """
        if SIMULATION_MODE or not NFC_AVAILABLE:
            logger.info("Simulationsmodus: Simuliere verfügbare NFC-Geräte.")
            return ["Simuliertes NFC-Gerät"]
        
        try:
            # nfcpy kann verfügbare Geräte auflisten
            devices = []
            for name in nfc.clf.transport_names():
                try:
                    for device in nfc.clf.find_devices(name):
                        devices.append(str(device))
                except Exception as e:
                    logger.warning(f"Fehler beim Suchen nach {name}-Geräten: {e}")
            
            if not devices:
                logger.warning("Keine NFC-Geräte gefunden.")
            else:
                logger.info(f"Gefundene NFC-Geräte: {devices}")
            
            return devices
        except Exception as e:
            logger.error(f"Fehler beim Auflisten der NFC-Geräte: {e}")
            return []
    
    def get_tag_info(self):
        """
        Gibt Informationen über den aktuell verbundenen Tag zurück
        
        Returns:
            dict: Informationen über den Tag oder None
        """
        if self.simulation_mode:
            # Simulierte Tag-Informationen
            return {
                "type": "Simulierter Tag",
                "id": "01:02:03:04",
                "size": 1024,
                "product": "Simulation",
                "vendor": "Spool-Coder"
            }
            
        if not self.tag:
            return None
            
        # Extrahiere Tag-Informationen
        info = {
            "type": str(type(self.tag).__name__),
            "id": str(self.tag.identifier.hex() if hasattr(self.tag, 'identifier') else "unbekannt"),
            "size": getattr(self.tag, 'capacity', 0),
            "product": getattr(self.tag, 'product', "unbekannt"),
            "vendor": getattr(self.tag, 'vendor', "unbekannt")
        }
        
        return info
