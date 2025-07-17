"""
Security logging service for tracking security events
"""

import logging
import datetime
import os

class SecurityLogger:
    """
    Logger for security-related events
    """
    
    def __init__(self, log_file=None):
        """
        Initialize security logger
        
        Args:
            log_file (str): Path to log file, if None uses default location
        """
        # Set up logging
        self.logger = logging.getLogger('security')
        self.logger.setLevel(logging.INFO)
        
        # Remove existing handlers to avoid duplicates
        for handler in self.logger.handlers[:]:
            self.logger.removeHandler(handler)
        
        # Create formatter
        formatter = logging.Formatter(
            '%(asctime)s - %(levelname)s - SECURITY - %(message)s'
        )
        
        # Console handler
        console_handler = logging.StreamHandler()
        console_handler.setFormatter(formatter)
        self.logger.addHandler(console_handler)
        
        # File handler
        if log_file is None:
            # Create logs directory if it doesn't exist
            log_dir = os.path.join(os.path.dirname(__file__), '..', '..', '..', 'logs')
            os.makedirs(log_dir, exist_ok=True)
            log_file = os.path.join(log_dir, 'security.log')
        
        try:
            file_handler = logging.FileHandler(log_file)
            file_handler.setFormatter(formatter)
            self.logger.addHandler(file_handler)
        except Exception as e:
            # If file logging fails, just continue with console logging
            print(f"Warning: Could not create log file {log_file}: {e}")
    
    def log_unauthorized_access_attempt(self, resource, user=None, details=None):
        """
        Log an unauthorized access attempt
        
        Args:
            resource (str): The resource being accessed
            user (str): Username if known, None otherwise
            details (str): Additional details about the attempt
        """
        user_str = f"User: {user}" if user else "User: Unknown"
        details_str = f" - {details}" if details else ""
        
        message = f"UNAUTHORIZED ACCESS ATTEMPT - Resource: {resource} - {user_str}{details_str}"
        self.logger.warning(message)
    
    def log_access_denied(self, resource, reason, user=None):
        """
        Log an access denied event
        
        Args:
            resource (str): The resource being accessed
            reason (str): Reason for denial
            user (str): Username if known
        """
        user_str = f"User: {user}" if user else "User: Unknown"
        message = f"ACCESS DENIED - Resource: {resource} - Reason: {reason} - {user_str}"
        self.logger.warning(message)
    
    def log_authorization_event(self, event_type, user=None, details=None):
        """
        Log general authorization events
        
        Args:
            event_type (str): Type of authorization event
            user (str): Username if known
            details (str): Additional details
        """
        user_str = f"User: {user}" if user else "User: Unknown"
        details_str = f" - {details}" if details else ""
        
        message = f"AUTHORIZATION EVENT - {event_type} - {user_str}{details_str}"
        self.logger.info(message)


# Global security logger instance
_security_logger = SecurityLogger()

def get_security_logger():
    """
    Get the global security logger instance
    
    Returns:
        SecurityLogger: The security logger
    """
    return _security_logger