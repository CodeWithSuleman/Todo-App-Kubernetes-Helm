# Data Model: AI Backend & MCP Tooling

**Feature**: AI Backend & MCP Tooling
**Date**: 2026-02-05

## Overview

This document defines the data models required for the AI Backend & MCP Tooling feature. It extends the existing data model to include conversation and message entities while maintaining compatibility with the existing todo and user models.

## Entity Definitions

### Conversation
**Description**: Represents a single conversation thread between a user and the AI assistant

**Fields**:
- `id`: UUID (Primary Key) - Unique identifier for the conversation
- `user_id`: UUID (Foreign Key) - Reference to the user who owns this conversation
- `created_at`: DateTime - Timestamp when the conversation was created
- `updated_at`: DateTime - Timestamp when the conversation was last updated

**Relationships**:
- One-to-Many with Message (one conversation can have many messages)
- Many-to-One with User (many conversations belong to one user)

**Validation Rules**:
- `user_id` must reference an existing user
- `created_at` must be in the past
- `updated_at` must be >= `created_at`

### Message
**Description**: Represents an individual message within a conversation thread

**Fields**:
- `id`: UUID (Primary Key) - Unique identifier for the message
- `user_id`: UUID (Foreign Key) - Reference to the user who sent/owns this message
- `conversation_id`: UUID (Foreign Key) - Reference to the conversation this message belongs to
- `role`: String (Enum: 'user', 'assistant', 'system') - The role of the message sender
- `content`: Text - The actual content of the message
- `created_at`: DateTime - Timestamp when the message was created
- `updated_at`: DateTime - Timestamp when the message was last updated

**Relationships**:
- Many-to-One with Conversation (many messages belong to one conversation)
- Many-to-One with User (many messages belong to one user)

**Validation Rules**:
- `user_id` must reference an existing user
- `conversation_id` must reference an existing conversation
- `user_id` in message must match the `user_id` of the conversation
- `role` must be one of the allowed values ('user', 'assistant', 'system')
- `content` cannot be empty or null
- `created_at` must be in the past
- `updated_at` must be >= `created_at`

## Existing Entity Relationships

### User (Existing)
- One-to-Many with Conversation
- One-to-Many with Message
- One-to-Many with Todo (existing relationship)

### Todo (Existing)
- No direct changes required for this feature
- Related to users through existing foreign key relationship

## State Transitions

### Message State
Messages are immutable once created in this system. Updates are primarily for metadata like timestamps.

### Conversation State
Conversations are extended by adding new messages. The `updated_at` field reflects when the last message was added.

## Constraints and Business Rules

1. **User Isolation**: Users can only access conversations and messages associated with their user_id
2. **Data Integrity**: Foreign key constraints ensure referential integrity between entities
3. **Immutability**: Message content should not be modified after creation to preserve conversation history
4. **Ownership**: All data access must be validated against the authenticated user's identity

## Indexes

1. Conversation: Index on (user_id, created_at) for efficient retrieval of user's conversations
2. Message: Index on (conversation_id, created_at) for efficient chronological retrieval of messages
3. Message: Index on (user_id, conversation_id) for efficient user-specific message queries

## API Access Patterns

1. Retrieve all conversations for a user
2. Retrieve all messages in a specific conversation
3. Add a new message to a conversation
4. Update conversation metadata