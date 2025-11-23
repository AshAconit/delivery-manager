"""
Product data model.
"""
from dataclasses import dataclass
from typing import Optional


@dataclass
class Product:
    """
    Product data container.
    
    Attributes:
        code: Product code (e.g., "CA", "TA")
        name: Product name
        price: Unit price
        unit: Unit of measurement (e.g., "unit", "g")
    """
    code: str
    name: str
    price: float
    unit: str = "unit"
    
    def __post_init__(self):
        """Validate product data."""
        if not self.code:
            raise ValueError("Product code is required")
        if not self.name:
            raise ValueError("Product name is required")
        if self.price < 0:
            raise ValueError("Product price cannot be negative")
