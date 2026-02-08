# Quickstart Guide: Chat Interface & AI UX

## Overview
This guide explains how to implement and run the chat interface feature for the Todo Web Application.

## Prerequisites
- Node.js 18+ installed
- Python 3.9+ installed
- Access to Neon PostgreSQL database
- Valid OpenAI API key

## Frontend Setup

### 1. Install Dependencies
```bash
cd frontend
npm install
```

### 2. Environment Variables
Create a `.env.local` file in the frontend directory:
```env
NEXT_PUBLIC_API_BASE_URL=http://localhost:8000
NEXT_PUBLIC_JWT_SECRET=your-jwt-secret
```

## Backend Setup

### 1. Install Dependencies
```bash
cd backend
poetry install
```

### 2. Environment Variables
Ensure your backend `.env` file contains:
```env
DATABASE_URL=your_neon_database_url
JWT_SECRET_KEY=your-jwt-secret
OPENAI_API_KEY=your_openai_api_key
```

### 3. Run Backend Server
```bash
cd backend
poetry run python -m src.main
```

## Implementation Steps

### 1. Create Chat Page Component
Create a new page at `frontend/app/protected/chat/page.tsx` that:
- Fetches the authenticated user's ID
- Implements the chat UI with message history
- Integrates with the `/api/{user_id}/chat` endpoint
- Handles loading, error, and empty states

### 2. Create Chat Service
Create a service at `frontend/lib/api/chat.ts` that:
- Manages API calls to the backend chat endpoint
- Handles JWT authentication
- Formats request/response objects

### 3. Create Chat Components
Create reusable components in `frontend/components/chat/`:
- MessageList: Displays chat history
- MessageInput: Handles user input
- LoadingIndicator: Shows when AI is processing
- ErrorMessage: Displays error messages

### 4. Implement Conversation Persistence
- Use localStorage to store conversation history
- Restore conversation state on page load
- Clear old conversations to manage storage

## Running the Application

### Frontend Development Server
```bash
cd frontend
npm run dev
```

### Backend Server
```bash
cd backend
poetry run python -m src.main
```

Visit `http://localhost:3000` to access the application.

## Testing the Chat Feature

1. Log in to the application
2. Navigate to the protected chat page
3. Type a natural language command like "Add a task to buy milk"
4. Verify the AI responds and the task is added to your todo list
5. Refresh the page to verify conversation persistence

## Troubleshooting

### Common Issues
- **401 Unauthorized**: Verify JWT token is valid and included in requests
- **403 Forbidden**: Ensure the user_id in the API path matches the authenticated user
- **Network Error**: Verify backend server is running and accessible
- **Empty Chat Window**: Check localStorage is enabled in the browser

### Debugging
- Enable browser developer tools to inspect network requests
- Check backend logs for error messages
- Verify API endpoint URL is correctly configured