"""Generates a SHA256 hash of extracted content for change detection."""

import hashlib


def hash_content(content):
    """Return the SHA256 hex digest of a content string.

    Args:
        content: The text string to hash.

    Returns:
        str: 64-character hexadecimal hash string.
    """
    return hashlib.sha256(content.encode("utf-8")).hexdigest()
