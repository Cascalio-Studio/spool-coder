"""
Hauptfenster der Anwendung
"""

from PyQt6.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QPushButton,
                           QLabel, QStackedWidget, QHBoxLayout, QMenuBar, QMenu, QStatusBar,
                           QMessageBox, QFileDialog, QApplication, QGridLayout, QSpacerItem, 
                           QSizePolicy, QScrollArea)
from PyQt6.QtCore import Qt, pyqtSignal, QSettings, QTimer
from PyQt6.QtGui import QIcon, QFont, QAction, QKeySequence, QPalette, QColor, QShortcut

from ..components.modern_card import ModernCard
from src.ui.dialogs import NFCDeviceDialog

class MainWindow(QMainWindow):
    """
    Hauptfenster der Spool-Coder Anwendung
    """
    
    def __init__(self):
        super().__init__()
        
        # Grundlegende Fenstereinstellungen
        self.setWindowTitle("Spool-Coder - Bambulab NFC Tool")
        self.setMinimumSize(700, 550)  # Größere Mindestgröße für bessere Darstellung
        
        # Griffain-inspiriertes dunkles Farbschema anwenden
        self.apply_dark_theme()
        
        # Responsive Layout Variablen
        self.current_layout_mode = "desktop"  # desktop, tablet, mobile
        self.cards_layout = None
        self.resize_timer = QTimer()
        self.resize_timer.setSingleShot(True)
        self.resize_timer.timeout.connect(self.update_responsive_layout)
        
        # Lade gespeicherte Fenstergeometrie
        self.load_settings()
        
        # Status-Bar erstellen
        self.statusBar = QStatusBar()
        self.setStatusBar(self.statusBar)
        
        # NFC-Status-Indikator zur Statusleiste hinzufügen
        self.nfc_status_label = QLabel("🔴 NFC: Nicht verbunden")
        self.nfc_status_label.setStyleSheet("""
            QLabel {
                color: #68658A;
                font-weight: bold;
                padding: 4px 8px;
                border-radius: 4px;
                background-color: #2A2A2F;
            }
        """)
        self.statusBar.addPermanentWidget(self.nfc_status_label)
        
        # Quick-Actions zur Statusleiste hinzufügen
        self.quick_read_button = QPushButton("⚡ Schnell lesen")
        self.quick_read_button.setToolTip("Startet sofort das Auslesen einer NFC-Spule")
        self.quick_read_button.clicked.connect(self.quick_read_action)
        self.quick_read_button.setMaximumHeight(24)
        self.statusBar.addPermanentWidget(self.quick_read_button)
        
        self.statusBar.showMessage("Bereit")
        
        # Menü-Bar erstellen
        self.setup_menu()
        
        # Zentrales Widget mit Scroll-Unterstützung
        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        self.scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        self.setCentralWidget(self.scroll_area)
        
        self.central_widget = QWidget()
        self.scroll_area.setWidget(self.central_widget)
        
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
        
        # Tastaturkürzel einrichten
        self.setup_keyboard_shortcuts()
        
        # Stack für verschiedene Ansichten
        self.view_stack = QStackedWidget()
        self.main_layout.addWidget(self.view_stack)
        
        # Startseite als Standard setzen
        self.view_stack.setCurrentIndex(0)
        self.view_stack.hide()
    
    def apply_dark_theme(self):
        """
        Wendet das Griffain-inspirierte dunkle Farbschema an
        """
        self.setStyleSheet("""
            QMainWindow {
                background-color: #1A191E;
                color: #FEFDFF;
            }
            QMenuBar {
                background-color: #2A2A2F;
                color: #FEFDFF;
                border-bottom: 1px solid #404040;
                padding: 4px;
            }
            QMenuBar::item {
                background-color: transparent;
                padding: 8px 12px;
                border-radius: 4px;
            }
            QMenuBar::item:selected {
                background-color: #5EFB7B;
                color: #1A191E;
            }
            QMenu {
                background-color: #2A2A2F;
                color: #FEFDFF;
                border: 1px solid #404040;
                border-radius: 8px;
                padding: 4px;
            }
            QMenu::item {
                padding: 8px 20px;
                border-radius: 4px;
            }
            QMenu::item:selected {
                background-color: #5EFB7B;
                color: #1A191E;
            }
            QMenu::separator {
                height: 1px;
                background-color: #404040;
                margin: 4px 8px;
            }
            QStatusBar {
                background-color: #2A2A2F;
                color: #68658A;
                border-top: 1px solid #404040;
            }
            QLabel {
                color: #FEFDFF;
            }
            QScrollArea {
                background-color: #1A191E;
                border: none;
            }
            QPushButton {
                background-color: #2A2A2F;
                color: #FEFDFF;
                border: 1px solid #404040;
                border-radius: 6px;
                padding: 8px 16px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #5EFB7B;
                color: #1A191E;
                border-color: #5EFB7B;
            }
            QPushButton:pressed {
                background-color: #4AE65C;
            }
        """)
    
    def load_settings(self):
        """Lädt gespeicherte Einstellungen"""
        settings = QSettings()
        
        # Fenstergeometrie wiederherstellen
        geometry = settings.value("geometry")
        if geometry:
            self.restoreGeometry(geometry)
        
        # Fensterstatus wiederherstellen
        window_state = settings.value("windowState")
        if window_state:
            self.restoreState(window_state)
    
    def setup_menu(self):
        """
        Erstellt die erweiterte Menüleiste
        """
        self.menuBar = QMenuBar(self)
        self.setMenuBar(self.menuBar)
        
        # Datei-Menü
        file_menu = QMenu("&Datei", self)
        self.menuBar.addMenu(file_menu)
        
        # Neue Spule erstellen
        new_action = QAction("&Neue Spule erstellen...", self)
        new_action.setShortcut(QKeySequence("Ctrl+N"))
        new_action.setStatusTip("Erstelle eine neue NFC-Spule mit benutzerdefinierten Daten")
        new_action.triggered.connect(self.show_write_view)
        file_menu.addAction(new_action)
        
        # Spule auslesen
        read_action = QAction("Spule &auslesen...", self)
        read_action.setShortcut(QKeySequence("Ctrl+R"))
        read_action.setStatusTip("Lese eine vorhandene Bambu Lab NFC-Spule aus")
        read_action.triggered.connect(self.show_read_view)
        file_menu.addAction(read_action)
        
        file_menu.addSeparator()
        
        # Einstellungen exportieren/importieren
        export_action = QAction("Einstellungen &exportieren...", self)
        export_action.setStatusTip("Exportiere Anwendungseinstellungen in eine Datei")
        export_action.triggered.connect(self.export_settings)
        file_menu.addAction(export_action)
        
        import_action = QAction("Einstellungen &importieren...", self)
        import_action.setStatusTip("Importiere Anwendungseinstellungen aus einer Datei")
        import_action.triggered.connect(self.import_settings)
        file_menu.addAction(import_action)
        
        file_menu.addSeparator()
        
        # Beenden
        exit_action = QAction("&Beenden", self)
        exit_action.setShortcut(QKeySequence("Ctrl+Q"))
        exit_action.setStatusTip("Anwendung beenden")
        exit_action.triggered.connect(self.close)
        file_menu.addAction(exit_action)
        
        # Bearbeiten-Menü
        edit_menu = QMenu("&Bearbeiten", self)
        self.menuBar.addMenu(edit_menu)
        
        # Demo-Daten laden
        demo_action = QAction("&Demo-Daten laden", self)
        demo_action.setShortcut(QKeySequence("Ctrl+D"))
        demo_action.setStatusTip("Lade Beispiel-Filamentdaten für Tests")
        demo_action.triggered.connect(self.load_demo_data)
        edit_menu.addAction(demo_action)
        
        edit_menu.addSeparator()
        
        # Einstellungen
        settings_action = QAction("&Einstellungen...", self)
        settings_action.setShortcut(QKeySequence("Ctrl+,"))
        settings_action.setStatusTip("Anwendungseinstellungen öffnen")
        settings_action.triggered.connect(self.show_settings)
        edit_menu.addAction(settings_action)
        
        # Werkzeuge-Menü
        tools_menu = QMenu("&Werkzeuge", self)
        self.menuBar.addMenu(tools_menu)
        
        # NFC-Gerät verwalten
        nfc_device_action = QAction("&NFC-Gerät verwalten...", self)
        nfc_device_action.setShortcut(QKeySequence("Ctrl+Shift+N"))
        nfc_device_action.setStatusTip("NFC-Gerät konfigurieren und testen")
        nfc_device_action.triggered.connect(self.show_nfc_device_dialog)
        tools_menu.addAction(nfc_device_action)
        
        # Algorithmus testen
        test_algorithm_action = QAction("Bambu &Algorithmus testen...", self)
        test_algorithm_action.setShortcut(QKeySequence("Ctrl+T"))
        test_algorithm_action.setStatusTip("Teste den Bambu Lab Verschlüsselungsalgorithmus")
        test_algorithm_action.triggered.connect(self.show_demo_view)
        tools_menu.addAction(test_algorithm_action)
        
        tools_menu.addSeparator()
        
        # Log anzeigen
        log_action = QAction("&Log anzeigen...", self)
        log_action.setStatusTip("Zeige Anwendungs-Logs und Debug-Informationen")
        log_action.triggered.connect(self.show_log_dialog)
        tools_menu.addAction(log_action)
        
        # Ansicht-Menü
        view_menu = QMenu("&Ansicht", self)
        self.menuBar.addMenu(view_menu)
        
        # Startseite
        home_action = QAction("&Startseite", self)
        home_action.setShortcut(QKeySequence("Alt+Home"))
        home_action.setStatusTip("Zur Hauptseite zurückkehren")
        home_action.triggered.connect(self.show_home)
        view_menu.addAction(home_action)
        
        view_menu.addSeparator()
        
        # Vollbild
        fullscreen_action = QAction("&Vollbild", self)
        fullscreen_action.setShortcut(QKeySequence("F11"))
        fullscreen_action.setStatusTip("Vollbildmodus ein/ausschalten")
        fullscreen_action.setCheckable(True)
        fullscreen_action.triggered.connect(self.toggle_fullscreen)
        view_menu.addAction(fullscreen_action)
        self.fullscreen_action = fullscreen_action
        
        # Statusleiste anzeigen
        statusbar_action = QAction("&Statusleiste anzeigen", self)
        statusbar_action.setStatusTip("Statusleiste ein/ausblenden")
        statusbar_action.setCheckable(True)
        statusbar_action.setChecked(True)
        statusbar_action.triggered.connect(self.toggle_statusbar)
        view_menu.addAction(statusbar_action)
        
        # Hilfe-Menü
        help_menu = QMenu("&Hilfe", self)
        self.menuBar.addMenu(help_menu)
        
        # Benutzerhandbuch
        manual_action = QAction("&Benutzerhandbuch", self)
        manual_action.setShortcut(QKeySequence("F1"))
        manual_action.setStatusTip("Öffne das Benutzerhandbuch")
        manual_action.triggered.connect(self.show_manual)
        help_menu.addAction(manual_action)
        
        # Bambu Lab Dokumentation
        bambu_docs_action = QAction("&Bambu Lab NFC Dokumentation", self)
        bambu_docs_action.setStatusTip("Öffne die technische Dokumentation zum Bambu Lab NFC-Format")
        bambu_docs_action.triggered.connect(self.show_bambu_docs)
        help_menu.addAction(bambu_docs_action)
        
        help_menu.addSeparator()
        
        # GitHub Repository
        github_action = QAction("&GitHub Repository", self)
        github_action.setStatusTip("Öffne das GitHub Repository des Projekts")
        github_action.triggered.connect(self.open_github)
        help_menu.addAction(github_action)
        
        # Bug Report
        bug_action = QAction("&Bug melden...", self)
        bug_action.setStatusTip("Melde einen Fehler oder schlage Verbesserungen vor")
        bug_action.triggered.connect(self.report_bug)
        help_menu.addAction(bug_action)
        
        help_menu.addSeparator()
        
        # Info
        info_action = QAction("&Über Spool-Coder...", self)
        info_action.setStatusTip("Informationen über diese Anwendung")
        info_action.triggered.connect(self.show_info)
        help_menu.addAction(info_action)
    
    def create_menu_buttons(self):
        """
        Erstellt das moderne Card-basierte Hauptmenü mit responsivem Design
        """
        # Grid-Layout für die Cards erstellen
        self.cards_layout = QGridLayout()
        
        # Card 1: Spule auslesen (Primäre Aktion)
        self.read_card = ModernCard(
            title="Spule auslesen",
            description="Lese Informationen von einer\nexistierenden NFC-Spule",
            icon_text="📖",
            primary=True
        )
        self.read_card.clicked.connect(self.show_read_view)
        self.read_card.setToolTip(
            "<b>Spule auslesen</b><br/>"
            "• Liest alle Daten von einer Bambu Lab NFC-Spule<br/>"
            "• Zeigt Filament-Typ, Farbe und Gewicht an<br/>"
            "• Entschlüsselt automatisch die Tag-Informationen<br/>"
            "• Tastenkürzel: Strg+R"
        )
        
        # Card 2: Spule programmieren (Primäre Aktion)
        self.write_card = ModernCard(
            title="Spule programmieren", 
            description="Schreibe neue Filament-Daten\nauf eine NFC-Spule",
            icon_text="✏️",
            primary=True
        )
        self.write_card.clicked.connect(self.show_write_view)
        self.write_card.setToolTip(
            "<b>Spule programmieren</b><br/>"
            "• Schreibt neue Filament-Informationen auf eine NFC-Spule<br/>"
            "• Unterstützt alle Bambu Lab Filament-Typen<br/>"
            "• Automatische Verschlüsselung der Daten<br/>"
            "• Tastenkürzel: Strg+N"
        )
        
        # Card 3: Demo & Test (Sekundäre Aktion)
        self.demo_card = ModernCard(
            title="Demo & Test",
            description="Teste den NFC-Algorithmus\nmit Beispieldaten",
            icon_text="🧪",
            primary=False
        )
        self.demo_card.clicked.connect(self.show_demo_view)
        self.demo_card.setToolTip(
            "<b>Demo & Test</b><br/>"
            "• Testet den Bambu Lab Verschlüsselungsalgorithmus<br/>"
            "• Funktioniert auch ohne physische NFC-Hardware<br/>"
            "• Zeigt Verschlüsselung/Entschlüsselung in Echtzeit<br/>"
            "• Tastenkürzel: Strg+T"
        )
        
        # Card 4: Info & Hilfe (Sekundäre Aktion)
        self.info_card = ModernCard(
            title="Info & Hilfe",
            description="Über diese Anwendung\nund Dokumentation",
            icon_text="ℹ️",
            primary=False
        )
        self.info_card.clicked.connect(self.show_info)
        self.info_card.setToolTip(
            "<b>Info & Hilfe</b><br/>"
            "• Informationen über die Anwendung<br/>"
            "• Benutzerhandbuch und Dokumentation<br/>"
            "• GitHub Repository und Bug-Berichte<br/>"
            "• Tastenkürzel: F1"
        )
        
        # Jetzt erst das responsive Layout anwenden, nachdem die Cards erstellt wurden
        self.apply_responsive_layout()
        
        # Cards zum Layout hinzufügen
        self.menu_layout.addLayout(self.cards_layout)
        
        # Spacer hinzufügen für bessere Verteilung
        spacer = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)
        self.menu_layout.addItem(spacer)
    
    def update_responsive_layout(self):
        """
        Aktualisiert das Layout basierend auf der aktuellen Fenstergröße
        """
        if not self.cards_layout:
            return
            
        # Bestimme Layout-Modus basierend auf Fenstergröße
        width = self.width()
        new_mode = self.determine_layout_mode(width)
        
        # Nur aktualisieren wenn sich der Modus geändert hat
        if new_mode != self.current_layout_mode:
            self.current_layout_mode = new_mode
            self.apply_responsive_layout()
    
    def determine_layout_mode(self, width):
        """
        Bestimmt den Layout-Modus basierend auf der Fensterbreite
        """
        if width < 768:  # Mobile
            return "mobile"
        elif width < 1024:  # Tablet
            return "tablet"
        else:  # Desktop
            return "desktop"
    
    def apply_responsive_layout(self):
        """
        Wendet das responsive Layout basierend auf dem aktuellen Modus an
        """
        if not hasattr(self, 'read_card') or not self.read_card:
            return
            
        # Bestimme aktuellen Layout-Modus
        width = self.width()
        self.current_layout_mode = self.determine_layout_mode(width)
        
        # Entferne alle Widgets aus dem Layout (nur wenn bereits hinzugefügt)
        for i in reversed(range(self.cards_layout.count())):
            item = self.cards_layout.itemAt(i)
            if item and item.widget():
                item.widget().setParent(None)
        
        # Konfiguriere Layout basierend auf Modus
        if self.current_layout_mode == "mobile":
            # Mobile: 1 Spalte (vertikal gestapelt)
            self.cards_layout.setSpacing(20)
            self.cards_layout.setContentsMargins(25, 20, 25, 20)
            
            self.cards_layout.addWidget(self.read_card, 0, 0)
            self.cards_layout.addWidget(self.write_card, 1, 0)
            self.cards_layout.addWidget(self.demo_card, 2, 0)
            self.cards_layout.addWidget(self.info_card, 3, 0)
            
            # Kompakte Schriftgrößen für Mobile
            self.update_card_sizes("compact")
            
        elif self.current_layout_mode == "tablet":
            # Tablet: 2 Spalten
            self.cards_layout.setSpacing(25)
            self.cards_layout.setContentsMargins(35, 25, 35, 25)
            
            self.cards_layout.addWidget(self.read_card, 0, 0)
            self.cards_layout.addWidget(self.write_card, 0, 1)
            self.cards_layout.addWidget(self.demo_card, 1, 0)
            self.cards_layout.addWidget(self.info_card, 1, 1)
            
            # Mittlere Schriftgrößen für Tablet
            self.update_card_sizes("medium")
            
        else:  # Desktop
            # Desktop: 2x2 Grid mit mehr Abstand
            self.cards_layout.setSpacing(30)
            self.cards_layout.setContentsMargins(50, 30, 50, 30)
            
            self.cards_layout.addWidget(self.read_card, 0, 0)
            self.cards_layout.addWidget(self.write_card, 0, 1)
            self.cards_layout.addWidget(self.demo_card, 1, 0)
            self.cards_layout.addWidget(self.info_card, 1, 1)
            
            # Normale Schriftgrößen für Desktop
            self.update_card_sizes("normal")
    
    def update_card_sizes(self, size_mode):
        """
        Aktualisiert die Kartengröße basierend auf dem Layout-Modus
        """
        cards = [self.read_card, self.write_card, self.demo_card, self.info_card]
        
        for card in cards:
            # Verwende die neue responsive Methode der ModernCard
            card.set_responsive_size(size_mode)
            
            if size_mode == "compact":
                # Mobile: kompakte Größen mit mehr Höhe
                card.setMinimumSize(320, 180)
                card.setMaximumSize(450, 220)
            elif size_mode == "medium":
                # Tablet: mittlere Größen mit mehr Höhe
                card.setMinimumSize(280, 200)
                card.setMaximumSize(380, 240)
            else:  # normal (Desktop)
                # Desktop: normale Größen mit mehr Höhe
                card.setMinimumSize(300, 220)
                card.setMaximumSize(420, 280)
    
    def update_welcome_text_responsive(self):
        """
        Passt den Willkommenstext an die Bildschirmgröße an
        """
        if self.current_layout_mode == "mobile":
            # Mobile: kleinere Schrift
            font = QFont()
            font.setPointSize(18)
            font.setBold(True)
            self.welcome_label.setFont(font)
            self.welcome_label.setText("Spool-Coder")
            
        elif self.current_layout_mode == "tablet":
            # Tablet: mittlere Schrift
            font = QFont()
            font.setPointSize(20)
            font.setBold(True)
            self.welcome_label.setFont(font)
            self.welcome_label.setText("Willkommen beim Spool-Coder!")
            
        else:  # Desktop
            # Desktop: normale Schrift
            font = QFont()
            font.setPointSize(24)
            font.setBold(True)
            self.welcome_label.setFont(font)
            self.welcome_label.setText("Willkommen beim Spool-Coder!")
    
    def resizeEvent(self, event):
        """
        Wird bei Größenänderungen des Fensters aufgerufen
        """
        super().resizeEvent(event)
        
        # Verwende Timer um häufige Aufrufe zu vermeiden
        self.resize_timer.stop()
        self.resize_timer.start(150)  # 150ms Verzögerung
        
        # Aktualisiere Willkommenstext sofort für bessere Responsivität
        self.update_welcome_text_responsive()
    
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

    # Neue Menü-Methoden
    def export_settings(self):
        """Exportiert Anwendungseinstellungen"""
        file_path, _ = QFileDialog.getSaveFileName(
            self,
            "Einstellungen exportieren",
            "spool_coder_settings.ini",
            "INI Dateien (*.ini);;Alle Dateien (*)"
        )
        
        if file_path:
            try:
                settings = QSettings()
                # Erstelle eine neue QSettings-Instanz für die Export-Datei
                export_settings = QSettings(file_path, QSettings.Format.IniFormat)
                
                # Kopiere alle Einstellungen
                for key in settings.allKeys():
                    export_settings.setValue(key, settings.value(key))
                
                export_settings.sync()
                QMessageBox.information(self, "Export erfolgreich", 
                                      f"Einstellungen wurden nach {file_path} exportiert.")
                self.statusBar.showMessage("Einstellungen exportiert", 3000)
            except Exception as e:
                QMessageBox.warning(self, "Export fehlgeschlagen", 
                                  f"Fehler beim Exportieren: {str(e)}")

    def import_settings(self):
        """Importiert Anwendungseinstellungen"""
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "Einstellungen importieren",
            "",
            "INI Dateien (*.ini);;Alle Dateien (*)"
        )
        
        if file_path:
            reply = QMessageBox.question(
                self,
                "Einstellungen importieren",
                "Möchten Sie die aktuellen Einstellungen durch die importierten ersetzen?\n"
                "Diese Aktion kann nicht rückgängig gemacht werden.",
                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
                QMessageBox.StandardButton.No
            )
            
            if reply == QMessageBox.StandardButton.Yes:
                try:
                    import_settings = QSettings(file_path, QSettings.Format.IniFormat)
                    current_settings = QSettings()
                    
                    # Importiere alle Einstellungen
                    for key in import_settings.allKeys():
                        current_settings.setValue(key, import_settings.value(key))
                    
                    current_settings.sync()
                    QMessageBox.information(self, "Import erfolgreich", 
                                          "Einstellungen wurden erfolgreich importiert.\n"
                                          "Starten Sie die Anwendung neu, um alle Änderungen zu übernehmen.")
                    self.statusBar.showMessage("Einstellungen importiert", 3000)
                except Exception as e:
                    QMessageBox.warning(self, "Import fehlgeschlagen", 
                                      f"Fehler beim Importieren: {str(e)}")

    def load_demo_data(self):
        """Lädt Demo-Daten für Tests"""
        QMessageBox.information(
            self,
            "Demo-Daten",
            "Demo-Daten werden geladen...\n\n"
            "Dies würde normalerweise vordefinierte Filament-Profile laden:\n"
            "• Bambu Lab PLA Basic (Verschiedene Farben)\n"
            "• Bambu Lab PETG-CF\n"
            "• Bambu Lab ABS\n"
            "• Generische Profile für Tests"
        )
        self.statusBar.showMessage("Demo-Daten geladen", 3000)

    def show_nfc_device_dialog(self):
        """Zeigt den NFC-Gerät Dialog"""
        dialog = NFCDeviceDialog(self)
        dialog.exec()

    def show_log_dialog(self):
        """Zeigt die Log-Anzeige"""
        QMessageBox.information(
            self,
            "Log-Anzeige",
            "Hier würden normalerweise die Anwendungs-Logs angezeigt werden:\n\n"
            "• Debug-Nachrichten\n"
            "• NFC-Kommunikation\n"
            "• Verschlüsselung/Entschlüsselung\n"
            "• Fehler und Warnungen\n"
            "• Performance-Metriken"
        )

    def toggle_fullscreen(self):
        """Schaltet Vollbildmodus ein/aus"""
        if self.isFullScreen():
            self.showNormal()
            self.fullscreen_action.setChecked(False)
            self.statusBar.showMessage("Vollbildmodus deaktiviert", 2000)
        else:
            self.showFullScreen()
            self.fullscreen_action.setChecked(True)
            self.statusBar.showMessage("Vollbildmodus aktiviert - Drücken Sie F11 zum Beenden", 3000)

    def toggle_statusbar(self):
        """Schaltet Statusleiste ein/aus"""
        if self.statusBar.isVisible():
            self.statusBar.hide()
        else:
            self.statusBar.show()
            self.statusBar.showMessage("Statusleiste aktiviert", 2000)

    def show_manual(self):
        """Öffnet das Benutzerhandbuch"""
        QMessageBox.information(
            self,
            "Benutzerhandbuch",
            "Das vollständige Benutzerhandbuch finden Sie in:\n\n"
            "• docs/user_guide.md\n"
            "• docs/installation.md\n"
            "• docs/developer_guide.md\n\n"
            "Online: https://github.com/Cascalio-Studio/spool-coder/docs"
        )

    def show_bambu_docs(self):
        """Öffnet die Bambu Lab Dokumentation"""
        QMessageBox.information(
            self,
            "Bambu Lab NFC Dokumentation",
            "Technische Dokumentation zum Bambu Lab NFC-Format:\n\n"
            "• docs/bambu_algorithm.md\n"
            "• docs/nfc_protocol.md\n"
            "• vendor/bambu-research/README.md\n\n"
            "Enthält Informationen über:\n"
            "• NFC-Tag Struktur\n"
            "• Verschlüsselungsalgorithmus\n"
            "• Datenformat und Felder\n"
            "• Reverse Engineering Erkenntnisse"
        )

    def open_github(self):
        """Öffnet das GitHub Repository"""
        import webbrowser
        try:
            webbrowser.open("https://github.com/Cascalio-Studio/spool-coder")
            self.statusBar.showMessage("GitHub Repository geöffnet", 3000)
        except Exception as e:
            QMessageBox.warning(self, "Fehler", f"Konnte GitHub nicht öffnen: {str(e)}")

    def report_bug(self):
        """Öffnet Bug-Report Dialog"""
        reply = QMessageBox.question(
            self,
            "Bug melden",
            "Möchten Sie einen Bug melden oder eine Verbesserung vorschlagen?\n\n"
            "Sie werden zum GitHub Issues-Bereich weitergeleitet.",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
            QMessageBox.StandardButton.Yes
        )
        
        if reply == QMessageBox.StandardButton.Yes:
            import webbrowser
            try:
                webbrowser.open("https://github.com/Cascalio-Studio/spool-coder/issues/new")
                self.statusBar.showMessage("GitHub Issues geöffnet", 3000)
            except Exception as e:
                QMessageBox.warning(self, "Fehler", f"Konnte GitHub nicht öffnen: {str(e)}")

    def closeEvent(self, event):
        """Wird beim Schließen der Anwendung aufgerufen"""
        reply = QMessageBox.question(
            self,
            "Anwendung beenden",
            "Möchten Sie Spool-Coder wirklich beenden?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
            QMessageBox.StandardButton.No
        )
        
        if reply == QMessageBox.StandardButton.Yes:
            # Einstellungen speichern
            settings = QSettings()
            settings.setValue("geometry", self.saveGeometry())
            settings.setValue("windowState", self.saveState())
            event.accept()
        else:
            event.ignore()
    
    # Quick-Actions und NFC-Status-Methoden
    def quick_read_action(self):
        """Schnell-Lese-Aktion für häufige Nutzung"""
        self.show_read_view()
        self.statusBar.showMessage("Schnell-Lesen gestartet...", 3000)
    
    def update_nfc_status(self, connected=False, device_name=""):
        """Aktualisiert den NFC-Status-Indikator"""
        if connected:
            self.nfc_status_label.setText(f"🟢 NFC: {device_name or 'Verbunden'}")
            self.nfc_status_label.setStyleSheet("""
                QLabel {
                    color: #5EFB7B;
                    font-weight: bold;
                    padding: 4px 8px;
                    border-radius: 4px;
                    background-color: #2A2A2F;
                }
            """)
        else:
            self.nfc_status_label.setText("🔴 NFC: Nicht verbunden")
            self.nfc_status_label.setStyleSheet("""
                QLabel {
                    color: #68658A;
                    font-weight: bold;
                    padding: 4px 8px;
                    border-radius: 4px;
                    background-color: #2A2A2F;
                }
            """)
    
    def setup_keyboard_shortcuts(self):
        """Richtet globale Tastaturkürzel ein"""
        # Tastaturkürzel für Karten-Navigation
        
        # Tab-Navigation zwischen Karten
        tab_shortcut = QShortcut(QKeySequence("Tab"), self)
        tab_shortcut.activated.connect(self.focus_next_card)
        
        # Shift+Tab für rückwärts Navigation
        shift_tab_shortcut = QShortcut(QKeySequence("Shift+Tab"), self)
        shift_tab_shortcut.activated.connect(self.focus_previous_card)
        
        # Quick-Actions
        quick_read_shortcut = QShortcut(QKeySequence("Ctrl+Shift+R"), self)
        quick_read_shortcut.activated.connect(self.quick_read_action)
    
    def focus_next_card(self):
        """Setzt den Fokus auf die nächste Karte"""
        cards = [self.read_card, self.write_card, self.demo_card, self.info_card]
        current_focus = self.focusWidget()
        
        if current_focus in cards:
            current_index = cards.index(current_focus)
            next_index = (current_index + 1) % len(cards)
            cards[next_index].setFocus()
        else:
            cards[0].setFocus()
    
    def focus_previous_card(self):
        """Setzt den Fokus auf die vorherige Karte"""
        cards = [self.read_card, self.write_card, self.demo_card, self.info_card]
        current_focus = self.focusWidget()
        
        if current_focus in cards:
            current_index = cards.index(current_focus)
            prev_index = (current_index - 1) % len(cards)
            cards[prev_index].setFocus()
        else:
            cards[-1].setFocus()
