"""
Order data models.
"""
from dataclasses import dataclass, field
from typing import List, Optional, Dict


@dataclass
class OrderLine:
    """
    Individual product line in an order.
    
    Attributes:
        product_code: Product code
        quantity: Quantity ordered
        unit_price: Price per unit
        line_total: Total price for this line (quantity * unit_price)
    """
    product_code: str
    quantity: int
    unit_price: float
    line_total: float = field(init=False)
    
    def __post_init__(self):
        """Calculate line total."""
        self.line_total = self.quantity * self.unit_price


@dataclass
class Order:
    """
    Complete order with all fields.
    
    Attributes:
        client_name: Client's name
        phone: Phone number(s)
        address: Delivery address
        delivery_fee: Delivery fee amount
        products: Product field text (e.g., "CA x 2, TA:3")
        total_price: Total order price
        status: Order status
        agent: Assigned delivery agent
        notes: Optional notes
        order_lines: Parsed product lines
    """
    client_name: str
    phone: str
    address: str
    delivery_fee: float
    products: str
    total_price: float
    status: str
    agent: str
    notes: str = ""
    order_lines: List[OrderLine] = field(default_factory=list)
    
    def is_valid(self) -> bool:
        """
        Check if order has all required fields.
        
        Returns:
            True if order is valid, False otherwise
        """
        if not self.client_name or not self.client_name.strip():
            return False
        if not self.phone or not self.phone.strip():
            return False
        if not self.address or not self.address.strip():
            return False
        if self.delivery_fee is None or self.delivery_fee < 0:
            return False
        return True
    
    def calculate_total(self) -> float:
        """
        Calculate total price from order lines and delivery fee.
        
        Returns:
            Total price
        """
        products_total = sum(line.line_total for line in self.order_lines)
        return products_total + self.delivery_fee
    
    def to_dict(self) -> Dict:
        """Convert order to dictionary format."""
        return {
            "Client Name": self.client_name,
            "Phone": self.phone,
            "Address": self.address,
            "Delivery Fee": self.delivery_fee,
            "Product(s)": self.products,
            "Total Price": self.total_price,
            "Status": self.status,
            "Agent": self.agent,
            "Notes": self.notes
        }
