"""
Factory for document parsers.
"""

import logging
from typing import Dict, Optional, Type

from src.parsers.base import BaseParser
from src.parsers.pdf_parser import PDFParser
from src.parsers.docx_parser import DOCXParser
from src.parsers.pptx_parser import PPTXParser
from src.parsers.xlsx_parser import XLSXParser

logger = logging.getLogger(__name__)


class ParserFactory:
    """Factory for creating document parsers based on document type."""
    
    def __init__(self):
        """Initialize the parser factory with all available parsers."""
        self.parsers: Dict[str, Type[BaseParser]] = {}
        self._register_parsers()
    
    def _register_parsers(self):
        """Register all available parsers."""
        for parser_cls in [PDFParser, DOCXParser, PPTXParser, XLSXParser]:
            for mime_type in parser_cls.supported_mime_types():
                self.parsers[mime_type] = parser_cls
        
        logger.debug(f"Registered parsers for MIME types: {list(self.parsers.keys())}")
    
    def get_parser(self, mime_type: str) -> Optional[BaseParser]:
        """
        Get a parser for the given MIME type.
        
        Args:
            mime_type: MIME type of the document
            
        Returns:
            Parser instance if available, None otherwise
        """
        parser_cls = self.parsers.get(mime_type)
        
        if not parser_cls:
            # Try to find a compatible parser
            for cls in [PDFParser, DOCXParser, PPTXParser, XLSXParser]:
                if cls.can_parse(mime_type):
                    parser_cls = cls
                    break
        
        if parser_cls:
            try:
                return parser_cls()
            except Exception as e:
                logger.error(f"Error creating parser for MIME type {mime_type}: {e}")
                return None
        
        logger.warning(f"No parser available for MIME type: {mime_type}")
        return None
