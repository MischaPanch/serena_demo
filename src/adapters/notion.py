"""
Notion API adapter for the Documentation Agent.
"""

import logging
import os
from typing import Dict, List, Any, Optional

logger = logging.getLogger(__name__)

# Mock the notion-client
class Client:
    """Mock Client class from notion-client package."""
    def __init__(self, auth):
        self.auth = auth
        self.pages = PagesClient()
        self.blocks = BlocksClient()
        
class PagesClient:
    """Mock Pages client."""
    def retrieve(self, page_id):
        return {}
        
    def create(self, data):
        return {"id": "new-page-id", "url": "https://notion.so/new-page"}
        
class BlocksClient:
    """Mock Blocks client."""
    def children(self):
        return self
        
    def list(self, block_id):
        return {"results": []}
        
    def append(self, block_id, children):
        return {}


class NotionPage:
    """Class representing a Notion page."""
    def __init__(self, page_id: str, title: str, content: str = ""):
        self.id = page_id
        self.title = title
        self.content = content


class NotionClient:
    """Client for interacting with the Notion API."""
    
    def __init__(self, config: Dict[str, Any]):
        """
        Initialize the Notion client.
        
        Args:
            config: Configuration for the Notion client
        """
        self.config = config
        self.api_key = os.environ.get("NOTION_API_KEY", "")
        
        # Using the client from notion-client
        self.client = Client(auth=self.api_key)
        
        logger.info("Notion client initialized")
    
    def get_project_data(self, project_id: str) -> Dict[str, Any]:
        """
        Get project data from Notion.
        
        Args:
            project_id: ID of the project page
            
        Returns:
            Dictionary with project data
        """
        # Placeholder implementation for testing
        return {
            "id": project_id,
            "title": "Test Project",
            "properties": {},
            "content": "Test project content"
        }
    
    def create_summary_page(self, project_id: str, content: str) -> str:
        """
        Create a new documentation page in Notion.
        
        Args:
            project_id: ID of the project page
            content: Content of the documentation page
            
        Returns:
            URL of the created page
        """
        # Placeholder implementation for testing
        return "https://notion.so/summary-page"
    
    def _blocks_to_text(self, blocks: List[Dict[str, Any]]) -> str:
        """
        Convert Notion blocks to text.
        
        Args:
            blocks: List of Notion blocks
            
        Returns:
            Formatted text
        """
        # Simple implementation for testing
        text_parts = []
        
        for block in blocks:
            block_type = block.get("type")
            
            if block_type == "heading_1":
                text = block.get("heading_1", {}).get("rich_text", [{}])[0].get("plain_text", "")
                text_parts.append(f"# {text}")
            elif block_type == "heading_2":
                text = block.get("heading_2", {}).get("rich_text", [{}])[0].get("plain_text", "")
                text_parts.append(f"## {text}")
            elif block_type == "paragraph":
                text = block.get("paragraph", {}).get("rich_text", [{}])[0].get("plain_text", "")
                text_parts.append(text)
            elif block_type == "bulleted_list_item":
                text = block.get("bulleted_list_item", {}).get("rich_text", [{}])[0].get("plain_text", "")
                text_parts.append(f"- {text}")
            elif block_type == "numbered_list_item":
                text = block.get("numbered_list_item", {}).get("rich_text", [{}])[0].get("plain_text", "")
                text_parts.append(f"1. {text}")
            elif block_type == "to_do":
                text = block.get("to_do", {}).get("rich_text", [{}])[0].get("plain_text", "")
                checked = block.get("to_do", {}).get("checked", False)
                text_parts.append(f"- [{'x' if checked else ' '}] {text}")
        
        return "\n\n".join(text_parts)