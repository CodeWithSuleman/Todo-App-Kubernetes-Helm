'use client';

import React, { useState, useEffect } from 'react';
import { ChatMessage, ChatState, Conversation, ConversationMetadata } from '@/lib/types/chat';
import { MessageList } from './MessageList';
import { MessageInput } from './MessageInput';
import { ConversationHistory } from './ConversationHistory';
import { chatService } from '@/lib/api/chat/service';
import { conversationStorage } from '@/lib/api/chat/storage';
import { useAuth } from '@/components/providers/auth-provider';
import { LoadingIndicator } from './LoadingIndicator';
import { ErrorMessage } from './ErrorMessage';
import { EmptyState } from './EmptyState';
import ErrorBoundary from './ErrorBoundary';

const ChatContainerInternal: React.FC = () => {
  const { user, token } = useAuth();
  const [chatState, setChatState] = useState<ChatState>({
    isLoading: false,
    error: null,
    currentConversationId: null,
    conversations: [],
    inputText: '',
  });
  const [messages, setMessages] = useState<ChatMessage[]>([]);
  const [showHistory, setShowHistory] = useState(true);
  const [conversationMetadata, setConversationMetadata] = useState<ConversationMetadata[]>([]);
  const [lastMessage, setLastMessage] = useState<string | null>(null);

  // Set token in chat service when available
  useEffect(() => {
    if (token) {
      chatService.setToken(token);
    }
  }, [token]);

  // Load conversations and most recent conversation on mount
  useEffect(() => {
    if (user) {
      // Load conversation metadata
      const metadata = conversationStorage.getConversationMetadata();
      setConversationMetadata(metadata.filter(m => m.userId === user.id));

      // Load most recent conversation
      const recentConversation = conversationStorage.getMostRecentConversation();
      if (recentConversation && recentConversation.userId === user.id) {
        setMessages(recentConversation.messages);
        setChatState(prev => ({
          ...prev,
          currentConversationId: recentConversation.id,
        }));
        conversationStorage.setCurrentConversationId(recentConversation.id);
      }
    }
  }, [user]);

  const handleSelectConversation = (conversationId: string) => {
    const conversation = conversationStorage.loadConversation(conversationId);
    if (conversation && conversation.userId === user?.id) {
      setMessages(conversation.messages);
      setChatState(prev => ({
        ...prev,
        currentConversationId: conversation.id,
        error: null,
      }));
      conversationStorage.setCurrentConversationId(conversation.id);
    }
  };

  const handleDeleteConversation = (conversationId: string) => {
    conversationStorage.deleteConversation(conversationId);

    // Update metadata
    const metadata = conversationStorage.getConversationMetadata();
    setConversationMetadata(metadata.filter(m => m.userId === user?.id));

    // Clear messages if current conversation was deleted
    if (chatState.currentConversationId === conversationId) {
      setMessages([]);
      setChatState(prev => ({
        ...prev,
        currentConversationId: null,
      }));
    }
  };

  const handleNewConversation = () => {
    setMessages([]);
    setChatState(prev => ({
      ...prev,
      currentConversationId: null,
      error: null,
    }));
    conversationStorage.clearCurrentConversationId();
  };

  const handleSendMessage = async (messageContent: string) => {
    if (!user || !token) {
      setChatState(prev => ({
        ...prev,
        error: 'You must be logged in to send messages',
      }));
      return;
    }
    setLastMessage(messageContent);

    // Create user message
    const userMessage: ChatMessage = {
      id: `temp-${Date.now()}`,
      content: messageContent,
      sender: 'user',
      timestamp: new Date(),
      status: 'sending',
      conversationId: chatState.currentConversationId || '',
    };

    // Add user message to UI immediately
    setMessages(prev => [...prev, userMessage]);
    setChatState(prev => ({ ...prev, isLoading: true, error: null }));

    try {
      // Send message to API
      const response = await chatService.sendMessage(user.id, {
        message: messageContent,
        conversation_id: chatState.currentConversationId,
      });

      // Update user message status
      setMessages(prev =>
        prev.map(msg =>
          msg.id === userMessage.id
            ? { ...msg, status: 'delivered' as const, conversationId: response.conversation_id }
            : msg
        )
      );

      // Add AI response
      const aiMessage: ChatMessage = {
        id: response.message_id,
        content: response.response,
        sender: 'ai',
        timestamp: new Date(),
        status: 'delivered',
        conversationId: response.conversation_id,
      };

      setMessages(prev => [...prev, aiMessage]);

      // Update conversation ID if this is a new conversation
      if (!chatState.currentConversationId) {
        setChatState(prev => ({
          ...prev,
          currentConversationId: response.conversation_id,
        }));
      }

      // Persist conversation to localStorage
      const updatedMessages = [...messages.map(msg =>
        msg.id === userMessage.id
          ? { ...msg, status: 'delivered' as const, conversationId: response.conversation_id }
          : msg
      ), aiMessage];

      const conversation: Conversation = {
        id: response.conversation_id,
        userId: user.id,
        title: updatedMessages[0]?.content.substring(0, 50) || 'New conversation',
        messages: updatedMessages,
        createdAt: new Date(),
        updatedAt: new Date(),
      };

      conversationStorage.saveConversation(conversation);
      conversationStorage.setCurrentConversationId(response.conversation_id);

      // Update conversation metadata
      const metadata = conversationStorage.getConversationMetadata();
      setConversationMetadata(metadata.filter(m => m.userId === user.id));
    } catch (error) {
      console.error('Failed to send message:', error);

      // Update user message to error state
      setMessages(prev =>
        prev.map(msg =>
          msg.id === userMessage.id
            ? { ...msg, status: 'error' as const }
            : msg
        )
      );

      setChatState(prev => ({
        ...prev,
        error: error instanceof Error ? error.message : 'Failed to send message',
      }));
    } finally {
      setChatState(prev => ({ ...prev, isLoading: false }));
    }
  };

  const handleRetry = () => {
    if (lastMessage) {
        handleSendMessage(lastMessage);
    }
  }

  return (
    <div className="flex h-full bg-white">
      {/* Conversation History Sidebar */}
      {showHistory && (
        <ConversationHistory
          conversations={conversationMetadata}
          onSelectConversation={handleSelectConversation}
          onDeleteConversation={handleDeleteConversation}
        />
      )}

      {/* Main Chat Area */}
      <div className="flex flex-1 flex-col">
        {/* Header */}
        <div className="border-b border-gray-200 bg-white px-6 py-4 flex items-center justify-between">
          <div>
            <h1 className="text-xl font-semibold text-gray-900">AI Assistant</h1>
            <p className="text-sm text-gray-500">
              Manage your todos with natural language
            </p>
          </div>
          <div className="flex items-center gap-2">
            <button
              onClick={handleNewConversation}
              className="px-3 py-2 text-sm bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors"
              title="Start new conversation"
            >
              New Chat
            </button>
            <button
              onClick={() => setShowHistory(!showHistory)}
              className="p-2 rounded-lg hover:bg-gray-100 transition-colors"
              title={showHistory ? 'Hide history' : 'Show history'}
            >
              <svg
                className="w-6 h-6 text-gray-600"
                fill="none"
                stroke="currentColor"
                viewBox="0 0 24 24"
              >
                <path
                  strokeLinecap="round"
                  strokeLinejoin="round"
                  strokeWidth={2}
                  d="M4 6h16M4 12h16M4 18h16"
                />
              </svg>
            </button>
          </div>
        </div>

        {/* Error banner */}
        {chatState.error && (
          <ErrorMessage message={chatState.error} onRetry={handleRetry} />
        )}

        {/* Messages */}
        {messages.length === 0 && !chatState.isLoading && !chatState.error && <EmptyState />}
        <MessageList messages={messages} />
        {chatState.isLoading && <LoadingIndicator />}


        {/* Input */}
        <MessageInput
          onSendMessage={handleSendMessage}
          disabled={chatState.isLoading || !user}
        />
      </div>
    </div>
  );
};

export const ChatContainer: React.FC = () => (
    <ErrorBoundary>
        <ChatContainerInternal />
    </ErrorBoundary>
)