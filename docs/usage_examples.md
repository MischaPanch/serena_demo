# Usage Examples

This document provides practical examples of how to use the Project Documentation Agent for different scenarios.

## Basic Usage

### Generating Documentation for a Single Project

```bash
python -m src.main --project-id abc123def456
```

This command will:
1. Extract information from the Notion page with ID `abc123def456`
2. Find and download relevant files from Google Drive
3. Extract tasks from the associated Jira project
4. Generate a comprehensive summary
5. Create a new documentation page in Notion

### Dry Run Mode

To test the process without creating a Notion page:

```bash
python -m src.main --project-id abc123def456 --dry-run
```

The generated documentation will be saved to the output directory specified in the configuration.

### Custom Output Directory

```bash
python -m src.main --project-id abc123def456 --output-dir ./documents/project_abc
```

This will save the output (in dry run mode) or the file paths (in normal mode) to the specified directory.

### Custom Configuration File

```bash
python -m src.main --project-id abc123def456 --config ./config/custom_config.yaml
```

This will use the settings from `custom_config.yaml` instead of the default configuration.

### Verbose Logging

```bash
python -m src.main --project-id abc123def456 --log-level DEBUG
```

This will provide more detailed logs, which can be helpful for troubleshooting.

## Advanced Usage Examples

### Batch Processing Multiple Projects

Use a shell script to process multiple projects:

```bash
#!/bin/bash
# batch_process.sh

projects=(
  "abc123def456"
  "ghi789jkl012"
  "mno345pqr678"
)

for project_id in "${projects[@]}"; do
  echo "Processing project $project_id"
  python -m src.main --project-id "$project_id" --output-dir "./output/$project_id"
  
  # Add a delay to avoid API rate limits
  sleep 60
done

echo "All projects processed"
```

Make the script executable and run it:

```bash
chmod +x batch_process.sh
./batch_process.sh
```

### Scheduling Regular Documentation Updates

Create a cron job to update documentation weekly:

1. Create a script:

```bash
#!/bin/bash
# update_docs.sh

cd /path/to/project-documentation-agent
source venv/bin/activate

# List of active projects
projects=(
  "abc123def456"
  "ghi789jkl012"
)

date_str=$(date +%Y-%m-%d)

for project_id in "${projects[@]}"; do
  echo "Updating documentation for project $project_id on $date_str"
  python -m src.main --project-id "$project_id" --output-dir "./output/$date_str/$project_id"
  
  # Add a delay to avoid API rate limits
  sleep 60
done

echo "Documentation update completed"
```

2. Add a cron job:

```bash
crontab -e
```

Add this line to run the script every Sunday at 1 AM:

```
0 1 * * 0 /path/to/update_docs.sh >> /path/to/cron.log 2>&1
```

### Creating an Archive of Project Documentation

This example demonstrates how to generate documentation for a project and archive it:

```bash
#!/bin/bash
# archive_project.sh

project_id=$1
archive_dir="./archives"

if [ -z "$project_id" ]; then
  echo "Usage: ./archive_project.sh <project_id>"
  exit 1
fi

# Create archive directory if it doesn't exist
mkdir -p "$archive_dir"

# Generate timestamp
timestamp=$(date +%Y%m%d_%H%M%S)
output_dir="$archive_dir/$project_id/$timestamp"
mkdir -p "$output_dir"

# Generate documentation in dry-run mode
python -m src.main --project-id "$project_id" --output-dir "$output_dir" --dry-run

# Create a zip archive
zip_file="$archive_dir/$project_id"_"$timestamp.zip"
zip -r "$zip_file" "$output_dir"

echo "Documentation archived to $zip_file"
```

Run it for a specific project:

```bash
./archive_project.sh abc123def456
```

## Integration Examples

### CI/CD Pipeline Integration (GitLab CI Example)

Create a `.gitlab-ci.yml` file in your project repository:

```yaml
stages:
  - document

generate_documentation:
  stage: document
  image: python:3.9
  script:
    - pip install -e .
    - python -m src.main --project-id $NOTION_PROJECT_ID --dry-run
    - cp -r output /documentation
  artifacts:
    paths:
      - /documentation
  only:
    - tags
  variables:
    NOTION_API_KEY: $NOTION_API_KEY
    OPENAI_API_KEY: $OPENAI_API_KEY
    JIRA_EMAIL: $JIRA_EMAIL
    JIRA_API_TOKEN: $JIRA_API_TOKEN
```

This pipeline will generate documentation whenever a new tag is created.

### Slack Integration Example

Create a script that generates documentation and sends a notification to Slack:

```python
#!/usr/bin/env python3
import subprocess
import os
import requests
import json
import sys

# Configuration
project_id = sys.argv[1] if len(sys.argv) > 1 else "default_project_id"
slack_webhook_url = os.environ.get("SLACK_WEBHOOK_URL")
output_dir = f"./output/{project_id}"

# Run documentation generator
print(f"Generating documentation for project {project_id}...")
result = subprocess.run(
    ["python", "-m", "src.main", "--project-id", project_id, "--output-dir", output_dir],
    capture_output=True,
    text=True
)

# Check if successful
if result.returncode == 0:
    # Find the documentation URL in the output
    output_lines = result.stdout.splitlines()
    doc_url = None
    for line in output_lines:
        if "Documentation generated successfully" in line:
            doc_url = line.split(": ")[1].strip()
            break
    
    # Send Slack notification
    if slack_webhook_url and doc_url:
        message = {
            "text": f"📄 New project documentation generated!",
            "blocks": [
                {
                    "type": "header",
                    "text": {
                        "type": "plain_text",
                        "text": "📄 New Project Documentation"
                    }
                },
                {
                    "type": "section",
                    "text": {
                        "type": "mrkdwn",
                        "text": f"Documentation for project *{project_id}* has been generated successfully."
                    }
                },
                {
                    "type": "section",
                    "text": {
                        "type": "mrkdwn",
                        "text": f"*<{doc_url}|View Documentation>*"
                    }
                }
            ]
        }
        
        response = requests.post(
            slack_webhook_url,
            data=json.dumps(message),
            headers={'Content-Type': 'application/json'}
        )
        
        if response.status_code == 200:
            print("Slack notification sent successfully")
        else:
            print(f"Failed to send Slack notification: {response.text}")
    
    print("Documentation generated successfully")
    sys.exit(0)
else:
    print(f"Error generating documentation: {result.stderr}")
    
    # Send error notification to Slack
    if slack_webhook_url:
        message = {
            "text": "❌ Documentation generation failed",
            "blocks": [
                {
                    "type": "header",
                    "text": {
                        "type": "plain_text",
                        "text": "❌ Documentation Generation Failed"
                    }
                },
                {
                    "type": "section",
                    "text": {
                        "type": "mrkdwn",
                        "text": f"Failed to generate documentation for project *{project_id}*."
                    }
                },
                {
                    "type": "section",
                    "text": {
                        "type": "mrkdwn",
                        "text": f"```{result.stderr[:500]}```"
                    }
                }
            ]
        }
        
        requests.post(
            slack_webhook_url,
            data=json.dumps(message),
            headers={'Content-Type': 'application/json'}
        )
    
    sys.exit(1)
```

Run it with:

```bash
export SLACK_WEBHOOK_URL="https://hooks.slack.com/services/XXX/YYY/ZZZ"
./notify_slack.py abc123def456
```

## Use Case Examples

### End-of-Project Documentation

At the end of a project, run:

```bash
python -m src.main --project-id <project-id>
```

This will generate a comprehensive summary of the project, which can be shared with stakeholders or used for knowledge transfer.

### Knowledge Base Building

For archiving institutional knowledge about multiple projects:

```bash
./batch_process.sh
```

This creates a searchable archive of project documentation that can be referenced for future projects.

### Client Handover Documentation

Before handing over a project to a client:

```bash
python -m src.main --project-id <project-id> --config config/client_handover.yaml
```

Using a specialized configuration, this generates client-friendly documentation focusing on deliverables and outcomes rather than internal processes.

## Troubleshooting Examples

### API Authentication Issues

If you're experiencing authentication issues with any of the APIs:

```bash
# Check if your API keys are properly set
env | grep -E 'NOTION|JIRA|OPENAI|GDRIVE'

# Test Notion API authentication
python -c "from notion_client import Client; client = Client(auth=os.environ.get('NOTION_API_KEY')); print(client.users.me())"

# Test Google Drive API authentication
python -c "from googleapiclient.discovery import build; from google.oauth2.credentials import Credentials; creds = Credentials.from_authorized_user_info(info=json.loads(open(os.environ.get('GDRIVE_TOKEN_FILE')).read())); drive = build('drive', 'v3', credentials=creds); print(drive.files().list(pageSize=5).execute())"
```

### Document Parsing Errors

If you encounter errors parsing specific document types:

```bash
# Test PDF parsing
python -c "from PyPDF2 import PdfReader; reader = PdfReader('path/to/problematic.pdf'); print(f'Pages: {len(reader.pages)}')"

# Test DOCX parsing
python -c "import docx; doc = docx.Document('path/to/problematic.docx'); print(f'Paragraphs: {len(doc.paragraphs)}')"
```

### OpenAI API Rate Limiting

If you're hitting OpenAI API rate limits:

```bash
# Use a configuration with longer delays between requests
python -m src.main --project-id <project-id> --config config/rate_limit_safe.yaml
```

Example `rate_limit_safe.yaml` configuration:
```yaml
summarization:
  model_name: "gpt-3.5-turbo"  # Use a model with higher rate limits
  temperature: 0.2
  max_tokens: 1500
  chunk_size: 3000
  chunk_overlap: 150
```

### Memory Issues with Large Projects

If you're processing very large projects and experiencing memory issues:

```bash
# Limit the number of files and issues to fetch
python -m src.main --project-id <project-id> --config config/low_memory.yaml
```

Example `low_memory.yaml` configuration:
```yaml
gdrive:
  max_files_to_fetch: 25
jira:
  max_issues_to_fetch: 50
summarization:
  chunk_size: 2000
  chunk_overlap: 100
```

## Advanced Configuration Examples

### Specialized Client Report Configuration

Create a `config/client_report.yaml` file:

```yaml
# Focus on client-relevant information
notion:
  search_depth: 1  # Only direct content

gdrive:
  file_types:
    - "application/pdf"
    - "application/vnd.openxmlformats-officedocument.presentationml.presentation"
  max_files_to_fetch: 20

jira:
  include_statuses:
    - "Done"
    - "Released"
  exclude_labels:
    - "internal-only"
    - "not-for-client"
  max_issues_to_fetch: 100

summarization:
  model_name: "gpt-4"
  temperature: 0.3
  max_tokens: 3000
  prompt_template: "client_report_template.txt"  # Custom prompt template
```

### Technical Deep-Dive Configuration

Create a `config/technical_deep_dive.yaml` file:

```yaml
# Focus on technical details and implementation
notion:
  search_depth: 3  # Go deeper into linked pages

gdrive:
  file_types:
    - "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    - "application/vnd.openxmlformats-officedocument.wordprocessingml.document"
    - "text/plain"
  max_files_to_fetch: 200

jira:
  include_statuses:
    - "Done"
  include_types:
    - "Bug"
    - "Task"
    - "Technical Task"
  exclude_labels:
    - "non-technical"
  max_issues_to_fetch: 500

summarization:
  model_name: "gpt-4"
  temperature: 0.1
  max_tokens: 4000
  chunk_size: 6000
  chunk_overlap: 300
  technical_focus: true  # Custom setting for technical focus
```

## Conclusion

These examples demonstrate the flexibility of the Project Documentation Agent for various scenarios. You can adapt and combine these examples to suit your specific needs. For more details on configuration options, refer to the [Configuration Guide](configuration.md).
