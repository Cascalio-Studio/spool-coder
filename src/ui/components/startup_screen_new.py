"""
Startup Screen Component - Beautiful loading screen with logo and progress indication
"""

import sys
import os
from typing import Callable, Optional
from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
                           QProgressBar, QFrame, QApplication)
from PyQt6.QtCore import Qt, QTimer, QThread, pyqtSignal, QPropertyAnimation, QEasingCurve
from PyQt6.QtGui import QFont, QPalette, QPixmap, QPainter, QBrush, QColor, QLinearGradient

# Try to import QSvgRenderer, but fall back gracefully if not available
try:
    from PyQt6.QtSvg import QSvgRenderer
    SVG_AVAILABLE = True
except ImportError:
    SVG_AVAILABLE = False
    QSvgRenderer = None

class StartupInitializationThread(QThread):
    """
    Background thread for application initialization tasks
    """
    progress_updated = pyqtSignal(int, str)  # progress percentage, status message
    initialization_complete = pyqtSignal()
    
    def __init__(self, initialization_tasks: list = None):
        super().__init__()
        self.initialization_tasks = initialization_tasks or []
        self.total_tasks = len(self.initialization_tasks)
    
    def run(self):
        """Run initialization tasks in background"""
        try:
            for i, (task_name, task_func) in enumerate(self.initialization_tasks):
                # Update progress
                progress = int((i / self.total_tasks) * 100)
                self.progress_updated.emit(progress, f"Initializing {task_name}...")
                
                # Execute the task
                if callable(task_func):
                    task_func()
                else:
                    # Simulate task execution time
                    self.msleep(200)
                
                # Brief pause for visual feedback
                self.msleep(100)
            
            # Complete
            self.progress_updated.emit(100, "Ready!")
            self.msleep(300)  # Brief pause to show completion
            self.initialization_complete.emit()
            
        except Exception as e:
            self.progress_updated.emit(100, f"Error: {str(e)}")
            self.msleep(1000)
            self.initialization_complete.emit()

class AnimatedProgressBar(QProgressBar):
    """
    Custom animated progress bar with modern styling
    """
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setRange(0, 100)
        self.setValue(0)
        self.setTextVisible(False)
        self.setFixedHeight(8)
        
        # Apply modern styling
        self.setStyleSheet("""
            QProgressBar {
                border: none;
                border-radius: 4px;
                background-color: rgba(255, 255, 255, 0.1);
            }
            QProgressBar::chunk {
                border-radius: 4px;
                background: qlineargradient(x1: 0, y1: 0, x2: 1, y2: 0,
                                          stop: 0 #4FC3F7, stop: 1 #29B6F6);
            }
        """)

class LogoWidget(QLabel):
    """
    Logo widget with fade-in animation
    """
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.setFixedSize(120, 120)
        
        # Create a placeholder logo (you can replace this with an actual logo file)
        self.create_logo()
        
        # Set up fade-in animation
        self.opacity_animation = QPropertyAnimation(self, b"windowOpacity")
        self.opacity_animation.setDuration(1000)
        self.opacity_animation.setStartValue(0.0)
        self.opacity_animation.setEndValue(1.0)
        self.opacity_animation.setEasingCurve(QEasingCurve.Type.InOutQuad)
    
    def create_logo(self):
        """Create a logo from SVG file or fallback to placeholder"""
        # Try to load SVG logo first if SVG support is available
        if SVG_AVAILABLE:
            logo_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'assets', 'logo.svg')
            
            if os.path.exists(logo_path):
                try:
                    # Load SVG logo
                    renderer = QSvgRenderer(logo_path)
                    pixmap = QPixmap(120, 120)
                    pixmap.fill(Qt.GlobalColor.transparent)
                    
                    painter = QPainter(pixmap)
                    renderer.render(painter)
                    painter.end()
                    
                    self.setPixmap(pixmap)
                    return
                except Exception as e:
                    print(f"Failed to load SVG logo: {e}")
        
        # Fallback: Create a placeholder logo
        pixmap = QPixmap(120, 120)
        pixmap.fill(Qt.GlobalColor.transparent)
        
        painter = QPainter(pixmap)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        
        # Create gradient
        gradient = QLinearGradient(0, 0, 120, 120)
        gradient.setColorAt(0, QColor("#4FC3F7"))
        gradient.setColorAt(1, QColor("#29B6F6"))
        
        # Draw circle
        painter.setBrush(QBrush(gradient))
        painter.setPen(Qt.PenStyle.NoPen)
        painter.drawEllipse(10, 10, 100, 100)
        
        # Add text
        painter.setPen(QColor("white"))
        font = QFont("Arial", 16, QFont.Weight.Bold)
        painter.setFont(font)
        painter.drawText(pixmap.rect(), Qt.AlignmentFlag.AlignCenter, "SC")
        
        painter.end()
        self.setPixmap(pixmap)
    
    def start_animation(self):
        """Start the fade-in animation"""
        self.opacity_animation.start()

class StartupScreen(QWidget):
    """
    Beautiful startup screen with logo, progress bar, and status updates
    """
    startup_complete = pyqtSignal()
    
    def __init__(self, initialization_tasks: list = None, parent=None):
        super().__init__(parent)
        self.initialization_tasks = initialization_tasks or self.get_default_tasks()
        
        # Window setup
        self.setWindowFlags(Qt.WindowType.SplashScreen | Qt.WindowType.FramelessWindowHint)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        self.setFixedSize(400, 300)
        
        # Center the window
        self.center_on_screen()
        
        # Setup UI
        self.setup_ui()
        
        # Initialize background thread
        self.init_thread = StartupInitializationThread(self.initialization_tasks)
        self.init_thread.progress_updated.connect(self.update_progress)
        self.init_thread.initialization_complete.connect(self.on_initialization_complete)
    
    def center_on_screen(self):
        """Center the startup screen on the screen"""
        screen = QApplication.primaryScreen()
        screen_geometry = screen.availableGeometry()
        x = (screen_geometry.width() - self.width()) // 2
        y = (screen_geometry.height() - self.height()) // 2
        self.move(x, y)
    
    def setup_ui(self):
        """Setup the user interface"""
        # Main layout
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(30, 30, 30, 30)
        main_layout.setSpacing(20)
        
        # Background frame
        self.background_frame = QFrame()
        self.background_frame.setStyleSheet("""
            QFrame {
                background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,
                                          stop: 0 rgba(255, 255, 255, 0.95),
                                          stop: 1 rgba(240, 240, 240, 0.95));
                border-radius: 15px;
                border: 1px solid rgba(200, 200, 200, 0.3);
            }
        """)
        
        frame_layout = QVBoxLayout(self.background_frame)
        frame_layout.setContentsMargins(30, 30, 30, 30)
        frame_layout.setSpacing(25)
        
        # Logo
        self.logo_widget = LogoWidget()
        frame_layout.addWidget(self.logo_widget, alignment=Qt.AlignmentFlag.AlignCenter)
        
        # App name
        self.app_name_label = QLabel("Spool-Coder")
        self.app_name_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        font = QFont("Arial", 24, QFont.Weight.Bold)
        self.app_name_label.setFont(font)
        self.app_name_label.setStyleSheet("color: #2E3440;")
        frame_layout.addWidget(self.app_name_label)
        
        # Subtitle
        self.subtitle_label = QLabel("Bambu Lab NFC Tool")
        self.subtitle_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        font = QFont("Arial", 12)
        self.subtitle_label.setFont(font)
        self.subtitle_label.setStyleSheet("color: #5E81AC;")
        frame_layout.addWidget(self.subtitle_label)
        
        # Progress bar
        self.progress_bar = AnimatedProgressBar()
        frame_layout.addWidget(self.progress_bar)
        
        # Status label
        self.status_label = QLabel("Initializing application...")
        self.status_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        font = QFont("Arial", 10)
        self.status_label.setFont(font)
        self.status_label.setStyleSheet("color: #4C566A;")
        frame_layout.addWidget(self.status_label)
        
        # Version label
        self.version_label = QLabel("Version 0.1.0")
        self.version_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        font = QFont("Arial", 8)
        self.version_label.setFont(font)
        self.version_label.setStyleSheet("color: #81A1C1;")
        frame_layout.addWidget(self.version_label)
        
        main_layout.addWidget(self.background_frame)
    
    def get_default_tasks(self):
        """Get default initialization tasks"""
        return [
            ("Python Environment", None),
            ("UI Components", None),
            ("NFC Services", None),
            ("Bambu Algorithm", None),
            ("Configuration", None),
            ("Ready", None)
        ]
    
    def show_and_initialize(self):
        """Show the startup screen and begin initialization"""
        self.show()
        
        # Start logo animation
        self.logo_widget.start_animation()
        
        # Start initialization after a brief delay
        QTimer.singleShot(500, self.start_initialization)
    
    def start_initialization(self):
        """Start the initialization process"""
        self.init_thread.start()
    
    def update_progress(self, progress: int, status: str):
        """Update progress bar and status text"""
        self.progress_bar.setValue(progress)
        self.status_label.setText(status)
        QApplication.processEvents()  # Update UI immediately
    
    def on_initialization_complete(self):
        """Called when initialization is complete"""
        # Brief delay before closing
        QTimer.singleShot(500, self.close_startup)
    
    def close_startup(self):
        """Close startup screen and emit completion signal"""
        self.startup_complete.emit()
        self.close()

class StartupManager:
    """
    Manager class to coordinate startup screen and main application
    """
    
    def __init__(self, app: QApplication, main_window_class, initialization_tasks: list = None):
        self.app = app
        self.main_window_class = main_window_class
        self.main_window = None
        self.startup_screen = None
        self.initialization_tasks = initialization_tasks
    
    def start_application(self):
        """Start the application with startup screen"""
        # Create startup screen
        self.startup_screen = StartupScreen(self.initialization_tasks)
        self.startup_screen.startup_complete.connect(self.show_main_window)
        
        # Show startup screen and begin initialization
        self.startup_screen.show_and_initialize()
    
    def show_main_window(self):
        """Show the main application window"""
        if self.main_window is None:
            self.main_window = self.main_window_class()
        
        self.main_window.show()
        
        # Clean up startup screen
        if self.startup_screen:
            self.startup_screen.deleteLater()
            self.startup_screen = None
