"""
ReadView - Ansicht zum Auslesen einer NFC-Spule
"""

from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QPushButton,
                           QLabel, QProgressBar, QMessageBox)
from PyQt6.QtCore import Qt, QTimer, pyqtSlot

from src.ui.components import FilamentDetailWidget
from src.services.nfc import NFCDevice
from src.models import FilamentSpool

class ReadView(QWidget):
    """
    Ansicht zum Auslesen einer NFC-Spule
    """
    
    def __init__(self, parent=None):
        super().__init__(parent)
        
        # Store reference to MainWindow for navigation
        # Check by class name instead of specific import to handle different import paths
        print(f"ReadView: Parent type: {type(parent)}")
        print(f"ReadView: Parent class name: {parent.__class__.__name__ if parent else 'None'}")
        
        if parent and hasattr(parent, '__class__') and parent.__class__.__name__ == 'MainWindow':
            self.main_window = parent
            print("ReadView: MainWindow reference stored successfully")
        else:
            self.main_window = None
            print("ReadView: No MainWindow reference - will search for it")
        
        # Layout erstellen
        main_layout = QVBoxLayout(self)
        
        # Titel
        title_label = QLabel("Spule auslesen")
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
            "Verbinden Sie zuerst das NFC-Lesegerät, dann halten Sie die Bambu Lab Filamentspule an das Gerät.\n"
            "Der Algorithmus kann NFC-Tags im Bambu Lab Format entschlüsseln und validiert die gespeicherten Daten."
        )
        instructions_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        instructions_label.setWordWrap(True)
        main_layout.addWidget(instructions_label)
        
        # Button zum Verbinden
        self.connect_button = QPushButton("NFC-Gerät verbinden")
        self.connect_button.clicked.connect(self.on_connect_clicked)
        main_layout.addWidget(self.connect_button, 0, Qt.AlignmentFlag.AlignCenter)
        
        # Button zum Auslesen
        self.read_button = QPushButton("Bambu Lab Spule auslesen")
        self.read_button.clicked.connect(self.on_read_clicked)
        self.read_button.setEnabled(False)  # Initially disabled until connected
        main_layout.addWidget(self.read_button, 0, Qt.AlignmentFlag.AlignCenter)
        
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
        
        # FilamentDetailWidget zur Anzeige der ausgelesenen Daten
        self.filament_details = FilamentDetailWidget(editable=False)
        self.filament_details.setVisible(False)
        main_layout.addWidget(self.filament_details)
        
        # Alias for test compatibility
        self.filament_detail_widget = self.filament_details
        
        # Zurück-Button
        self.back_button = QPushButton("Zurück")
        self.back_button.clicked.connect(self.on_back_clicked)
        main_layout.addWidget(self.back_button, 0, Qt.AlignmentFlag.AlignCenter)
        
        # NFC-Gerät
        self.nfc_device = NFCDevice()
        
        # Timer für simulierten Lesevorgang
        self.read_timer = QTimer()
        self.read_timer.timeout.connect(self.update_read_progress)
        self.read_progress = 0

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
        self.read_timer.stop()
        self.nfc_device.disconnect()
        
        print("Back button clicked in ReadView")
        
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

    def update_read_progress(self):
        """
        Aktualisiert den Fortschritt des simulierten Lesevorgangs
        """
        self.read_progress += 4  # Faster progress for better UX
        self.progress_bar.setValue(self.read_progress)
        
        # Update status text based on progress
        if self.read_progress < 30:
            self.status_label.setText("Verbinde mit NFC-Tag...")
        elif self.read_progress < 60:
            self.status_label.setText("Lese Bambu Lab Daten...")
        elif self.read_progress < 90:
            self.status_label.setText("Entschlüssele Daten...")
        else:
            self.status_label.setText("Validiere Daten...")
        
        if self.read_progress >= 100:
            self.read_timer.stop()
            self.reading_completed()
    
    def reading_completed(self):
        """
        Wird aufgerufen, wenn der Lesevorgang abgeschlossen ist
        """
        # Try to read the tag
        data = self.nfc_device.read_tag()
        
        if data:
            self.status_label.setText("Auslesen erfolgreich!")
            
            # Show success message
            QMessageBox.information(
                self,
                "Bambu Lab NFC Tag erkannt",
                "Die Bambu Lab NFC Spule wurde erfolgreich ausgelesen und decodiert."
            )
            
            # Convert data to FilamentSpool object and display
            try:
                spool = FilamentSpool.from_dict(data)
                self.filament_details.set_data(spool.to_dict())
                self.filament_details.setVisible(True)
            except Exception as e:
                # Fallback: just fill the form directly
                self.filament_detail_widget.fill_form(data)
                self.filament_details.setVisible(True)
        else:
            self.status_label.setText("Fehler: Keine Daten gefunden oder Spule nicht erkannt.")
            
            # Show detailed error message
            QMessageBox.warning(
                self,
                "Fehler beim Lesen",
                "Die Spule konnte nicht ausgelesen werden. Mögliche Gründe:\n\n"
                "1. Keine Bambu Lab kompatible Spule erkannt\n"
                "2. Beschädigte oder fehlerhafte NFC-Daten\n"
                "3. NFC-Tag nicht innerhalb der Lesereichweite"
            )
        
        # Reset UI
        self.read_button.setEnabled(True)
        self.progress_bar.setVisible(False)

    # Methods for test compatibility
    def start_reading(self):
        """Legacy method for backward compatibility - now connects first if needed"""
        if not self.nfc_device.is_connected():
            # Connect directly without calling on_connect_clicked to avoid recursion
            if self.nfc_device.connect():
                self.update_ui()
            else:
                QMessageBox.warning(self, "Verbindungsfehler", "Konnte keine Verbindung zum NFC-Gerät herstellen.")
                return
        
        # In testing mode, skip the progress bar for faster execution
        if hasattr(self, '_testing_mode') and self._testing_mode:
            data = self.nfc_device.read_tag()
            if data:
                self.filament_detail_widget.fill_form(data)
                self.status_label.setText("Auslesen erfolgreich!")
                self.filament_details.setVisible(True)
            else:
                QMessageBox.warning(self, "Lesefehler", "Fehler beim Lesen des NFC-Tags.")
        else:
            # Use the progress bar for normal operation
            self.on_read_clicked()
    
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
    
    def on_read_clicked(self):
        """Handle read button click"""
        if not self.nfc_device.is_connected():
            QMessageBox.warning(self, "Nicht verbunden", "Keine Verbindung zum NFC-Gerät.")
            return
        
        # In testing mode, skip the progress animation
        if hasattr(self, '_testing_mode') and self._testing_mode:
            self.reading_completed()
            return
        
        # Start progress bar and disable UI
        self.read_button.setEnabled(False)
        self.progress_bar.setVisible(True)
        self.progress_bar.setValue(0)
        self.status_label.setText("Lese NFC-Tag...")
        self.filament_details.setVisible(False)
        
        # Start the reading process with progress animation
        self.read_progress = 0
        self.read_timer.start(50)  # Update every 50ms
    
    def update_ui(self):
        """Update UI based on connection status"""
        if self.nfc_device.is_connected():
            self.connect_button.setEnabled(False)  # Disable connect button when connected
            self.read_button.setEnabled(True)       # Enable read button when connected
            self.status_label.setText("Gerät verbunden - bereit zum Lesen")
        else:
            self.connect_button.setEnabled(True)    # Enable connect button when disconnected  
            self.read_button.setEnabled(False)      # Disable read button when disconnected
            self.status_label.setText("Gerät nicht verbunden")
