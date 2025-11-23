"""
Configuration module for Delivery Manager.
Centralized constants and settings.
"""
import os

class Config:
    """Application configuration and constants."""
    
    # File paths
    BASE_DIR = os.path.dirname(os.path.dirname(__file__))
    AGENTS_FILE = os.path.join(BASE_DIR, "agents.txt")
    ADDRESSES_FILE = os.path.join(BASE_DIR, "addresses.txt")
    PRODUCTS_FILE = os.path.join(BASE_DIR, "products.csv")
    
    # Status configuration
    DEFAULT_STATUSES = ["Ok", "Ok with retour", "Cancelled", "Reported", "Pending"]
    DEFAULT_STATUS = "Pending"
    
    STATUS_COLORS = {
        "Pending": "#fffce6",
        "Ok": "#e6ffed",
        "Ok with retour": "#fff7e6",
        "Cancelled": "#ffe6e6",
        "Reported": "#ffe8f0",
    }
    
    INVALID_ROW_COLOR = "#fff2b2"
    
    # Delivery fees
    DELIVERY_FEE_OPTIONS = ["3000", "4000"]
    
    # Column configuration
    COLUMNS = [
        "Client Name",
        "Phone",
        "Address",
        "Delivery Fee",
        "Product(s)",
        "Total Price",
        "Status",
        "Agent",
        "Notes"
    ]
    
    COLUMN_WIDTHS = {
        "Address": 320,
        "Notes": 320,
        "Product(s)": 320,
        "Client Name": 180,
        "default": 120
    }
    
    # UI settings
    WINDOW_SIZE = "1280x760"
    WINDOW_TITLE = "Delivery Manager — Bulk status + Filter"
    ROW_HEIGHT = 32
    FONT_FAMILY = "Segoe UI"
    FONT_SIZE = 10
    
    # Validation rules
    PHONE_MIN_LENGTH = 8
    PHONE_MAX_LENGTH = 15
    MAX_ADDRESS_HISTORY = 200
    
    # Default agents
    DEFAULT_AGENTS = ["Jean", "Hery", "Mamy", "Rado", "External Courier"]
    
    # Sample products for initialization
    SAMPLE_PRODUCTS = [
        ["CA", "Creme Affinante", "25000", "unit"],
        ["TA", "Tisane Affinante", "25000", "unit"],
        ["CG", "Creme Galbante", "25000", "unit"],
        ["SG", "SAVON GALBANT", "15000", "unit"],
        ["BS", "Base de Savon", "50", "g"],
        ["G", "Gaine", "10000", "unit"]
    ]
