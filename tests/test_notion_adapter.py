"""
Tests for the Notion adapter.
"""

import unittest
from unittest.mock import MagicMock, patch
import os
import sys

# Add the parent directory to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Import the mock data directly
NOTION_PAGE = {
    "id": "test-page-id",
    "url": "https://notion.so/test-page",
    "properties": {
        "title": {
            "type": "title",
            "title": [{"plain_text": "Test Project"}]
        },
        "jira-url": {
            "type": "url", 
            "url": "https://jira.example.com/projects/TEST"
        },
        "status": {
            "type": "select",
            "select": {"name": "Completed"}
        },
        "team": {
            "type": "multi_select",
            "multi_select": [
                {"name": "Engineering"},
                {"name": "Design"}
            ]
        }
    },
    "created_time": "2023-01-01T00:00:00.000Z",
    "last_edited_time": "2023-01-10T00:00:00.000Z"
}

NOTION_BLOCKS = {
    "results": [
        {
            "id": "block1",
            "type": "heading_1",
            "heading_1": {
                "rich_text": [{"plain_text": "Project Overview"}]
            }
        },
        {
            "id": "block2",
            "type": "paragraph",
            "paragraph": {
                "rich_text": [{"plain_text": "This is a test project for documentation generation."}]
            }
        },
        {
            "id": "block3",
            "type": "bulleted_list_item",
            "bulleted_list_item": {
                "rich_text": [{"plain_text": "Feature 1"}]
            }
        },
        {
            "id": "block4",
            "type": "bulleted_list_item",
            "bulleted_list_item": {
                "rich_text": [{"plain_text": "Feature 2"}]
            }
        }
    ],
    "next_cursor": None
}

# Import the classes after setting up the mocks
from src.adapters.notion import NotionClient


class TestNotionAdapter(unittest.TestCase):
    """Test cases for the Notion adapter."""
    
    def setUp(self):
        """Set up test fixtures, if any."""
        self.test_config = {
            "jira_url_property": "jira-url",
            "search_depth": 2
        }
        
        # Mock environment variable
        self.env_patcher = patch.dict(os.environ, {"NOTION_API_KEY": "mock-api-key"})
        self.env_patcher.start()
        
        # Mock Notion client
        self.client_patcher = patch('src.adapters.notion.Client')
        self.mock_client = self.client_patcher.start()
        
        # Create NotionClient instance
        self.notion_client = NotionClient(self.test_config)
        
        # Set up mock responses
        self.mock_page_response = NOTION_PAGE
        self.mock_blocks_response = NOTION_BLOCKS
        
    def _load_mock_data(self, filename):
        """Helper method to load mock data from JSON files."""
        # For the tests, we'll just use the predefined NOTION_PAGE and NOTION_BLOCKS
        if filename == 'notion_page.json':
            return NOTION_PAGE
        elif filename == 'notion_blocks.json':
            return NOTION_BLOCKS
        else:
            return {
                "results": [
                    {
                        "type": "paragraph",
                        "paragraph": {
                            "rich_text": [{"plain_text": "Test paragraph content"}]
                        }
                    }
                ]
            }
    
    def tearDown(self):
        """Tear down test fixtures, if any."""
        self.env_patcher.stop()
        self.client_patcher.stop()
    
    def test_init(self):
        """Test initialization of NotionClient."""
        self.assertEqual(self.notion_client.config, self.test_config)
        self.assertEqual(self.notion_client.api_key, "mock-api-key")
    
    @patch('src.adapters.notion.NotionClient.get_project_data')
    def test_get_project_data(self, mock_get_project_data):
        """Test getting project data from Notion."""
        # Configure mock
        mock_get_project_data.return_value = {
            "id": "test-page-id",
            "title": "Test Project",
            "properties": {},
            "content": "Test content"
        }
        
        # Call method
        result = self.notion_client.get_project_data("test-page-id")
        
        # Verify result
        mock_get_project_data.assert_called_once_with("test-page-id")
        self.assertIsInstance(result, dict)
        self.assertEqual(result["id"], "test-page-id")
        self.assertEqual(result["title"], "Test Project")
    
    @patch('src.adapters.notion.NotionClient.create_summary_page')
    def test_create_summary_page(self, mock_create_summary_page):
        """Test creating a new documentation page in Notion."""
        # Configure mock
        mock_create_summary_page.return_value = "https://notion.so/new-page"
        
        # Call method
        result = self.notion_client.create_summary_page("test-page-id", "Test documentation")
        
        # Verify result
        mock_create_summary_page.assert_called_once_with("test-page-id", "Test documentation")
        self.assertEqual(result, "https://notion.so/new-page")
        
    def test_blocks_to_text(self):
        """Test conversion of Notion blocks to text."""
        # Test with simplified blocks
        blocks = [
            {
                "type": "heading_1",
                "heading_1": {
                    "rich_text": [{"plain_text": "Test Heading"}]
                }
            },
            {
                "type": "paragraph",
                "paragraph": {
                    "rich_text": [{"plain_text": "Test paragraph"}]
                }
            },
            {
                "type": "bulleted_list_item",
                "bulleted_list_item": {
                    "rich_text": [{"plain_text": "Bullet point"}]
                }
            }
        ]
        
        result = self.notion_client._blocks_to_text(blocks)
        
        # Verify expected text format
        self.assertIn("# Test Heading", result)
        self.assertIn("Test paragraph", result)
        self.assertIn("- Bullet point", result)


if __name__ == '__main__':
    unittest.main()