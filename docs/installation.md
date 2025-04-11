# Installation and Setup Guide

This guide provides detailed instructions for setting up and installing the Project Documentation Agent.

## System Requirements

- Python 3.9 or later
- pip package manager
- Access to Notion, Google Drive, and Jira APIs
- OpenAI API key

## Step-by-Step Installation

### 1. Clone the Repository

```bash
git clone <repository-url>
cd project-documentation-agent
```

### 2. Create a Virtual Environment

**Linux/macOS:**
```bash
python -m venv venv
source venv/bin/activate
```

**Windows:**
```bash
python -m venv venv
venv\Scripts\activate
```

### 3. Install Dependencies

```bash
pip install -e .
```

This will install all required dependencies defined in `setup.py`:

- notion-client
- google-api-python-client
- google-auth-oauthlib
- PyPDF2
- python-docx
- python-pptx
- openpyxl
- langchain
- langchain_openai
- atlassian-python-api
- pydantic
- tenacity
- python-dotenv
- PyYAML
- click

### 4. Configure API Access

#### Notion API Setup

1. Go to [Notion Developers](https://www.notion.so/my-integrations)
2. Click "New integration"
3. Name your integration (e.g., "Project Documentation Agent")
4. Select the workspace where your projects are stored
5. Click "Submit"
6. Copy the "Internal Integration Token" 
7. Go to the Notion page you want to document
8. Click "Share" in the top right corner
9. Click "Invite" and find your integration
10. Click "Invite"

#### Google Drive API Setup

1. Go to the [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project
3. Enable the Google Drive API:
   - In the navigation menu, click "APIs & Services" > "Library"
   - Search for "Google Drive API" and enable it
4. Create credentials:
   - In the navigation menu, click "APIs & Services" > "Credentials"
   - Click "Create Credentials" > "OAuth client ID"
   - Select "Desktop app" as the application type
   - Name your client
   - Download the JSON file and save it (e.g., as `credentials.json`)

#### Jira API Setup

1. Go to [Atlassian Account Settings](https://id.atlassian.com/manage/api-tokens)
2. Click "Create API token"
3. Give your token a name (e.g., "Project Documentation Agent")
4. Click "Create"
5. Copy the token value

#### OpenAI API Setup

1. Go to [OpenAI API](https://platform.openai.com/account/api-keys)
2. Create a new API key
3. Copy the key value

### 5. Configure Environment Variables

Create a `.env` file in the project root directory:

```
NOTION_API_KEY=secret_your_notion_integration_token
GDRIVE_CREDENTIALS_FILE=/absolute/path/to/credentials.json
GDRIVE_TOKEN_FILE=/absolute/path/to/token.json
JIRA_EMAIL=your.email@example.com
JIRA_API_TOKEN=your_jira_api_token
OPENAI_API_KEY=your_openai_api_key
```

Note: The `token.json` file will be generated automatically the first time you run the application. You'll need to authenticate with Google by following the prompts.

### 6. Create Output Directory

```bash
mkdir output
```

## Testing the Installation

Run a simple dry run test to make sure everything is working:

```bash
python -m src.main --project-id <notion-page-id> --dry-run
```

Replace `<notion-page-id>` with the ID of your Notion project page. You can find this ID in the page URL:
- For URLs like `https://www.notion.so/workspace/My-Project-1234abcd5678efgh`, the ID is `1234abcd5678efgh`
- For URLs like `https://www.notion.so/1234abcd5678efgh`, the ID is `1234abcd5678efgh`

If the installation is successful, you should see output in the console and a summary document in the `output` directory.

## Troubleshooting

### Common Issues

#### "ModuleNotFoundError: No module named 'X'"

```bash
pip install X
```

#### "FileNotFoundError: [Errno 2] No such file or directory: 'credentials.json'"

Make sure you've set the correct absolute path to your credentials file in the `.env` file.

#### "Error retrieving project data from Notion: 401 Client Error: unauthorized"

Make sure your Notion API key is correct and that you've shared the Notion page with your integration.

#### Google Authentication Flow Not Working

If you're having trouble with the Google authentication flow, try:

```bash
rm token.json  # Delete existing token file if one exists
python -m src.main --project-id <notion-page-id> --dry-run
```

Follow the authentication flow in your browser when prompted.

#### "Error initializing LLM: 401 Client Error: unauthorized"

Double-check your OpenAI API key. Make sure you have sufficient credits in your OpenAI account.

## Running with Docker (Optional)

If you prefer using Docker, create a `Dockerfile`:

```dockerfile
FROM python:3.9-slim

WORKDIR /app

COPY . .
RUN pip install -e .

CMD ["python", "-m", "src.main"]
```

Build and run:

```bash
docker build -t project-documentation-agent .
docker run -it --env-file .env project-documentation-agent --project-id <notion-page-id>
```
