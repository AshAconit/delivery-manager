"""
Address history management.
"""
import os
from typing import List
from ..config import Config


class AddressManager:
    """Manages address history for autocomplete."""
    
    def __init__(self, addresses_file: str = None):
        """
        Initialize address manager.
        
        Args:
            addresses_file: Path to addresses file (default from Config)
        """
        self.addresses_file = addresses_file or Config.ADDRESSES_FILE
    
    def load_addresses(self) -> List[str]:
        """
        Load addresses from history file.
        
        Returns:
            List of addresses (most recent first)
        """
        if not os.path.exists(self.addresses_file):
            return []
        
        try:
            with open(self.addresses_file, 'r', encoding='utf-8') as f:
                addresses = [line.strip() for line in f if line.strip()]
                return addresses
        except Exception as e:
            print(f"Error loading addresses: {e}")
            return []
    
    def save_address(self, address: str):
        """
        Save address to history.
        
        Maintains max history size defined in Config.MAX_ADDRESS_HISTORY.
        Avoids duplicates by moving existing address to top.
        
        Args:
            address: Address to save
        """
        if not address or not address.strip():
            return
        
        address = address.strip()
        addresses = self.load_addresses()
        
        # Remove duplicate if exists
        if address in addresses:
            addresses.remove(address)
        
        # Add to top
        addresses.insert(0, address)
        
        # Limit history size
        addresses = addresses[:Config.MAX_ADDRESS_HISTORY]
        
        # Save back to file
        try:
            with open(self.addresses_file, 'w', encoding='utf-8') as f:
                for addr in addresses:
                    f.write(f"{addr}\n")
        except Exception as e:
            print(f"Error saving address: {e}")
    
    def clear_history(self):
        """Clear all address history."""
        try:
            if os.path.exists(self.addresses_file):
                os.remove(self.addresses_file)
        except Exception as e:
            print(f"Error clearing address history: {e}")
