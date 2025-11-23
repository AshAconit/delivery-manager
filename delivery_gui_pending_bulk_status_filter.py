#!/usr/bin/env python3
"""
Delivery Manager GUI - Backward compatibility wrapper.

This file maintains backward compatibility with the original monolithic structure.
The application has been refactored into a modular architecture.

New structure:
- src/config.py - Configuration and constants
- src/models/ - Data models (Order, Product, OrderLine)
- src/validators/ - Validation functions
- src/utils/ - Utility functions (formatters, parsers)
- src/data/ - Data access layer (CSV, agents, addresses, products)
- src/ui/ - UI components (table, dialogs, components, main window)
- src/main.py - Application entry point

To run the application, execute this file or run: python -m src.main
"""

from src.main import main

if __name__ == "__main__":
    main()
