"""
Tests for the LLM summarizer.
"""

import unittest
from unittest.mock import MagicMock, patch
import os
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

from tests.data.mock_data import NOTION_PAGE, GDRIVE_FILES, JIRA_TASKS

# Now that we've set up mocks, we can import the module
from src.summarizers.llm import LLMSummarizer


class TestLLMSummarizer(unittest.TestCase):
    """Test cases for the LLM summarizer."""
    
    def setUp(self):
        """Set up test fixtures, if any."""
        self.test_config = {
            "model_name": "gpt-4",
            "temperature": 0.2,
            "max_tokens": 2000,
            "chunk_size": 4000,
            "chunk_overlap": 200
        }
        
        # Mock environment variable
        self.env_patcher = patch.dict(os.environ, {"OPENAI_API_KEY": "mock-api-key"})
        self.env_patcher.start()
        
        # Mock LangChain components
        self.chat_openai_patcher = patch('src.summarizers.llm.ChatOpenAI')
        self.mock_chat_openai = self.chat_openai_patcher.start()
        
        self.llm_chain_patcher = patch('src.summarizers.llm.LLMChain')
        self.mock_llm_chain = self.llm_chain_patcher.start()
        
        self.summarize_chain_patcher = patch('src.summarizers.llm.load_summarize_chain')
        self.mock_summarize_chain = self.summarize_chain_patcher.start()
        
        # Configure mock chain
        mock_chain_instance = MagicMock()
        mock_chain_instance.run.return_value = "Test summary content"
        self.mock_llm_chain.return_value = mock_chain_instance
        self.mock_summarize_chain.return_value = mock_chain_instance
        
        # Create LLMSummarizer instance
        self.summarizer = LLMSummarizer(self.test_config)
        
        # Mock test data
        self.notion_data = {
            "id": "test-page-id",
            "title": "Test Project",
            "content": "Test project content with multiple paragraphs.\n\nSecond paragraph of test content."
        }
        
        self.drive_documents = [
            {
                "id": "doc1",
                "name": "Test Document",
                "type": "application/pdf",
                "content": "Test document content",
                "url": "https://drive.google.com/doc1"
            }
        ]
        
        self.jira_tasks = [
            {
                "key": "TEST-1",
                "summary": "Test task",
                "issue_type": {"name": "Task"},
                "status": {"name": "Done"}
            }
        ]
        
    def tearDown(self):
        """Tear down test fixtures, if any."""
        self.env_patcher.stop()
        self.chat_openai_patcher.stop()
        self.llm_chain_patcher.stop()
        self.summarize_chain_patcher.stop()
    
    def test_init(self):
        """Test initialization of LLMSummarizer."""
        self.assertEqual(self.summarizer.config, self.test_config)
        self.assertEqual(self.summarizer.api_key, "mock-api-key")
        self.assertEqual(self.summarizer.model_name, "gpt-4")
        self.assertEqual(self.summarizer.temperature, 0.2)
        self.assertEqual(self.summarizer.max_tokens, 2000)
        self.assertEqual(self.summarizer.chunk_size, 4000)
        self.assertEqual(self.summarizer.chunk_overlap, 200)
        
    def test_generate_summary(self):
        """Test generation of a comprehensive summary."""
        # Prepare test data
        test_data = {
            "notion_data": self.notion_data,
            "drive_documents": self.drive_documents,
            "jira_tasks": self.jira_tasks,
            "project_id": "TEST-123"
        }
        
        # Get summary
        result = self.summarizer.generate_summary(test_data)
        
        # Verify calls and result
        self.assertIn("Project Summary: TEST-123", result)
        self.assertIn("Generated on:", result)
        
    def test_summarize_notion_data(self):
        """Test summarization of Notion data."""
        result = self.summarizer._summarize_notion_data(self.notion_data)
        
        # Verify result format
        self.assertIn("# Project Overview", result)
        self.assertIn("## Test Project", result)
        
    def test_summarize_drive_documents(self):
        """Test summarization of Google Drive documents."""
        result = self.summarizer._summarize_drive_documents(self.drive_documents)
        
        # Verify result format
        self.assertIn("# Project Documents", result)
        self.assertIn("### Test Document", result)
        self.assertIn("- Type: application/pdf", result)
        
    def test_summarize_jira_tasks(self):
        """Test summarization of Jira tasks."""
        result = self.summarizer._summarize_jira_tasks(self.jira_tasks)
        
        # Verify result format
        self.assertIn("# Project Tasks", result)
        self.assertIn("## Task", result)
        self.assertIn("[TEST-1]", result)
        
    def test_empty_data(self):
        """Test handling of empty data."""
        empty_data = {
            "notion_data": {},
            "drive_documents": [],
            "jira_tasks": [],
            "project_id": "EMPTY-123"
        }
        
        result = self.summarizer.generate_summary(empty_data)
        
        # Verify result still contains project ID
        self.assertIn("Project Summary: EMPTY-123", result)
        
    def test_no_llm(self):
        """Test behavior when LLM is not initialized."""
        # Create new summarizer with no LLM
        with patch.dict(os.environ, {"OPENAI_API_KEY": ""}):
            summarizer = LLMSummarizer(self.test_config)
            
            # Try to generate summary
            result = summarizer.generate_summary({"project_id": "TEST-123"})
            
            # Verify error message
            self.assertIn("Error: LLM not initialized", result)
    
    def test_error_handling(self):
        """Test error handling during summarization."""
        # Directly patch the generate_summary method to force an exception
        with patch.object(LLMSummarizer, '_summarize_notion_data', side_effect=Exception("Test error")):
            # Try to generate summary
            result = self.summarizer.generate_summary({
                "notion_data": self.notion_data,
                "project_id": "ERROR-123"
            })
            
            # Verify error handling
            self.assertIn("Error generating summary", result)


if __name__ == '__main__':
    unittest.main()