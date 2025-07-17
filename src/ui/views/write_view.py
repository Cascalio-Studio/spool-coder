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
        
        # Anweisungen
        instructions_label = QLabel(
            "Geben Sie die Filament-Daten ein und drücken Sie 'Programmieren'.\n"
            "Die Daten werden im Bambu Lab NFC Format codiert und sind mit Bambu Lab 3D-Druckern kompatibel."
        )
        instructions_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        instructions_label.setWordWrap(True)
        main_layout.addWidget(instructions_label)
        
        # FilamentDetailWidget zur Eingabe der Daten
        self.filament_details = FilamentDetailWidget(editable=True)
        main_layout.addWidget(self.filament_details)
        
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
        self.write_button.clicked.connect(self.start_writing)
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
    
    def start_writing(self):
        """
        Startet den Schreibvorgang
        """
        # UI vorbereiten
        self.write_button.setEnabled(False)
        self.filament_details.setEnabled(False)
        self.status_label.setText("Verbindung zum Lesegerät wird hergestellt...")
        self.progress_bar.setVisible(True)
        self.progress_bar.setValue(0)
        
        # Bestätigung anfordern
        msg_box = QMessageBox()
        msg_box.setIcon(QMessageBox.Icon.Question)
        msg_box.setText("Möchten Sie die Spule mit den eingegebenen Daten programmieren?")
        msg_box.setWindowTitle("Bestätigung")
        msg_box.setStandardButtons(QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
        
        if msg_box.exec() == QMessageBox.StandardButton.Yes:
            # Simuliere Verbindungsaufbau
            QTimer.singleShot(1000, self.connect_device)
        else:
            # UI zurücksetzen
            self.write_button.setEnabled(True)
            self.filament_details.setEnabled(True)
            self.progress_bar.setVisible(False)
            self.status_label.setText("")
    
    def connect_device(self):
        """
        Verbindet zum NFC-Gerät
        """
        if self.nfc_device.connect():
            self.status_label.setText("Gerät gefunden. Starten Sie den Schreibvorgang...")
            
            # Starte simulierten Schreibvorgang
            self.write_progress = 0
            self.write_timer.start(50)  # Aktualisiere alle 50ms
        else:
            self.status_label.setText("Fehler: Gerät konnte nicht gefunden werden.")
            self.write_button.setEnabled(True)
            self.filament_details.setEnabled(True)
            self.progress_bar.setVisible(False)
    
    def update_write_progress(self):
        """
        Aktualisiert den Fortschritt des simulierten Schreibvorgangs
        """
        self.write_progress += 2
        self.progress_bar.setValue(self.write_progress)
        
        if self.write_progress < 30:
            self.status_label.setText("Spule wird vorbereitet...")
        elif self.write_progress < 60:
            self.status_label.setText("Daten werden geschrieben...")
        elif self.write_progress < 90:
            self.status_label.setText("Daten werden verifiziert...")
        
        if self.write_progress >= 100:
            self.write_timer.stop()
            self.writing_completed()
    
    def writing_completed(self):
        """
        Wird aufgerufen, wenn der Schreibvorgang abgeschlossen ist
        """
        # Hole die Daten aus dem Formular
        data = self.filament_details.get_data()
        
        # Schreibe die Daten mit dem Bambu Lab NFC Algorithmus
        success = self.nfc_device.write_tag(data)
        
        if success:
            self.status_label.setText("Programmieren erfolgreich!")
            
            # Detaillierte Erfolgsmeldung anzeigen
            msg_box = QMessageBox()
            msg_box.setIcon(QMessageBox.Icon.Information)
            msg_box.setText("Die Spule wurde erfolgreich mit dem Bambu Lab NFC Format programmiert.")
            msg_box.setInformativeText(
                "Die folgenden Informationen wurden auf die Spule geschrieben:\n"
                f"- Name: {data['name']}\n"
                f"- Typ: {data['type']}\n"
                f"- Hersteller: {data['manufacturer']}\n"
                f"- Düsentemperatur: {data['nozzle_temp']}°C\n"
                f"- Betttemperatur: {data['bed_temp']}°C"
            )
            msg_box.setDetailedText(
                f"Vollständige Daten:\n"
                f"Name: {data['name']}\n"
                f"Typ: {data['type']}\n"
                f"Farbe: {data['color']}\n"
                f"Hersteller: {data['manufacturer']}\n"
                f"Dichte: {data['density']} g/cm³\n"
                f"Durchmesser: {data['diameter']} mm\n"
                f"Düsentemperatur: {data['nozzle_temp']}°C\n"
                f"Betttemperatur: {data['bed_temp']}°C\n"
                f"Verbleibende Länge: {data['remaining_length']} m\n"
                f"Verbleibendes Gewicht: {data['remaining_weight']} g"
            )
            msg_box.setWindowTitle("Erfolgreiche Programmierung")
            msg_box.exec()
        else:
            self.status_label.setText("Fehler: Programmieren fehlgeschlagen.")
            
            # Detaillierte Fehlermeldung anzeigen
            msg_box = QMessageBox()
            msg_box.setIcon(QMessageBox.Icon.Critical)
            msg_box.setText("Beim Programmieren der Spule mit dem Bambu Lab NFC Format ist ein Fehler aufgetreten.")
            msg_box.setInformativeText(
                "Mögliche Ursachen:\n"
                "1. Spule nicht im Lesebereich\n"
                "2. Spule ist schreibgeschützt\n"
                "3. Spule ist nicht kompatibel mit dem Bambu Lab Format\n"
                "4. Hardware-Fehler am NFC-Lesegerät"
            )
            msg_box.setWindowTitle("Fehler beim Programmieren")
            msg_box.exec()
        
        # UI zurücksetzen
        self.write_button.setEnabled(True)
        self.filament_details.setEnabled(True)
        self.progress_bar.setVisible(False)
        
        # Trennen vom Gerät
        self.nfc_device.disconnect()
    
    def on_back_clicked(self):
        """
        Wird aufgerufen, wenn der Zurück-Button geklickt wird
        """
        # Stoppe alle laufenden Prozesse
        self.write_timer.stop()
        self.nfc_device.disconnect()
        
        # Finde das MainWindow-Objekt und rufe seine show_home-Methode auf
        from src.ui.views.main_window import MainWindow
        
        # Suche nach dem MainWindow unter den Eltern-Widgets
        parent = self.parent()
        while parent and not isinstance(parent, MainWindow):
            parent = parent.parent()
            
        if parent and isinstance(parent, MainWindow):
            parent.show_home()
