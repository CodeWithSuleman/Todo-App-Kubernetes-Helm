// frontend/lib/api/chat/storage.ts

import { Conversation } from '../../types/chat';

const CONVERSATIONS_KEY = 'chat_conversations';
const CURRENT_CONVERSATION_ID_KEY = 'current_chat_conversation_id';

export const conversationStorage = {
  saveConversation(conversation: Conversation): void {
    try {
      const conversations = this.loadConversations();
      const index = conversations.findIndex((c) => c.id === conversation.id);
      if (index !== -1) {
        conversations[index] = conversation;
      } else {
        conversations.push(conversation);
      }
      localStorage.setItem(CONVERSATIONS_KEY, JSON.stringify(conversations));
    } catch (error) {
      console.error('Failed to save conversation to localStorage:', error);
    }
  },

  loadConversations(): Conversation[] {
    try {
      const conversationsJson = localStorage.getItem(CONVERSATIONS_KEY);
      return conversationsJson ? JSON.parse(conversationsJson) : [];
    } catch (error) {
      console.error('Failed to load conversations from localStorage:', error);
      return [];
    }
  },

  loadConversation(conversationId: string): Conversation | undefined {
    const conversations = this.loadConversations();
    return conversations.find((c) => c.id === conversationId);
  },

  deleteConversation(conversationId: string): void {
    try {
      const conversations = this.loadConversations();
      const updatedConversations = conversations.filter((c) => c.id !== conversationId);
      localStorage.setItem(CONVERSATIONS_KEY, JSON.stringify(updatedConversations));
    } catch (error) {
      console.error('Failed to delete conversation from localStorage:', error);
    }
  },

  getConversationMetadata() {
    const conversations = this.loadConversations();
    return conversations.map(c => ({
      id: c.id,
      title: c.title || 'Untitled Conversation',
      userId: c.userId,
      lastMessage: c.messages[c.messages.length - 1]?.content || 'No messages',
      timestamp: c.updatedAt,
    }));
  },

  getMostRecentConversation(): Conversation | undefined {
    const conversations = this.loadConversations();
    if (conversations.length === 0) {
      return undefined;
    }
    return conversations.reduce((latest, current) => {
      return new Date(latest.updatedAt) > new Date(current.updatedAt) ? latest : current;
    });
  },

  setCurrentConversationId(conversationId: string): void {
    localStorage.setItem(CURRENT_CONVERSATION_ID_KEY, conversationId);
  },

  getCurrentConversationId(): string | null {
    return localStorage.getItem(CURRENT_CONVERSATION_ID_KEY);
  },

  clearCurrentConversationId(): void {
    localStorage.removeItem(CURRENT_CONVERSATION_ID_KEY);
  },
};