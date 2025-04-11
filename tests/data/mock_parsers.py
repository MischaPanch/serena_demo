"""
Mock PDF parser for testing.
"""

import logging
import os
from typing import List

from src.parsers.base import BaseParser

logger = logging.getLogger(__name__)


class PDFParser(BaseParser):
    """Parser for PDF documents."""
    
    @staticmethod
    def supported_mime_types() -> List[str]:
        """
        Get the list of MIME types supported by this parser.
        
        Returns:
            List of supported MIME types
        """
        return ['application/pdf']
    
    @classmethod
    def can_parse(cls, mime_type: str) -> bool:
        """
        Check if this parser can handle the given mime type.
        
        Args:
            mime_type: MIME type of the document
            
        Returns:
            True if this parser can handle the mime type, False otherwise
        """
        return mime_type in cls.supported_mime_types() or mime_type.endswith('/pdf')
    
    def parse(self, file_path: str) -> str:
        """
        Parse a PDF file and extract text content.
        
        Args:
            file_path: Path to the PDF file
            
        Returns:
            Extracted text content
        """
        # This is a mock implementation for testing
        return f"Title: Mock PDF\nAuthor: Test Author\n\n--- Page 1 ---\nMock PDF content for testing"