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
        
        # Store reference to MainWindow for navigation
        # Check by class name instead of specific import to handle different import paths
        print(f"InfoView: Parent type: {type(parent)}")
        print(f"InfoView: Parent class name: {parent.__class__.__name__ if parent else 'None'}")
        
        if parent and hasattr(parent, '__class__') and parent.__class__.__name__ == 'MainWindow':
            self.main_window = parent
            print("InfoView: MainWindow reference stored successfully")
        else:
            self.main_window = None
            print("InfoView: No MainWindow reference - will search for it")
        
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
            "<p>Version 0.2.0</p>"
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
        # Prevent multiple clicks
        if hasattr(self, '_back_clicked') and self._back_clicked:
            return
        self._back_clicked = True
        
        # Disable the back button to prevent multiple clicks
        self.back_button.setEnabled(False)
        
        print("Back button clicked in InfoView")
        
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
        from PyQt6.QtCore import QTimer
        QTimer.singleShot(1000, lambda: self.back_button.setEnabled(True))
