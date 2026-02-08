/**
 * TypeScript type definitions for chat entities
 * Chat Interface & AI UX Feature
 */

export type MessageSender = "user" | "ai";
export type MessageStatus = "sending" | "delivered" | "error";

/**
 * Represents an individual message in the chat interface
 */
export interface ChatMessage {
  id: string;
  content: string;
  sender: MessageSender;
  timestamp: Date;
  status: MessageStatus;
  conversationId: string;
}

/**
 * Represents a conversation thread between user and AI
 */
export interface Conversation {
  id: string;
  userId: string;
  title?: string;
  messages: ChatMessage[];
  createdAt: Date;
  updatedAt: Date;
}

/**
 * Lightweight metadata for conversation list display
 */
export interface ConversationMetadata {
  id: string;
  title: string;
  userId: string;
  lastMessage: string;
  timestamp: Date;
}

/**
 * Represents the current state of the chat interface
 */
export interface ChatState {
  isLoading: boolean;
  error: string | null;
  currentConversationId: string | null;
  conversations: Conversation[];
  inputText: string;
}

/**
 * Request payload for sending a chat message to the API
 */
export interface ChatRequest {
  message: string;
  conversation_id?: string | null;
}

/**
 * Tool call result from the AI assistant
 */
export interface ToolCallResult {
  tool_name: string;
  parameters: Record<string, unknown>;
  result: Record<string, unknown>;
}

/**
 * Response payload from the chat API
 */
export interface ChatResponse {
  response: string;
  conversation_id: string;
  tool_calls: ToolCallResult[];
  message_id: string;
}
