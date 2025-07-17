"""
Hauptfenster der Anwendung
"""

from PyQt6.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QPushButton,
                           QLabel, QStackedWidget, QHBoxLayout, QMenuBar, QMenu, QStatusBar, QMessageBox)
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QIcon, QFont, QAction
from services.nfc import NFCManager

class MainWindow(QMainWindow):
    """
    Hauptfenster der Spool-Coder Anwendung
    """
    
    def __init__(self):
        super().__init__()
        
        # NFC Manager initialisieren
        self.nfc_manager = NFCManager()
        
        # Grundlegende Fenstereinstellungen
        self.setWindowTitle("Spool-Coder - Bambulab NFC Tool")
        self.setMinimumSize(800, 600)
        
        # Status-Bar erstellen
        self.statusBar = QStatusBar()
        self.setStatusBar(self.statusBar)
        self.statusBar.showMessage("Bereit - NFC nicht initialisiert")
        
        # Menü-Bar erstellen
        self.setup_menu()
        
        # Zentrales Widget
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        
        # Layout für zentrales Widget
        self.main_layout = QVBoxLayout(self.central_widget)
        
        # Willkommenstext
        self.welcome_label = QLabel("Willkommen beim Spool-Coder!")
        self.welcome_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        font = QFont()
        font.setPointSize(24)
        font.setBold(True)
        self.welcome_label.setFont(font)
        self.main_layout.addWidget(self.welcome_label)
        
        # Beschreibungstext
        self.description_label = QLabel(
            "Mit dieser Software können Sie NFC-Spulen für Bambulab Filament Rollen auslesen und umprogrammieren."
        )
        self.description_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.main_layout.addWidget(self.description_label)
        
        # NFC Status Label
        self.nfc_status_label = QLabel("NFC-Status: Nicht initialisiert")
        self.nfc_status_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.nfc_status_label.setStyleSheet("color: red; font-weight: bold;")
        self.main_layout.addWidget(self.nfc_status_label)
        
        # Container für die Menü-Buttons
        self.menu_container = QWidget()
        self.menu_layout = QVBoxLayout(self.menu_container)
        self.main_layout.addWidget(self.menu_container)
        
        # Menü-Buttons erstellen
        self.create_menu_buttons()
        
        # Stack für verschiedene Ansichten
        self.view_stack = QStackedWidget()
        self.main_layout.addWidget(self.view_stack)
        
        # Startseite als Standard setzen
        self.view_stack.setCurrentIndex(0)
        self.view_stack.hide()
    
    def setup_menu(self):
        """
        Erstellt die Menüleiste
        """
        self.menuBar = QMenuBar(self)
        self.setMenuBar(self.menuBar)
        
        # Datei-Menü
        file_menu = QMenu("&Datei", self)
        self.menuBar.addMenu(file_menu)
        
        exit_action = QAction("&Beenden", self)
        exit_action.triggered.connect(self.close)
        file_menu.addAction(exit_action)
        
        # Ansicht-Menü
        view_menu = QMenu("&Ansicht", self)
        self.menuBar.addMenu(view_menu)
        
        home_action = QAction("&Startseite", self)
        home_action.triggered.connect(self.show_home)
        view_menu.addAction(home_action)
        
        # Hilfe-Menü
        help_menu = QMenu("&Hilfe", self)
        self.menuBar.addMenu(help_menu)
        
        # NFC-Menü
        nfc_menu = QMenu("&NFC", self)
        self.menuBar.addMenu(nfc_menu)
        
        init_nfc_action = QAction("&NFC initialisieren", self)
        init_nfc_action.triggered.connect(self.initialize_nfc)
        nfc_menu.addAction(init_nfc_action)
        
        detect_devices_action = QAction("&Geräte erkennen", self)
        detect_devices_action.triggered.connect(self.detect_nfc_devices)
        nfc_menu.addAction(detect_devices_action)
        
        info_action = QAction("&Info", self)
        info_action.triggered.connect(self.show_info)
        help_menu.addAction(info_action)
    
    def create_menu_buttons(self):
        """
        Erstellt die Hauptmenü-Buttons
        """
        # Button-Stil
        button_style = """
        QPushButton {
            background-color: #4a86e8;
            color: white;
            border: none;
            padding: 10px;
            border-radius: 5px;
            font-size: 16px;
            min-width: 200px;
        }
        QPushButton:hover {
            background-color: #3a76d8;
        }
        """
        
        # NFC initialisieren Button
        self.init_nfc_button = QPushButton("NFC initialisieren")
        self.init_nfc_button.setStyleSheet(button_style)
        self.init_nfc_button.clicked.connect(self.initialize_nfc)
        self.menu_layout.addWidget(self.init_nfc_button, 0, Qt.AlignmentFlag.AlignCenter)
        
        # Spule auslesen
        self.read_button = QPushButton("Spule auslesen")
        self.read_button.setStyleSheet(button_style)
        self.read_button.clicked.connect(self.show_read_view)
        self.menu_layout.addWidget(self.read_button, 0, Qt.AlignmentFlag.AlignCenter)
        
        # Spule programmieren
        self.write_button = QPushButton("Spule programmieren")
        self.write_button.setStyleSheet(button_style)
        self.write_button.clicked.connect(self.show_write_view)
        self.menu_layout.addWidget(self.write_button, 0, Qt.AlignmentFlag.AlignCenter)
        
        # Einstellungen
        self.settings_button = QPushButton("Einstellungen")
        self.settings_button.setStyleSheet(button_style)
        self.settings_button.clicked.connect(self.show_settings)
        self.menu_layout.addWidget(self.settings_button, 0, Qt.AlignmentFlag.AlignCenter)
        
        # Info
        self.info_button = QPushButton("Info")
        self.info_button.setStyleSheet(button_style)
        self.info_button.clicked.connect(self.show_info)
        self.menu_layout.addWidget(self.info_button, 0, Qt.AlignmentFlag.AlignCenter)
    
    def show_home(self):
        """
        Zeigt die Startseite an
        """
        self.view_stack.hide()
        self.menu_container.show()
        self.welcome_label.show()
        self.description_label.show()
        self.statusBar.showMessage("Startseite")
    
    def show_read_view(self):
        """
        Zeigt die Ansicht zum Auslesen der Spule an
        """
        self.menu_container.hide()
        self.welcome_label.hide()
        self.description_label.hide()
        
        # Hier würde die ReadView zum view_stack hinzugefügt und angezeigt werden
        from ui.views.read_view import ReadView
        
        # Entferne alle vorherigen Widgets aus dem Stack
        while self.view_stack.count() > 0:
            self.view_stack.removeWidget(self.view_stack.widget(0))
        
        read_view = ReadView(self)
        self.view_stack.addWidget(read_view)
        self.view_stack.show()
        self.statusBar.showMessage("Spule auslesen")
    
    def show_write_view(self):
        """
        Zeigt die Ansicht zum Programmieren der Spule an
        """
        self.menu_container.hide()
        self.welcome_label.hide()
        self.description_label.hide()
        
        # Hier würde die WriteView zum view_stack hinzugefügt und angezeigt werden
        from ui.views.write_view import WriteView
        
        # Entferne alle vorherigen Widgets aus dem Stack
        while self.view_stack.count() > 0:
            self.view_stack.removeWidget(self.view_stack.widget(0))
        
        write_view = WriteView(self)
        self.view_stack.addWidget(write_view)
        self.view_stack.show()
        self.statusBar.showMessage("Spule programmieren")
    
    def show_settings(self):
        """
        Zeigt die Einstellungen an
        """
        self.menu_container.hide()
        self.welcome_label.hide()
        self.description_label.hide()
        
        # Hier würde die SettingsView zum view_stack hinzugefügt und angezeigt werden
        self.statusBar.showMessage("Einstellungen")
        
        # Platzhalter-Nachricht
        self.show_placeholder_message("Einstellungen", "Funktionalität wird bald implementiert")
    
    def show_info(self):
        """
        Zeigt die Info-Seite an
        """
        self.menu_container.hide()
        self.welcome_label.hide()
        self.description_label.hide()
        
        # Hier würde die InfoView zum view_stack hinzugefügt und angezeigt werden
        from ui.views.info_view import InfoView
        
        # Entferne alle vorherigen Widgets aus dem Stack
        while self.view_stack.count() > 0:
            self.view_stack.removeWidget(self.view_stack.widget(0))
        
        info_view = InfoView(self)
        self.view_stack.addWidget(info_view)
        self.view_stack.show()
        self.statusBar.showMessage("Info")
    
    def show_placeholder_message(self, title, message):
        """
        Zeigt eine Platzhalter-Nachricht an, bis die entsprechende Ansicht implementiert ist
        """
        placeholder = QWidget()
        layout = QVBoxLayout(placeholder)
        
        title_label = QLabel(title)
        font = QFont()
        font.setPointSize(20)
        font.setBold(True)
        title_label.setFont(font)
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        message_label = QLabel(message)
        message_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        back_button = QPushButton("Zurück zur Startseite")
        back_button.clicked.connect(self.show_home)
        
        layout.addWidget(title_label)
        layout.addWidget(message_label)
        layout.addWidget(back_button, 0, Qt.AlignmentFlag.AlignCenter)
        
        # Entferne alle vorherigen Widgets aus dem Stack und füge das neue hinzu
        while self.view_stack.count() > 0:
            self.view_stack.removeWidget(self.view_stack.widget(0))
        
        self.view_stack.addWidget(placeholder)
        self.view_stack.show()
    
    def initialize_nfc(self):
        """
        Initialisiert den NFC-Treiber
        """
        try:
            self.statusBar.showMessage("NFC wird initialisiert...")
            self.nfc_status_label.setText("NFC-Status: Initialisiere...")
            self.nfc_status_label.setStyleSheet("color: orange; font-weight: bold;")
            
            # NFC-Manager initialisieren
            success = self.nfc_manager.initialize()
            
            if success:
                device_info = self.nfc_manager.get_device_info()
                device_name = device_info.get('id', 'Unbekanntes Gerät') if device_info else 'Unbekanntes Gerät'
                port = device_info.get('port', 'Unbekannt') if device_info else 'Unbekannt'
                
                self.statusBar.showMessage(f"NFC erfolgreich initialisiert - {device_name} an {port}")
                self.nfc_status_label.setText(f"NFC-Status: Verbunden - {device_name}")
                self.nfc_status_label.setStyleSheet("color: green; font-weight: bold;")
                
                # Erfolgs-Nachricht anzeigen
                QMessageBox.information(
                    self,
                    "NFC Initialisierung",
                    f"NFC-Treiber erfolgreich initialisiert!\n\n"
                    f"Gerät: {device_name}\n"
                    f"Port: {port}\n"
                    f"Status: Verbunden"
                )
            else:
                error_msg = self.nfc_manager.get_last_error() or "Unbekannter Fehler"
                self.statusBar.showMessage(f"NFC-Initialisierung fehlgeschlagen: {error_msg}")
                self.nfc_status_label.setText("NFC-Status: Initialisierung fehlgeschlagen")
                self.nfc_status_label.setStyleSheet("color: red; font-weight: bold;")
                
                # Fehler-Nachricht anzeigen
                QMessageBox.warning(
                    self,
                    "NFC Initialisierung fehlgeschlagen",
                    f"Der NFC-Treiber konnte nicht initialisiert werden.\n\n"
                    f"Fehler: {error_msg}\n\n"
                    f"Stellen Sie sicher, dass ein unterstütztes NFC-Gerät angeschlossen ist."
                )
                
        except Exception as e:
            error_msg = f"Unerwarteter Fehler: {str(e)}"
            self.statusBar.showMessage(f"NFC-Initialisierung fehlgeschlagen: {error_msg}")
            self.nfc_status_label.setText("NFC-Status: Fehler")
            self.nfc_status_label.setStyleSheet("color: red; font-weight: bold;")
            
            QMessageBox.critical(
                self,
                "Kritischer Fehler",
                f"Ein unerwarteter Fehler ist aufgetreten:\n\n{error_msg}"
            )
    
    def detect_nfc_devices(self):
        """
        Erkennt verfügbare NFC-Geräte und zeigt sie an
        """
        try:
            devices = self.nfc_manager.get_detected_devices()
            
            if devices:
                device_list = "\n".join([
                    f"• {device['description']} ({device['port']})"
                    for device in devices
                ])
                
                QMessageBox.information(
                    self,
                    "Erkannte NFC-Geräte",
                    f"Folgende NFC-Geräte wurden erkannt:\n\n{device_list}\n\n"
                    f"Verwenden Sie 'NFC initialisieren' um eine Verbindung herzustellen."
                )
            else:
                QMessageBox.warning(
                    self,
                    "Keine Geräte gefunden",
                    "Es wurden keine unterstützten NFC-Geräte gefunden.\n\n"
                    "Stellen Sie sicher, dass:\n"
                    "• Ein NFC-Gerät angeschlossen ist\n"
                    "• Die entsprechenden Treiber installiert sind\n"
                    "• Das Gerät nicht von einer anderen Anwendung verwendet wird"
                )
                
        except Exception as e:
            QMessageBox.critical(
                self,
                "Fehler bei Geräteerkennung",
                f"Fehler bei der Erkennung von NFC-Geräten:\n\n{str(e)}"
            )
