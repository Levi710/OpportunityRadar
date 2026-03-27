/**
 * Format a date string into a relative time string (e.g., "2 hours ago", "just now").
 * No external library — hand-built as per spec.
 */
export function timeAgo(dateString: string): string {
  const date = new Date(dateString + 'Z'); // treat as UTC
  const now = new Date();
  const seconds = Math.floor((now.getTime() - date.getTime()) / 1000);

  if (seconds < 60) return 'just now';
  if (seconds < 3600) {
    const mins = Math.floor(seconds / 60);
    return `${mins}m ago`;
  }
  if (seconds < 86400) {
    const hours = Math.floor(seconds / 3600);
    return `${hours}h ago`;
  }
  if (seconds < 604800) {
    const days = Math.floor(seconds / 86400);
    return `${days}d ago`;
  }
  const weeks = Math.floor(seconds / 604800);
  return `${weeks}w ago`;
}

/**
 * Truncate a string to a maximum length, appending ellipsis if truncated.
 */
export function truncate(text: string, maxLength = 40): string {
  if (text.length <= maxLength) return text;
  return text.slice(0, maxLength) + '…';
}

/**
 * Extract the hostname from a URL for display purposes.
 */
export function extractDomain(url: string): string {
  try {
    return new URL(url).hostname;
  } catch {
    return url;
  }
}

/**
 * Check if a date string represents today (UTC).
 */
export function isToday(dateString: string): boolean {
  const date = new Date(dateString + 'Z');
  const today = new Date();
  return (
    date.getUTCFullYear() === today.getUTCFullYear() &&
    date.getUTCMonth() === today.getUTCMonth() &&
    date.getUTCDate() === today.getUTCDate()
  );
}

/**
 * Check if a date string is within the last 24 hours.
 */
export function isWithin24h(dateString: string): boolean {
  if (!dateString) return false;
  const date = new Date(dateString + 'Z');
  const now = new Date();
  return now.getTime() - date.getTime() < 86400000;
}
