// frontend/lib/utils/sanitize.ts

/**
 * Sanitize HTML to prevent XSS attacks
 * @param html The HTML string to sanitize
 * @returns Sanitized HTML string
 */
export const sanitizeHtml = (html: string): string => {
  if (typeof window === 'undefined') {
    return html;
  }
  const div = document.createElement('div');
  div.textContent = html;
  return div.innerHTML;
};

/**
 * Normalize message by trimming whitespace
 * @param message The message to normalize
 * @returns Normalized message
 */
export const normalizeMessage = (message: string): string => {
  return message.trim();
};

/**
 * Check if a message is empty
 * @param message The message to check
 * @returns True if the message is empty
 */
export const isEmptyMessage = (message: string): boolean => {
  return normalizeMessage(message).length === 0;
};

/**
 * Check if a message exceeds the maximum length
 * @param message The message to check
 * @param maxLength The maximum allowed length
 * @returns True if the message is within the length limit
 */
export const isValidMessageLength = (message: string, maxLength: number): boolean => {
  return normalizeMessage(message).length <= maxLength;
};