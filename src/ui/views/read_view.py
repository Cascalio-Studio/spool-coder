"""
ReadView - Ansicht zum Auslesen einer NFC-Spule
"""

from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QPushButton,
                           QLabel, QProgressBar, QMessageBox)
from PyQt6.QtCore import Qt, QTimer, pyqtSlot

from ui.components import FilamentDetailWidget
from services.nfc import NFCDevice
from models import FilamentSpool

class ReadView(QWidget):
    """
    Ansicht zum Auslesen einer NFC-Spule
    """
    
    def __init__(self, parent=None):
        super().__init__(parent)
        
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
        
        # Anweisungen
        instructions_label = QLabel(
            "Halten Sie die Filamentspule an das NFC-Lesegerät und drücken Sie 'Auslesen'."
        )
        instructions_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        instructions_label.setWordWrap(True)
        main_layout.addWidget(instructions_label)
        
        # Buttons zum Auslesen
        button_layout = QHBoxLayout()
        
        self.read_button = QPushButton("Auslesen")
        self.read_button.clicked.connect(self.start_reading)
        button_layout.addWidget(self.read_button)
        
        self.read_raw_button = QPushButton("Raw-Daten lesen")
        self.read_raw_button.clicked.connect(self.start_raw_reading)
        button_layout.addWidget(self.read_raw_button)
        
        main_layout.addLayout(button_layout)
        
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
        
        # Raw data display area
        self.raw_data_label = QLabel("Raw NFC Daten:")
        self.raw_data_label.setVisible(False)
        main_layout.addWidget(self.raw_data_label)
        
        self.raw_data_display = QLabel()
        self.raw_data_display.setStyleSheet("""
            QLabel {
                background-color: #f0f0f0;
                border: 1px solid #ccc;
                padding: 10px;
                font-family: monospace;
                font-size: 10px;
            }
        """)
        self.raw_data_display.setWordWrap(True)
        self.raw_data_display.setVisible(False)
        main_layout.addWidget(self.raw_data_display)
        
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
        self.reading_raw_data = False  # Flag to track if we're reading raw data
    
    def start_reading(self):
        """
        Startet den Lesevorgang
        """
        self.reading_raw_data = False
        self._start_reading_common("Verbindung zum Lesegerät wird hergestellt...")
    
    def start_raw_reading(self):
        """
        Startet den Raw-Daten Lesevorgang
        """
        self.reading_raw_data = True
        self._start_reading_common("Verbindung zum Lesegerät wird hergestellt (Raw-Modus)...")
    
    def _start_reading_common(self, status_text):
        """
        Gemeinsame Funktionalität für beide Lesevorgänge
        """
        # UI vorbereiten
        self.read_button.setEnabled(False)
        self.read_raw_button.setEnabled(False)
        self.status_label.setText(status_text)
        self.progress_bar.setVisible(True)
        self.progress_bar.setValue(0)
        self.filament_details.setVisible(False)
        self.raw_data_label.setVisible(False)
        self.raw_data_display.setVisible(False)
        
        # Simuliere Verbindungsaufbau
        QTimer.singleShot(1000, self.connect_device)
    
    def connect_device(self):
        """
        Verbindet zum NFC-Gerät
        """
        if self.nfc_device.connect():
            if self.reading_raw_data:
                self.status_label.setText("Gerät gefunden. Lese Raw-Daten von Spule...")
            else:
                self.status_label.setText("Gerät gefunden. Suche nach Spule...")
            
            # Starte simulierten Lesevorgang
            self.read_progress = 0
            self.read_timer.start(50)  # Aktualisiere alle 50ms
        else:
            self.status_label.setText("Fehler: Gerät konnte nicht gefunden werden.")
            self.read_button.setEnabled(True)
            self.read_raw_button.setEnabled(True)
            self.progress_bar.setVisible(False)
    
    def update_read_progress(self):
        """
        Aktualisiert den Fortschritt des simulierten Lesevorgangs
        """
        self.read_progress += 2
        self.progress_bar.setValue(self.read_progress)
        
        if self.read_progress >= 100:
            self.read_timer.stop()
            self.reading_completed()
    
    def reading_completed(self):
        """
        Wird aufgerufen, wenn der Lesevorgang abgeschlossen ist
        """
        if self.reading_raw_data:
            # Lese Raw-Daten
            raw_data = self.nfc_device.read_raw_data()
            
            if raw_data:
                self.status_label.setText("Raw-Daten erfolgreich gelesen!")
                
                # Zeige Raw-Daten an
                self.display_raw_data(raw_data)
                self.raw_data_label.setVisible(True)
                self.raw_data_display.setVisible(True)
            else:
                self.status_label.setText("Fehler: Keine Raw-Daten gefunden oder Spule nicht erkannt.")
        else:
            # Simuliere das Lesen von Daten
            data = self.nfc_device.read_tag()
            
            if data:
                self.status_label.setText("Auslesen erfolgreich!")
                
                # Konvertiere die Daten in ein FilamentSpool-Objekt und zeige sie an
                spool = FilamentSpool.from_dict(data)
                self.filament_details.set_data(spool.to_dict())
                self.filament_details.setVisible(True)
            else:
                self.status_label.setText("Fehler: Keine Daten gefunden oder Spule nicht erkannt.")
        
        # UI zurücksetzen
        self.read_button.setEnabled(True)
        self.read_raw_button.setEnabled(True)
        self.progress_bar.setVisible(False)
        
        # Trennen vom Gerät
        self.nfc_device.disconnect()
    
    def display_raw_data(self, raw_data):
        """
        Zeigt die Raw-Daten in einem benutzerfreundlichen Format an
        
        Args:
            raw_data (bytes): Die rohen NFC-Daten
        """
        # Formatiere die Daten für die Anzeige
        hex_data = raw_data.hex().upper()
        
        # Teile in 16-Byte Zeilen auf
        formatted_lines = []
        for i in range(0, len(hex_data), 32):  # 32 hex chars = 16 bytes
            line = hex_data[i:i+32]
            # Füge Leerzeichen zwischen Bytes ein
            spaced_line = ' '.join(line[j:j+2] for j in range(0, len(line), 2))
            formatted_lines.append(f"{i//2:04X}: {spaced_line}")
        
        # Zusätzliche Informationen
        info_text = f"Raw NFC Payload ({len(raw_data)} bytes):\n\n"
        info_text += '\n'.join(formatted_lines[:10])  # Zeige nur die ersten 10 Zeilen
        
        if len(formatted_lines) > 10:
            info_text += f"\n... ({len(formatted_lines) - 10} weitere Zeilen)"
        
        # Versuche den JSON-Teil zu dekodieren
        try:
            # Suche nach JSON-Start und -Ende
            json_start = raw_data.find(b'{')
            json_end = raw_data.rfind(b'}')
            
            if json_start != -1 and json_end != -1 and json_start < json_end:
                json_data = raw_data[json_start:json_end+1]
                decoded_json = json_data.decode('utf-8', errors='ignore')
                info_text += f"\n\nDekodierte JSON-Daten:\n{decoded_json}"
        except Exception:
            pass
        
        self.raw_data_display.setText(info_text)
    
    def on_back_clicked(self):
        """
        Wird aufgerufen, wenn der Zurück-Button geklickt wird
        """
        # Stoppe alle laufenden Prozesse
        self.read_timer.stop()
        self.nfc_device.disconnect()
        
        # Finde das MainWindow-Objekt und rufe seine show_home-Methode auf
        from ui.views.main_window import MainWindow
        
        # Suche nach dem MainWindow unter den Eltern-Widgets
        parent = self.parent()
        while parent and not isinstance(parent, MainWindow):
            parent = parent.parent()
            
        if parent and isinstance(parent, MainWindow):
            parent.show_home()
