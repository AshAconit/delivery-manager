"""
Formatting utilities for display and parsing.
"""
from typing import Optional


def format_currency(value: Optional[float]) -> str:
    """
    Format numeric value as currency with thousands separator.
    
    Args:
        value: Numeric value to format
        
    Returns:
        Formatted string like "25 000 Ar" or original value if invalid
    """
    if value is None:
        return ""
    
    try:
        v = float(value)
    except (ValueError, TypeError):
        return str(value)
    
    is_negative = v < 0
    v_abs = abs(v)
    
    # Use integer formatting if value is whole number
    if abs(v_abs - round(v_abs)) < 0.0001:
        formatted = f"{int(round(v_abs)):,}".replace(",", " ")
    else:
        formatted = f"{v_abs:,.2f}".replace(",", " ")
    
    prefix = "-" if is_negative else ""
    return f"{prefix}{formatted} Ar"


def parse_numeric(value_str: str, allow_negative: bool = True) -> Optional[float]:
    """
    Parse string to numeric value, handling various formats.
    
    Handles formats like:
    - "25000"
    - "25 000"
    - "25,000"
    - "25000 Ar"
    
    Args:
        value_str: String to parse
        allow_negative: Whether negative values are allowed
        
    Returns:
        Float value or None if parsing fails
    """
    if value_str is None:
        return None
    
    # Clean the string
    cleaned = str(value_str).strip()
    cleaned = cleaned.replace(" ", "").replace("Ar", "").replace("ar", "").replace(",", "")
    
    if not cleaned:
        return None
    
    try:
        value = float(cleaned) if "." in cleaned else int(cleaned)
        
        if not allow_negative and value < 0:
            return None
            
        return value
    except (ValueError, TypeError):
        return None


def capitalize_name(name: str) -> str:
    """
    Capitalize each word in a name.
    
    Args:
        name: Name to capitalize
        
    Returns:
        Capitalized name
    """
    return " ".join(word.capitalize() for word in name.split())
