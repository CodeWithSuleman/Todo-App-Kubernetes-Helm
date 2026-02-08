/**
 * ChatService - Handles API communication with the chat endpoint
 * Chat Interface & AI UX Feature
 */

import { ChatRequest, ChatResponse, Conversation, ChatMessage } from '@/lib/types/chat';
import { CHAT_API_ENDPOINT, ERROR_MESSAGES } from '@/lib/constants/chat';
import { conversationStorage } from './storage';

export class ChatService {
  private baseUrl: string;
  private token: string | null;

  constructor(baseUrl: string = process.env.NEXT_PUBLIC_API_BASE_URL || 'http://localhost:8000') {
    this.baseUrl = baseUrl;
    this.token = null;
  }

  /**
   * Set the JWT authentication token
   * @param token JWT token for authentication
   */
  setToken(token: string): void {
    this.token = token;
  }

  /**
   * Remove the JWT authentication token
   */
  removeToken(): void {
    this.token = null;
  }

  /**
   * Get authentication headers with JWT token
   * @returns Headers object with authorization
   */
  private getAuthHeaders(): HeadersInit {
    const headers: HeadersInit = {
      'Content-Type': 'application/json',
    };

    if (this.token) {
      headers['Authorization'] = `Bearer ${this.token}`;
    }

    return headers;
  }

  /**
   * Send a message to the AI assistant
   * @param userId User ID from authenticated session
   * @param request Chat request payload
   * @returns Chat response from the API
   */
  async sendMessage(userId: string, request: ChatRequest): Promise<ChatResponse> {
    if (!this.token) {
      throw new Error(ERROR_MESSAGES.AUTH_ERROR);
    }

    try {
      const response = await fetch(
        `${this.baseUrl}${CHAT_API_ENDPOINT}/${userId}/chat`,
        {
          method: 'POST',
          headers: this.getAuthHeaders(),
          body: JSON.stringify(request),
        }
      );

      if (!response.ok) {
        if (response.status === 401 || response.status === 403) {
          throw new Error(ERROR_MESSAGES.AUTH_ERROR);
        }
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      const data: ChatResponse = await response.json();
      
      // Save conversation
      if (data.conversation_id) {
        const conversations = this.loadConversations();
        let conversation = conversations.find(c => c.id === data.conversation_id);
        if (!conversation) {
          conversation = {
            id: data.conversation_id,
            userId: userId,
            messages: [],
            createdAt: new Date(),
            updatedAt: new Date(),
          };
        }
        conversation.messages.push({
            id: data.message_id,
            content: data.response,
            sender: 'ai',
            timestamp: new Date(),
            status: 'delivered',
            conversationId: data.conversation_id,
        });
        conversation.updatedAt = new Date();
        this.saveConversation(conversation);
      }

      return data;
    } catch (error) {
      if (error instanceof Error) {
        if (error.message.includes('Failed to fetch') || error.message.includes('NetworkError')) {
          throw new Error(ERROR_MESSAGES.NETWORK_ERROR);
        }
        throw error;
      }
      throw new Error(ERROR_MESSAGES.GENERIC_ERROR);
    }
  }

  /**
   * Save a message to a conversation
   * @param userId 
   * @param conversationId 
   * @param message 
   */
  saveMessage(userId: string, conversationId: string, message: ChatMessage): void {
    const conversations = this.loadConversations();
    let conversation = conversations.find(c => c.id === conversationId);
    if (!conversation) {
      conversation = {
        id: conversationId,
        userId: userId,
        messages: [],
        createdAt: new Date(),
        updatedAt: new Date(),
      };
    }
    conversation.messages.push(message);
    conversation.updatedAt = new Date();
    this.saveConversation(conversation);
  }

  /**
   * Save a conversation
   * @param conversation
   */
  saveConversation(conversation: Conversation): void {
    conversationStorage.saveConversation(conversation);
  }

  /**
   * Load all conversations
   * @returns Array of conversations
   */
  loadConversations(): Conversation[] {
    return conversationStorage.loadConversations();
  }

  /**
   * Delete a conversation
   * @param conversationId
   */
  deleteConversation(conversationId: string): void {
    conversationStorage.deleteConversation(conversationId);
  }


  /**
   * Check if the service has a valid token
   * @returns true if token is set
   */
  hasToken(): boolean {
    return this.token !== null;
  }
}

// Export a singleton instance
export const chatService = new ChatService();
