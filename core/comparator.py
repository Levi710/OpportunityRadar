"""Compares a new content hash against the most recent stored snapshot."""

from db.models import get_latest_snapshot, insert_snapshot, update_snapshot_checked_at
from loguru import logger


def compare(source_id, new_hash, raw_content):
    """Compare a new hash with the latest stored snapshot for a source.

    Three outcomes:
    - First run: no previous snapshot exists, stores the new one.
    - No change: hash matches, updates the checked_at timestamp.
    - Changed: hash differs, stores a new snapshot marked as changed.

    Args:
        source_id: The database ID of the source.
        new_hash: SHA256 hash of the newly fetched content.
        raw_content: The raw text that was hashed (stored for reference).

    Returns:
        tuple: (changed: bool, reason: str) where reason is one of
               'first_run', 'no_change', or 'changed'.
    """
    latest = get_latest_snapshot(source_id)

    if latest is None:
        # First time checking this source — flag as "changed" in DB so UI populates immediately!
        insert_snapshot(source_id, new_hash, raw_content, changed=True)
        logger.info("Source {} — first run, baseline snapshot stored (visible in UI)", source_id)
        # Return False so we don't spam 25+ Telegram alerts on the very first boot
        return (False, "first_run")

    if latest["content_hash"] == new_hash:
        # Content unchanged — just update the timestamp
        update_snapshot_checked_at(latest["id"])
        logger.info("Source {} — no change detected", source_id)
        return (False, "no_change")

    # Content changed — store new snapshot
    insert_snapshot(source_id, new_hash, raw_content, changed=True)
    logger.info("Source {} — CHANGE DETECTED", source_id)
    return (True, "changed")
