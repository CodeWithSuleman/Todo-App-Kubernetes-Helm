# Data Model: Chat Interface & AI UX

## Overview
This document defines the data structures and relationships for the chat interface feature, focusing on client-side representations that align with the existing backend models.

## Client-Side Data Structures

### ChatMessage
Represents an individual message in the chat interface:

- **id**: string (unique identifier for the message)
- **content**: string (the text content of the message)
- **sender**: "user" | "ai" (indicates the source of the message)
- **timestamp**: Date (when the message was sent/received)
- **status**: "sending" | "delivered" | "error" (delivery status of the message)
- **conversationId**: string (ID of the conversation this message belongs to)

### Conversation
Represents a conversation thread between user and AI:

- **id**: string (unique identifier for the conversation)
- **userId**: string (ID of the user this conversation belongs to)
- **title**: string (optional, derived from first message or user-defined)
- **messages**: ChatMessage[] (array of messages in chronological order)
- **createdAt**: Date (when the conversation was started)
- **updatedAt**: Date (when the conversation was last updated)

### ChatState
Represents the current state of the chat interface:

- **isLoading**: boolean (whether the AI is currently processing a response)
- **error**: string | null (any error message to display)
- **currentConversationId**: string | null (ID of the active conversation)
- **conversations**: Conversation[] (list of all conversations for the user)
- **inputText**: string (current value in the message input field)

## API Request/Response Models

### ChatRequest (Client → Server)
- **message**: string (the user's message to send to the AI)
- **conversation_id**: string | null (ID of the conversation to continue, or null for new conversation)

### ChatResponse (Server → Client)
- **response**: string (the AI's response to the user's message)
- **conversation_id**: string (ID of the conversation this response belongs to)
- **tool_calls**: Array<{tool_name: string, parameters: Object, result: Object}> (list of tools called by the AI)
- **message_id**: string (unique ID for this response message)

## Validation Rules

### From Requirements
- **FR-005**: Conversation history must persist between browser refreshes
- **FR-006**: Loading indicators must show when awaiting AI responses
- **FR-007**: Error messages must be displayed when API calls fail
- **FR-009**: User ID validation must prevent access to other users' conversations

### Implementation Considerations
- Message content must be sanitized to prevent XSS attacks (FR-010)
- User ID from JWT must match the conversation's user ID
- Message length should be limited to prevent abuse
- Timestamps must be properly formatted for display

## State Transitions

### Chat Loading States
1. Initial state: `isLoading = false`, `error = null`
2. Message sending: `isLoading = true`, `error = null`
3. Successful response: `isLoading = false`, `error = null`
4. Error occurred: `isLoading = false`, `error = errorMessage`
5. Retry after error: `isLoading = true`, `error = null`

### Message Status Transitions
1. User sends message: `status = "sending"`
2. Message delivered to server: `status = "delivered"`
3. Error occurs: `status = "error"`