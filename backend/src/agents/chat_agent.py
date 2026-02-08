"""
Chat Agent for AI Backend & MCP Tooling feature.

This module implements the OpenAI agent with tool registration for natural language processing.
"""

import json
import logging
from typing import Dict, Any, List
from openai import OpenAI
from ..mcp.server import MCPCall, MCPResponse, MCPServer
from ..services.conversation_service import ConversationService
from sqlmodel import Session
from ..database import get_session
from ..config import settings
import uuid
from datetime import datetime

logger = logging.getLogger(__name__)


class ChatAgent:
    """
    Implements an OpenAI agent that can interact with MCP tools for task management.
    """

    def __init__(self, mcp_server: MCPServer):
        """
        Initialize the chat agent with the MCP server for tool access.
        """
        self.client = OpenAI(api_key=settings.OPENAI_API_KEY)
        self.mcp_server = mcp_server
        self.conversation_service = ConversationService()
        self.model = settings.OPENAI_MODEL

        # Define the tools available to the agent
        self.tools = [
            {
                "type": "function",
                "function": {
                    "name": "add_task",
                    "description": "Add a new task to the user's todo list",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "title": {"type": "string", "description": "The title of the task to add"},
                            "description": {"type": "string", "description": "A detailed description of the task"},
                            "user_id": {"type": "string", "description": "The ID of the user creating the task"}
                        },
                        "required": ["title", "user_id"]
                    }
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "list_tasks",
                    "description": "Retrieve all tasks for the current user",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "user_id": {"type": "string", "description": "The ID of the user whose tasks to retrieve"}
                        },
                        "required": ["user_id"]
                    }
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "update_task",
                    "description": "Update an existing task's properties",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "task_id": {"type": "string", "description": "The ID of the task to update"},
                            "user_id": {"type": "string", "description": "The ID of the user who owns the task"},
                            "title": {"type": "string", "description": "The new title of the task"},
                            "description": {"type": "string", "description": "The new description of the task"},
                            "status": {"type": "string", "description": "The new status of the task", "enum": ["pending", "in_progress", "completed"]}
                        },
                        "required": ["task_id", "user_id"]
                    }
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "complete_task",
                    "description": "Mark a task as completed",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "task_id": {"type": "string", "description": "The ID of the task to complete"},
                            "user_id": {"type": "string", "description": "The ID of the user who owns the task"}
                        },
                        "required": ["task_id", "user_id"]
                    }
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "delete_task",
                    "description": "Delete a task from the user's todo list",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "task_id": {"type": "string", "description": "The ID of the task to delete"},
                            "user_id": {"type": "string", "description": "The ID of the user who owns the task"}
                        },
                        "required": ["task_id", "user_id"]
                    }
                }
            }
        ]

    async def process_message(self, user_id: str, conversation_id: str, message: str) -> Dict[str, Any]:
        """
        Process a natural language message and return an appropriate response.

        Args:
            user_id: The ID of the user sending the message
            conversation_id: The ID of the conversation (if continuing)
            message: The natural language message from the user

        Returns:
            Dictionary containing the response and any tool calls made
        """
        try:
            # Store the user message in the conversation
            with next(get_session()) as session:
                message_data = {
                    'user_id': uuid.UUID(user_id),
                    'role': 'user',
                    'content': message
                }

                # If no conversation exists yet, create one
                if not conversation_id:
                    from ..models.conversation import ConversationCreate
                    conversation_data = ConversationCreate(
                        user_id=uuid.UUID(user_id),
                        title=f"AI Chat Session - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
                    )
                    conversation = self.conversation_service.create_conversation(session, conversation_data)
                    conversation_id = str(conversation.id)
                else:
                    # Validate conversation exists and belongs to user
                    conversation = self.conversation_service.get_conversation_by_id(session, conversation_id)
                    if not conversation or str(conversation.user_id) != user_id:
                        raise ValueError("Invalid conversation or user mismatch")

                # Add the user message to the conversation
                self.conversation_service.add_message_to_conversation(session, conversation_id, message_data)

            # Prepare the conversation history for the AI
            with next(get_session()) as session:
                # Get recent conversation context
                conversation_context = self.conversation_service.get_conversation_context(session, conversation_id, limit=10)

                # Build the message history for the AI
                messages = [
                    {
                        "role": "system",
                        "content": "You are a helpful AI assistant that manages tasks for users. "
                                  "You can add, list, update, complete, and delete tasks using the available tools. "
                                  "Always ensure that user IDs match the authenticated user for security."
                    }
                ]

                # Add historical messages in reverse order (oldest first)
                for ctx_msg in reversed(conversation_context):
                    messages.append({
                        "role": ctx_msg['role'],
                        "content": ctx_msg['content']
                    })

                # Add the current user message
                messages.append({
                    "role": "user",
                    "content": message
                })

            # Call the OpenAI API with function calling enabled
            response = self.client.chat.completions.create(
                model=self.model,  # Could be configurable
                messages=messages,
                tools=self.tools,
                tool_choice="auto",  # Auto-select tools as needed
            )

            # Process the response
            response_message = response.choices[0].message
            tool_calls = response_message.tool_calls

            tool_call_results = []
            ai_response = ""

            # If the model wanted to call tools, process those calls
            if tool_calls:
                for tool_call in tool_calls:
                    function_name = tool_call.function.name
                    function_args = json.loads(tool_call.function.arguments)

                    # Add the user_id to the function args for security validation
                    function_args["user_id"] = user_id

                    # Create an MCPCall object
                    mcp_call = MCPCall(
                        tool_name=function_name,
                        parameters=function_args
                    )

                    # Execute the tool via the MCP server
                    mcp_result: MCPResponse = await self.mcp_server.execute_tool(mcp_call)

                    # Store the result
                    tool_call_results.append({
                        "tool_name": function_name,
                        "parameters": function_args,
                        "result": mcp_result.result if mcp_result.success else {"error": mcp_result.error}
                    })

                # After executing tools, get a final response from the model
                # with the results of the tool calls
                follow_up_messages = messages + [
                    response_message,
                ]

                for tool_call in tool_calls:
                    function_name = tool_call.function.name
                    function_args = json.loads(tool_call.function.arguments)

                    # Add the user_id to the function args for security validation
                    function_args["user_id"] = user_id

                    # Create an MCPCall object
                    mcp_call = MCPCall(
                        tool_name=function_name,
                        parameters=function_args
                    )

                    # Execute the tool via the MCP server
                    mcp_result: MCPResponse = await self.mcp_server.execute_tool(mcp_call)

                    # Add the tool result to the conversation for the AI to see
                    follow_up_messages.append({
                        "role": "tool",
                        "content": json.dumps(mcp_result.result if mcp_result.success else {"error": mcp_result.error}),
                        "tool_call_id": tool_call.id
                    })

                # Get the final response from the AI after seeing tool results
                final_response = self.client.chat.completions.create(
                    model=self.model,
                    messages=follow_up_messages
                )

                ai_response = final_response.choices[0].message.content
            else:
                # If no tools were called, just return the AI's response
                ai_response = response_message.content

            # Store the AI's response in the conversation
            with next(get_session()) as session:
                ai_message_data = {
                    'user_id': uuid.UUID(user_id),  # The AI acts on behalf of the user
                    'role': 'assistant',
                    'content': ai_response
                }
                self.conversation_service.add_message_to_conversation(session, conversation_id, ai_message_data)

            return {
                "response": ai_response,
                "conversation_id": conversation_id,
                "tool_calls": tool_call_results
            }

        except Exception as e:
            # Handle any errors gracefully
            with next(get_session()) as session:
                # Store the error message in the conversation
                error_message_data = {
                    'user_id': uuid.UUID(user_id),
                    'role': 'assistant',
                    'content': f"I'm sorry, I encountered an error processing your request: {str(e)}"
                }
                self.conversation_service.add_message_to_conversation(session, conversation_id, error_message_data)

            return {
                "response": f"I'm sorry, I encountered an error processing your request: {str(e)}",
                "conversation_id": conversation_id,
                "tool_calls": [],
                "error": str(e)
            }

    def get_available_tools(self) -> List[str]:
        """
        Get a list of available tools that the agent can use.
        """
        return self.mcp_server.get_available_tools()