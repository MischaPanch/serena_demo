# Configuration Guide

The Project Documentation Agent is highly configurable to adapt to different project needs. This guide explains all the available configuration options in the `config/config.yaml` file.

## Configuration File Structure

The configuration file is organized into the following sections:

- Logging configuration
- Project settings
- Notion API settings
- Google Drive settings
- Jira settings
- Summarization settings

Below is a detailed explanation of each section and its options.

## Logging Configuration

```yaml
logging:
  level: INFO
  file: project_documentation_agent.log
  format: "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
```

| Option | Description | Default | Valid Values |
|--------|-------------|---------|-------------|
| `level` | Logging level | `INFO` | `DEBUG`, `INFO`, `WARNING`, `ERROR`, `CRITICAL` |
| `file` | Name of the log file | `project_documentation_agent.log` | Any valid file path |
| `format` | Format string for log messages | `%(asctime)s - %(name)s - %(levelname)s - %(message)s` | Any valid Python logging format string |

**Example:**
```yaml
logging:
  level: DEBUG  # More detailed logging
  file: logs/my_project.log  # Store logs in a specific directory
  format: "%(asctime)s [%(levelname)s] %(message)s"  # Simplified format
```

## Project Settings

```yaml
project:
  default_output_folder: "output"
```

| Option | Description | Default | Valid Values |
|--------|-------------|---------|-------------|
| `default_output_folder` | Directory to save output files | `output` | Any valid directory path |

**Example:**
```yaml
project:
  default_output_folder: "documentation/generated"
```

## Notion API Settings

```yaml
notion:
  jira_url_property: "jira-url"
  search_depth: 2
```

| Option | Description | Default | Valid Values |
|--------|-------------|---------|-------------|
| `jira_url_property` | Property name in Notion containing Jira URL | `jira-url` | Any valid Notion property name |
| `search_depth` | Maximum depth for retrieving linked pages | `2` | Any positive integer |

**Example:**
```yaml
notion:
  jira_url_property: "jira_project_url"  # Custom property name
  search_depth: 3  # Search deeper in linked pages
```

## Google Drive Settings

```yaml
gdrive:
  file_types:
    - "application/pdf"
    - "application/vnd.openxmlformats-officedocument.wordprocessingml.document"
    - "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    - "application/vnd.openxmlformats-officedocument.presentationml.presentation"
    - "application/vnd.google-apps.document"
    - "application/vnd.google-apps.spreadsheet"
    - "application/vnd.google-apps.presentation"
  max_files_to_fetch: 100
  search_depth: 3
```

| Option | Description | Default | Valid Values |
|--------|-------------|---------|-------------|
| `file_types` | List of MIME types to include | See example | Any valid MIME type |
| `max_files_to_fetch` | Maximum number of files to retrieve | `100` | Any positive integer |
| `search_depth` | Maximum folder depth to search | `3` | Any positive integer |

**Example with only PDF and Word documents:**
```yaml
gdrive:
  file_types:
    - "application/pdf"
    - "application/vnd.openxmlformats-officedocument.wordprocessingml.document"
  max_files_to_fetch: 50  # Limit to 50 files
  search_depth: 2  # Don't go too deep in folders
```

## Jira Settings

```yaml
jira:
  include_statuses:
    - "Done"
    - "Closed"
    - "Resolved"
    - "Completed"
  exclude_labels:
    - "duplicate"
    - "wontfix"
    - "invalid"
  max_issues_to_fetch: 200
```

| Option | Description | Default | Valid Values |
|--------|-------------|---------|-------------|
| `include_statuses` | List of issue statuses to include | `["Done", "Closed", "Resolved", "Completed"]` | Any valid Jira status |
| `exclude_labels` | List of issue labels to exclude | `["duplicate", "wontfix", "invalid"]` | Any valid Jira label |
| `max_issues_to_fetch` | Maximum number of issues to retrieve | `200` | Any positive integer |

**Example for a specific workflow:**
```yaml
jira:
  include_statuses:
    - "Production Ready"
    - "Released"
  exclude_labels:
    - "duplicate"
    - "not-for-documentation"
  max_issues_to_fetch: 500  # Include more issues
```

## Summarization Settings

```yaml
summarization:
  model_name: "gpt-4"
  temperature: 0.2
  max_tokens: 2000
  chunk_size: 4000
  chunk_overlap: 200
```

| Option | Description | Default | Valid Values |
|--------|-------------|---------|-------------|
| `model_name` | OpenAI model to use | `gpt-4` | `gpt-4`, `gpt-3.5-turbo`, etc. |
| `temperature` | Model temperature (creativity) | `0.2` | `0.0` to `1.0` |
| `max_tokens` | Maximum tokens in response | `2000` | Any positive integer up to model limit |
| `chunk_size` | Size of text chunks for processing | `4000` | Any positive integer |
| `chunk_overlap` | Overlap between chunks | `200` | Any positive integer less than chunk_size |

**Example for more concise summaries:**
```yaml
summarization:
  model_name: "gpt-3.5-turbo"  # Faster, cheaper model
  temperature: 0.1  # More deterministic
  max_tokens: 1000  # Shorter summaries
  chunk_size: 2000  # Smaller chunks
  chunk_overlap: 100  # Less overlap
```

## Complete Example Configuration

Here's a complete example configuration optimized for a large project with many documents:

```yaml
# Logging configuration
logging:
  level: INFO
  file: logs/large_project.log
  format: "%(asctime)s - %(name)s - %(levelname)s - %(message)s"

# Project settings
project:
  default_output_folder: "documentation/large_project"

# Notion API settings
notion:
  jira_url_property: "jira_link"
  search_depth: 2

# Google Drive settings
gdrive:
  file_types:
    - "application/pdf"
    - "application/vnd.openxmlformats-officedocument.wordprocessingml.document"
    - "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    - "application/vnd.openxmlformats-officedocument.presentationml.presentation"
  max_files_to_fetch: 200
  search_depth: 3

# Jira settings
jira:
  include_statuses:
    - "Done"
    - "Released"
  exclude_labels:
    - "duplicate"
    - "internal-only"
  max_issues_to_fetch: 500

# Summarization settings
summarization:
  model_name: "gpt-4"
  temperature: 0.2
  max_tokens: 4000
  chunk_size: 5000
  chunk_overlap: 250
```

## Environment-specific Configurations

You can create multiple configuration files for different environments:

- `config/config.yaml` - Default configuration
- `config/config.dev.yaml` - Development configuration
- `config/config.prod.yaml` - Production configuration

Then specify which configuration to use with the `--config` option:

```bash
python -m src.main --project-id <notion-page-id> --config config/config.prod.yaml
```

## Command-line Overrides

Remember that some configuration options can be overridden via command line arguments:

```bash
python -m src.main --project-id <notion-page-id> --output-dir custom_output --log-level DEBUG
```

This will override the `default_output_folder` and `level` settings in the configuration file.
