"""
Reusable UI components for the application.
"""
import tkinter as tk
from tkinter import ttk
from typing import Callable, List, Dict
from ..config import Config


class Toolbar:
    """
    Toolbar with action buttons.
    
    Provides buttons for common operations like Add, Save, Load, etc.
    """
    
    def __init__(self, parent: tk.Widget, callbacks: Dict[str, Callable]):
        """
        Initialize toolbar.
        
        Args:
            parent: Parent widget
            callbacks: Dictionary mapping button names to callback functions
        """
        self.frame = ttk.Frame(parent)
        self.callbacks = callbacks
        self._create_buttons()
    
    def _create_buttons(self):
        """Create toolbar buttons."""
        buttons = [
            ("Add Row", "add_row"),
            ("Delete Selected", "delete_selected"),
            ("Save CSV", "save_csv"),
            ("Load CSV", "load_csv"),
            ("Manage Agents", "manage_agents"),
            ("Clear All", "clear_all")
        ]
        
        for text, callback_key in buttons:
            if callback_key in self.callbacks:
                btn = ttk.Button(
                    self.frame,
                    text=text,
                    command=self.callbacks[callback_key]
                )
                btn.pack(side=tk.LEFT, padx=5, pady=5)
    
    def pack(self, **kwargs):
        """Pack the toolbar frame."""
        self.frame.pack(**kwargs)


class FilterPanel:
    """
    Status filter panel with checkboxes.
    
    Allows users to filter orders by status.
    """
    
    def __init__(self, parent: tk.Widget, statuses: List[str], 
                 on_filter_change: Callable):
        """
        Initialize filter panel.
        
        Args:
            parent: Parent widget
            statuses: List of available statuses
            on_filter_change: Callback when filter changes
        """
        self.frame = ttk.LabelFrame(parent, text="Filter by Status", padding=10)
        self.statuses = statuses
        self.on_filter_change = on_filter_change
        self.status_vars = {}
        self._create_checkboxes()
    
    def _create_checkboxes(self):
        """Create status filter checkboxes."""
        for status in self.statuses:
            var = tk.BooleanVar(value=True)
            self.status_vars[status] = var
            
            cb = ttk.Checkbutton(
                self.frame,
                text=status,
                variable=var,
                command=self.on_filter_change
            )
            cb.pack(anchor=tk.W, pady=2)
    
    def get_active_statuses(self) -> List[str]:
        """
        Get list of statuses that are currently filtered.
        
        Returns:
            List of active status names
        """
        return [
            status for status, var in self.status_vars.items()
            if var.get()
        ]
    
    def pack(self, **kwargs):
        """Pack the filter panel frame."""
        self.frame.pack(**kwargs)


class StatusButtons:
    """
    Quick status update buttons.
    
    Provides buttons for bulk status updates.
    """
    
    def __init__(self, parent: tk.Widget, statuses: List[str],
                 on_status_click: Callable):
        """
        Initialize status buttons.
        
        Args:
            parent: Parent widget
            statuses: List of available statuses
            on_status_click: Callback when status button clicked
        """
        self.frame = ttk.LabelFrame(parent, text="Bulk Status Update", padding=10)
        self.statuses = statuses
        self.on_status_click = on_status_click
        self._create_buttons()
    
    def _create_buttons(self):
        """Create status update buttons."""
        for status in self.statuses:
            btn = ttk.Button(
                self.frame,
                text=f"Set to {status}",
                command=lambda s=status: self.on_status_click(s)
            )
            btn.pack(fill=tk.X, pady=2)
    
    def pack(self, **kwargs):
        """Pack the status buttons frame."""
        self.frame.pack(**kwargs)
