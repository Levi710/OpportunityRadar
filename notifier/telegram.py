"""Sends Telegram alerts via Apprise when a change is detected."""

import os
import apprise
from loguru import logger
from utils.helpers import current_timestamp


def send_alert(name, url):
    """Send a Telegram notification about a detected change.

    Reads TELEGRAM_TOKEN and TELEGRAM_CHAT_ID from environment variables.
    Logs a warning and returns silently if credentials are missing or send fails.

    Args:
        name: Human-readable name of the source that changed.
        url: The URL of the changed source.
    """
    token = os.getenv("TELEGRAM_TOKEN")
    chat_id = os.getenv("TELEGRAM_CHAT_ID")

    if not token or not chat_id or token == "your_bot_token_here":
        logger.warning("Telegram credentials not configured — skipping notification")
        return

    message = (
        "🔔 New update detected\n\n"
        f"Source: {name}\n"
        f"URL: {url}\n"
        f"Detected at: {current_timestamp()}\n\n"
        "Check it out before it closes."
    )

    try:
        apobj = apprise.Apprise()
        apobj.add(f"tgram://{token}/{chat_id}")
        success = apobj.notify(title="OpportunityRadar Alert", body=message)

        if success:
            logger.info("Telegram alert sent for '{}'", name)
        else:
            logger.error("Telegram alert failed for '{}' — apprise returned False", name)
    except Exception as e:
        logger.error("Telegram notification error for '{}': {}", name, e)
