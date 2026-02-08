"""
MCP Tools for AI Backend & MCP Tooling feature.

This module implements the specific MCP tools for task operations.
"""

import uuid
from datetime import datetime
from typing import Dict, Any
from sqlmodel import Session, select
from ..database import get_session
from ..models.todo import Todo
from ..models.user import User
import asyncio


async def add_task_tool(params: Dict[str, Any]) -> Dict[str, Any]:
    """
    MCP Tool: add_task
    Purpose: Add a new task to the user's todo list
    Input schema:
      - title: string (required) - The title of the task
      - description: string (optional) - A detailed description of the task
      - user_id: string (required) - The ID of the user creating the task
    Output schema:
      - task_id: string (uuid) - The ID of the created task
      - title: string - The title of the created task
      - description: string - The description of the created task
      - status: string - The status of the task (pending)
      - created_at: string (datetime) - When the task was created
    """
    # Extract parameters
    title = params.get("title")
    description = params.get("description", "")
    user_id = params.get("user_id")

    if not title:
        raise ValueError("Title is required for add_task")

    if not user_id:
        raise ValueError("User ID is required for add_task")

    # Validate user_id format
    try:
        user_uuid = uuid.UUID(user_id)
    except ValueError:
        raise ValueError(f"Invalid user ID format: {user_id}")

    # Validate user ownership
    is_valid = await validate_user_ownership_for_add_task({"user_id": user_id})
    if not is_valid:
        raise ValueError(f"User {user_id} is not authorized to add tasks")

    # Create a new task using the database session
    with next(get_session()) as session:
        # Verify the user exists
        user = session.get(User, user_uuid)
        if not user:
            raise ValueError(f"User with ID {user_id} not found")

        # Create the new task
        new_task = Todo(
            title=title,
            description=description,
            user_id=user_uuid,
            status="pending"
        )

        session.add(new_task)
        session.commit()
        session.refresh(new_task)

        return {
            "task_id": str(new_task.id),
            "title": new_task.title,
            "description": new_task.description,
            "status": new_task.status,
            "created_at": new_task.created_at.isoformat() if new_task.created_at else datetime.utcnow().isoformat()
        }


async def list_tasks_tool(params: Dict[str, Any]) -> Dict[str, Any]:
    """
    MCP Tool: list_tasks
    Purpose: Retrieve all tasks for the current user
    Input schema:
      - user_id: string (required) - The ID of the user whose tasks to retrieve
    Output schema:
      - tasks: array of task objects
        - task_id: string (uuid) - The ID of the task
        - title: string - The title of the task
        - description: string - A detailed description of the task
        - status: string - The status of the task
        - created_at: string (datetime) - When the task was created
        - updated_at: string (datetime) - When the task was last updated
    """
    user_id = params.get("user_id")

    if not user_id:
        raise ValueError("User ID is required for list_tasks")

    # Validate user_id format
    try:
        user_uuid = uuid.UUID(user_id)
    except ValueError:
        raise ValueError(f"Invalid user ID format: {user_id}")

    # Validate user ownership
    is_valid = await validate_user_ownership_for_list_tasks({"user_id": user_id})
    if not is_valid:
        raise ValueError(f"User {user_id} is not authorized to list tasks")

    # Query tasks for the user
    with next(get_session()) as session:
        # Verify the user exists
        user = session.get(User, user_uuid)
        if not user:
            raise ValueError(f"User with ID {user_id} not found")

        # Get all tasks for the user
        statement = select(Todo).where(Todo.user_id == user_uuid)
        user_tasks = session.exec(statement).all()

        tasks = []
        for task in user_tasks:
            tasks.append({
                "task_id": str(task.id),
                "title": task.title,
                "description": task.description or "",
                "status": task.status,
                "created_at": task.created_at.isoformat() if task.created_at else "",
                "updated_at": task.updated_at.isoformat() if task.updated_at else ""
            })

        return {"tasks": tasks}


async def update_task_tool(params: Dict[str, Any]) -> Dict[str, Any]:
    """
    MCP Tool: update_task
    Purpose: Update an existing task's properties
    Input schema:
      - task_id: string (uuid, required) - The ID of the task to update
      - user_id: string (required) - The ID of the user who owns the task
      - title: string (optional) - The new title of the task
      - description: string (optional) - The new description of the task
      - status: string (optional) - The new status of the task
    Output schema:
      - task_id: string (uuid) - The ID of the updated task
      - title: string - The updated title of the task
      - description: string - The updated description of the task
      - status: string - The updated status of the task
      - updated_at: string (datetime) - When the task was last updated
    """
    task_id = params.get("task_id")
    user_id = params.get("user_id")
    title = params.get("title")
    description = params.get("description")
    status = params.get("status")

    if not task_id:
        raise ValueError("Task ID is required for update_task")

    if not user_id:
        raise ValueError("User ID is required for update_task")

    # Validate UUID formats
    try:
        task_uuid = uuid.UUID(task_id)
        user_uuid = uuid.UUID(user_id)
    except ValueError as e:
        raise ValueError(f"Invalid UUID format: {str(e)}")

    # Validate user ownership
    is_valid = await validate_user_ownership_for_update_task({
        "task_id": task_id,
        "user_id": user_id
    })
    if not is_valid:
        raise ValueError(f"User {user_id} is not authorized to update task {task_id}")

    # Update the task in the database
    with next(get_session()) as session:
        # Verify the user exists
        user = session.get(User, user_uuid)
        if not user:
            raise ValueError(f"User with ID {user_id} not found")

        # Get the task
        task = session.get(Todo, task_uuid)
        if not task:
            raise ValueError(f"Task with ID {task_id} not found")

        # Verify the task belongs to the user (redundant check with validation above)
        if str(task.user_id) != user_id:
            raise ValueError(f"Task with ID {task_id} does not belong to user {user_id}")

        # Update task properties if provided
        if title is not None:
            task.title = title
        if description is not None:
            task.description = description
        if status is not None:
            task.status = status

        task.updated_at = datetime.utcnow()
        session.add(task)
        session.commit()
        session.refresh(task)

        return {
            "task_id": str(task.id),
            "title": task.title,
            "description": task.description or "",
            "status": task.status,
            "updated_at": task.updated_at.isoformat()
        }


async def complete_task_tool(params: Dict[str, Any]) -> Dict[str, Any]:
    """
    MCP Tool: complete_task
    Purpose: Mark a task as completed
    Input schema:
      - task_id: string (uuid, required) - The ID of the task to complete
      - user_id: string (required) - The ID of the user who owns the task
    Output schema:
      - task_id: string (uuid) - The ID of the completed task
      - title: string - The title of the completed task
      - status: string - The status of the task (completed)
      - completed_at: string (datetime) - When the task was completed
    """
    task_id = params.get("task_id")
    user_id = params.get("user_id")

    if not task_id:
        raise ValueError("Task ID is required for complete_task")

    if not user_id:
        raise ValueError("User ID is required for complete_task")

    # Validate UUID formats
    try:
        task_uuid = uuid.UUID(task_id)
        user_uuid = uuid.UUID(user_id)
    except ValueError as e:
        raise ValueError(f"Invalid UUID format: {str(e)}")

    # Validate user ownership
    is_valid = await validate_user_ownership_for_complete_task({
        "task_id": task_id,
        "user_id": user_id
    })
    if not is_valid:
        raise ValueError(f"User {user_id} is not authorized to complete task {task_id}")

    # Update the task status to completed
    with next(get_session()) as session:
        # Verify the user exists
        user = session.get(User, user_uuid)
        if not user:
            raise ValueError(f"User with ID {user_id} not found")

        # Get the task
        task = session.get(Todo, task_uuid)
        if not task:
            raise ValueError(f"Task with ID {task_id} not found")

        # Verify the task belongs to the user (redundant check with validation above)
        if str(task.user_id) != user_id:
            raise ValueError(f"Task with ID {task_id} does not belong to user {user_id}")

        # Update task status to completed
        task.status = "completed"
        task.updated_at = datetime.utcnow()
        session.add(task)
        session.commit()
        session.refresh(task)

        return {
            "task_id": str(task.id),
            "title": task.title,
            "status": task.status,
            "completed_at": task.updated_at.isoformat()
        }


async def delete_task_tool(params: Dict[str, Any]) -> Dict[str, Any]:
    """
    MCP Tool: delete_task
    Purpose: Delete a task from the user's todo list
    Input schema:
      - task_id: string (uuid, required) - The ID of the task to delete
      - user_id: string (required) - The ID of the user who owns the task
    Output schema:
      - task_id: string (uuid) - The ID of the deleted task
      - deleted: boolean - Whether the task was successfully deleted
    """
    task_id = params.get("task_id")
    user_id = params.get("user_id")

    if not task_id:
        raise ValueError("Task ID is required for delete_task")

    if not user_id:
        raise ValueError("User ID is required for delete_task")

    # Validate UUID formats
    try:
        task_uuid = uuid.UUID(task_id)
        user_uuid = uuid.UUID(user_id)
    except ValueError as e:
        raise ValueError(f"Invalid UUID format: {str(e)}")

    # Validate user ownership
    is_valid = await validate_user_ownership_for_delete_task({
        "task_id": task_id,
        "user_id": user_id
    })
    if not is_valid:
        raise ValueError(f"User {user_id} is not authorized to delete task {task_id}")

    # Delete the task from the database
    with next(get_session()) as session:
        # Verify the user exists
        user = session.get(User, user_uuid)
        if not user:
            raise ValueError(f"User with ID {user_id} not found")

        # Get the task
        task = session.get(Todo, task_uuid)
        if not task:
            raise ValueError(f"Task with ID {task_id} not found")

        # Verify the task belongs to the user (redundant check with validation above)
        if str(task.user_id) != user_id:
            raise ValueError(f"Task with ID {task_id} does not belong to user {user_id}")

        # Delete the task
        session.delete(task)
        session.commit()

        return {
            "task_id": task_id,
            "deleted": True
        }


# User ownership validation functions for security (used in User Story 2)
async def validate_user_ownership_for_add_task(params: Dict[str, Any]) -> bool:
    """Validate that the user has permission to add a task for themselves."""
    user_id = params.get("user_id")
    if not user_id:
        return False

    try:
        user_uuid = uuid.UUID(user_id)
        with next(get_session()) as session:
            user = session.get(User, user_uuid)
            return user is not None
    except ValueError:
        return False


async def validate_user_ownership_for_list_tasks(params: Dict[str, Any]) -> bool:
    """Validate that the user has permission to list their own tasks."""
    user_id = params.get("user_id")
    if not user_id:
        return False

    try:
        user_uuid = uuid.UUID(user_id)
        with next(get_session()) as session:
            user = session.get(User, user_uuid)
            return user is not None
    except ValueError:
        return False


async def validate_user_ownership_for_update_task(params: Dict[str, Any]) -> bool:
    """Validate that the user has permission to update a task they own."""
    task_id = params.get("task_id")
    user_id = params.get("user_id")

    if not task_id or not user_id:
        return False

    try:
        task_uuid = uuid.UUID(task_id)
        user_uuid = uuid.UUID(user_id)

        with next(get_session()) as session:
            task = session.get(Todo, task_uuid)
            return task and str(task.user_id) == user_id
    except ValueError:
        return False


async def validate_user_ownership_for_complete_task(params: Dict[str, Any]) -> bool:
    """Validate that the user has permission to complete a task they own."""
    task_id = params.get("task_id")
    user_id = params.get("user_id")

    if not task_id or not user_id:
        return False

    try:
        task_uuid = uuid.UUID(task_id)
        user_uuid = uuid.UUID(user_id)

        with next(get_session()) as session:
            task = session.get(Todo, task_uuid)
            return task and str(task.user_id) == user_id
    except ValueError:
        return False


async def validate_user_ownership_for_delete_task(params: Dict[str, Any]) -> bool:
    """Validate that the user has permission to delete a task they own."""
    task_id = params.get("task_id")
    user_id = params.get("user_id")

    if not task_id or not user_id:
        return False

    try:
        task_uuid = uuid.UUID(task_id)
        user_uuid = uuid.UUID(user_id)

        with next(get_session()) as session:
            task = session.get(Todo, task_uuid)
            return task and str(task.user_id) == user_id
    except ValueError:
        return False