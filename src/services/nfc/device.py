"""
Basis-Klasse für die NFC-Kommunikation mit dem Gerät
"""

import serial
import time
from typing import Optional, Dict, List, Any


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
        self.serial_connection = None
        self.device_info = None
        self.last_error = None

    @staticmethod
    def detect_supported_devices() -> List[Dict[str, Any]]:
        """
        Erkennt verfügbare NFC-Lesegeräte

        Returns:
            List[Dict]: Liste der erkannten Geräte mit Port und Geräteinformationen
        """
        detected_devices = []

        # Suche nach verfügbaren seriellen Ports
        try:
            from serial.tools import list_ports
            available_ports = list_ports.comports()

            for port_info in available_ports:
                # Prüfe auf bekannte NFC-Geräte (Beispiel-Hersteller und Produktkennungen)
                device_description = (port_info.description or '').lower()
                device_manufacturer = (getattr(port_info, 'manufacturer', '') or '').lower()

                # Liste unterstützter Geräte (erweitert bei Bedarf)
                supported_devices = [
                    'pn532',  # PN532 NFC Module
                    'acr122',  # ACR122U USB NFC Reader
                    'spool_coder',  # Unser eigenes Gerät
                    'nfc',  # Allgemeine NFC-Geräte
                ]

                if any(device_id in device_description or device_id in device_manufacturer
                       for device_id in supported_devices):
                    detected_devices.append({
                        'port': port_info.device,
                        'description': port_info.description or 'Unknown Device',
                        'manufacturer': getattr(port_info, 'manufacturer', '') or 'Unknown',
                        'vid': getattr(port_info, 'vid', None),
                        'pid': getattr(port_info, 'pid', None),
                    })

        except ImportError:
            # Falls pyserial nicht verfügbar ist, gebe leere Liste zurück
            pass
        except Exception as e:
            # Bei anderen Fehlern, protokolliere sie aber gib leere Liste zurück
            print(f"Fehler bei der Geräteerkennung: {e}")

        return detected_devices

    def initialize_driver(self) -> bool:
        """
        Initialisiert den NFC-Treiber und erkennt Hardware

        Returns:
            bool: True bei erfolgreicher Initialisierung, False sonst
        """
        try:
            self.last_error = None

            # Automatische Geräteerkennung, falls kein Port angegeben
            if not self.port:
                detected_devices = self.detect_supported_devices()
                if not detected_devices:
                    self.last_error = "Keine unterstützten NFC-Geräte gefunden"
                    return False

                # Verwende das erste erkannte Gerät
                self.port = detected_devices[0]['port']
                print(f"Automatisch erkanntes Gerät: {self.port}")

            # Verbindung herstellen
            success = self.connect()
            if success:
                # Geräteidentifikation durchführen
                return self._identify_device()

            return False

        except Exception as e:
            self.last_error = f"Fehler bei Treiberinitialisierung: {str(e)}"
            return False

    def connect(self):
        """
        Stellt eine Verbindung zum Gerät her

        Returns:
            bool: True bei erfolgreicher Verbindung, False sonst
        """
        try:
            self.last_error = None

            if not self.port:
                self.last_error = "Kein Port angegeben"
                return False

            # Serielle Verbindung öffnen
            self.serial_connection = serial.Serial(
                port=self.port,
                baudrate=115200,
                bytesize=serial.EIGHTBITS,
                parity=serial.PARITY_NONE,
                stopbits=serial.STOPBITS_ONE,
                timeout=5
            )

            # Kurze Pause für Verbindungsaufbau
            time.sleep(0.1)

            self.connected = True
            return True

        except serial.SerialException as e:
            self.last_error = f"Serielle Verbindung fehlgeschlagen: {str(e)}"
            self.connected = False
            return False
        except Exception as e:
            self.last_error = f"Unerwarteter Fehler bei Verbindung: {str(e)}"
            self.connected = False
            return False

    def _identify_device(self) -> bool:
        """
        Identifiziert das verbundene NFC-Gerät

        Returns:
            bool: True bei erfolgreicher Identifikation, False sonst
        """
        try:
            if not self.serial_connection:
                self.last_error = "Keine Verbindung zum Gerät"
                return False

            # PING-Befehl senden zur Geräteidentifikation
            self.serial_connection.write(b"PING\n")
            response = self.serial_connection.readline().decode('utf-8').strip()

            if response.startswith("OK:"):
                device_id = response[3:]  # "OK:" entfernen
                self.device_info = {
                    'id': device_id,
                    'port': self.port,
                    'status': 'connected',
                    'protocol_version': '1.0'
                }
                print(f"NFC-Gerät identifiziert: {device_id}")
                return True
            else:
                # Fallback: Auch ohne PING-Antwort als erkannt markieren
                # (für Geräte, die das Protokoll noch nicht unterstützen)
                self.device_info = {
                    'id': 'UNKNOWN_NFC_DEVICE',
                    'port': self.port,
                    'status': 'connected',
                    'protocol_version': 'unknown'
                }
                print(f"NFC-Gerät verbunden (unbekanntes Protokoll): {self.port}")
                return True

        except Exception as e:
            self.last_error = f"Fehler bei Geräteidentifikation: {str(e)}"
            return False

    def disconnect(self):
        """
        Trennt die Verbindung zum Gerät
        """
        try:
            if self.serial_connection and self.serial_connection.is_open:
                self.serial_connection.close()
        except Exception as e:
            print(f"Fehler beim Trennen der Verbindung: {e}")
        finally:
            self.connected = False
            self.serial_connection = None
            self.device_info = None

    def is_connected(self):
        """
        Überprüft, ob eine Verbindung besteht

        Returns:
            bool: True wenn verbunden, False sonst
        """
        return self.connected and self.serial_connection and self.serial_connection.is_open

    def get_device_info(self) -> Optional[Dict[str, Any]]:
        """
        Gibt Informationen über das verbundene Gerät zurück

        Returns:
            Dict oder None: Geräteinformationen oder None wenn nicht verbunden
        """
        return self.device_info

    def get_last_error(self) -> Optional[str]:
        """
        Gibt den letzten aufgetretenen Fehler zurück

        Returns:
            str oder None: Fehlermeldung oder None wenn kein Fehler
        """
        return self.last_error

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
