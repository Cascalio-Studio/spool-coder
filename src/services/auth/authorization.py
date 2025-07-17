"""
Authorization service for controlling NFC access
"""

class AuthorizationService:
    """
    Service to manage authorization for NFC device access
    """
    
    def __init__(self):
        """
        Initialize authorization service
        """
        self._authorized = False
        self._user_authenticated = False
    
    def authenticate_user(self, username=None, password=None):
        """
        Authenticate user for NFC access
        
        Args:
            username (str): Username (optional for demo)
            password (str): Password (optional for demo)
            
        Returns:
            bool: True if authentication successful, False otherwise
        """
        # Simple authentication - in real implementation this would check against
        # a proper authentication system
        if username == "admin" and password == "admin123":
            self._user_authenticated = True
            self._authorized = True
            return True
        return False
    
    def is_authorized(self):
        """
        Check if current user is authorized for NFC access
        
        Returns:
            bool: True if authorized, False otherwise
        """
        return self._authorized and self._user_authenticated
    
    def revoke_authorization(self):
        """
        Revoke current authorization
        """
        self._authorized = False
        self._user_authenticated = False
    
    def get_current_user(self):
        """
        Get current authenticated user
        
        Returns:
            str: Username if authenticated, None otherwise
        """
        if self._user_authenticated:
            return "admin"  # In real implementation, store actual username
        return None


# Global authorization service instance
_auth_service = AuthorizationService()

def get_auth_service():
    """
    Get the global authorization service instance
    
    Returns:
        AuthorizationService: The authorization service
    """
    return _auth_service