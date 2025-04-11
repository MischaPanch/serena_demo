"""
Parser for PDF documents.
"""

import logging
import os
import PyPDF2
from typing import List, Set

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
        if not os.path.exists(file_path):
            logger.error(f"PDF file not found: {file_path}")
            return ""
        
        try:
            text_content = []
            
            with open(file_path, 'rb') as file:
                pdf_reader = PyPDF2.PdfReader(file)
                
                # Get document info (metadata)
                info = pdf_reader.metadata
                if info:
                    title = info.title or os.path.basename(file_path)
                    author = info.author or "Unknown"
                    text_content.append(f"Title: {title}")
                    text_content.append(f"Author: {author}")
                    text_content.append("")  # Empty line
                
                # Extract text from each page
                num_pages = len(pdf_reader.pages)
                logger.debug(f"Extracting text from {num_pages} pages in {file_path}")
                
                for page_num in range(num_pages):
                    page = pdf_reader.pages[page_num]
                    page_text = page.extract_text()
                    
                    if page_text:
                        text_content.append(f"--- Page {page_num + 1} ---")
                        text_content.append(page_text)
                        text_content.append("")  # Empty line
            
            return "\n".join(text_content)
            
        except Exception as e:
            logger.exception(f"Error parsing PDF file {file_path}: {e}")
            return f"Error parsing PDF file: {str(e)}"
