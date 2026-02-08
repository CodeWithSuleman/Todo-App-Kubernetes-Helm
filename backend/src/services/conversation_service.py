"""
Conversation Service for AI Backend & MCP Tooling feature.

This service handles conversation-related operations including creation,
retrieval, and management of conversation threads.
"""

from datetime import datetime
from typing import List, Optional
from sqlmodel import Session, select
from ..models.conversation import Conversation, ConversationCreate
from ..models.message import Message


class ConversationService:
    """Service class for managing conversations."""

    def create_conversation(self, session: Session, conversation_data: ConversationCreate) -> Conversation:
        """Create a new conversation."""
        conversation = Conversation(
            user_id=conversation_data.user_id,
            title=conversation_data.title,
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow()
        )
        session.add(conversation)
        session.commit()
        session.refresh(conversation)
        return conversation

    def get_conversation_by_id(self, session: Session, conversation_id: str) -> Optional[Conversation]:
        """Retrieve a conversation by its ID."""
        statement = select(Conversation).where(Conversation.id == conversation_id)
        return session.exec(statement).first()

    def get_conversations_by_user(self, session: Session, user_id: str) -> List[Conversation]:
        """Retrieve all conversations for a specific user."""
        statement = select(Conversation).where(Conversation.user_id == user_id)
        return session.exec(statement).all()

    def update_conversation(self, session: Session, conversation_id: str, title: str = None) -> Optional[Conversation]:
        """Update a conversation's details."""
        conversation = self.get_conversation_by_id(session, conversation_id)
        if conversation:
            if title is not None:
                conversation.title = title
            conversation.updated_at = datetime.utcnow()
            session.add(conversation)
            session.commit()
            session.refresh(conversation)
        return conversation

    def delete_conversation(self, session: Session, conversation_id: str) -> bool:
        """Delete a conversation."""
        conversation = self.get_conversation_by_id(session, conversation_id)
        if conversation:
            session.delete(conversation)
            session.commit()
            return True
        return False

    def add_message_to_conversation(self, session: Session, conversation_id: str, message_data: dict) -> Message:
        """Add a message to a conversation."""
        from ..models.message import Message  # Import here to avoid circular imports

        message = Message(
            user_id=message_data['user_id'],
            conversation_id=conversation_id,
            role=message_data['role'],
            content=message_data['content'],
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow()
        )
        session.add(message)
        session.commit()
        session.refresh(message)
        return message

    def get_messages_for_conversation(self, session: Session, conversation_id: str) -> List[Message]:
        """Retrieve all messages for a specific conversation."""
        from ..models.message import Message  # Import here to avoid circular imports

        statement = select(Message).where(Message.conversation_id == conversation_id)
        return session.exec(statement).all()

    def get_conversation_context(self, session: Session, conversation_id: str, limit: int = 10) -> List[dict]:
        """Get conversation context (recent messages) for AI processing."""
        messages = self.get_messages_for_conversation(session, conversation_id)
        # Sort by creation time and take the most recent messages up to the limit
        sorted_messages = sorted(messages, key=lambda msg: msg.created_at, reverse=True)[:limit]

        # Return message context in a format suitable for AI processing
        return [
            {
                'role': msg.role,
                'content': msg.content,
                'timestamp': msg.created_at.isoformat()
            }
            for msg in sorted_messages
        ]