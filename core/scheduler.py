"""APScheduler setup — runs the check pipeline every N hours."""

import os
import time
from apscheduler.schedulers.blocking import BlockingScheduler
from loguru import logger

from db.models import get_all_active_sources
from core.fetcher import fetch
from core.parser import parse
from core.hasher import hash_content
from core.comparator import compare
from notifier.telegram import send_alert


def run_all_checks():
    """Execute the full fetch→parse→hash→compare→notify pipeline for every active source.

    Iterates all active sources from the database. For each source:
    1. Fetches the page HTML.
    2. Parses the target section using the CSS selector.
    3. Hashes the extracted text.
    4. Compares against the stored snapshot.
    5. Sends a Telegram alert if a change is detected.

    Sleeps 2 seconds between sources to be respectful to target servers.
    All exceptions are caught at the job level so one failure does not stop the run.
    """
    sources = get_all_active_sources()
    logger.info("Starting check run — {} active sources", len(sources))

    for source in sources:
        try:
            name = source["name"]
            url = source["url"]
            css_selector = source["css_selector"]
            is_js = bool(source["is_js_rendered"])
            source_id = source["id"]

            logger.info("Checking: {} ({})", name, url)

            # Step 1: Fetch
            html = fetch(url, is_js_rendered=is_js)
            if html is None:
                logger.warning("Skipping {} — fetch returned None", name)
                continue

            # Step 2: Parse
            content = parse(html, css_selector)
            if not content:
                logger.warning("Skipping {} — no content extracted for selector '{}'", name, css_selector)
                continue

            # Step 3: Hash
            content_hash = hash_content(content)

            # Step 4: Compare
            changed, reason = compare(source_id, content_hash, content)

            # Step 5: Notify
            if changed:
                send_alert(name, url)

            logger.info("{} — result: {}", name, reason)

        except Exception as e:
            logger.error("Error processing source '{}': {}", source.get("name", "unknown"), e)

        # Be polite — wait between requests
        time.sleep(2)

    logger.info("Check run complete")


def start_scheduler():
    """Initialize and start the blocking scheduler.

    Runs run_all_checks immediately on startup, then every N hours
    (configured via CHECK_INTERVAL_HOURS env var, default 6).
    """
    interval_hours = int(os.getenv("CHECK_INTERVAL_HOURS", "6"))

    scheduler = BlockingScheduler()
    scheduler.add_job(
        run_all_checks,
        "interval",
        hours=interval_hours,
        id="opportunity_check",
        name="OpportunityRadar periodic check",
    )

    logger.info("Scheduler started — checking every {} hours", interval_hours)
    logger.info("Running initial check now...")
    run_all_checks()

    scheduler.start()
