"""
Modelle für die Darstellung von Filamentspulen-Daten
"""

class FilamentSpool:
    """
    Klasse zur Repräsentation einer Filamentspule mit NFC-Daten
    """
    
    def __init__(self, name="", type="PLA", color="#FFFFFF", manufacturer="", 
                 density=1.24, diameter=1.75, nozzle_temp=200, bed_temp=60, 
                 remaining_length=240, remaining_weight=1000):
        """
        Initialisiert eine neue Filamentspule
        
        Args:
            name (str): Name des Filaments
            type (str): Filament-Typ (z.B. PLA, PETG, ABS)
            color (str): Farbe als Hex-Code
            manufacturer (str): Hersteller des Filaments
            density (float): Dichte des Materials in g/cm³
            diameter (float): Durchmesser des Filaments in mm
            nozzle_temp (int): Empfohlene Düsentemperatur in °C
            bed_temp (int): Empfohlene Betttemperatur in °C
            remaining_length (float): Verbleibende Filamentlänge in m
            remaining_weight (float): Verbleibendes Gewicht in g
        """
        self.name = name
        self.type = type
        self.color = color
        self.manufacturer = manufacturer
        self.density = density
        self.diameter = diameter
        self.nozzle_temp = nozzle_temp
        self.bed_temp = bed_temp
        self.remaining_length = remaining_length
        self.remaining_weight = remaining_weight
    
    def to_dict(self):
        """
        Konvertiert die Filamentspule in ein Dictionary für die NFC-Codierung
        
        Returns:
            dict: Dictionary-Repräsentation der Filamentspule
        """
        return {
            "name": self.name,
            "type": self.type,
            "color": self.color,
            "manufacturer": self.manufacturer,
            "density": self.density,
            "diameter": self.diameter,
            "nozzle_temp": self.nozzle_temp,
            "bed_temp": self.bed_temp,
            "remaining_length": self.remaining_length,
            "remaining_weight": self.remaining_weight
        }
    
    @classmethod
    def from_dict(cls, data):
        """
        Erstellt eine Filamentspule aus einem Dictionary
        
        Args:
            data (dict): Dictionary mit Filamentspulen-Daten
            
        Returns:
            FilamentSpool: Eine neue Filamentspule mit den gegebenen Daten
            
        Raises:
            ValueError: Wenn die Daten ungültig sind
            TypeError: Wenn data nicht ein Dictionary ist
        """
        if data is None:
            raise ValueError("Daten dürfen nicht None sein")
        
        if not isinstance(data, dict):
            raise TypeError("Daten müssen ein Dictionary sein")
        
        return cls(
            name=data.get("name", ""),
            type=data.get("type", "PLA"),
            color=data.get("color", "#FFFFFF"),
            manufacturer=data.get("manufacturer", ""),
            density=data.get("density", 1.24),
            diameter=data.get("diameter", 1.75),
            nozzle_temp=data.get("nozzle_temp", 200),
            bed_temp=data.get("bed_temp", 60),
            remaining_length=data.get("remaining_length", 240),
            remaining_weight=data.get("remaining_weight", 1000)
        )
    
    @classmethod 
    def from_dict_safe(cls, data):
        """
        Erstellt eine Filamentspule aus einem Dictionary mit sicherer Fehlerbehandlung
        
        Args:
            data: Daten beliebigen Typs
            
        Returns:
            tuple: (FilamentSpool or None, error_message or None)
        """
        try:
            if data is None:
                return None, "INVALID_TAG: Keine Daten vorhanden"
            
            if not isinstance(data, dict):
                return None, "INVALID_TAG: Daten haben falsches Format"
            
            # Erstelle Filamentspule mit Standardwerten für fehlende Daten
            spool = cls.from_dict(data)
            return spool, None
            
        except (ValueError, TypeError) as e:
            return None, f"INVALID_TAG: {str(e)}"
        except Exception as e:
            return None, f"INVALID_TAG: Unbekannter Fehler bei der Dekodierung"
