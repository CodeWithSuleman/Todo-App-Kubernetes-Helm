// frontend/lib/constants/chat.ts

export const MAX_MESSAGE_LENGTH = 1000;
export const MESSAGE_INPUT_PLACEHOLDER = 'Type your message...';

export const ERROR_MESSAGES = {
  INVALID_MESSAGE: 'Message cannot be empty.',
  MESSAGE_TOO_LONG: `Message cannot exceed ${MAX_MESSAGE_LENGTH} characters.`,
  AUTH_ERROR: 'Authentication error. Please log in again.',
  NETWORK_ERROR: 'Network error. Please check your connection.',
  GENERIC_ERROR: 'An unexpected error occurred.',
};

export const CHAT_API_ENDPOINT = '/api/v1';
export const AUTO_SCROLL_THRESHOLD = 100;