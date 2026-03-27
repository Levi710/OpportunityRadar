"""Extracts the target section from raw HTML using a CSS selector."""

from bs4 import BeautifulSoup
from loguru import logger


def parse(html, css_selector):
    """Extract text from a specific HTML section identified by a CSS selector.

    Uses BeautifulSoup to find the first element matching the selector
    and returns its stripped text content.

    Args:
        html: Raw HTML string.
        css_selector: CSS selector string targeting the desired section.

    Returns:
        str: Extracted text, or empty string if the selector finds nothing.
    """
    try:
        soup = BeautifulSoup(html, "html.parser")
        element = soup.select_one(css_selector)

        if element is None:
            logger.warning("No content found for selector '{}'", css_selector)
            return ""

        text = element.get_text(separator=" ", strip=True)
        logger.debug("Parsed {} chars from selector '{}'", len(text), css_selector)
        return text
    except Exception as e:
        logger.error("Parser error with selector '{}': {}", css_selector, e)
        return ""
