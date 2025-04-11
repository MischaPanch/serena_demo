"""
Tests for document parsers.
"""

import unittest
from unittest.mock import MagicMock, patch
import os
import tempfile
import sys

# Add the parent directory to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.parsers.base import BaseParser


class MockPDFParser(BaseParser):
    """Mock PDF parser for testing."""
    
    @staticmethod
    def supported_mime_types():
        return ['application/pdf']
    
    @classmethod
    def can_parse(cls, mime_type):
        return mime_type in cls.supported_mime_types() or mime_type.endswith('/pdf')
    
    def parse(self, file_path):
        return "Mock PDF content"


class MockDOCXParser(BaseParser):
    """Mock DOCX parser for testing."""
    
    @staticmethod
    def supported_mime_types():
        return ['application/vnd.openxmlformats-officedocument.wordprocessingml.document']
    
    @classmethod
    def can_parse(cls, mime_type):
        return mime_type in cls.supported_mime_types() or 'word' in mime_type.lower()
    
    def parse(self, file_path):
        return "Mock DOCX content"


class MockPPTXParser(BaseParser):
    """Mock PPTX parser for testing."""
    
    @staticmethod
    def supported_mime_types():
        return ['application/vnd.openxmlformats-officedocument.presentationml.presentation']
    
    @classmethod
    def can_parse(cls, mime_type):
        return mime_type in cls.supported_mime_types() or 'powerpoint' in mime_type.lower()
    
    def parse(self, file_path):
        return "Mock PPTX content"


class MockXLSXParser(BaseParser):
    """Mock XLSX parser for testing."""
    
    @staticmethod
    def supported_mime_types():
        return ['application/vnd.openxmlformats-officedocument.spreadsheetml.sheet']
    
    @classmethod
    def can_parse(cls, mime_type):
        return mime_type in cls.supported_mime_types() or 'excel' in mime_type.lower()
    
    def parse(self, file_path):
        return "Mock XLSX content"


# Mock the imports
sys.modules['src.parsers.pdf_parser'] = type('MockModule', (), {'PDFParser': MockPDFParser})
sys.modules['src.parsers.docx_parser'] = type('MockModule', (), {'DOCXParser': MockDOCXParser})
sys.modules['src.parsers.pptx_parser'] = type('MockModule', (), {'PPTXParser': MockPPTXParser})
sys.modules['src.parsers.xlsx_parser'] = type('MockModule', (), {'XLSXParser': MockXLSXParser})

# Now import the factory
from src.parsers.factory import ParserFactory


class TestParserFactory(unittest.TestCase):
    """Test cases for the parser factory."""
    
    def setUp(self):
        """Set up test fixtures, if any."""
        self.factory = ParserFactory()
    
    def test_get_parser_for_pdf(self):
        """Test getting parser for PDF documents."""
        parser = self.factory.get_parser("application/pdf")
        self.assertIsInstance(parser, MockPDFParser)
    
    def test_get_parser_for_docx(self):
        """Test getting parser for DOCX documents."""
        parser = self.factory.get_parser("application/vnd.openxmlformats-officedocument.wordprocessingml.document")
        self.assertIsInstance(parser, MockDOCXParser)
    
    def test_get_parser_for_pptx(self):
        """Test getting parser for PPTX documents."""
        parser = self.factory.get_parser("application/vnd.openxmlformats-officedocument.presentationml.presentation")
        self.assertIsInstance(parser, MockPPTXParser)
    
    def test_get_parser_for_xlsx(self):
        """Test getting parser for XLSX documents."""
        parser = self.factory.get_parser("application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
        self.assertIsInstance(parser, MockXLSXParser)
    
    def test_get_parser_for_unknown_type(self):
        """Test getting parser for unknown document type."""
        parser = self.factory.get_parser("application/unknown")
        self.assertIsNone(parser)


if __name__ == '__main__':
    unittest.main()