"""
Hauptfenster der Anwendung
"""

from PyQt6.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QPushButton,
                           QLabel, QStackedWidget, QHBoxLayout, QMenuBar, QMenu, QStatusBar)
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QIcon, QFont, QAction

from src.ui.dialogs import NFCDeviceDialog

class MainWindow(QMainWindow):
    """
    Hauptfenster der Spool-Coder Anwendung
    """
    
    def __init__(self):
        super().__init__()
        
        # Grundlegende Fenstereinstellungen
        self.setWindowTitle("Spool-Coder - Bambulab NFC Tool")
        self.setMinimumSize(800, 600)
        
        # Status-Bar erstellen
        self.statusBar = QStatusBar()
        self.setStatusBar(self.statusBar)
        self.statusBar.showMessage("Bereit")
        
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
        
        # Demo NFC Algorithm
        self.demo_button = QPushButton("NFC Algorithmus Demo")
        self.demo_button.setStyleSheet(button_style)
        self.demo_button.clicked.connect(self.show_demo_view)
        self.menu_layout.addWidget(self.demo_button, 0, Qt.AlignmentFlag.AlignCenter)
        
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
        from src.ui.views.read_view import ReadView
        
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
        from src.ui.views.write_view import WriteView
        
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
        from src.ui.views.info_view import InfoView
        
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
    
    def show_demo_view(self):
        """
        Zeigt die Demo-Ansicht für den NFC-Algorithmus an
        """
        self.menu_container.hide()
        self.welcome_label.hide()
        self.description_label.hide()
        
        # Hier wird die DemoView zum view_stack hinzugefügt und angezeigt
        from src.ui.views.demo_view import DemoView
        
        # Entferne alle vorherigen Widgets aus dem Stack
        while self.view_stack.count() > 0:
            self.view_stack.removeWidget(self.view_stack.widget(0))
        
        demo_view = DemoView(self)
        self.view_stack.addWidget(demo_view)
        self.view_stack.show()
        self.statusBar.showMessage("NFC Algorithmus Demo")
