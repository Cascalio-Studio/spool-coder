"""
Sample NFC payload data for regression testing of BambuLab filament spools.

This module contains known-good NFC payload data representing different 
BambuLab filament types and configurations that should continue to decode 
correctly after code changes.

Reference: https://github.com/Bambu-Research-Group/RFID-Tag-Guide
"""

# Standard PLA filament configurations
BAMBU_PLA_BASIC = {
    "name": "Bambu PLA Basic",
    "type": "PLA",
    "color": "#FFFFFF",
    "manufacturer": "Bambulab",
    "density": 1.24,
    "diameter": 1.75,
    "nozzle_temp": 210,
    "bed_temp": 60,
    "remaining_length": 240,
    "remaining_weight": 1000
}

BAMBU_PLA_MATTE = {
    "name": "Bambu PLA Matte Black",
    "type": "PLA",
    "color": "#000000",
    "manufacturer": "Bambulab",
    "density": 1.24,
    "diameter": 1.75,
    "nozzle_temp": 220,
    "bed_temp": 60,
    "remaining_length": 195,
    "remaining_weight": 812
}

BAMBU_PLA_SILK = {
    "name": "Bambu PLA Silk Red",
    "type": "PLA",
    "color": "#FF0000",
    "manufacturer": "Bambulab",
    "density": 1.24,
    "diameter": 1.75,
    "nozzle_temp": 215,
    "bed_temp": 60,
    "remaining_length": 220,
    "remaining_weight": 915
}

# PETG filament configurations
BAMBU_PETG_BASIC = {
    "name": "Bambu PETG Basic",
    "type": "PETG",
    "color": "#00FF00",
    "manufacturer": "Bambulab",
    "density": 1.27,
    "diameter": 1.75,
    "nozzle_temp": 250,
    "bed_temp": 80,
    "remaining_length": 230,
    "remaining_weight": 980
}

BAMBU_PETG_HF = {
    "name": "Bambu PETG-HF Blue",
    "type": "PETG-HF",
    "color": "#0000FF",
    "manufacturer": "Bambulab",
    "density": 1.27,
    "diameter": 1.75,
    "nozzle_temp": 260,
    "bed_temp": 80,
    "remaining_length": 185,
    "remaining_weight": 789
}

# ABS filament configurations
BAMBU_ABS_BASIC = {
    "name": "Bambu ABS Black",
    "type": "ABS",
    "color": "#000000",
    "manufacturer": "Bambulab",
    "density": 1.04,
    "diameter": 1.75,
    "nozzle_temp": 270,
    "bed_temp": 90,
    "remaining_length": 210,
    "remaining_weight": 875
}

# ASA filament configurations
BAMBU_ASA_BASIC = {
    "name": "Bambu ASA Grey",
    "type": "ASA",
    "color": "#808080",
    "manufacturer": "Bambulab",
    "density": 1.07,
    "diameter": 1.75,
    "nozzle_temp": 280,
    "bed_temp": 90,
    "remaining_length": 205,
    "remaining_weight": 865
}

# TPU flexible filament configurations
BAMBU_TPU_95A = {
    "name": "Bambu TPU 95A",
    "type": "TPU",
    "color": "#FFFF00",
    "manufacturer": "Bambulab",
    "density": 1.20,
    "diameter": 1.75,
    "nozzle_temp": 230,
    "bed_temp": 50,
    "remaining_length": 180,
    "remaining_weight": 720
}

# PC (Polycarbonate) filament
BAMBU_PC_BASIC = {
    "name": "Bambu PC Transparent",
    "type": "PC",
    "color": "#FFFFFF",
    "manufacturer": "Bambulab",
    "density": 1.20,
    "diameter": 1.75,
    "nozzle_temp": 300,
    "bed_temp": 100,
    "remaining_length": 200,
    "remaining_weight": 800
}

# PA-CF (Carbon Fiber Nylon) filament
BAMBU_PA_CF = {
    "name": "Bambu PA-CF",
    "type": "PA-CF",
    "color": "#000000",
    "manufacturer": "Bambulab",
    "density": 1.18,
    "diameter": 1.75,
    "nozzle_temp": 320,
    "bed_temp": 90,
    "remaining_length": 175,
    "remaining_weight": 692
}

# Edge cases and variations
BAMBU_PLA_CUSTOM_COLOR = {
    "name": "Bambu PLA Custom Purple",
    "type": "PLA",
    "color": "#800080",
    "manufacturer": "Bambulab",
    "density": 1.24,
    "diameter": 1.75,
    "nozzle_temp": 210,
    "bed_temp": 60,
    "remaining_length": 240,
    "remaining_weight": 1000
}

# Nearly empty spool
BAMBU_PLA_NEARLY_EMPTY = {
    "name": "Bambu PLA Basic White",
    "type": "PLA",
    "color": "#FFFFFF",
    "manufacturer": "Bambulab",
    "density": 1.24,
    "diameter": 1.75,
    "nozzle_temp": 210,
    "bed_temp": 60,
    "remaining_length": 5,
    "remaining_weight": 20
}

# Full new spool
BAMBU_PETG_FULL = {
    "name": "Bambu PETG Basic Green",
    "type": "PETG",
    "color": "#00FF00",
    "manufacturer": "Bambulab",
    "density": 1.27,
    "diameter": 1.75,
    "nozzle_temp": 250,
    "bed_temp": 80,
    "remaining_length": 330,  # Full 1kg spool
    "remaining_weight": 1000
}

# All test cases collected in a list for easy iteration
ALL_VALID_PAYLOADS = [
    ("BAMBU_PLA_BASIC", BAMBU_PLA_BASIC),
    ("BAMBU_PLA_MATTE", BAMBU_PLA_MATTE),
    ("BAMBU_PLA_SILK", BAMBU_PLA_SILK),
    ("BAMBU_PETG_BASIC", BAMBU_PETG_BASIC),
    ("BAMBU_PETG_HF", BAMBU_PETG_HF),
    ("BAMBU_ABS_BASIC", BAMBU_ABS_BASIC),
    ("BAMBU_ASA_BASIC", BAMBU_ASA_BASIC),
    ("BAMBU_TPU_95A", BAMBU_TPU_95A),
    ("BAMBU_PC_BASIC", BAMBU_PC_BASIC),
    ("BAMBU_PA_CF", BAMBU_PA_CF),
    ("BAMBU_PLA_CUSTOM_COLOR", BAMBU_PLA_CUSTOM_COLOR),
    ("BAMBU_PLA_NEARLY_EMPTY", BAMBU_PLA_NEARLY_EMPTY),
    ("BAMBU_PETG_FULL", BAMBU_PETG_FULL),
]

# Invalid/malformed payloads for error handling tests
INVALID_PAYLOADS = [
    # Missing required fields
    ("MISSING_NAME", {
        "type": "PLA",
        "color": "#FFFFFF",
        "manufacturer": "Bambulab",
        "density": 1.24,
        "diameter": 1.75,
        "nozzle_temp": 210,
        "bed_temp": 60,
        "remaining_length": 240,
        "remaining_weight": 1000
    }),
    
    # Invalid data types
    ("INVALID_TEMP_TYPE", {
        "name": "Test PLA",
        "type": "PLA",
        "color": "#FFFFFF",
        "manufacturer": "Bambulab",
        "density": 1.24,
        "diameter": 1.75,
        "nozzle_temp": "invalid",  # Should be int
        "bed_temp": 60,
        "remaining_length": 240,
        "remaining_weight": 1000
    }),
    
    # Negative values
    ("NEGATIVE_WEIGHT", {
        "name": "Test PLA",
        "type": "PLA",
        "color": "#FFFFFF",
        "manufacturer": "Bambulab",
        "density": 1.24,
        "diameter": 1.75,
        "nozzle_temp": 210,
        "bed_temp": 60,
        "remaining_length": 240,
        "remaining_weight": -100  # Invalid negative weight
    }),
    
    # Empty payload
    ("EMPTY_PAYLOAD", {}),
    
    # Corrupted color format
    ("INVALID_COLOR", {
        "name": "Test PLA",
        "type": "PLA",
        "color": "invalid_color",  # Should be hex format
        "manufacturer": "Bambulab",
        "density": 1.24,
        "diameter": 1.75,
        "nozzle_temp": 210,
        "bed_temp": 60,
        "remaining_length": 240,
        "remaining_weight": 1000
    }),
]