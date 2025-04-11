"""
Base summarizer interface.
"""

from abc import ABC, abstractmethod
from typing import Dict, Any


class BaseSummarizer(ABC):
    """Base class for all summarizers."""
    
    @abstractmethod
    def generate_summary(self, data: Dict[str, Any]) -> str:
        """
        Generate a summary from the provided data.
        
        Args:
            data: Data to summarize
            
        Returns:
            Generated summary text
        """
        pass
