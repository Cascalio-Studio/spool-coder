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
            "Halten Sie die Bambu Lab Filamentspule an das NFC-Lesegerät und drücken Sie 'Auslesen'.\n"
            "Der Algorithmus kann NFC-Tags im Bambu Lab Format entschlüsseln und validiert die gespeicherten Daten."
        )
        instructions_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        instructions_label.setWordWrap(True)
        main_layout.addWidget(instructions_label)
        
        # Button zum Auslesen
        self.read_button = QPushButton("Bambu Lab Spule auslesen")
        self.read_button.clicked.connect(self.start_reading)
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
    
    def start_reading(self):
        """
        Startet den Lesevorgang
        """
        # UI vorbereiten
        self.read_button.setEnabled(False)
        self.status_label.setText("Verbindung zum Lesegerät wird hergestellt...")
        self.progress_bar.setVisible(True)
        self.progress_bar.setValue(0)
        self.filament_details.setVisible(False)
        
        # Simuliere Verbindungsaufbau
        QTimer.singleShot(1000, self.connect_device)
    
    def connect_device(self):
        """
        Verbindet zum NFC-Gerät
        """
        if self.nfc_device.connect():
            self.status_label.setText("Gerät gefunden. Suche nach Spule...")
            
            # Starte simulierten Lesevorgang
            self.read_progress = 0
            self.read_timer.start(50)  # Aktualisiere alle 50ms
        else:
            self.status_label.setText("Fehler: Gerät konnte nicht gefunden werden.")
            self.read_button.setEnabled(True)
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
        # NFC Tag mit Bambu Lab Algorithmus lesen
        data = self.nfc_device.read_tag()
        
        if data:
            self.status_label.setText("Auslesen erfolgreich!")
            
            # Zeige erweiterte Erfolgsmeldung
            QMessageBox.information(
                self,
                "Bambu Lab NFC Tag erkannt",
                "Die Bambu Lab NFC Spule wurde erfolgreich ausgelesen und decodiert."
            )
            
            # Konvertiere die Daten in ein FilamentSpool-Objekt und zeige sie an
            spool = FilamentSpool.from_dict(data)
            self.filament_details.set_data(spool.to_dict())
            self.filament_details.setVisible(True)
        else:
            self.status_label.setText("Fehler: Keine Daten gefunden oder Spule nicht erkannt.")
            
            # Zeige detaillierte Fehlermeldung
            QMessageBox.warning(
                self,
                "Fehler beim Lesen",
                "Die Spule konnte nicht ausgelesen werden. Mögliche Gründe:\n\n"
                "1. Keine Bambu Lab kompatible Spule erkannt\n"
                "2. Beschädigte oder fehlerhafte NFC-Daten\n"
                "3. NFC-Tag nicht innerhalb der Lesereichweite"
            )
        
        # UI zurücksetzen
        self.read_button.setEnabled(True)
        self.progress_bar.setVisible(False)
        
        # Trennen vom Gerät
        self.nfc_device.disconnect()
    
    def on_back_clicked(self):
        """
        Wird aufgerufen, wenn der Zurück-Button geklickt wird
        """
        # Stoppe alle laufenden Prozesse
        self.read_timer.stop()
        self.nfc_device.disconnect()
        
        # Finde das MainWindow-Objekt und rufe seine show_home-Methode auf
        from src.ui.views.main_window import MainWindow
        
        # Suche nach dem MainWindow unter den Eltern-Widgets
        parent = self.parent()
        while parent and not isinstance(parent, MainWindow):
            parent = parent.parent()
            
        if parent and isinstance(parent, MainWindow):
            parent.show_home()
