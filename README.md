
# Info

> THIS IS A DEMO
>
> This project was generated entirely by [serena](https://github.com/oraios/serena).  
> The total generation cost was 0$, since it was done through Claude Desktop (the community version on Ubuntu).  
> It took minimal prompting and 4 conversations.  

For full transparency, here the conversations (we also included the memory files):

- [First](https://claude.ai/share/fd47766a-db22-4379-b53c-a7f7f3e0a657)
- [Second](https://claude.ai/share/32d9d5cd-5934-4324-ab68-141cd84fdd79)
- [Third](https://claude.ai/share/7425ecb4-da48-42e9-925c-4f1240dfc4b9)
- [Fourth](https://claude.ai/share/b143aabb-4547-4100-b99c-d6c5a4c68c1c)

By the end of the 4th conversation, the python environment was installed and all tests were passing (using mocks).

# Project Documentation Agent

A Python-based tool designed to automatically generate comprehensive project documentation by aggregating information from multiple sources:
- Notion (existing project documentation)
- Google Drive (presentations, documents, etc.)
- Jira (project tasks and tickets)

## Project Purpose

The goal is to eliminate the need for manual documentation work at the end of a project, enabling efficient knowledge sharing and reuse across teams.

## Architecture

The project follows a modular architecture:

1. **API Adapters** (`src/adapters/`):
   - `notion.py`: Client for Notion API
   - `gdrive.py`: Client for Google Drive API
   - `jira.py`: Client for Jira API

2. **Document Parsers** (`src/parsers/`):
   - `base.py`: Abstract base parser interface
   - `pdf_parser.py`: PDF document parser using PyPDF2
   - `docx_parser.py`: Word document parser using python-docx
   - `pptx_parser.py`: PowerPoint parser using python-pptx
   - `xlsx_parser.py`: Excel parser using openpyxl
   - `factory.py`: Factory for creating appropriate parsers

3. **Summarization Logic** (`src/summarizers/`):
   - `base.py`: Abstract summarizer interface
   - `llm.py`: Implementation using OpenAI and LangChain

4. **Core Components**:
   - `agent.py`: Main agent orchestration
   - `main.py`: CLI entry point

## Setup Requirements

To use the project:
1. Python 3.9+
2. Dependencies from requirements.txt
3. API access credentials:
   - NOTION_API_KEY
   - GDRIVE_CREDENTIALS_FILE and GDRIVE_TOKEN_FILE
   - JIRA_EMAIL and JIRA_API_TOKEN
   - OPENAI_API_KEY

## Installation

```bash
pip install -r requirements.txt
```

## Running Tests

Due to the way mocks are implemented in different test files, tests must be run individually to avoid namespace conflicts.

Use the provided script to run all tests:

```bash
./run_tests.sh
```

Or run individual test files:

```bash
python -m pytest tests/test_agent.py -v
python -m pytest tests/test_parsers.py -v
python -m pytest tests/test_notion_adapter.py -v
python -m pytest tests/test_llm_summarizer.py -v
```

## Usage

```bash
python -m src.main --project-id <NOTION_PROJECT_ID> [--dry-run]
```

The tool will:
1. Extract data from the specified Notion project page
2. Get the Jira URL from Notion and retrieve project issues
3. Find and download relevant Google Drive documents
4. Parse all documents
5. Generate a comprehensive summary
6. Create a documentation page in Notion (or save locally with --dry-run)
