"""
Products data loader for CSV file operations.
"""
import csv
import os
from typing import Dict, List
from ..config import Config


def load_products() -> Dict[str, float]:
    """
    Load products from CSV file.
    
    Handles multiple CSV formats:
    - With header: Code,Name,Price,Unit
    - Without header: CA,Creme Affinante,25000,unit
    
    Returns:
        Dictionary mapping product code to price
    """
    if not os.path.exists(Config.PRODUCTS_FILE):
        # Create sample file if it doesn't exist
        save_products_example()
    
    products = {}
    
    try:
        with open(Config.PRODUCTS_FILE, 'r', encoding='utf-8') as f:
            reader = csv.reader(f)
            rows = list(reader)
            
            if not rows:
                return products
            
            # Check if first row is header
            first_row = rows[0]
            has_header = (
                len(first_row) > 0 and 
                first_row[0].lower() in ['code', 'product', 'sku']
            )
            
            # Skip header if present
            data_rows = rows[1:] if has_header else rows
            
            for row in data_rows:
                if len(row) < 3:
                    continue
                
                code = row[0].strip().upper()
                try:
                    price = float(row[2].strip())
                    products[code] = price
                except (ValueError, IndexError):
                    continue
    
    except FileNotFoundError:
        pass
    except Exception as e:
        print(f"Error loading products: {e}")
    
    return products


def save_products_example():
    """
    Create sample products CSV file.
    
    Creates a CSV with sample products from Config.SAMPLE_PRODUCTS.
    """
    try:
        with open(Config.PRODUCTS_FILE, 'w', encoding='utf-8', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(["Code", "Name", "Price", "Unit"])
            writer.writerows(Config.SAMPLE_PRODUCTS)
    except Exception as e:
        print(f"Error creating sample products file: {e}")


def get_product_price(code: str, products: Dict[str, float]) -> float:
    """
    Get price for a product code.
    
    Args:
        code: Product code
        products: Dictionary of products
        
    Returns:
        Product price or 0.0 if not found
    """
    return products.get(code.upper(), 0.0)
