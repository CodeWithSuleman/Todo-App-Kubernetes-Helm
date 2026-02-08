"""
Todo schemas for the Todo Web Application - Backend Only
"""
from pydantic import BaseModel, ConfigDict, field_serializer
from datetime import datetime
from typing import Optional
import uuid


class TodoBase(BaseModel):
    """Base schema for Todo"""
    title: str
    description: Optional[str] = None
    completed: bool = False
    priority: str = "medium"
    due_date: Optional[str] = None


class TodoCreate(TodoBase):
    """Schema for creating a new Todo"""
    title: str
    priority: str = "medium"
    due_date: Optional[str] = None


class TodoUpdate(BaseModel):
    """Schema for updating a Todo"""
    title: Optional[str] = None
    description: Optional[str] = None
    completed: Optional[bool] = None
    priority: Optional[str] = None
    due_date: Optional[str] = None


class TodoResponse(TodoBase):
    """Schema for Todo response with automatic UUID serialization"""
    id: uuid.UUID
    user_id: uuid.UUID
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)

    @field_serializer('id', 'user_id')
    def serialize_uuid(self, value: uuid.UUID) -> str:
        """Convert UUID to string for JSON serialization"""
        return str(value)
