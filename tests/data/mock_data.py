"""
Mock data for tests.
"""

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

GDRIVE_FILES = [
    {
        "id": "file1",
        "name": "Project Proposal.pdf",
        "mimeType": "application/pdf",
        "webViewLink": "https://drive.google.com/file1"
    },
    {
        "id": "file2",
        "name": "Technical Design.docx",
        "mimeType": "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
        "webViewLink": "https://drive.google.com/file2"
    },
    {
        "id": "file3",
        "name": "Project Plan.xlsx",
        "mimeType": "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        "webViewLink": "https://drive.google.com/file3"
    }
]

JIRA_TASKS = [
    {
        "key": "TEST-1",
        "id": "1001",
        "summary": "Implement feature 1",
        "description": "Implement the first key feature of the project",
        "issue_type": {"name": "Task"},
        "status": {"name": "Done", "category": "Done"},
        "priority": {"name": "High"},
        "assignee": {"name": "John Doe", "email": "john@example.com"},
        "created": "2023-01-05T10:00:00.000Z",
        "resolved": "2023-01-08T15:30:00.000Z",
        "labels": ["feature", "sprint-1"],
        "components": ["backend"]
    },
    {
        "key": "TEST-2",
        "id": "1002",
        "summary": "Implement feature 2",
        "description": "Implement the second key feature of the project",
        "issue_type": {"name": "Task"},
        "status": {"name": "Done", "category": "Done"},
        "priority": {"name": "Medium"},
        "assignee": {"name": "Jane Smith", "email": "jane@example.com"},
        "created": "2023-01-06T09:15:00.000Z",
        "resolved": "2023-01-09T11:45:00.000Z",
        "labels": ["feature", "sprint-1"],
        "components": ["frontend"]
    },
    {
        "key": "TEST-3",
        "id": "1003",
        "summary": "Fix critical bug",
        "description": "Fix critical bug in the authentication flow",
        "issue_type": {"name": "Bug"},
        "status": {"name": "Done", "category": "Done"},
        "priority": {"name": "Critical"},
        "assignee": {"name": "John Doe", "email": "john@example.com"},
        "created": "2023-01-07T14:20:00.000Z",
        "resolved": "2023-01-07T18:10:00.000Z",
        "labels": ["bug", "security", "sprint-1"],
        "components": ["backend", "auth"]
    }
]