"""
Conversation model for AI Backend & MCP Tooling feature.

This model represents a single conversation thread between a user and the AI assistant.
"""

from datetime import datetime
from typing import Optional
from sqlmodel import SQLModel, Field, Relationship
import uuid


class ConversationBase(SQLModel):
    user_id: uuid.UUID = Field(default=None, foreign_key="users.id")
    title: Optional[str] = Field(default=None, max_length=255)


class Conversation(ConversationBase, table=True):
    """
    Represents a single conversation thread between a user and the AI assistant.
    """
    __tablename__ = "conversation"

    id: Optional[uuid.UUID] = Field(default_factory=uuid.uuid4, primary_key=True)
    user_id: uuid.UUID = Field(foreign_key="users.id")
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    # Relationships
    messages: list["Message"] = Relationship(back_populates="conversation")


class ConversationCreate(ConversationBase):
    """Schema for creating a new conversation."""
    pass


class ConversationRead(ConversationBase):
    """Schema for reading conversation data."""
    id: uuid.UUID
    created_at: datetime
    updated_at: datetime