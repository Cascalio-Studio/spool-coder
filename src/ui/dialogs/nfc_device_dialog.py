"""
Dialog zur Auswahl und Konfiguration des NFC-Geräts
"""

from PyQt6.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, QPushButton,
                           QLabel, QComboBox, QCheckBox, QMessageBox)
from PyQt6.QtCore import Qt, pyqtSignal, QSettings

from src.services.nfc.device import NFCDevice


class NFCDeviceDialog(QDialog):
    """
    Dialog zur Auswahl und Konfiguration des NFC-Geräts
    """
    
    # Signal, das gesendet wird, wenn die Konfiguration geändert wurde
    config_changed = pyqtSignal(dict)
    
    def __init__(self, parent=None):
        super().__init__(parent)
        
        self.setWindowTitle("NFC-Gerät konfigurieren")
        self.setMinimumWidth(450)
        
        # Lade gespeicherte Einstellungen
        self.settings = QSettings("Cascalio-Studio", "Spool-Coder")
        self.use_simulation = self.settings.value("nfc/use_simulation", True, type=bool)
        self.selected_device = self.settings.value("nfc/selected_device", "", type=str)
        
        # Layout erstellen
        main_layout = QVBoxLayout(self)
        
        # Überschrift
        title_label = QLabel("NFC-Gerät konfigurieren")
        title_font = title_label.font()
        title_font.setBold(True)
        title_font.setPointSize(14)
        title_label.setFont(title_font)
        main_layout.addWidget(title_label)
        
        # Beschreibung
        desc_label = QLabel(
            "Konfigurieren Sie das zu verwendende NFC-Gerät. "
            "Sie können entweder ein echtes NFC-Lesegerät verwenden oder "
            "den Simulationsmodus aktivieren, um die Software ohne Hardware zu testen."
        )
        desc_label.setWordWrap(True)
        main_layout.addWidget(desc_label)
        
        # Simulationsmodus
        sim_layout = QHBoxLayout()
        self.sim_checkbox = QCheckBox("Simulationsmodus verwenden")
        self.sim_checkbox.setChecked(self.use_simulation)
        self.sim_checkbox.stateChanged.connect(self.on_simulation_changed)
        sim_layout.addWidget(self.sim_checkbox)
        sim_layout.addStretch()
        main_layout.addLayout(sim_layout)
        
        # Geräteauswahl
        device_layout = QHBoxLayout()
        device_layout.addWidget(QLabel("NFC-Gerät:"))
        self.device_combo = QComboBox()
        device_layout.addWidget(self.device_combo, 1)
        self.refresh_button = QPushButton("Aktualisieren")
        self.refresh_button.clicked.connect(self.refresh_devices)
        device_layout.addWidget(self.refresh_button)
        main_layout.addLayout(device_layout)
        
        # Hinweis
        self.hint_label = QLabel()
        self.hint_label.setWordWrap(True)
        main_layout.addWidget(self.hint_label)
        
        # Buttons
        button_layout = QHBoxLayout()
        button_layout.addStretch()
        self.test_button = QPushButton("Verbindung testen")
        self.test_button.clicked.connect(self.test_connection)
        button_layout.addWidget(self.test_button)
        self.save_button = QPushButton("Speichern")
        self.save_button.clicked.connect(self.save_config)
        button_layout.addWidget(self.save_button)
        self.cancel_button = QPushButton("Abbrechen")
        self.cancel_button.clicked.connect(self.reject)
        button_layout.addWidget(self.cancel_button)
        main_layout.addLayout(button_layout)
        
        # Initialisiere die Geräteliste
        self.refresh_devices()
        
        # UI-Status aktualisieren
        self.update_ui_state()
    
    def refresh_devices(self):
        """
        Aktualisiert die Liste der verfügbaren NFC-Geräte
        """
        self.device_combo.clear()
        
        # Füge simuliertes Gerät hinzu, wenn Simulationsmodus aktiviert
        if self.sim_checkbox.isChecked():
            self.device_combo.addItem("Simuliertes NFC-Gerät", "")
            self.hint_label.setText("Im Simulationsmodus wird kein echtes NFC-Gerät verwendet. "
                                  "Die Software simuliert alle NFC-Operationen.")
            return
            
        # Suche nach verfügbaren Geräten
        self.hint_label.setText("Suche nach NFC-Geräten...")
        self.setEnabled(False)
        self.repaint()  # Force UI update
        
        devices = NFCDevice.list_available_devices()
        
        if not devices:
            self.device_combo.addItem("Kein NFC-Gerät gefunden", "")
            self.hint_label.setText(
                "Es wurden keine NFC-Geräte gefunden. Stellen Sie sicher, dass ein "
                "kompatibles NFC-Gerät angeschlossen ist und die nötigen Treiber installiert sind."
            )
        else:
            for device in devices:
                self.device_combo.addItem(device, device)
            
            self.hint_label.setText(f"{len(devices)} NFC-Gerät(e) gefunden. "
                                  f"Wählen Sie das zu verwendende Gerät aus.")
            
            # Stelle zuvor gespeichertes Gerät wieder ein, falls verfügbar
            if self.selected_device:
                index = self.device_combo.findData(self.selected_device)
                if index >= 0:
                    self.device_combo.setCurrentIndex(index)
        
        self.setEnabled(True)
    
    def on_simulation_changed(self):
        """
        Wird aufgerufen, wenn der Simulationsmodus geändert wird
        """
        self.update_ui_state()
        self.refresh_devices()
    
    def update_ui_state(self):
        """
        Aktualisiert den UI-Zustand basierend auf den aktuellen Einstellungen
        """
        use_sim = self.sim_checkbox.isChecked()
        self.device_combo.setEnabled(not use_sim)
        self.refresh_button.setEnabled(not use_sim)
    
    def test_connection(self):
        """
        Testet die Verbindung zum ausgewählten NFC-Gerät
        """
        use_sim = self.sim_checkbox.isChecked()
        device_path = self.device_combo.currentData() if not use_sim else None
        
        try:
            # Versuche, eine Verbindung herzustellen
            nfc_device = NFCDevice(port=device_path, simulation=use_sim)
            if nfc_device.connect():
                QMessageBox.information(
                    self,
                    "Verbindung erfolgreich",
                    "Die Verbindung zum NFC-Gerät wurde erfolgreich hergestellt."
                )
                nfc_device.disconnect()
            else:
                QMessageBox.warning(
                    self,
                    "Verbindungsfehler",
                    "Die Verbindung zum NFC-Gerät konnte nicht hergestellt werden."
                )
        except Exception as e:
            QMessageBox.critical(
                self,
                "Fehler",
                f"Bei der Verbindung mit dem NFC-Gerät ist ein Fehler aufgetreten:\n\n{str(e)}"
            )
    
    def save_config(self):
        """
        Speichert die Konfiguration und schließt den Dialog
        """
        use_sim = self.sim_checkbox.isChecked()
        device_path = self.device_combo.currentData() if not use_sim else ""
        
        # Speichere Einstellungen
        self.settings.setValue("nfc/use_simulation", use_sim)
        self.settings.setValue("nfc/selected_device", device_path)
        
        # Sende Signal
        self.config_changed.emit({
            "use_simulation": use_sim,
            "device_path": device_path
        })
        
        # Schließe Dialog
        self.accept()
