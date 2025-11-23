"""
Order table component using Treeview.
"""
import tkinter as tk
from tkinter import ttk
from typing import List, Dict, Callable, Optional
from ..config import Config
from ..validators.validators import validate_phone, validate_address, validate_delivery_fee


class OrderTable:
    """
    Treeview wrapper for displaying and editing orders.
    
    Handles row display with colors, cell editing, and selection management.
    """
    
    def __init__(self, parent: tk.Widget, columns: List[str],
                 on_cell_edit: Optional[Callable] = None):
        """
        Initialize order table.
        
        Args:
            parent: Parent widget
            columns: List of column names
            on_cell_edit: Optional callback when cell is edited
        """
        self.columns = columns
        self.on_cell_edit = on_cell_edit
        self._create_table(parent)
        self._setup_bindings()
    
    def _create_table(self, parent: tk.Widget):
        """Create treeview table with scrollbars."""
        # Frame for table and scrollbars
        self.frame = ttk.Frame(parent)
        
        # Scrollbars
        vsb = ttk.Scrollbar(self.frame, orient="vertical")
        hsb = ttk.Scrollbar(self.frame, orient="horizontal")
        
        # Treeview
        self.tree = ttk.Treeview(
            self.frame,
            columns=self.columns,
            show="headings",
            yscrollcommand=vsb.set,
            xscrollcommand=hsb.set,
            selectmode="extended"
        )
        
        vsb.config(command=self.tree.yview)
        hsb.config(command=self.tree.xview)
        
        # Layout
        self.tree.grid(row=0, column=0, sticky="nsew")
        vsb.grid(row=0, column=1, sticky="ns")
        hsb.grid(row=1, column=0, sticky="ew")
        
        self.frame.grid_rowconfigure(0, weight=1)
        self.frame.grid_columnconfigure(0, weight=1)
        
        # Configure columns
        for col in self.columns:
            width = Config.COLUMN_WIDTHS.get(col, Config.COLUMN_WIDTHS["default"])
            self.tree.heading(col, text=col)
            self.tree.column(col, width=width, minwidth=50)
        
        # Configure row height
        style = ttk.Style()
        style.configure("Treeview", rowheight=Config.ROW_HEIGHT)
        
        # Configure tags for colors
        for status, color in Config.STATUS_COLORS.items():
            self.tree.tag_configure(f"status_{status}", background=color)
        
        self.tree.tag_configure("invalid", background=Config.INVALID_ROW_COLOR)
    
    def _setup_bindings(self):
        """Setup event bindings."""
        self.tree.bind("<Double-1>", self._on_double_click)
    
    def _on_double_click(self, event):
        """Handle double-click for cell editing."""
        region = self.tree.identify("region", event.x, event.y)
        
        if region != "cell":
            return
        
        item = self.tree.identify_row(event.y)
        column = self.tree.identify_column(event.x)
        
        if not item or not column:
            return
        
        # Get column index
        col_index = int(column.replace("#", "")) - 1
        col_name = self.columns[col_index]
        
        # Get current value
        values = list(self.tree.item(item, "values"))
        current_value = values[col_index]
        
        # Create edit entry
        self._edit_cell(item, col_index, col_name, current_value)
    
    def _edit_cell(self, item: str, col_index: int, col_name: str, 
                   current_value: str):
        """
        Create entry widget for cell editing.
        
        Args:
            item: Tree item ID
            col_index: Column index
            col_name: Column name
            current_value: Current cell value
        """
        # Get cell coordinates
        bbox = self.tree.bbox(item, col_index)
        if not bbox:
            return
        
        x, y, width, height = bbox
        
        # Create entry widget
        entry = tk.Entry(self.tree, width=width)
        entry.insert(0, current_value)
        entry.select_range(0, tk.END)
        entry.focus()
        
        # Position entry over cell
        entry.place(x=x, y=y, width=width, height=height)
        
        def save_edit(event=None):
            new_value = entry.get()
            values = list(self.tree.item(item, "values"))
            values[col_index] = new_value
            self.tree.item(item, values=values)
            
            # Update row color based on validation
            self._update_row_color(item, values)
            
            entry.destroy()
            
            if self.on_cell_edit:
                self.on_cell_edit(item, col_name, new_value)
        
        def cancel_edit(event=None):
            entry.destroy()
        
        entry.bind("<Return>", save_edit)
        entry.bind("<Escape>", cancel_edit)
        entry.bind("<FocusOut>", save_edit)
    
    def _update_row_color(self, item: str, values: List[str]):
        """
        Update row background color based on validation.
        
        Args:
            item: Tree item ID
            values: Row values
        """
        # Map columns to values
        row_data = dict(zip(self.columns, values))
        
        # Validate row
        is_valid = True
        
        if "Phone" in row_data:
            valid, _ = validate_phone(row_data["Phone"])
            is_valid = is_valid and valid
        
        if "Address" in row_data:
            valid, _ = validate_address(row_data["Address"])
            is_valid = is_valid and valid
        
        if "Delivery Fee" in row_data:
            valid, _ = validate_delivery_fee(row_data["Delivery Fee"])
            is_valid = is_valid and valid
        
        # Set tag based on validation and status
        tags = []
        if not is_valid:
            tags.append("invalid")
        elif "Status" in row_data:
            status = row_data["Status"]
            if status in Config.STATUS_COLORS:
                tags.append(f"status_{status}")
        
        self.tree.item(item, tags=tags)
    
    def insert_row(self, values: List[str], index: str = "end") -> str:
        """
        Insert new row into table.
        
        Args:
            values: Row values
            index: Insert position (default: end)
            
        Returns:
            Item ID
        """
        item = self.tree.insert("", index, values=values)
        self._update_row_color(item, values)
        return item
    
    def get_selected_items(self) -> List[str]:
        """
        Get list of selected item IDs.
        
        Returns:
            List of item IDs
        """
        return self.tree.selection()
    
    def get_item_values(self, item: str) -> List[str]:
        """
        Get values for an item.
        
        Args:
            item: Item ID
            
        Returns:
            List of values
        """
        return list(self.tree.item(item, "values"))
    
    def get_all_rows(self) -> List[Dict[str, str]]:
        """
        Get all rows as dictionaries.
        
        Returns:
            List of row dictionaries
        """
        rows = []
        for item in self.tree.get_children():
            values = self.tree.item(item, "values")
            row = dict(zip(self.columns, values))
            rows.append(row)
        return rows
    
    def clear(self):
        """Clear all rows from table."""
        for item in self.tree.get_children():
            self.tree.delete(item)
    
    def delete_item(self, item: str):
        """
        Delete specific item.
        
        Args:
            item: Item ID to delete
        """
        self.tree.delete(item)
    
    def pack(self, **kwargs):
        """Pack the table frame."""
        self.frame.pack(**kwargs)
