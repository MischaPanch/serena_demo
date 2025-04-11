"""
Base parser interface for document parsers.
"""

from abc import ABC, abstractmethod
from typing import Optional


class BaseParser(ABC):
    """Base class for all document parsers."""
    
    @abstractmethod
    def parse(self, file_path: str) -> str:
        """
        Parse the document and extract text content.
        
        Args:
            file_path: Path to the document file
            
        Returns:
            Extracted text content
        """
        pass
    
    @staticmethod
    def supported_mime_types() -> list:
        """
        Get the list of MIME types supported by this parser.
        
        Returns:
            List of supported MIME types
        """
        return []
    
    @classmethod
    def can_parse(cls, mime_type: str) -> bool:
        """
        Check if this parser can handle the given mime type.
        
        Args:
            mime_type: MIME type of the document
            
        Returns:
            True if this parser can handle the mime type, False otherwise
        """
        return False
