"""
Main agent for documentation generation.
"""

import logging
import os
import tempfile
from typing import Dict, List, Any, Optional

from src.adapters.notion import NotionClient
from src.adapters.gdrive import GoogleDriveClient
from src.adapters.jira import JiraClient
from src.parsers.factory import ParserFactory
from src.summarizers.llm import LLMSummarizer

logger = logging.getLogger(__name__)


class DocumentationAgent:
    """
    Agent for generating project documentation by collecting and summarizing
    information from various sources (Notion, Google Drive, Jira).
    """
    
    def __init__(self, config: Dict[str, Any], project_id: str, dry_run: bool = False):
        """
        Initialize the documentation agent.
        
        Args:
            config: Configuration dictionary
            project_id: ID of the project to document
            dry_run: If True, don't create the actual documentation page
        """
        self.config = config
        self.project_id = project_id
        self.dry_run = dry_run
        
        # Initialize clients
        self.notion_client = NotionClient(config.get("notion", {}))
        self.gdrive_client = GoogleDriveClient(config.get("gdrive", {}))
        self.jira_client = None  # Will be initialized when we get the Jira URL
        
        # Initialize parser factory
        self.parser_factory = ParserFactory()
        
        # Initialize summarizer
        self.summarizer = LLMSummarizer(config.get("summarization", {}))
        
        # Create temporary directory for downloading files
        self.temp_dir = tempfile.TemporaryDirectory()
        
        logger.info(f"Documentation agent initialized for project {project_id}")
        
    def run(self) -> Optional[str]:
        """
        Run the documentation generation process.
        
        Returns:
            URL of the created documentation page or path to the saved file (dry_run),
            or None if an error occurred
        """
        try:
            logger.info(f"Starting documentation generation for project {self.project_id}")
            
            # Step 1: Extract data from Notion
            notion_data = self._extract_notion_data()
            logger.info(f"Extracted Notion data for project {self.project_id}")
            
            # Step 2: Get Jira URL and initialize Jira client
            jira_url = self._extract_jira_url(notion_data)
            if jira_url:
                self.jira_client = JiraClient(jira_url, self.config.get("jira", {}))
                logger.info(f"Initialized Jira client with URL: {jira_url}")
            
            # Step 3: Find and download relevant Google Drive documents
            drive_documents = []
            drive_files = self.gdrive_client.get_relevant_files(self.project_id)
            logger.info(f"Found {len(drive_files)} relevant files in Google Drive")
            
            for file in drive_files:
                try:
                    file_path = self.gdrive_client.download_file(file["id"], self.temp_dir.name)
                    parser = self.parser_factory.get_parser(file["mimeType"])
                    
                    if parser:
                        content = parser.parse(file_path)
                        drive_documents.append({
                            "id": file["id"],
                            "name": file["name"],
                            "type": file["mimeType"],
                            "content": content,
                            "url": file.get("webViewLink", "")
                        })
                    else:
                        logger.warning(f"No parser available for file: {file['name']} ({file['mimeType']})")
                except Exception as e:
                    logger.error(f"Error processing file {file['name']}: {e}")
            
            # Step 4: Extract tasks from Jira
            jira_tasks = []
            if self.jira_client:
                jira_tasks = self.jira_client.get_project_issues(self.project_id)
                logger.info(f"Found {len(jira_tasks)} tasks in Jira")
            
            # Step 5: Generate comprehensive summary
            summary_data = {
                "notion_data": notion_data,
                "drive_documents": drive_documents,
                "jira_tasks": jira_tasks,
                "project_id": self.project_id
            }
            
            summary = self.summarizer.generate_summary(summary_data)
            logger.info("Generated comprehensive summary")
            
            # Step 6: Create documentation page in Notion or save locally
            if self.dry_run:
                # Save to file
                output_folder = self.config.get("project", {}).get("default_output_folder", ".")
                os.makedirs(output_folder, exist_ok=True)
                output_file = os.path.join(output_folder, f"{self.project_id}_summary.md")
                
                with open(output_file, "w") as f:
                    f.write(summary)
                    
                logger.info(f"Saved summary to file: {output_file}")
                return output_file
            else:
                # Create Notion page
                url = self.notion_client.create_summary_page(self.project_id, summary)
                logger.info(f"Created summary page in Notion: {url}")
                return url
                
        except Exception as e:
            logger.exception(f"Error generating documentation: {e}")
            return None
            
    def _extract_notion_data(self) -> Dict[str, Any]:
        """
        Extract project data from Notion.
        
        Returns:
            Dictionary with project data
        """
        return self.notion_client.get_project_data(self.project_id)
    
    def _extract_jira_url(self, notion_data: Dict[str, Any]) -> Optional[str]:
        """
        Extract Jira URL from Notion data.
        
        Args:
            notion_data: Project data from Notion
            
        Returns:
            Jira URL if found, None otherwise
        """
        try:
            jira_url_property = self.config.get("notion", {}).get("jira_url_property", "jira-url")
            jira_url = notion_data.get("properties", {}).get(jira_url_property, {}).get("url")
            return jira_url
        except (KeyError, TypeError) as e:
            logger.warning(f"Could not extract Jira URL from Notion data: {e}")
            return None