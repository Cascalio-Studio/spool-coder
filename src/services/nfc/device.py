"""
Basis-Klasse für die NFC-Kommunikation mit dem Gerät
"""

from services.auth.authorization import get_auth_service
from services.auth.security_logger import get_security_logger

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
        self.auth_service = get_auth_service()
        self.security_logger = get_security_logger()
    
    def _check_authorization(self, operation):
        """
        Check if current user is authorized for the operation
        
        Args:
            operation (str): The operation being attempted
            
        Returns:
            bool: True if authorized, False otherwise
        """
        if not self.auth_service.is_authorized():
            # Log unauthorized access attempt
            current_user = self.auth_service.get_current_user()
            self.security_logger.log_unauthorized_access_attempt(
                resource=f"NFC-{operation}",
                user=current_user,
                details=f"Attempted {operation} operation without authorization"
            )
            self.security_logger.log_access_denied(
                resource=f"NFC-{operation}",
                reason="User not authenticated/authorized",
                user=current_user
            )
            return False
        return True
    
    def connect(self):
        """
        Stellt eine Verbindung zum Gerät her
        
        Returns:
            bool: True bei erfolgreicher Verbindung, False sonst
        """
        # Connection itself doesn't require authorization, but log the event
        if self.auth_service.is_authorized():
            current_user = self.auth_service.get_current_user()
            self.security_logger.log_authorization_event(
                "NFC_DEVICE_CONNECT",
                user=current_user,
                details="Authorized user connecting to NFC device"
            )
        
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
            dict: Die gelesenen Daten oder None bei Fehler/unauthorized access
        """
        # Check authorization before allowing read access
        if not self._check_authorization("READ"):
            return None
            
        if not self.connected:
            return None
            
        # Log successful authorized access
        current_user = self.auth_service.get_current_user()
        self.security_logger.log_authorization_event(
            "NFC_READ_SUCCESS",
            user=current_user,
            details="Authorized NFC tag read operation"
        )
        
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
        # Check authorization before allowing write access
        if not self._check_authorization("WRITE"):
            return False
            
        if not self.connected:
            return False
        
        # Log successful authorized access
        current_user = self.auth_service.get_current_user()
        self.security_logger.log_authorization_event(
            "NFC_WRITE_SUCCESS",
            user=current_user,
            details="Authorized NFC tag write operation"
        )
            
        # Hier würde der Code zum Schreiben des NFC-Tags stehen
        # Simulation eines erfolgreichen Schreibvorgangs
        return True
