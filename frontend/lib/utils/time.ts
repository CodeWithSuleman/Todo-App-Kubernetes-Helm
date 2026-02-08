/**
 * Utility functions for timestamp formatting
 * Chat Interface & AI UX Feature
 */

/**
 * Format a date to a user-friendly time string
 * @param date The date to format
 * @returns Formatted time string (e.g., "2:30 PM", "Yesterday 3:15 PM", "Jan 5, 2026")
 */
export function formatTimestamp(date: Date): string {
  const now = new Date();
  const messageDate = new Date(date);

  const diffInMs = now.getTime() - messageDate.getTime();
  const diffInHours = diffInMs / (1000 * 60 * 60);
  const diffInDays = Math.floor(diffInHours / 24);

  // Today: show time only
  if (diffInDays === 0) {
    return messageDate.toLocaleTimeString('en-US', {
      hour: 'numeric',
      minute: '2-digit',
      hour12: true
    });
  }

  // Yesterday
  if (diffInDays === 1) {
    return `Yesterday ${messageDate.toLocaleTimeString('en-US', {
      hour: 'numeric',
      minute: '2-digit',
      hour12: true
    })}`;
  }

  // Within last week: show day name
  if (diffInDays < 7) {
    return messageDate.toLocaleDateString('en-US', {
      weekday: 'short',
      hour: 'numeric',
      minute: '2-digit',
      hour12: true
    });
  }

  // Older: show full date
  return messageDate.toLocaleDateString('en-US', {
    month: 'short',
    day: 'numeric',
    year: 'numeric'
  });
}

/**
 * Format a date to a short time string for message bubbles
 * @param date The date to format
 * @returns Short time string (e.g., "2:30 PM")
 */
export function formatMessageTime(date: Date): string {
  return new Date(date).toLocaleTimeString('en-US', {
    hour: 'numeric',
    minute: '2-digit',
    hour12: true
  });
}

/**
 * Get relative time string (e.g., "just now", "5 minutes ago")
 * @param date The date to compare
 * @returns Relative time string
 */
export function getRelativeTime(date: Date): string {
  const now = new Date();
  const messageDate = new Date(date);
  const diffInSeconds = Math.floor((now.getTime() - messageDate.getTime()) / 1000);

  if (diffInSeconds < 10) return 'just now';
  if (diffInSeconds < 60) return `${diffInSeconds} seconds ago`;

  const diffInMinutes = Math.floor(diffInSeconds / 60);
  if (diffInMinutes < 60) return `${diffInMinutes} minute${diffInMinutes > 1 ? 's' : ''} ago`;

  const diffInHours = Math.floor(diffInMinutes / 60);
  if (diffInHours < 24) return `${diffInHours} hour${diffInHours > 1 ? 's' : ''} ago`;

  const diffInDays = Math.floor(diffInHours / 24);
  return `${diffInDays} day${diffInDays > 1 ? 's' : ''} ago`;
}
