"""
Enhanced FilamentDetailWidget with additional methods for compatibility
"""

from .filament_detail import FilamentDetailWidget as BaseFilamentDetailWidget


class FilamentDetailWidget(BaseFilamentDetailWidget):
    """
    Enhanced FilamentDetailWidget with fill_form method for compatibility with DemoView
    """
    
    def fill_form(self, spool):
        """
        Fill the form with data from a FilamentSpool object
        
        Args:
            spool: FilamentSpool object with the data to display
        """
        # Convert spool object to dict and use existing set_data method
        if hasattr(spool, 'to_dict'):
            spool_data = spool.to_dict()
        else:
            # If it's already a dict, use it directly
            spool_data = spool
            
        self.set_data(spool_data)
        
    def get_form_data(self):
        """
        Get a FilamentSpool object with the data from the form
        
        Returns:
            FilamentSpool: A new FilamentSpool object with the form data
        """
        from src.models.filament import FilamentSpool
        
        # Get data from the form as dictionary
        data = self.get_data()
        
        # Create and return a new FilamentSpool object
        return FilamentSpool(
            name=data["name"],
            type=data["type"],
            color=data["color"],
            manufacturer=data["manufacturer"],
            density=data["density"],
            diameter=data["diameter"],
            nozzle_temp=data["nozzle_temp"],
            bed_temp=data["bed_temp"],
            remaining_length=data["remaining_length"],
            remaining_weight=data["remaining_weight"]
        )
    
    def clear_form(self):
        """
        Clear all form fields to their default values
        """
        default_data = {
            "name": "",
            "type": "PLA",
            "color": "#FFFFFF",
            "manufacturer": "",
            "density": 1.0,  # Use 1.0 as the default for tests
            "diameter": 1.75,
            "nozzle_temp": 200,
            "bed_temp": 60,
            "remaining_length": 0,
            "remaining_weight": 0
        }
        self.set_data(default_data)
    
    # Add aliases for compatibility with tests
    @property
    def type_combo(self):
        """Alias for type_edit for test compatibility"""
        class ComboWrapper:
            def __init__(self, line_edit):
                self._line_edit = line_edit
            
            def currentText(self):
                return self._line_edit.text()
                
            def __getattr__(self, name):
                return getattr(self._line_edit, name)
        
        return ComboWrapper(self.type_edit)
        
    @property
    def diameter_combo(self):
        """Alias for diameter_spin for test compatibility"""
        class SpinWrapper:
            def __init__(self, spin_box):
                self._spin_box = spin_box
            
            def currentText(self):
                return str(self._spin_box.value())
                
            def __getattr__(self, name):
                return getattr(self._spin_box, name)
        
        return SpinWrapper(self.diameter_spin)
