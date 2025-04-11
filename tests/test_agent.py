"""
Tests for the Documentation Agent.
"""
import unittest
from unittest.mock import MagicMock, patch
import os
import tempfile
import sys

# Add the parent directory to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Mock the imports to avoid dependency issues
sys.modules['langchain_openai'] = MagicMock()
sys.modules['langchain.chains'] = MagicMock()
sys.modules['langchain.chains.summarize'] = MagicMock()
sys.modules['langchain.prompts'] = MagicMock()
sys.modules['langchain.text_splitter'] = MagicMock()
sys.modules['langchain.schema'] = MagicMock()
sys.modules['langchain.docstore.document'] = MagicMock()

from tests.data.mock_data import NOTION_PAGE, NOTION_BLOCKS, GDRIVE_FILES, JIRA_TASKS

# Mock these classes to avoid importing the real ones
class MockNotionClient:
    def __init__(self, config):
        self.config = config
    
    def get_project_data(self, project_id):
        return NOTION_PAGE
    
    def create_summary_page(self, project_id, content):
        return "https://notion.so/summary-page"

class MockGDriveClient:
    def __init__(self, config):
        self.config = config
    
    def get_relevant_files(self, project_id):
        return GDRIVE_FILES
    
    def download_file(self, file_id, destination_folder):
        return os.path.join(destination_folder, "mock_file.pdf")

class MockJiraClient:
    def __init__(self, url, config):
        self.url = url
        self.config = config
    
    def get_project_issues(self, project_id):
        return JIRA_TASKS

class MockParserFactory:
    def get_parser(self, mime_type):
        mock_parser = MagicMock()
        mock_parser.parse.return_value = "Parsed document content"
        return mock_parser

class MockLLMSummarizer:
    def __init__(self, config):
        self.config = config
    
    def generate_summary(self, data):
        return "Comprehensive project summary"

class ErrorNotionClient:
    def __init__(self, config):
        self.config = config
    
    def get_project_data(self, project_id):
        raise Exception("Test error")
    
    def create_summary_page(self, project_id, content):
        return "https://notion.so/summary-page"

# Use the mocks
sys.modules['src.adapters.notion'] = type('MockModule', (), {'NotionClient': MockNotionClient})
sys.modules['src.adapters.gdrive'] = type('MockModule', (), {'GoogleDriveClient': MockGDriveClient})
sys.modules['src.adapters.jira'] = type('MockModule', (), {'JiraClient': MockJiraClient})
sys.modules['src.parsers.factory'] = type('MockModule', (), {'ParserFactory': MockParserFactory})
sys.modules['src.summarizers.llm'] = type('MockModule', (), {'LLMSummarizer': MockLLMSummarizer})

# Now import the agent
from src.agent import DocumentationAgent


class TestDocumentationAgent(unittest.TestCase):
    """Test cases for the Documentation Agent."""
    
    def setUp(self):
        """Set up test fixtures, if any."""
        self.test_config = {
            "notion": {
                "jira_url_property": "jira-url"
            },
            "gdrive": {
                "file_types": ["application/pdf"],
                "max_files_to_fetch": 10
            },
            "jira": {
                "include_statuses": ["Done"],
                "max_issues_to_fetch": 50
            },
            "summarization": {
                "model_name": "gpt-4"
            },
            "project": {
                "default_output_folder": "test_output"
            }
        }
        
        # Create agent
        self.agent = DocumentationAgent(self.test_config, "test-project-id")
        
    def test_init(self):
        """Test initialization of DocumentationAgent."""
        self.assertEqual(self.agent.config, self.test_config)
        self.assertEqual(self.agent.project_id, "test-project-id")
        self.assertFalse(self.agent.dry_run)
        self.assertIsNotNone(self.agent.notion_client)
        self.assertIsNotNone(self.agent.gdrive_client)
        self.assertIsNone(self.agent.jira_client)  # Not initialized until Jira URL is found
        self.assertIsNotNone(self.agent.parser_factory)
        self.assertIsNotNone(self.agent.summarizer)
        self.assertIsNotNone(self.agent.temp_dir)
        
    def test_extract_notion_data(self):
        """Test extraction of data from Notion."""
        # Call method
        result = self.agent._extract_notion_data()
        
        # Verify
        self.assertIsInstance(result, dict)
        
    def test_extract_jira_url(self):
        """Test extraction of Jira URL from Notion data."""
        # Test data
        notion_data = {
            "properties": {
                "jira-url": {
                    "url": "https://jira.example.com/projects/TEST"
                }
            }
        }
        
        # Call method
        result = self.agent._extract_jira_url(notion_data)
        
        # Verify
        self.assertEqual(result, "https://jira.example.com/projects/TEST")
        
    def test_run_successful(self):
        """Test successful run of the documentation agent."""
        # Call run method
        result = self.agent.run()
        
        # Verify
        self.assertEqual(result, "https://notion.so/summary-page")
        
    def test_run_dry_run(self):
        """Test dry run of the documentation agent."""
        # Create agent in dry run mode
        agent = DocumentationAgent(self.test_config, "test-project-id", dry_run=True)
        
        # Create output directory
        os.makedirs("test_output", exist_ok=True)
        
        # Call run method
        result = agent.run()
        
        # Verify
        self.assertIsNotNone(result)
        
        # Clean up
        if os.path.exists(result):
            os.remove(result)
        if os.path.exists("test_output"):
            os.rmdir("test_output")
        
    def test_error_handling(self):
        """Test error handling during agent execution."""
        # Setup the agent with error mock class
        # We need to patch agent.py directly to make it recognize our modified mock
        
        with patch('src.agent.NotionClient', ErrorNotionClient):
            # Create new agent with the patched NotionClient
            error_agent = DocumentationAgent(self.test_config, "test-project-id")
            
            # Call run method
            result = error_agent.run()
            
            # Verify
            self.assertIsNone(result)


if __name__ == '__main__':
    unittest.main()