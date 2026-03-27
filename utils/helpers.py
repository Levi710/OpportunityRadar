"""Shared utility functions for OpportunityRadar."""

from datetime import datetime


def current_timestamp():
    """Return the current UTC timestamp as a formatted string.

    Returns:
        str: Timestamp in 'YYYY-MM-DD HH:MM:SS' format.
    """
    return datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")


def truncate_text(text, max_length=200):
    """Truncate text to a maximum length with ellipsis.

    Args:
        text: The string to truncate.
        max_length: Maximum number of characters before truncation.

    Returns:
        str: Truncated string with '...' appended if it exceeded max_length.
    """
    if len(text) <= max_length:
        return text
    return text[:max_length] + "..."
