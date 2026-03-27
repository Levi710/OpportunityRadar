"""Fetches raw HTML from a URL using requests or Playwright depending on source config."""

import requests
from loguru import logger

# Realistic User-Agent to avoid bot-detection blocks
_USER_AGENT = (
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
    "AppleWebKit/537.36 (KHTML, like Gecko) "
    "Chrome/125.0.0.0 Safari/537.36"
)


def fetch(url, is_js_rendered=False):
    """Fetch and return the raw HTML content of a URL.

    Uses requests for static pages and Playwright for JS-rendered pages.
    Falls back to requests if Playwright fails to launch.

    Args:
        url: The page URL to fetch.
        is_js_rendered: If True, use Playwright headless browser.

    Returns:
        str or None: Raw HTML string, or None on failure.
    """
    if is_js_rendered:
        return _fetch_with_playwright(url)
    return _fetch_with_requests(url)


def _fetch_with_requests(url):
    """Fetch a static page using the requests library.

    Args:
        url: The URL to fetch.

    Returns:
        str or None: HTML content or None on failure.
    """
    try:
        response = requests.get(url, headers={"User-Agent": _USER_AGENT}, timeout=30)
        response.raise_for_status()
        logger.info("Fetched (requests) {} — status {}", url, response.status_code)
        return response.text
    except requests.RequestException as e:
        logger.error("Failed to fetch {} with requests: {}", url, e)
        return None


def _fetch_with_playwright(url):
    """Fetch a JS-rendered page using Playwright's sync API.

    Falls back to requests if Playwright cannot launch.

    Args:
        url: The URL to fetch.

    Returns:
        str or None: Rendered HTML content or None on failure.
    """
    try:
        from playwright.sync_api import sync_playwright

        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            page = browser.new_page()
            page.goto(url, wait_until="networkidle", timeout=60000)
            html = page.content()
            browser.close()
            logger.info("Fetched (playwright) {} — success", url)
            return html
    except ImportError:
        logger.warning("Playwright not installed. Falling back to requests for {}", url)
        return _fetch_with_requests(url)
    except Exception as e:
        logger.error("Playwright failed for {}: {}. Falling back to requests.", url, e)
        return _fetch_with_requests(url)
