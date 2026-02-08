'use client';

import React, { useState, useRef, KeyboardEvent } from 'react';
import { MAX_MESSAGE_LENGTH, MESSAGE_INPUT_PLACEHOLDER, ERROR_MESSAGES } from '@/lib/constants/chat';
import { isEmptyMessage, isValidMessageLength, normalizeMessage } from '@/lib/utils/sanitize';

interface MessageInputProps {
  onSendMessage: (message: string) => void;
  disabled?: boolean;
  placeholder?: string;
}

export const MessageInput: React.FC<MessageInputProps> = ({
  onSendMessage,
  disabled = false,
  placeholder = MESSAGE_INPUT_PLACEHOLDER,
}) => {
  const [message, setMessage] = useState('');
  const [error, setError] = useState<string | null>(null);
  const textareaRef = useRef<HTMLTextAreaElement>(null);

  const handleSubmit = () => {
    const normalizedMessage = normalizeMessage(message);

    if (isEmptyMessage(normalizedMessage)) {
      setError(ERROR_MESSAGES.INVALID_MESSAGE);
      return;
    }

    if (!isValidMessageLength(normalizedMessage, MAX_MESSAGE_LENGTH)) {
      setError(ERROR_MESSAGES.MESSAGE_TOO_LONG);
      return;
    }

    setError(null);
    onSendMessage(normalizedMessage);
    setMessage('');

    // Reset textarea height
    if (textareaRef.current) {
      textareaRef.current.style.height = 'auto';
    }
  };

  const handleKeyDown = (e: KeyboardEvent<HTMLTextAreaElement>) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSubmit();
    }
  };

  const handleChange = (e: React.ChangeEvent<HTMLTextAreaElement>) => {
    const value = e.target.value;
    setMessage(value);
    setError(null);

    // Auto-resize textarea
    if (textareaRef.current) {
      textareaRef.current.style.height = 'auto';
      textareaRef.current.style.height = `${textareaRef.current.scrollHeight}px`;
    }
  };

  return (
    <div className="border-t border-gray-200 bg-white p-4">
      {error && (
        <div className="mb-2 text-sm text-red-600">
          {error}
        </div>
      )}
      <div className="flex items-end gap-2">
        <textarea
          ref={textareaRef}
          value={message}
          onChange={handleChange}
          onKeyDown={handleKeyDown}
          placeholder={placeholder}
          disabled={disabled}
          rows={1}
          className="flex-1 resize-none rounded-lg border border-gray-300 px-4 py-2 focus:border-blue-500 focus:outline-none focus:ring-2 focus:ring-blue-500 disabled:bg-gray-100 disabled:cursor-not-allowed"
          style={{ maxHeight: '200px', minHeight: '44px' }}
        />
        <button
          onClick={handleSubmit}
          disabled={disabled || isEmptyMessage(message)}
          className="rounded-lg bg-blue-600 px-6 py-2 text-white hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-blue-500 disabled:bg-gray-300 disabled:cursor-not-allowed transition-colors"
          style={{ height: '44px' }}
        >
          Send
        </button>
      </div>
      <div className="mt-1 text-xs text-gray-500 text-right">
        {message.length}/{MAX_MESSAGE_LENGTH}
      </div>
    </div>
  );
};
