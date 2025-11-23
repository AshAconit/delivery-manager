"""
Main entry point for Delivery Manager application.
"""
import tkinter as tk
from .ui.main_window import DeliveryApp


def main():
    """Initialize and run the application."""
    root = tk.Tk()
    app = DeliveryApp(root)
    app.run()


if __name__ == "__main__":
    main()
