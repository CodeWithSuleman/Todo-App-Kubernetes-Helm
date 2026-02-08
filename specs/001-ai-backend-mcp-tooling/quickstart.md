# Quickstart Guide: AI Backend & MCP Tooling

**Feature**: AI Backend & MCP Tooling
**Date**: 2026-02-05

## Overview

This guide provides instructions for setting up and running the AI-powered chat backend with MCP tooling for natural language todo management.

## Prerequisites

- Python 3.9+
- Poetry (dependency manager)
- PostgreSQL database (Neon Serverless)
- OpenAI API key
- MCP SDK installed

## Environment Setup

1. **Clone the repository**
   ```bash
   git clone <repo-url>
   cd giaic-hackathon-2-phase-III
   ```

2. **Navigate to backend directory**
   ```bash
   cd backend
   ```

3. **Install dependencies**
   ```bash
   poetry install
   ```

4. **Set up environment variables**
   Create a `.env` file in the backend directory with the following:
   ```env
   DATABASE_URL=postgresql://username:password@host:port/database_name
   OPENAI_API_KEY=your_openai_api_key_here
   JWT_SECRET=your_jwt_secret_here
   MCP_SERVER_PORT=3001
   ```

5. **Activate virtual environment**
   ```bash
   poetry shell
   ```

## Running the Application

1. **Start the MCP server separately**
   ```bash
   python -m backend.src.mcp.server
   ```

2. **Start the main FastAPI application**
   ```bash
   python -m backend.src.main
   ```

## Key Components

### MCP Server (`backend/src/mcp/server.py`)
- Runs the Model Context Protocol server
- Exposes the todo management tools to AI agents
- Handles tool calls and returns results

### Chat Endpoint (`backend/src/api/chat.py`)
- Accepts natural language requests at `/api/{user_id}/chat`
- Processes requests through the AI agent
- Returns AI-generated responses

### Data Models (`backend/src/models/conversation.py`, `backend/src/models/message.py`)
- Handle persistence of conversation and message data
- Ensure user isolation and data integrity

## API Usage

### Chat Endpoint
```
POST /api/{user_id}/chat
Authorization: Bearer <jwt_token>
Content-Type: application/json

{
  "message": "Add a task to buy groceries",
  "conversation_id": "optional_conversation_uuid"
}
```

Response:
```json
{
  "response": "I've added the task 'buy groceries' to your list.",
  "conversation_id": "123e4567-e89b-12d3-a456-426614174000",
  "tool_calls": [
    {
      "tool_name": "add_task",
      "parameters": {
        "title": "buy groceries"
      },
      "result": {
        "task_id": "456e7890-f90b-23e4-c567-837725285111",
        "title": "buy groceries",
        "status": "pending"
      }
    }
  ],
  "message_id": "789a0123-c12d-34f5-g678-901234567890"
}
```

## Testing

1. **Run backend tests**
   ```bash
   poetry run pytest tests/
   ```

2. **Test the chat endpoint**
   ```bash
   curl -X POST http://localhost:8000/api/123e4567-e89b-12d3-a456-426614174000/chat \
     -H "Authorization: Bearer your_jwt_token" \
     -H "Content-Type: application/json" \
     -d '{"message": "Add a task to buy groceries"}'
   ```

## Troubleshooting

- **MCP Server Connection Issues**: Ensure the MCP server is running before starting the main application
- **JWT Authentication Errors**: Verify the JWT token format and secret
- **Tool Call Failures**: Check that the user has permission to access the requested resources

## Development

When developing new features:

1. Always follow the stateless architecture pattern
2. Ensure all database operations happen through MCP tools
3. Maintain user isolation in all operations
4. Add appropriate error handling for AI and tool failures