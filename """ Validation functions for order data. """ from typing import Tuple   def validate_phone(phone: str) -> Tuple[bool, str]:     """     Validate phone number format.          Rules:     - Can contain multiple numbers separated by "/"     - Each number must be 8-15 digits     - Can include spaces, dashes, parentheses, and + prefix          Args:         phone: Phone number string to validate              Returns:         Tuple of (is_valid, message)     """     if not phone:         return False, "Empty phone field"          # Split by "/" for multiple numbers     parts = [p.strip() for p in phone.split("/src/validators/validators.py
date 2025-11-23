"""
Validation functions for order data.
"""
from typing import Tuple


def validate_phone(phone: str) -> Tuple[bool, str]:
    """
    Validate phone number format.
    
    Rules:
    - Can contain multiple numbers separated by "/"
    - Each number must be 8-15 digits
    - Can include spaces, dashes, parentheses, and + prefix
    
    Args:
        phone: Phone number string to validate
        
    Returns:
        Tuple of (is_valid, message)
    """
    if not phone:
        return False, "Empty phone field"
    
    # Split by "/" for multiple numbers
    parts = [p.strip() for p in phone.split("/") if p.strip()]
    
    if not parts:
        return False, "Empty phone field"
    
    for part in parts:
        # Clean the phone number
        cleaned = part.replace(" ", "").replace("-", "").replace("(", "").replace(")", "")
        
        # Handle international format
        if cleaned.startswith("+"):
            digits = cleaned[1:]
        else:
            digits = cleaned
        
        # Check if all characters are digits
        if not digits.isdigit():
            return False, f"Phone '{part}' contains invalid characters"
        
        # Check length
        if len(digits) < 8 or len(digits) > 15:
            return False, f"Phone '{part}' length must be 8–15 digits"
    
    return True, "OK"


def validate_address(address: str) -> Tuple[bool, str]:
    """
    Validate address field.
    
    Args:
        address: Address string to validate
        
    Returns:
        Tuple of (is_valid, message)
    """
    if not address or not address.strip():
        return False, "Address cannot be empty"
    
    return True, "OK"


def validate_delivery_fee(fee: any) -> Tuple[bool, str]:
    """
    Validate delivery fee value.
    
    Args:
        fee: Fee value to validate
        
    Returns:
        Tuple of (is_valid, message)
    """
    if fee is None or fee == "":
        return False, "Delivery fee is required"
    
    try:
        fee_value = float(fee)
        if fee_value < 0:
            return False, "Delivery fee cannot be negative"
        return True, "OK"
    except (ValueError, TypeError):
        return False, "Delivery fee must be a valid number"
