"""
Modern Card Component - Moderne Karten-UI-Komponente
Inspiriert von modernen Design-Systemen wie dem Griffain-Interface
"""

from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
                           QPushButton, QGraphicsDropShadowEffect)
from PyQt6.QtCore import Qt, QPropertyAnimation, QEasingCurve, pyqtSignal, QRect
from PyQt6.QtGui import QFont, QPixmap, QPainter, QColor, QPen, QBrush

class ModernCard(QWidget):
    """
    Moderne Karten-Komponente mit Hover-Effekten und ansprechendem Design
    """
    
    clicked = pyqtSignal()
    
    def __init__(self, title, description, icon_text="", primary=False, parent=None):
        super().__init__(parent)
        
        self.title = title
        self.description = description
        self.icon_text = icon_text
        self.primary = primary
        self.is_hovered = False
        
        self.setup_ui()
        self.setup_animations()
        self.apply_styling()
        
    def setup_ui(self):
        """Erstellt das UI-Layout der Karte"""
        # Größere Mindestgröße für bessere Textdarstellung
        self.setMinimumSize(220, 160)
        self.setMaximumSize(450, 280)
        self.setCursor(Qt.CursorShape.PointingHandCursor)
        
        # Tastatur-Navigation aktivieren
        self.setFocusPolicy(Qt.FocusPolicy.StrongFocus)
        self.setAttribute(Qt.WidgetAttribute.WA_AcceptTouchEvents, True)
        
        # Hauptlayout mit mehr Platz
        layout = QVBoxLayout(self)
        layout.setContentsMargins(25, 25, 25, 25)
        layout.setSpacing(12)
        
        # Icon/Emoji Bereich
        self.icon_label = QLabel(self.icon_text)
        self.icon_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.icon_font = QFont()
        self.icon_font.setPointSize(32)
        self.icon_label.setFont(self.icon_font)
        layout.addWidget(self.icon_label)
        
        # Titel mit mehr Platz
        self.title_label = QLabel(self.title)
        self.title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.title_font = QFont()
        self.title_font.setPointSize(16)
        self.title_font.setBold(True)
        self.title_label.setFont(self.title_font)
        self.title_label.setMinimumHeight(30)
        layout.addWidget(self.title_label)
        
        # Beschreibung mit mehr Platz und besserer Formatierung
        self.desc_label = QLabel(self.description)
        self.desc_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.desc_label.setWordWrap(True)
        self.desc_font = QFont()
        self.desc_font.setPointSize(11)
        self.desc_label.setFont(self.desc_font)
        self.desc_label.setMinimumHeight(50)
        layout.addWidget(self.desc_label)
        
        layout.addStretch()
        
    def setup_animations(self):
        """Erstellt die Hover-Animationen"""
        self.scale_animation = QPropertyAnimation(self, b"geometry")
        self.scale_animation.setDuration(200)
        self.scale_animation.setEasingCurve(QEasingCurve.Type.OutCubic)
        
    def apply_styling(self):
        """Wendet das Styling basierend auf dem Griffain-Design an"""
        if self.primary:
            # Primäre Karte (Grün-Akzent für wichtige Aktionen)
            self.setStyleSheet("""
                ModernCard {
                    background-color: #2A2A2F;
                    border: 2px solid #5EFB7B;
                    border-radius: 12px;
                    color: #FEFDFF;
                }
                ModernCard:hover {
                    background-color: #323238;
                    border-color: #6FFC8C;
                }
            """)
            self.icon_label.setStyleSheet("color: #5EFB7B;")
            self.title_label.setStyleSheet("color: #FEFDFF;")
            self.desc_label.setStyleSheet("color: #68658A;")
        else:
            # Sekundäre Karte (Standard grau)
            self.setStyleSheet("""
                ModernCard {
                    background-color: #2A2A2F;
                    border: 1px solid #404040;
                    border-radius: 12px;
                    color: #FEFDFF;
                }
                ModernCard:hover {
                    background-color: #323238;
                    border-color: #505050;
                }
            """)
            self.icon_label.setStyleSheet("color: #FEFDFF;")
            self.title_label.setStyleSheet("color: #FEFDFF;")
            self.desc_label.setStyleSheet("color: #68658A;")
        
        # Schatten-Effekt
        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(20)
        shadow.setXOffset(0)
        shadow.setYOffset(4)
        shadow.setColor(QColor(0, 0, 0, 30))
        self.setGraphicsEffect(shadow)
    
    def enterEvent(self, event):
        """Wird aufgerufen, wenn die Maus über die Karte fährt"""
        self.is_hovered = True
        self.animate_scale(1.05)
        
        # Schatten verstärken
        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(30)
        shadow.setXOffset(0)
        shadow.setYOffset(8)
        shadow.setColor(QColor(0, 0, 0, 60))
        self.setGraphicsEffect(shadow)
        
        super().enterEvent(event)
    
    def leaveEvent(self, event):
        """Wird aufgerufen, wenn die Maus die Karte verlässt"""
        self.is_hovered = False
        self.animate_scale(1.0)
        
        # Schatten zurücksetzen
        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(20)
        shadow.setXOffset(0)
        shadow.setYOffset(4)
        shadow.setColor(QColor(0, 0, 0, 30))
        self.setGraphicsEffect(shadow)
        
        super().leaveEvent(event)
    
    def mousePressEvent(self, event):
        """Behandelt Mausklicks"""
        if event.button() == Qt.MouseButton.LeftButton:
            self.animate_scale(0.95)  # Kurzes Eindrücken
            
    def mouseReleaseEvent(self, event):
        """Behandelt das Loslassen der Maus"""
        if event.button() == Qt.MouseButton.LeftButton:
            if self.is_hovered:
                self.animate_scale(1.05)
            else:
                self.animate_scale(1.0)
            self.clicked.emit()
    
    def animate_scale(self, scale_factor):
        """Animiert die Skalierung der Karte"""
        current_geometry = self.geometry()
        center = current_geometry.center()
        
        new_width = int(200 * scale_factor)
        new_height = int(140 * scale_factor)
        
        new_geometry = QRect(
            center.x() - new_width // 2,
            center.y() - new_height // 2,
            new_width,
            new_height
        )
        
        self.scale_animation.setStartValue(current_geometry)
        self.scale_animation.setEndValue(new_geometry)
        self.scale_animation.start()
    
    def set_responsive_size(self, size_mode):
        """
        Passt die Kartengröße und Schriftgrößen an verschiedene Bildschirmgrößen an
        """
        if size_mode == "compact":  # Mobile
            # Kompakte Größen und Schriften
            self.icon_font.setPointSize(26)
            self.title_font.setPointSize(14)
            self.desc_font.setPointSize(10)
            
        elif size_mode == "medium":  # Tablet
            # Mittlere Größen und Schriften
            self.icon_font.setPointSize(30)
            self.title_font.setPointSize(15)
            self.desc_font.setPointSize(11)
            
        else:  # "normal" - Desktop
            # Standard Größen und Schriften
            self.icon_font.setPointSize(32)
            self.title_font.setPointSize(16)
            self.desc_font.setPointSize(11)
        
        # Fonts aktualisieren
        self.icon_label.setFont(self.icon_font)
        self.title_label.setFont(self.title_font)
        self.desc_label.setFont(self.desc_font)
    
    def keyPressEvent(self, event):
        """Behandelt Tastatureingaben für Navigation"""
        if event.key() in (Qt.Key.Key_Return, Qt.Key.Key_Enter, Qt.Key.Key_Space):
            self.clicked.emit()
        else:
            super().keyPressEvent(event)
    
    def focusInEvent(self, event):
        """Behandelt Focus-In Events für Tastatur-Navigation"""
        super().focusInEvent(event)
        self.animate_scale(1.05)
        # Fokus-Rahmen hinzufügen
        if self.primary:
            self.setStyleSheet(self.styleSheet() + """
                ModernCard {
                    border: 2px solid #6FFC8C;
                }
            """)
        else:
            self.setStyleSheet(self.styleSheet() + """
                ModernCard {
                    border: 2px solid #5EFB7B;
                }
            """)
    
    def focusOutEvent(self, event):
        """Behandelt Focus-Out Events für Tastatur-Navigation"""
        super().focusOutEvent(event)
        self.animate_scale(1.0)
        # Styling zurücksetzen
        self.apply_styling()
