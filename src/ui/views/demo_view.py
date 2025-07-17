"""
Demo view for the Bambu Lab NFC algorithm
"""

from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QPushButton,
                           QLabel, QTextEdit, QGroupBox, QComboBox, QSpinBox,
                           QDoubleSpinBox, QColorDialog, QLineEdit, QMessageBox)
from PyQt6.QtGui import QColor, QPalette
from PyQt6.QtCore import Qt, pyqtSlot, QBuffer
import json
import base64

from src.services.nfc.bambu_algorithm import BambuLabNFCEncoder, BambuLabNFCDecoder, SAMPLE_TAG_DATA
from src.models.filament import FilamentSpool
from src.ui.components.filament_detail_widget import FilamentDetailWidget


class DemoView(QWidget):
    """
    Demo view for testing the Bambu Lab NFC algorithm
    """
    
    def __init__(self, parent=None):
        super().__init__(parent)
        
        # Create the NFC algorithm instances
        self.encoder = BambuLabNFCEncoder()
        self.decoder = BambuLabNFCDecoder()
        
        # Set a minimum size for this view to ensure it's readable
        self.setMinimumSize(900, 700)
        
        # Set up the UI
        self.setup_ui()
    
    def setup_ui(self):
        """Set up the UI elements"""
        # Main layout
        main_layout = QVBoxLayout(self)
        
        # Title
        title_label = QLabel("Bambu Lab NFC Algorithm Demo")
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title_font = title_label.font()
        title_font.setPointSize(16)
        title_font.setBold(True)
        title_label.setFont(title_font)
        main_layout.addWidget(title_label)
        
        # Description
        desc_label = QLabel("This demo shows the encoding and decoding of Bambu Lab NFC tags "
                           "without requiring actual NFC hardware.")
        desc_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        desc_label.setWordWrap(True)
        main_layout.addWidget(desc_label)
        
        # Create horizontal layout for input and output
        h_layout = QHBoxLayout()
        main_layout.addLayout(h_layout)
        
        # Left side - Filament detail widget
        self.left_group = QGroupBox("Filament Data Input")
        left_layout = QVBoxLayout(self.left_group)
        self.filament_detail = FilamentDetailWidget()
        left_layout.addWidget(self.filament_detail)
        
        # Sample data button
        sample_btn = QPushButton("Load Sample Data")
        sample_btn.clicked.connect(self.on_sample_clicked)
        left_layout.addWidget(sample_btn)
        
        # Encode button
        encode_btn = QPushButton("Encode Data")
        encode_btn.clicked.connect(self.on_encode_clicked)
        left_layout.addWidget(encode_btn)
        
        h_layout.addWidget(self.left_group, 40)  # 40% of the width
        
        # Right side - Raw data and decoding
        self.right_group = QGroupBox("NFC Tag Data")
        right_layout = QVBoxLayout(self.right_group)
        
        # Encoded data display
        encoded_label = QLabel("Encoded Tag Data (Base64):")
        right_layout.addWidget(encoded_label)
        
        self.encoded_text = QTextEdit()
        self.encoded_text.setReadOnly(True)
        self.encoded_text.setAcceptRichText(False)
        self.encoded_text.setMinimumHeight(150)
        self.encoded_text.setMinimumWidth(400)
        right_layout.addWidget(self.encoded_text)
        
        # Decode button
        decode_btn = QPushButton("Decode Data")
        decode_btn.clicked.connect(self.on_decode_clicked)
        right_layout.addWidget(decode_btn)
        
        # Decoded data display
        decoded_label = QLabel("Decoded Tag Data (JSON):")
        right_layout.addWidget(decoded_label)
        
        self.decoded_text = QTextEdit()
        self.decoded_text.setReadOnly(True)
        self.decoded_text.setAcceptRichText(False)
        self.decoded_text.setMinimumHeight(300)
        self.decoded_text.setMinimumWidth(400)
        right_layout.addWidget(self.decoded_text)
        
        h_layout.addWidget(self.right_group, 60)  # 60% of the width
        
        # Status bar
        self.status_label = QLabel("Ready")
        main_layout.addWidget(self.status_label)
        
        # Back button
        back_layout = QHBoxLayout()
        back_btn = QPushButton("Back to Home")
        back_btn.clicked.connect(self.on_back_clicked)
        back_layout.addStretch()
        back_layout.addWidget(back_btn)
        main_layout.addLayout(back_layout)
    
    @pyqtSlot()
    def on_sample_clicked(self):
        """Load sample data into the form"""
        try:
            # Convert the sample tag data to a format suitable for FilamentSpool
            sample_data = {
                "name": SAMPLE_TAG_DATA["spool_data"]["name"],
                "type": SAMPLE_TAG_DATA["spool_data"]["type"],
                "color": SAMPLE_TAG_DATA["spool_data"]["color"],
                "manufacturer": SAMPLE_TAG_DATA["spool_data"]["manufacturer"],
                "density": SAMPLE_TAG_DATA["spool_data"]["density"],
                "diameter": SAMPLE_TAG_DATA["spool_data"]["diameter"],
                "nozzle_temp": SAMPLE_TAG_DATA["spool_data"]["nozzle_temp"],
                "bed_temp": SAMPLE_TAG_DATA["spool_data"]["bed_temp"],
                "remaining_length": SAMPLE_TAG_DATA["spool_data"]["remaining_length"],
                "remaining_weight": SAMPLE_TAG_DATA["spool_data"]["remaining_weight"]
            }
            
            # Create a FilamentSpool object
            spool = FilamentSpool.from_dict(sample_data)
            
            # Fill the form
            self.filament_detail.fill_form(spool)
            
            self.status_label.setText("Sample data loaded")
        except Exception as e:
            self.status_label.setText(f"Error loading sample data: {str(e)}")
    
    @pyqtSlot()
    def on_encode_clicked(self):
        """Encode the form data to NFC tag format"""
        try:
            # Get data from form
            spool = self.filament_detail.get_form_data()
            
            # Convert to dictionary
            spool_dict = spool.to_dict()
            
            # Prepare data for encoding
            tag_data = {
                "version": 1,
                "flags": "000000",
                "spool_data": {
                    "type": spool_dict["type"],
                    "color": spool_dict["color"],
                    "diameter": spool_dict["diameter"],
                    "nozzle_temp": spool_dict["nozzle_temp"],
                    "bed_temp": spool_dict["bed_temp"],
                    "density": spool_dict["density"],
                    "remaining_length": spool_dict["remaining_length"],
                    "remaining_weight": spool_dict["remaining_weight"],
                    "manufacturer": spool_dict["manufacturer"],
                    "name": spool_dict["name"]
                },
                "manufacturing_info": {
                    "serial": "DEMO12345",
                    "date": 1626912000  # July 22, 2021
                }
            }
            
            # Encode the data
            encoded_data = self.encoder.encode_tag_data(tag_data)
            
            # Convert to base64 for display
            base64_data = base64.b64encode(encoded_data).decode('ascii')
            
            # Display in text area
            self.encoded_text.setText(base64_data)
            
            self.status_label.setText("Data encoded successfully")
        except Exception as e:
            self.status_label.setText(f"Error encoding data: {str(e)}")
    
    @pyqtSlot()
    def on_decode_clicked(self):
        """Decode the NFC tag data from the text area"""
        try:
            # Get base64 data from text area
            base64_data = self.encoded_text.toPlainText()
            if not base64_data:
                QMessageBox.warning(self, "No Data", "No encoded data to decode")
                return
                
            # Convert from base64
            try:
                raw_data = base64.b64decode(base64_data)
            except Exception:
                QMessageBox.warning(self, "Invalid Data", "The data is not valid base64")
                return
                
            # Decode the data
            decoded_data = self.decoder.decode_tag_data(raw_data)
            
            if decoded_data:
                # Format as JSON for display
                json_data = json.dumps(decoded_data, indent=2)
                self.decoded_text.setText(json_data)
                
                # Update status
                self.status_label.setText("Data decoded successfully")
                
                # Ask if user wants to load this data into the form
                reply = QMessageBox.question(
                    self, 
                    "Load Data", 
                    "Do you want to load this data into the form?",
                    QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
                    QMessageBox.StandardButton.No
                )
                
                if reply == QMessageBox.StandardButton.Yes:
                    # Convert to FilamentSpool and load into form
                    spool_data = decoded_data["spool_data"]
                    spool = FilamentSpool(
                        name=spool_data["name"],
                        type=spool_data["type"],
                        color=spool_data["color"],
                        manufacturer=spool_data["manufacturer"],
                        density=spool_data["density"],
                        diameter=spool_data["diameter"],
                        nozzle_temp=spool_data["nozzle_temp"],
                        bed_temp=spool_data["bed_temp"],
                        remaining_length=spool_data["remaining_length"],
                        remaining_weight=spool_data["remaining_weight"]
                    )
                    self.filament_detail.fill_form(spool)
            else:
                QMessageBox.warning(self, "Decode Failed", 
                                  "Failed to decode the data. It might be corrupted.")
        except Exception as e:
            self.status_label.setText(f"Error decoding data: {str(e)}")
    
    @pyqtSlot()
    def on_back_clicked(self):
        """Go back to the home screen"""
        # Find the main window and show the home screen
        parent = self.parent()
        while parent is not None:
            if hasattr(parent, 'show_home'):
                parent.show_home()
                break
            parent = parent.parent()
