"""
NFC Service Manager für die Verwaltung der NFC-Geräteverbindungen
"""

from typing import Optional, Dict, List, Any
from .device import NFCDevice


class NFCManager:
    """
    Manager-Klasse für die Verwaltung von NFC-Geräten
    """

    def __init__(self):
        """
        Initialisiert den NFC-Manager
        """
        self.current_device: Optional[NFCDevice] = None
        self.last_error: Optional[str] = None
        self.initialization_status = False

    def initialize(self, port: Optional[str] = None) -> bool:
        """
        Initialisiert den NFC-Service und verbindet sich mit einem Gerät

        Args:
            port (str, optional): Spezifischer Port für die Verbindung

        Returns:
            bool: True bei erfolgreicher Initialisierung, False sonst
        """
        try:
            self.last_error = None

            # Neue Geräteinstanz erstellen
            self.current_device = NFCDevice(port)

            # Treiber initialisieren
            success = self.current_device.initialize_driver()

            if success:
                self.initialization_status = True
                print("NFC-Service erfolgreich initialisiert")
                return True
            else:
                self.last_error = (self.current_device.get_last_error() or
                                   "Unbekannter Initialisierungsfehler")
                self.initialization_status = False
                return False

        except Exception as e:
            self.last_error = f"Fehler bei NFC-Service-Initialisierung: {str(e)}"
            self.initialization_status = False
            return False

    def get_detected_devices(self) -> List[Dict[str, Any]]:
        """
        Gibt eine Liste der erkannten NFC-Geräte zurück

        Returns:
            List[Dict]: Liste der verfügbaren Geräte
        """
        try:
            return NFCDevice.detect_supported_devices()
        except Exception as e:
            self.last_error = f"Fehler bei Geräteerkennung: {str(e)}"
            return []

    def is_initialized(self) -> bool:
        """
        Prüft, ob der NFC-Service initialisiert ist

        Returns:
            bool: True wenn initialisiert, False sonst
        """
        return (self.initialization_status and self.current_device and
                self.current_device.is_connected())

    def get_device_info(self) -> Optional[Dict[str, Any]]:
        """
        Gibt Informationen über das aktuelle Gerät zurück

        Returns:
            Dict oder None: Geräteinformationen oder None
        """
        if self.current_device:
            return self.current_device.get_device_info()
        return None

    def get_last_error(self) -> Optional[str]:
        """
        Gibt den letzten aufgetretenen Fehler zurück

        Returns:
            str oder None: Fehlermeldung oder None
        """
        return self.last_error

    def shutdown(self) -> None:
        """
        Beendet den NFC-Service und trennt alle Verbindungen
        """
        try:
            if self.current_device:
                self.current_device.disconnect()
            self.current_device = None
            self.initialization_status = False
            print("NFC-Service heruntergefahren")
        except Exception as e:
            print(f"Fehler beim Herunterfahren des NFC-Service: {e}")

    def read_tag(self) -> Optional[Dict[str, Any]]:
        """
        Liest Daten von einem NFC-Tag

        Returns:
            Dict oder None: Gelesene Daten oder None bei Fehler
        """
        if not self.is_initialized():
            self.last_error = "NFC-Service nicht initialisiert"
            return None

        try:
            return self.current_device.read_tag()
        except Exception as e:
            self.last_error = f"Fehler beim Lesen des NFC-Tags: {str(e)}"
            return None

    def write_tag(self, data: Dict[str, Any]) -> bool:
        """
        Schreibt Daten auf ein NFC-Tag

        Args:
            data (Dict): Zu schreibende Daten

        Returns:
            bool: True bei Erfolg, False sonst
        """
        if not self.is_initialized():
            self.last_error = "NFC-Service nicht initialisiert"
            return False

        try:
            return self.current_device.write_tag(data)
        except Exception as e:
            self.last_error = f"Fehler beim Schreiben des NFC-Tags: {str(e)}"
            return False
