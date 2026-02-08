"""
MCP (Model Context Protocol) Server for AI Backend & MCP Tooling feature.

This server exposes task management operations as secure, deterministic tools
for AI agents to use.
"""

import asyncio
from typing import Dict, Any, List
from pydantic import BaseModel
import uuid
import logging

logger = logging.getLogger(__name__)


class MCPCall(BaseModel):
    """Represents an MCP tool call."""
    tool_name: str
    parameters: Dict[str, Any]


class MCPResponse(BaseModel):
    """Represents an MCP tool response."""
    success: bool
    result: Dict[str, Any]
    error: str = None


class MCPServer:
    """MCP Server implementation for exposing tools to AI agents."""

    def __init__(self):
        self.tools = {}
        self.registered_tools = {}

    def register_tool(self, name: str, handler):
        """Register an MCP tool with its handler function."""
        self.tools[name] = handler
        logger.info(f"MCP tool registered: {name}")

    async def execute_tool(self, tool_call: MCPCall) -> MCPResponse:
        """Execute an MCP tool call."""
        tool_name = tool_call.tool_name

        if tool_name not in self.tools:
            return MCPResponse(
                success=False,
                result={},
                error=f"Tool '{tool_name}' not found"
            )

        try:
            handler = self.tools[tool_name]
            result = await handler(tool_call.parameters) if asyncio.iscoroutinefunction(handler) else handler(tool_call.parameters)
            return MCPResponse(success=True, result=result)
        except Exception as e:
            logger.error(f"Error executing tool {tool_name}: {str(e)}")
            return MCPResponse(
                success=False,
                result={},
                error=str(e)
            )

    def get_available_tools(self) -> List[str]:
        """Get list of available tools."""
        return list(self.tools.keys())


# Global MCP server instance
mcp_server = MCPServer()


# Import actual tool implementations
from .tools import (
    add_task_tool,
    list_tasks_tool,
    update_task_tool,
    complete_task_tool,
    delete_task_tool
)

# Register the tools with the MCP server
mcp_server.register_tool("add_task", add_task_tool)
mcp_server.register_tool("list_tasks", list_tasks_tool)
mcp_server.register_tool("update_task", update_task_tool)
mcp_server.register_tool("complete_task", complete_task_tool)
mcp_server.register_tool("delete_task", delete_task_tool)


def get_mcp_server():
    """Get the global MCP server instance."""
    return mcp_server