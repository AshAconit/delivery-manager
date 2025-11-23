"""
CSV file handler for order import/export.
"""
import csv
import json
from typing import List, Dict
from ..models.order import Order


class CSVHandler:
    """Handles CSV import and export operations for orders."""
    
    def export_orders(self, orders: List[Order], path: str):
        """
        Export orders to CSV file.
        
        Args:
            orders: List of Order objects to export
            path: Path to CSV file
        """
        try:
            with open(path, 'w', encoding='utf-8', newline='') as f:
                fieldnames = [
                    "Client Name",
                    "Phone",
                    "Address",
                    "Delivery Fee",
                    "Product(s)",
                    "Total Price",
                    "Status",
                    "Agent",
                    "Notes",
                    "OrderLinesJSON"
                ]
                
                writer = csv.DictWriter(f, fieldnames=fieldnames)
                writer.writeheader()
                
                for order in orders:
                    row = order.to_dict()
                    
                    # Serialize order lines to JSON
                    if order.order_lines:
                        order_lines_data = [
                            {
                                "product_code": line.product_code,
                                "quantity": line.quantity,
                                "unit_price": line.unit_price,
                                "line_total": line.line_total
                            }
                            for line in order.order_lines
                        ]
                        row["OrderLinesJSON"] = json.dumps(order_lines_data)
                    else:
                        row["OrderLinesJSON"] = ""
                    
                    writer.writerow(row)
        
        except Exception as e:
            print(f"Error exporting orders: {e}")
            raise
    
    def import_orders(self, path: str) -> List[Dict]:
        """
        Import orders from CSV file.
        
        Args:
            path: Path to CSV file
            
        Returns:
            List of order dictionaries
        """
        orders = []
        
        try:
            with open(path, 'r', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                
                for row in reader:
                    # Parse OrderLinesJSON if present
                    if "OrderLinesJSON" in row and row["OrderLinesJSON"]:
                        try:
                            row["order_lines"] = json.loads(row["OrderLinesJSON"])
                        except json.JSONDecodeError:
                            row["order_lines"] = []
                    else:
                        row["order_lines"] = []
                    
                    orders.append(row)
        
        except Exception as e:
            print(f"Error importing orders: {e}")
            raise
        
        return orders
