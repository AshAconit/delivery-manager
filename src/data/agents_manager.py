"""
Agent management for delivery personnel.
"""
import os
from typing import List
from ..config import Config


class AgentManager:
    """Manages delivery agents list."""
    
    def __init__(self, agents_file: str = None):
        """
        Initialize agent manager.
        
        Args:
            agents_file: Path to agents file (default from Config)
        """
        self.agents_file = agents_file or Config.AGENTS_FILE
    
    def load_agents(self) -> List[str]:
        """
        Load agents from file.
        
        Returns:
            List of agent names
        """
        if not os.path.exists(self.agents_file):
            return self.get_default_agents()
        
        try:
            with open(self.agents_file, 'r', encoding='utf-8') as f:
                agents = [line.strip() for line in f if line.strip()]
                return agents if agents else self.get_default_agents()
        except Exception as e:
            print(f"Error loading agents: {e}")
            return self.get_default_agents()
    
    def save_agents(self, agents: List[str]):
        """
        Save agents to file.
        
        Args:
            agents: List of agent names to save
        """
        try:
            with open(self.agents_file, 'w', encoding='utf-8') as f:
                for agent in agents:
                    if agent.strip():
                        f.write(f"{agent.strip()}\n")
        except Exception as e:
            print(f"Error saving agents: {e}")
    
    def get_default_agents(self) -> List[str]:
        """
        Get default list of agents.
        
        Returns:
            Default agent names from Config
        """
        return Config.DEFAULT_AGENTS.copy()
