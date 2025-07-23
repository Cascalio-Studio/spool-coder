"""
WriteView - Ansicht zum Programmieren einer NFC-Spule
"""

from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QPushButton,
                           QLabel, QProgressBar, QMessageBox)
from PyQt6.QtCore import Qt, QTimer, pyqtSlot

from src.ui.components import FilamentDetailWidget
from src.services.nfc import NFCDevice
from src.models import FilamentSpool

class WriteView(QWidget):
    """
    Ansicht zum Programmieren einer NFC-Spule
    """
    
    def __init__(self, parent=None):
        super().__init__(parent)
        
        # Store reference to MainWindow for navigation
        # Check by class name instead of specific import to handle different import paths
        print(f"WriteView: Parent type: {type(parent)}")
        print(f"WriteView: Parent class name: {parent.__class__.__name__ if parent else 'None'}")
        
        if parent and hasattr(parent, '__class__') and parent.__class__.__name__ == 'MainWindow':
            self.main_window = parent
            print("WriteView: MainWindow reference stored successfully")
        else:
            self.main_window = None
            print("WriteView: No MainWindow reference - will search for it")
        
        # Layout erstellen
        main_layout = QVBoxLayout(self)
        
        # Titel
        title_label = QLabel("Spule programmieren")
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        font = title_label.font()
        font.setPointSize(18)
        font.setBold(True)
        title_label.setFont(font)
        main_layout.addWidget(title_label)
        
        # Store as instance variable for test compatibility
        self.title_label = title_label
        
        # Anweisungen
        instructions_label = QLabel(
            "Verbinden Sie zuerst das NFC-Lesegerät, geben Sie die Filament-Daten ein und drücken Sie 'Programmieren'.\n"
            "Die Daten werden im Bambu Lab NFC Format codiert und sind mit Bambu Lab 3D-Druckern kompatibel."
        )
        instructions_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        instructions_label.setWordWrap(True)
        main_layout.addWidget(instructions_label)
        
        # Button zum Verbinden
        self.connect_button = QPushButton("NFC-Gerät verbinden")
        self.connect_button.clicked.connect(self.on_connect_clicked)
        main_layout.addWidget(self.connect_button, 0, Qt.AlignmentFlag.AlignCenter)
        
        # FilamentDetailWidget zur Eingabe der Daten
        self.filament_details = FilamentDetailWidget(editable=True)
        main_layout.addWidget(self.filament_details)
        
        # Alias for test compatibility
        self.filament_detail_widget = self.filament_details
        
        # Initialisiere mit Standarddaten
        default_data = FilamentSpool(
            name="Mein Filament",
            type="PLA",
            color="#1E90FF",
            manufacturer="Generic",
            density=1.24,
            diameter=1.75,
            nozzle_temp=210,
            bed_temp=60,
            remaining_length=240,
            remaining_weight=1000
        )
        self.filament_details.set_data(default_data.to_dict())
        
        # Button zum Programmieren
        self.write_button = QPushButton("Als Bambu Lab Spule programmieren")
        self.write_button.clicked.connect(self.on_write_clicked)
        self.write_button.setEnabled(False)  # Initially disabled until connected
        main_layout.addWidget(self.write_button, 0, Qt.AlignmentFlag.AlignCenter)
        
        # Fortschrittsanzeige
        self.progress_bar = QProgressBar()
        self.progress_bar.setRange(0, 100)
        self.progress_bar.setValue(0)
        self.progress_bar.setVisible(False)
        main_layout.addWidget(self.progress_bar)
        
        # Status-Label
        self.status_label = QLabel()
        self.status_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        main_layout.addWidget(self.status_label)
        
        # Zurück-Button
        self.back_button = QPushButton("Zurück")
        self.back_button.clicked.connect(self.on_back_clicked)
        main_layout.addWidget(self.back_button, 0, Qt.AlignmentFlag.AlignCenter)
        
        # NFC-Gerät
        self.nfc_device = NFCDevice()
        
        # Timer für simulierten Schreibvorgang
        self.write_timer = QTimer()
        self.write_timer.timeout.connect(self.update_write_progress)
        self.write_progress = 0

    def update_write_progress(self):
        """
        Aktualisiert den Fortschritt des simulierten Schreibvorgangs
        """
        self.write_progress += 2
        self.progress_bar.setValue(self.write_progress)
        
        if self.write_progress >= 100:
            self.write_timer.stop()

    def on_back_clicked(self):
        """
        Wird aufgerufen, wenn der Zurück-Button geklickt wird
        """
        # Prevent multiple clicks
        if hasattr(self, '_back_clicked') and self._back_clicked:
            return
        self._back_clicked = True
        
        # Disable the back button to prevent multiple clicks
        self.back_button.setEnabled(False)
        
        # Stoppe alle laufenden Prozesse
        self.write_timer.stop()
        self.nfc_device.disconnect()
        
        print("Back button clicked in WriteView")
        
        # Use the stored MainWindow reference
        if self.main_window:
            print("Using stored MainWindow reference")
            self.main_window.show_home()
        else:
            print("No stored MainWindow reference, searching...")
            # Fallback: Search for MainWindow in parent hierarchy
            # Look for any class named MainWindow, regardless of module path
            
            current = self.parent()
            depth = 0
            max_depth = 10
            
            while current and depth < max_depth:
                print(f"Checking parent at depth {depth}: {type(current)}")
                # Check if this is a MainWindow by class name, not full module path
                if hasattr(current, '__class__') and current.__class__.__name__ == 'MainWindow':
                    print(f"Found MainWindow at depth {depth}: {current.__class__}")
                    # Check if it has the show_home method
                    if hasattr(current, 'show_home'):
                        print("Calling show_home method")
                        current.show_home()
                        return
                    else:
                        print("MainWindow found but no show_home method")
                current = current.parent()
                depth += 1
            
            print("Error: Could not find MainWindow in parent hierarchy!")
            # Last resort: try to find MainWindow through QApplication
            try:
                from PyQt6.QtWidgets import QApplication
                app = QApplication.instance()
                if app:
                    for widget in app.allWidgets():
                        if hasattr(widget, '__class__') and widget.__class__.__name__ == 'MainWindow':
                            if hasattr(widget, 'show_home'):
                                print("Found MainWindow through QApplication")
                                widget.show_home()
                                return
                print("Error: Could not find MainWindow anywhere!")
            except Exception as e:
                print(f"Error searching for MainWindow: {e}")
        
        # Re-enable the button after a short delay
        QTimer.singleShot(1000, lambda: self.back_button.setEnabled(True))

    # Methods for test compatibility
    def start_writing(self):
        """Legacy method for backward compatibility - now connects first if needed"""
        if not self.nfc_device.is_connected():
            # Connect directly without calling on_connect_clicked to avoid recursion
            if self.nfc_device.connect():
                self.update_ui()
            else:
                QMessageBox.warning(self, "Verbindungsfehler", "Konnte keine Verbindung zum NFC-Gerät herstellen.")
                return
        
        if self.nfc_device.is_connected():
            self.on_write_clicked()
    
    def on_connect_clicked(self):
        """Handle connect button click"""
        if hasattr(self, '_testing_mode') and self._testing_mode:
            # In testing mode, directly handle connection
            if self.nfc_device.connect():
                self.update_ui()
            else:
                QMessageBox.warning(self, "Verbindungsfehler", "Konnte keine Verbindung zum NFC-Gerät herstellen.")
        else:
            # Normal mode - connect and update UI
            if self.nfc_device.connect():
                self.update_ui()
            else:
                QMessageBox.warning(self, "Verbindungsfehler", "Konnte keine Verbindung zum NFC-Gerät herstellen.")
    
    def on_write_clicked(self):
        """Handle write button click"""
        if hasattr(self, '_testing_mode') and self._testing_mode:
            # In testing mode, directly handle writing
            if not self.nfc_device.is_connected():
                QMessageBox.warning(self, "Nicht verbunden", "Keine Verbindung zum NFC-Gerät.")
                return
            
            # Get form data and try to write the tag
            data = self.filament_detail_widget.get_form_data()
            success = self.nfc_device.write_tag(data)
            if success:
                self.status_label.setText("Programmieren erfolgreich!")
                QMessageBox.information(self, "Erfolg", "Die Spule wurde erfolgreich programmiert.")
            else:
                QMessageBox.warning(self, "Schreibfehler", "Fehler beim Schreiben des NFC-Tags.")
        else:
            # Normal mode - directly write without calling start_writing to avoid recursion
            if not self.nfc_device.is_connected():
                QMessageBox.warning(self, "Nicht verbunden", "Keine Verbindung zum NFC-Gerät.")
                return
            
            # Get form data and try to write the tag
            data = self.filament_detail_widget.get_form_data()
            success = self.nfc_device.write_tag(data)
            if success:
                self.status_label.setText("Programmieren erfolgreich!")
                QMessageBox.information(self, "Erfolg", "Die Spule wurde erfolgreich programmiert.")
            else:
                QMessageBox.warning(self, "Schreibfehler", "Fehler beim Schreiben des NFC-Tags.")
    
    def update_ui(self):
        """Update UI based on connection status"""
        if self.nfc_device.is_connected():
            self.connect_button.setEnabled(False)  # Disable connect button when connected
            self.write_button.setEnabled(True)     # Enable write button when connected
            self.status_label.setText("Gerät verbunden - bereit zum Schreiben")
        else:
            self.connect_button.setEnabled(True)   # Enable connect button when disconnected  
            self.write_button.setEnabled(False)    # Disable write button when disconnected
            self.status_label.setText("Gerät nicht verbunden")
