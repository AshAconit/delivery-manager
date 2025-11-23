"""
Main application window.
"""
import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from typing import List, Dict
from ..config import Config
from ..data.products_loader import load_products
from ..data.agents_manager import AgentManager
from ..data.addresses_manager import AddressManager
from ..data.csv_handler import CSVHandler
from ..models.order import Order, OrderLine
from ..utils.parsers import parse_product_field
from ..utils.formatters import format_currency, capitalize_name
from .components import Toolbar, FilterPanel, StatusButtons
from .dialogs import AgentsDialog
from .table import OrderTable


class DeliveryApp:
    """
    Main application window for Delivery Manager.
    
    Coordinates between UI components and data managers.
    """
    
    def __init__(self, root: tk.Tk):
        """
        Initialize application.
        
        Args:
            root: Tkinter root window
        """
        self.root = root
        self.root.title(Config.WINDOW_TITLE)
        self.root.geometry(Config.WINDOW_SIZE)
        
        # Initialize managers
        self.agent_manager = AgentManager()
        self.address_manager = AddressManager()
        self.csv_handler = CSVHandler()
        
        # Load data
        self.products = load_products()
        self.agents = self.agent_manager.load_agents()
        
        # Create UI
        self._create_ui()
    
    def _create_ui(self):
        """Create main UI layout."""
        # Main container
        main_frame = ttk.Frame(self.root, padding=10)
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Left panel (table)
        left_frame = ttk.Frame(main_frame)
        left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        # Toolbar
        toolbar_callbacks = {
            "add_row": self._add_row,
            "delete_selected": self._delete_selected,
            "save_csv": self._save_csv,
            "load_csv": self._load_csv,
            "manage_agents": self._manage_agents,
            "clear_all": self._clear_all
        }
        self.toolbar = Toolbar(left_frame, toolbar_callbacks)
        self.toolbar.pack(fill=tk.X)
        
        # Order table
        self.table = OrderTable(
            left_frame,
            Config.COLUMNS,
            on_cell_edit=self._on_cell_edited
        )
        self.table.pack(fill=tk.BOTH, expand=True, pady=10)
        
        # Right panel (filters and status buttons)
        right_frame = ttk.Frame(main_frame)
        right_frame.pack(side=tk.RIGHT, fill=tk.Y, padx=(10, 0))
        
        # Filter panel
        self.filter_panel = FilterPanel(
            right_frame,
            Config.DEFAULT_STATUSES,
            self._on_filter_changed
        )
        self.filter_panel.pack(fill=tk.X, pady=(0, 10))
        
        # Status buttons
        self.status_buttons = StatusButtons(
            right_frame,
            Config.DEFAULT_STATUSES,
            self._on_status_clicked
        )
        self.status_buttons.pack(fill=tk.X)
    
    def _add_row(self):
        """Add new empty row to table."""
        empty_row = [""] * len(Config.COLUMNS)
        empty_row[Config.COLUMNS.index("Status")] = Config.DEFAULT_STATUS
        empty_row[Config.COLUMNS.index("Delivery Fee")] = Config.DELIVERY_FEE_OPTIONS[0]
        self.table.insert_row(empty_row)
    
    def _delete_selected(self):
        """Delete selected rows."""
        selected = self.table.get_selected_items()
        
        if not selected:
            messagebox.showwarning("No Selection", "Please select rows to delete.")
            return
        
        confirm = messagebox.askyesno(
            "Confirm Delete",
            f"Delete {len(selected)} row(s)?"
        )
        
        if confirm:
            for item in selected:
                self.table.delete_item(item)
    
    def _save_csv(self):
        """Save orders to CSV file."""
        filepath = filedialog.asksaveasfilename(
            defaultextension=".csv",
            filetypes=[("CSV files", "*.csv"), ("All files", "*.*")]
        )
        
        if not filepath:
            return
        
        try:
            rows = self.table.get_all_rows()
            orders = self._convert_rows_to_orders(rows)
            self.csv_handler.export_orders(orders, filepath)
            messagebox.showinfo("Success", f"Saved {len(orders)} orders to {filepath}")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save CSV: {e}")
    
    def _load_csv(self):
        """Load orders from CSV file."""
        filepath = filedialog.askopenfilename(
            filetypes=[("CSV files", "*.csv"), ("All files", "*.*")]
        )
        
        if not filepath:
            return
        
        try:
            order_dicts = self.csv_handler.import_orders(filepath)
            self.table.clear()
            
            for order_dict in order_dicts:
                row = [
                    order_dict.get("Client Name", ""),
                    order_dict.get("Phone", ""),
                    order_dict.get("Address", ""),
                    order_dict.get("Delivery Fee", ""),
                    order_dict.get("Product(s)", ""),
                    order_dict.get("Total Price", ""),
                    order_dict.get("Status", Config.DEFAULT_STATUS),
                    order_dict.get("Agent", ""),
                    order_dict.get("Notes", "")
                ]
                self.table.insert_row(row)
            
            messagebox.showinfo("Success", f"Loaded {len(order_dicts)} orders")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load CSV: {e}")
    
    def _manage_agents(self):
        """Open agents management dialog."""
        def on_save(agents: List[str]):
            self.agents = agents
            self.agent_manager.save_agents(agents)
            messagebox.showinfo("Success", "Agents updated successfully")
        
        AgentsDialog(self.root, self.agents, on_save)
    
    def _clear_all(self):
        """Clear all rows from table."""
        confirm = messagebox.askyesno(
            "Confirm Clear",
            "Clear all orders? This cannot be undone."
        )
        
        if confirm:
            self.table.clear()
    
    def _on_cell_edited(self, item: str, col_name: str, new_value: str):
        """Handle cell edit event."""
        # Save address to history if address column edited
        if col_name == "Address" and new_value.strip():
            self.address_manager.save_address(new_value)
        
        # Recalculate total if relevant fields changed
        if col_name in ["Product(s)", "Delivery Fee"]:
            self._recalculate_total(item)
    
    def _recalculate_total(self, item: str):
        """Recalculate and update total price for an order."""
        values = self.table.get_item_values(item)
        row_dict = dict(zip(Config.COLUMNS, values))
        
        # Parse products
        product_text = row_dict.get("Product(s)", "")
        parsed_products = parse_product_field(product_text)
        
        # Calculate products total
        products_total = 0.0
        for product in parsed_products:
            code = product["code"]
            qty = product["qty"]
            price = self.products.get(code, 0.0)
            products_total += price * qty
        
        # Add delivery fee
        try:
            delivery_fee = float(row_dict.get("Delivery Fee", 0))
        except ValueError:
            delivery_fee = 0.0
        
        total = products_total + delivery_fee
        
        # Update total in table
        values[Config.COLUMNS.index("Total Price")] = format_currency(total)
        self.table.tree.item(item, values=values)
    
    def _on_filter_changed(self):
        """Handle filter change event."""
        # This would filter visible rows based on selected statuses
        # Implementation depends on whether you want to hide rows or remove them
        pass
    
    def _on_status_clicked(self, status: str):
        """Handle bulk status update."""
        selected = self.table.get_selected_items()
        
        if not selected:
            messagebox.showwarning(
                "No Selection",
                "Please select rows to update."
            )
            return
        
        for item in selected:
            values = list(self.table.get_item_values(item))
            values[Config.COLUMNS.index("Status")] = status
            self.table.tree.item(item, values=values)
            self.table._update_row_color(item, values)
    
    def _convert_rows_to_orders(self, rows: List[Dict[str, str]]) -> List[Order]:
        """
        Convert table rows to Order objects.
        
        Args:
            rows: List of row dictionaries
            
        Returns:
            List of Order objects
        """
        orders = []
        
        for row in rows:
            try:
                # Parse numeric values
                delivery_fee = float(row.get("Delivery Fee", 0) or 0)
                total_price = float(row.get("Total Price", 0) or 0)
            except ValueError:
                delivery_fee = 0.0
                total_price = 0.0
            
            # Parse products into order lines
            product_text = row.get("Product(s)", "")
            parsed_products = parse_product_field(product_text)
            order_lines = []
            
            for product in parsed_products:
                code = product["code"]
                qty = product["qty"]
                price = self.products.get(code, 0.0)
                
                order_line = OrderLine(
                    product_code=code,
                    quantity=qty,
                    unit_price=price
                )
                order_lines.append(order_line)
            
            order = Order(
                client_name=row.get("Client Name", ""),
                phone=row.get("Phone", ""),
                address=row.get("Address", ""),
                delivery_fee=delivery_fee,
                products=product_text,
                total_price=total_price,
                status=row.get("Status", Config.DEFAULT_STATUS),
                agent=row.get("Agent", ""),
                notes=row.get("Notes", ""),
                order_lines=order_lines
            )
            orders.append(order)
        
        return orders
    
    def run(self):
        """Start the application main loop."""
        self.root.mainloop()
