"""
Komponentenbibliothek für wiederverwendbare UI-Elemente
"""

from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
                           QLineEdit, QPushButton, QColorDialog, QSpinBox,
                           QDoubleSpinBox, QFormLayout, QGroupBox)
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QColor

class FilamentDetailWidget(QWidget):
    """
    Widget zur Anzeige und Bearbeitung von Filamentspulen-Daten
    """
    
    # Signal, das gesendet wird, wenn Daten geändert wurden
    data_changed = pyqtSignal(dict)
    
    def __init__(self, parent=None, editable=False):
        """
        Initialisiert ein neues FilamentDetailWidget
        
        Args:
            parent (QWidget): Übergeordnetes Widget
            editable (bool): Ob die Felder bearbeitbar sein sollen
        """
        super().__init__(parent)
        
        self.editable = editable
        self.data = {}
        
        # Layout erstellen
        main_layout = QVBoxLayout(self)
        
        # Gruppe für Basisinformationen
        basic_group = QGroupBox("Basisinformationen")
        basic_layout = QFormLayout()
        basic_group.setLayout(basic_layout)
        main_layout.addWidget(basic_group)
        
        # Felder für Basisinformationen
        self.name_edit = QLineEdit()
        self.name_edit.setReadOnly(not editable)
        basic_layout.addRow("Name:", self.name_edit)
        
        self.type_edit = QLineEdit()
        self.type_edit.setReadOnly(not editable)
        basic_layout.addRow("Typ:", self.type_edit)
        
        # Farbe mit Farbauswahl
        color_layout = QHBoxLayout()
        self.color_preview = QWidget()
        self.color_preview.setFixedSize(20, 20)
        self.color_preview.setAutoFillBackground(True)
        
        self.color_edit = QLineEdit()
        self.color_edit.setReadOnly(not editable)
        
        self.color_button = QPushButton("...")
        self.color_button.setFixedSize(30, 20)
        self.color_button.setEnabled(editable)
        self.color_button.clicked.connect(self.select_color)
        
        color_layout.addWidget(self.color_preview)
        color_layout.addWidget(self.color_edit)
        color_layout.addWidget(self.color_button)
        basic_layout.addRow("Farbe:", color_layout)
        
        self.manufacturer_edit = QLineEdit()
        self.manufacturer_edit.setReadOnly(not editable)
        basic_layout.addRow("Hersteller:", self.manufacturer_edit)
        
        # Gruppe für technische Daten
        tech_group = QGroupBox("Technische Daten")
        tech_layout = QFormLayout()
        tech_group.setLayout(tech_layout)
        main_layout.addWidget(tech_group)
        
        # Felder für technische Daten
        self.density_spin = QDoubleSpinBox()
        self.density_spin.setRange(0.5, 2.5)
        self.density_spin.setDecimals(2)
        self.density_spin.setSingleStep(0.01)
        self.density_spin.setSuffix(" g/cm³")
        self.density_spin.setReadOnly(not editable)
        self.density_spin.setButtonSymbols(
            QSpinBox.ButtonSymbols.NoButtons if not editable else QSpinBox.ButtonSymbols.UpDownArrows
        )
        tech_layout.addRow("Dichte:", self.density_spin)
        
        self.diameter_spin = QDoubleSpinBox()
        self.diameter_spin.setRange(1.0, 3.0)
        self.diameter_spin.setDecimals(2)
        self.diameter_spin.setSingleStep(0.05)
        self.diameter_spin.setSuffix(" mm")
        self.diameter_spin.setReadOnly(not editable)
        self.diameter_spin.setButtonSymbols(
            QSpinBox.ButtonSymbols.NoButtons if not editable else QSpinBox.ButtonSymbols.UpDownArrows
        )
        tech_layout.addRow("Durchmesser:", self.diameter_spin)
        
        self.nozzle_temp_spin = QSpinBox()
        self.nozzle_temp_spin.setRange(150, 300)
        self.nozzle_temp_spin.setSingleStep(5)
        self.nozzle_temp_spin.setSuffix(" °C")
        self.nozzle_temp_spin.setReadOnly(not editable)
        self.nozzle_temp_spin.setButtonSymbols(
            QSpinBox.ButtonSymbols.NoButtons if not editable else QSpinBox.ButtonSymbols.UpDownArrows
        )
        tech_layout.addRow("Düsentemperatur:", self.nozzle_temp_spin)
        
        self.bed_temp_spin = QSpinBox()
        self.bed_temp_spin.setRange(0, 120)
        self.bed_temp_spin.setSingleStep(5)
        self.bed_temp_spin.setSuffix(" °C")
        self.bed_temp_spin.setReadOnly(not editable)
        self.bed_temp_spin.setButtonSymbols(
            QSpinBox.ButtonSymbols.NoButtons if not editable else QSpinBox.ButtonSymbols.UpDownArrows
        )
        tech_layout.addRow("Betttemperatur:", self.bed_temp_spin)
        
        # Gruppe für verbleibende Menge
        remaining_group = QGroupBox("Verbleibende Menge")
        remaining_layout = QFormLayout()
        remaining_group.setLayout(remaining_layout)
        main_layout.addWidget(remaining_group)
        
        # Felder für verbleibende Menge
        self.remaining_length_spin = QDoubleSpinBox()
        self.remaining_length_spin.setRange(0, 1000)
        self.remaining_length_spin.setDecimals(1)
        self.remaining_length_spin.setSingleStep(1)
        self.remaining_length_spin.setSuffix(" m")
        self.remaining_length_spin.setReadOnly(not editable)
        self.remaining_length_spin.setButtonSymbols(
            QSpinBox.ButtonSymbols.NoButtons if not editable else QSpinBox.ButtonSymbols.UpDownArrows
        )
        remaining_layout.addRow("Länge:", self.remaining_length_spin)
        
        self.remaining_weight_spin = QDoubleSpinBox()
        self.remaining_weight_spin.setRange(0, 2000)
        self.remaining_weight_spin.setDecimals(1)
        self.remaining_weight_spin.setSingleStep(10)
        self.remaining_weight_spin.setSuffix(" g")
        self.remaining_weight_spin.setReadOnly(not editable)
        self.remaining_weight_spin.setButtonSymbols(
            QSpinBox.ButtonSymbols.NoButtons if not editable else QSpinBox.ButtonSymbols.UpDownArrows
        )
        remaining_layout.addRow("Gewicht:", self.remaining_weight_spin)
        
        # Verbinde Signale für editierbare Widgets
        if editable:
            self.name_edit.textChanged.connect(self.on_data_changed)
            self.type_edit.textChanged.connect(self.on_data_changed)
            self.color_edit.textChanged.connect(self.on_data_changed)
            self.manufacturer_edit.textChanged.connect(self.on_data_changed)
            self.density_spin.valueChanged.connect(self.on_data_changed)
            self.diameter_spin.valueChanged.connect(self.on_data_changed)
            self.nozzle_temp_spin.valueChanged.connect(self.on_data_changed)
            self.bed_temp_spin.valueChanged.connect(self.on_data_changed)
            self.remaining_length_spin.valueChanged.connect(self.on_data_changed)
            self.remaining_weight_spin.valueChanged.connect(self.on_data_changed)
    
    def set_data(self, data):
        """
        Setzt die anzuzeigenden Daten
        
        Args:
            data (dict): Die anzuzeigenden Filamentdaten
        """
        self.data = data
        
        # Fülle die Felder mit den Daten
        self.name_edit.setText(data.get("name", ""))
        self.type_edit.setText(data.get("type", ""))
        self.set_color(data.get("color", "#FFFFFF"))
        self.manufacturer_edit.setText(data.get("manufacturer", ""))
        
        self.density_spin.setValue(data.get("density", 1.24))
        self.diameter_spin.setValue(data.get("diameter", 1.75))
        self.nozzle_temp_spin.setValue(data.get("nozzle_temp", 200))
        self.bed_temp_spin.setValue(data.get("bed_temp", 60))
        
        self.remaining_length_spin.setValue(data.get("remaining_length", 0))
        self.remaining_weight_spin.setValue(data.get("remaining_weight", 0))
    
    def get_data(self):
        """
        Gibt die aktuellen Daten zurück
        
        Returns:
            dict: Die aktuellen Filamentdaten
        """
        return {
            "name": self.name_edit.text(),
            "type": self.type_edit.text(),
            "color": self.color_edit.text().lower(),  # Ensure lowercase hex format
            "manufacturer": self.manufacturer_edit.text(),
            "density": self.density_spin.value(),
            "diameter": self.diameter_spin.value(),
            "nozzle_temp": self.nozzle_temp_spin.value(),
            "bed_temp": self.bed_temp_spin.value(),
            "remaining_length": self.remaining_length_spin.value(),
            "remaining_weight": self.remaining_weight_spin.value()
        }
    
    def select_color(self):
        """
        Öffnet einen Farbauswahldialog
        """
        current_color = QColor(self.color_edit.text())
        color = QColorDialog.getColor(current_color, self, "Filamentfarbe wählen")
        
        if color.isValid():
            self.set_color(color.name())
    
    def set_color(self, color_hex):
        """
        Setzt die Farbe im Vorschau-Widget und im Textfeld
        
        Args:
            color_hex (str): Farbe als Hex-Code (z.B. #FF0000)
        """
        self.color_edit.setText(color_hex)
        
        palette = self.color_preview.palette()
        palette.setColor(self.color_preview.backgroundRole(), QColor(color_hex))
        self.color_preview.setPalette(palette)
    
    def on_data_changed(self):
        """
        Wird aufgerufen, wenn sich Daten ändern
        """
        self.data_changed.emit(self.get_data())
