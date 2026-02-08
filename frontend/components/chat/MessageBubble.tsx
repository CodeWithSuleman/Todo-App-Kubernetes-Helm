'use client';

import React from 'react';
import { ChatMessage } from '@/lib/types/chat';
import { formatMessageTime } from '@/lib/utils/time';
import { sanitizeHtml } from '@/lib/utils/sanitize';

interface MessageBubbleProps {
  message: ChatMessage;
}

export const MessageBubble: React.FC<MessageBubbleProps> = ({ message }) => {
  const isUser = message.sender === 'user';
  const isError = message.status === 'error';
  const isSending = message.status === 'sending';

  return (
    <div
      className={`flex ${isUser ? 'justify-end' : 'justify-start'} mb-4`}
    >
      <div
        className={`max-w-[80%] md:max-w-[70%] rounded-lg px-4 py-2 ${
          isUser
            ? 'bg-blue-600 text-white'
            : isError
            ? 'bg-red-100 text-red-800'
            : 'bg-gray-200 text-gray-900'
        } ${isSending ? 'opacity-60' : ''}`}
      >
        <div className="whitespace-pre-wrap wrap-break-word" dangerouslySetInnerHTML={{ __html: sanitizeHtml(message.content) }}>
        </div>
        <div
          className={`mt-1 text-xs ${
            isUser ? 'text-blue-100' : 'text-gray-500'
          }`}
        >
          {formatMessageTime(message.timestamp)}
          {isSending && ' • Sending...'}
          {isError && ' • Failed to send'}
        </div>
      </div>
    </div>
  );
};
