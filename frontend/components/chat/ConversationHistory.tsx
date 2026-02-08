// frontend/components/chat/ConversationHistory.tsx

import React from 'react';
import { ConversationMetadata } from '@/lib/types/chat';

interface ConversationHistoryProps {
  conversations: ConversationMetadata[];
  onSelectConversation: (conversationId: string) => void;
  onDeleteConversation: (conversationId: string) => void;
}

export const ConversationHistory: React.FC<ConversationHistoryProps> = ({
  conversations,
  onSelectConversation,
  onDeleteConversation,
}) => {
  return (
    <div className="flex flex-col h-full bg-gray-100 dark:bg-gray-800 border-r border-gray-200 dark:border-gray-700">
      <div className="p-4 border-b border-gray-200 dark:border-gray-700">
        <h2 className="text-lg font-semibold">Conversations</h2>
      </div>
      <div className="flex-1 overflow-y-auto">
        {conversations.length === 0 ? (
          <p className="p-4 text-gray-500">No conversations yet.</p>
        ) : (
          <ul>
            {conversations.map((conversation) => (
              <li
                key={conversation.id}
                className="p-4 hover:bg-gray-200 dark:hover:bg-gray-700 cursor-pointer"
                onClick={() => onSelectConversation(conversation.id)}
              >
                <div className="flex justify-between">
                  <span className="font-semibold">{conversation.title || 'Untitled Conversation'}</span>
                  <button
                    onClick={(e) => {
                      e.stopPropagation();
                      onDeleteConversation(conversation.id);
                    }}
                    className="text-red-500 hover:text-red-700"
                  >
                    Delete
                  </button>
                </div>
                <p className="text-sm text-gray-500 truncate">
                  {conversation.lastMessage || 'No messages'}
                </p>
              </li>
            ))}
          </ul>
        )}
      </div>
    </div>
  );
};