"""
Dialog windows for the application.
"""
import tkinter as tk
from tkinter import ttk, messagebox
from typing import List, Callable


class AgentsDialog:
    """
    Dialog for managing delivery agents.
    
    Allows adding, editing, and removing agents from the list.
    """
    
    def __init__(self, parent: tk.Widget, agents: List[str], 
                 on_save: Callable[[List[str]], None]):
        """
        Initialize agents dialog.
        
        Args:
            parent: Parent widget
            agents: Current list of agents
            on_save: Callback to save agents
        """
        self.dialog = tk.Toplevel(parent)
        self.dialog.title("Manage Agents")
        self.dialog.geometry("400x400")
        self.dialog.transient(parent)
        self.dialog.grab_set()
        
        self.agents = agents.copy()
        self.on_save = on_save
        
        self._create_widgets()
        self._center_dialog()
    
    def _create_widgets(self):
        """Create dialog widgets."""
        # Instructions
        label = ttk.Label(
            self.dialog,
            text="Manage delivery agents:",
            font=("Segoe UI", 10, "bold")
        )
        label.pack(pady=10, padx=10)
        
        # Listbox with scrollbar
        list_frame = ttk.Frame(self.dialog)
        list_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        scrollbar = ttk.Scrollbar(list_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.listbox = tk.Listbox(
            list_frame,
            yscrollcommand=scrollbar.set,
            font=("Segoe UI", 10)
        )
        self.listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.config(command=self.listbox.yview)
        
        # Populate listbox
        for agent in self.agents:
            self.listbox.insert(tk.END, agent)
        
        # Entry for new agent
        entry_frame = ttk.Frame(self.dialog)
        entry_frame.pack(fill=tk.X, padx=10, pady=5)
        
        ttk.Label(entry_frame, text="New Agent:").pack(side=tk.LEFT, padx=5)
        self.entry = ttk.Entry(entry_frame)
        self.entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5)
        self.entry.bind("<Return>", lambda e: self._add_agent())
        
        # Buttons
        btn_frame = ttk.Frame(self.dialog)
        btn_frame.pack(fill=tk.X, padx=10, pady=10)
        
        ttk.Button(
            btn_frame,
            text="Add",
            command=self._add_agent
        ).pack(side=tk.LEFT, padx=5)
        
        ttk.Button(
            btn_frame,
            text="Remove Selected",
            command=self._remove_agent
        ).pack(side=tk.LEFT, padx=5)
        
        ttk.Button(
            btn_frame,
            text="Save & Close",
            command=self._save_and_close
        ).pack(side=tk.RIGHT, padx=5)
        
        ttk.Button(
            btn_frame,
            text="Cancel",
            command=self.dialog.destroy
        ).pack(side=tk.RIGHT, padx=5)
    
    def _add_agent(self):
        """Add new agent to list."""
        agent_name = self.entry.get().strip()
        
        if not agent_name:
            messagebox.showwarning(
                "Invalid Input",
                "Agent name cannot be empty.",
                parent=self.dialog
            )
            return
        
        if agent_name in self.agents:
            messagebox.showwarning(
                "Duplicate",
                "This agent already exists.",
                parent=self.dialog
            )
            return
        
        self.agents.append(agent_name)
        self.listbox.insert(tk.END, agent_name)
        self.entry.delete(0, tk.END)
    
    def _remove_agent(self):
        """Remove selected agent from list."""
        selection = self.listbox.curselection()
        
        if not selection:
            messagebox.showwarning(
                "No Selection",
                "Please select an agent to remove.",
                parent=self.dialog
            )
            return
        
        index = selection[0]
        agent = self.listbox.get(index)
        
        confirm = messagebox.askyesno(
            "Confirm Removal",
            f"Remove agent '{agent}'?",
            parent=self.dialog
        )
        
        if confirm:
            self.listbox.delete(index)
            self.agents.remove(agent)
    
    def _save_and_close(self):
        """Save agents and close dialog."""
        if not self.agents:
            messagebox.showwarning(
                "Empty List",
                "You must have at least one agent.",
                parent=self.dialog
            )
            return
        
        self.on_save(self.agents)
        self.dialog.destroy()
    
    def _center_dialog(self):
        """Center dialog on parent window."""
        self.dialog.update_idletasks()
        width = self.dialog.winfo_width()
        height = self.dialog.winfo_height()
        x = (self.dialog.winfo_screenwidth() // 2) - (width // 2)
        y = (self.dialog.winfo_screenheight() // 2) - (height // 2)
        self.dialog.geometry(f"{width}x{height}+{x}+{y}")
