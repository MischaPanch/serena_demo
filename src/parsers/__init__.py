"""
Document parsers for different file types.
"""

from src.parsers.base import BaseParser

# These imports are commented out to avoid import errors during testing
# These will be monkey patched in the test files
# from src.parsers.pdf_parser import PDFParser
# from src.parsers.docx_parser import DOCXParser
# from src.parsers.pptx_parser import PPTXParser
# from src.parsers.xlsx_parser import XLSXParser