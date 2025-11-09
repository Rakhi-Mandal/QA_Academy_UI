"""
Custom Validation Functions
"""
import re
from typing import Optional

def validate_email(email: str) -> bool:
    """
    Validate email format
    
    Args:
        email: Email address to validate
        
    Returns:
        True if valid, False otherwise
    """
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return bool(re.match(pattern, email))

def validate_employee_id(employee_id: str) -> bool:
    """
    Validate employee ID format (e.g., FS452)
    
    Args:
        employee_id: Employee ID to validate
        
    Returns:
        True if valid, False otherwise
    """
    pattern = r'^FS\d{3,4}$'
    return bool(re.match(pattern, employee_id))

def validate_file_extension(filename: str, allowed_extensions: set) -> bool:
    """
    Validate file extension
    
    Args:
        filename: Name of file
        allowed_extensions: Set of allowed extensions
        
    Returns:
        True if valid, False otherwise
    """
    if '.' not in filename:
        return False
    extension = filename.rsplit('.', 1)[1].lower()
    return extension in allowed_extensions

def sanitize_filename(filename: str) -> str:
    """
    Sanitize filename to prevent security issues
    
    Args:
        filename: Original filename
        
    Returns:
        Sanitized filename
    """
    # Remove any path separators
    filename = filename.replace('/', '_').replace('\\', '_')
    # Remove any potentially dangerous characters
    filename = re.sub(r'[^\w\s.-]', '', filename)
    return filename