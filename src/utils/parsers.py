"""
Product parsing utilities.
"""
import re
from typing import List, Dict


# Regex pattern for product code and quantity
PRODUCT_PATTERN = re.compile(r"([A-Za-z0-9]+)\s*(?:[:xX]?\s*(-?\d+))?")


def parse_product_field(field_text: str) -> List[Dict]:
    """
    Parse product field text into structured list.
    
    Supported formats:
    - "CA x 2" → code=CA, qty=2
    - "TA:3" → code=TA, qty=3
    - "CG" → code=CG, qty=1
    - "CA x 2, TA:1" → multiple products
    - "BS 100" → code=BS, qty=100
    
    Args:
        field_text: Product field string
        
    Returns:
        List of dicts with 'code' and 'qty' keys
    """
    if not field_text or not field_text.strip():
        return []
    
    # Split by comma or semicolon
    items = re.split(r"[;,]", field_text)
    parsed = []
    
    for item in items:
        item = item.strip()
        if not item:
            continue
        
        # Try regex match first
        match = PRODUCT_PATTERN.match(item)
        
        if not match:
            # Fallback: try splitting by space
            tokens = item.split()
            if len(tokens) == 2 and tokens[1].lstrip("-").isdigit():
                code = tokens[0].upper()
                qty = int(tokens[1])
                parsed.append({"code": code, "qty": qty})
            else:
                # Just the code, quantity = 1
                parsed.append({"code": item.upper(), "qty": 1})
            continue
        
        code = match.group(1).upper()
        qty_raw = match.group(2)
        qty = int(qty_raw) if (qty_raw is not None and qty_raw != "") else 1
        
        parsed.append({"code": code, "qty": qty})
    
    return parsed
