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
