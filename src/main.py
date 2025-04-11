#!/usr/bin/env python3
"""
Main entry point for the Project Documentation Agent.
"""

import os
import sys
import logging
import click
import yaml
from dotenv import load_dotenv
from typing import Optional

from src.agent import DocumentationAgent
from src.utils.logger import setup_logger

# Load environment variables
load_dotenv()

def load_config(config_path: str):
    """Load configuration from YAML file."""
    try:
        with open(config_path, 'r') as f:
            return yaml.safe_load(f)
    except Exception as e:
        logging.error(f"Error loading configuration: {e}")
        sys.exit(1)

@click.command()
@click.option('--project-id', required=True, help='Notion project page ID to document')
@click.option('--config', default='config/config.yaml', help='Path to configuration file')
@click.option('--output-dir', default=None, help='Directory to save output files')
@click.option('--log-level', default='INFO', help='Logging level')
@click.option('--dry-run', is_flag=True, help='Run without making actual changes to Notion')
def main(project_id: str, config: str, output_dir: Optional[str], log_level: str, dry_run: bool):
    """Generate project documentation by aggregating information from multiple sources."""
    
    # Load configuration
    config_data = load_config(config)
    
    # Setup logging
    log_config = config_data.get('logging', {})
    log_level = log_level or log_config.get('level', 'INFO')
    log_file = log_config.get('file', 'project_documentation_agent.log')
    log_format = log_config.get('format', '%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    
    logger = setup_logger(log_level, log_file, log_format)
    logger.info(f"Starting Project Documentation Agent for project {project_id}")
    
    # Set output directory
    if output_dir:
        config_data['project']['default_output_folder'] = output_dir
    
    # Initialize agent
    agent = DocumentationAgent(config_data, project_id, dry_run=dry_run)
    
    try:
        # Run the agent
        result = agent.run()
        
        # Report outcome
        if result:
            logger.info(f"Documentation generated successfully: {result}")
            click.echo(f"Documentation generated successfully: {result}")
            return 0
        else:
            logger.error("Documentation generation failed")
            click.echo("Documentation generation failed. Check logs for details.")
            return 1
            
    except Exception as e:
        logger.exception(f"Error during documentation generation: {e}")
        click.echo(f"Error: {e}")
        return 1

if __name__ == "__main__":
    main()
