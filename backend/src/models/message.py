"""
Message model for AI Backend & MCP Tooling feature.

This model represents an individual message within a conversation thread.
"""

from datetime import datetime
from typing import Optional
from sqlmodel import SQLModel, Field, Relationship
import uuid


class MessageBase(SQLModel):
    user_id: uuid.UUID = Field(default=None, foreign_key="users.id")
    conversation_id: uuid.UUID = Field(default=None, foreign_key="conversation.id")
    role: str = Field(max_length=20)  # 'user', 'assistant', 'system'
    content: str


class Message(MessageBase, table=True):
    """
    Represents an individual message within a conversation thread.
    """
    __tablename__ = "message"

    id: Optional[uuid.UUID] = Field(default_factory=uuid.uuid4, primary_key=True)
    user_id: uuid.UUID = Field(foreign_key="users.id")
    conversation_id: uuid.UUID = Field(foreign_key="conversation.id")
    role: str = Field(max_length=20)  # 'user', 'assistant', 'system'
    content: str
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    # Relationships
    conversation: "Conversation" = Relationship(back_populates="messages")


class MessageCreate(MessageBase):
    """Schema for creating a new message."""
    pass


class MessageRead(MessageBase):
    """Schema for reading message data."""
    id: uuid.UUID
    created_at: datetime
    updated_at: datetime