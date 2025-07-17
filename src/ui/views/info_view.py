"""
InfoView - Ansicht für Informationen zur Software
"""

from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QLabel, QPushButton, QTabWidget)
from PyQt6.QtCore import Qt

class InfoView(QWidget):
    """
    Ansicht für Informationen zur Software
    """
    
    def __init__(self, parent=None):
        super().__init__(parent)
        
        # Layout erstellen
        main_layout = QVBoxLayout(self)
        
        # Titel
        title_label = QLabel("Info")
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        font = title_label.font()
        font.setPointSize(18)
        font.setBold(True)
        title_label.setFont(font)
        main_layout.addWidget(title_label)
        
        # Tab-Widget für verschiedene Infos
        self.tab_widget = QTabWidget()
        main_layout.addWidget(self.tab_widget)
        
        # Über-Tab
        about_widget = QWidget()
        about_layout = QVBoxLayout(about_widget)
        
        about_text = QLabel(
            "<h2>Spool-Coder</h2>"
            "<p>Version 0.1.0</p>"
            "<p>Copyright © 2025 Cascalio-Studio</p>"
            "<p>Spool-Coder ist eine Software zum Auslesen und Umprogrammieren "
            "von NFC-Spulen für Bambulab Filament Rollen.</p>"
        )
        about_text.setTextFormat(Qt.TextFormat.RichText)
        about_text.setWordWrap(True)
        about_text.setAlignment(Qt.AlignmentFlag.AlignCenter)
        about_layout.addWidget(about_text)
        
        self.tab_widget.addTab(about_widget, "Über")
        
        # Anleitung-Tab
        guide_widget = QWidget()
        guide_layout = QVBoxLayout(guide_widget)
        
        guide_text = QLabel(
            "<h2>Anleitung</h2>"
            "<h3>Spule auslesen</h3>"
            "<p>1. Wählen Sie 'Spule auslesen' im Hauptmenü</p>"
            "<p>2. Halten Sie die Filamentspule an das NFC-Lesegerät</p>"
            "<p>3. Klicken Sie auf 'Auslesen'</p>"
            "<p>4. Die Daten der Spule werden angezeigt</p>"
            "<h3>Spule programmieren</h3>"
            "<p>1. Wählen Sie 'Spule programmieren' im Hauptmenü</p>"
            "<p>2. Geben Sie die gewünschten Daten ein</p>"
            "<p>3. Halten Sie die Filamentspule an das NFC-Lesegerät</p>"
            "<p>4. Klicken Sie auf 'Programmieren'</p>"
            "<p>5. Warten Sie, bis der Vorgang abgeschlossen ist</p>"
        )
        guide_text.setTextFormat(Qt.TextFormat.RichText)
        guide_text.setWordWrap(True)
        guide_text.setAlignment(Qt.AlignmentFlag.AlignLeft)
        guide_layout.addWidget(guide_text)
        
        self.tab_widget.addTab(guide_widget, "Anleitung")
        
        # Lizenz-Tab
        license_widget = QWidget()
        license_layout = QVBoxLayout(license_widget)
        
        license_text = QLabel(
            "<h2>Lizenz</h2>"
            "<p>Spool-Coder ist unter der MIT-Lizenz verfügbar.</p>"
            "<p>Die vollständige Lizenz finden Sie in der LICENSE-Datei im Quellcode-Repository.</p>"
        )
        license_text.setTextFormat(Qt.TextFormat.RichText)
        license_text.setWordWrap(True)
        license_text.setAlignment(Qt.AlignmentFlag.AlignCenter)
        license_layout.addWidget(license_text)
        
        self.tab_widget.addTab(license_widget, "Lizenz")
        
        # Zurück-Button
        self.back_button = QPushButton("Zurück")
        self.back_button.clicked.connect(self.on_back_clicked)
        main_layout.addWidget(self.back_button, 0, Qt.AlignmentFlag.AlignCenter)
    
    def on_back_clicked(self):
        """
        Wird aufgerufen, wenn der Zurück-Button geklickt wird
        """
        # Finde das MainWindow-Objekt und rufe seine show_home-Methode auf
        from src.ui.views.main_window import MainWindow
        
        # Suche nach dem MainWindow unter den Eltern-Widgets
        parent = self.parent()
        while parent and not isinstance(parent, MainWindow):
            parent = parent.parent()
            
        if parent and isinstance(parent, MainWindow):
            parent.show_home()
