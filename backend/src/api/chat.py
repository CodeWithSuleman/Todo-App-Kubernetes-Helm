"""
Chat API for AI Backend & MCP Tooling feature.

This module implements the chat endpoint for natural language todo management.
"""

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pydantic import BaseModel
from typing import Optional, List, Dict, Any
import uuid
from datetime import datetime
from ..middleware import get_current_user_from_token
from ..models.user import User
from ..services.conversation_service import ConversationService
from ..mcp.server import get_mcp_server
from ..agents.chat_agent import ChatAgent
from sqlmodel import Session
from ..database import get_session

router = APIRouter()
security = HTTPBearer()


class ChatRequest(BaseModel):
    """Request model for chat endpoint."""
    message: str
    conversation_id: Optional[str] = None


class ToolCallResult(BaseModel):
    """Model for tool call results."""
    tool_name: str
    parameters: Dict[str, Any]
    result: Dict[str, Any]


class ChatResponse(BaseModel):
    """Response model for chat endpoint."""
    response: str
    conversation_id: str
    tool_calls: List[ToolCallResult]
    message_id: str


@router.post("/{user_id}/chat", response_model=ChatResponse)
async def chat_endpoint(
    user_id: str,
    request: ChatRequest,
    credentials: HTTPAuthorizationCredentials = Depends(security)
):
    """
    Process natural language requests for todo management.

    Handles natural language input from users and processes it through an AI agent
    that selects appropriate tools for todo management operations.
    """
    # Validate the user_id in the path matches the authenticated user
    try:
        authenticated_user_id = await get_current_user_from_token(credentials.credentials)
        if str(authenticated_user_id) != user_id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="User ID in path does not match authenticated user"
            )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials"
        )

    # Initialize services
    mcp_server = get_mcp_server()
    chat_agent = ChatAgent(mcp_server)

    # Validate user_id format
    try:
        user_uuid = uuid.UUID(user_id)
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid user ID format"
        )

    # Process with AI agent - conversation persistence is handled inside the agent
    try:
        agent_response = await chat_agent.process_message(
            user_id=user_id,  # Pass as string to match function signature
            conversation_id=request.conversation_id,
            message=request.message
        )

        # Create response
        response = ChatResponse(
            response=agent_response.get('response', ''),
            conversation_id=agent_response.get('conversation_id', str(uuid.uuid4())),
            tool_calls=[
                ToolCallResult(
                    tool_name=call.get('tool_name', ''),
                    parameters=call.get('parameters', {}),
                    result=call.get('result', {})
                )
                for call in agent_response.get('tool_calls', [])
            ],
            message_id=str(uuid.uuid4())  # Generate a new message ID
        )

        return response
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error processing chat request: {str(e)}"
        )


# Note: The actual implementation of JWT validation is handled by the get_current_user_from_token
# function imported from middleware, which is already implemented in the existing middleware.py