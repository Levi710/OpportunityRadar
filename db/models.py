"""Query functions for the sources and snapshots tables."""

import json
from db.database import get_connection
from loguru import logger


def get_all_active_sources():
    """Fetch all sources where active is true.

    Returns:
        list[sqlite3.Row]: List of active source rows.
    """
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM sources WHERE active = 1")
    rows = cursor.fetchall()
    conn.close()
    return rows


def get_source_count():
    """Return the total number of rows in the sources table.

    Returns:
        int: Number of sources.
    """
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM sources")
    count = cursor.fetchone()[0]
    conn.close()
    return count


def insert_source(name, url, css_selector, is_js_rendered, category="general", tags=None):
    """Insert or update a source in the sources table.

    Updates name, css_selector, category, and tags if the URL already exists.

    Args:
        name: Human-readable name for the source.
        url: The URL to monitor.
        css_selector: CSS selector for the target section.
        is_js_rendered: Whether Playwright is needed (bool).
        category: The category of the source.
        tags: List of branch tags (e.g. ["cs", "it"]).
    """
    if tags is None:
        tags = ["all"]
    tags_json = json.dumps(tags)

    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute(
            """INSERT INTO sources 
               (name, url, css_selector, is_js_rendered, category, tags) 
               VALUES (?, ?, ?, ?, ?, ?)
               ON CONFLICT(url) DO UPDATE SET
               name=excluded.name,
               css_selector=excluded.css_selector,
               is_js_rendered=excluded.is_js_rendered,
               category=excluded.category,
               tags=excluded.tags""",
            (name, url, css_selector, int(is_js_rendered), category, tags_json),
        )
        conn.commit()
    except Exception as e:
        logger.error("Failed to insert/update source '{}': {}", name, e)
    finally:
        conn.close()


def get_sources_by_category(category: str) -> list:
    """Return all active sources for a given category."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM sources WHERE category = ? AND active = 1", (category,))
    rows = cursor.fetchall()
    conn.close()
    return rows


def get_sources_for_branch(branch: str) -> list:
    """Return sources where tags contains branch or 'all'."""
    conn = get_connection()
    cursor = conn.cursor()
    # We select all and filter in Python because SQLite JSON support varies
    cursor.execute("SELECT * FROM sources WHERE active = 1")
    rows = cursor.fetchall()
    conn.close()

    filtered = []
    for row in rows:
        try:
            tags = json.loads(row["tags"])
            if branch in tags or "all" in tags:
                filtered.append(row)
        except Exception:
            continue
    return filtered


def upsert_student_profile(email, name, branch, year, college) -> int:
    """Insert or update a student profile. Return id."""
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute(
            """INSERT INTO student_profiles (email, name, branch, year, college) 
               VALUES (?, ?, ?, ?, ?)
               ON CONFLICT(email) DO UPDATE SET
               name=excluded.name, branch=excluded.branch, year=excluded.year, college=excluded.college""",
            (email, name, branch, year, college),
        )
        conn.commit()
        return cursor.lastrowid
    except Exception as e:
        logger.error("Failed to upsert profile for {}: {}", email, e)
        return -1
    finally:
        conn.close()


def get_latest_snapshot(source_id):
    """Fetch the most recent snapshot for a given source.

    Args:
        source_id: The ID of the source.

    Returns:
        sqlite3.Row or None: The latest snapshot row, or None if no snapshot exists.
    """
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "SELECT * FROM snapshots WHERE source_id = ? ORDER BY checked_at DESC LIMIT 1",
        (source_id,),
    )
    row = cursor.fetchone()
    conn.close()
    return row


def insert_snapshot(source_id, content_hash, raw_content, changed):
    """Insert a new snapshot record.

    Args:
        source_id: The ID of the source.
        content_hash: SHA256 hash of the extracted content.
        raw_content: The raw text that was hashed.
        changed: Whether this snapshot represents a change from the previous one.
    """
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO snapshots (source_id, content_hash, raw_content, changed) VALUES (?, ?, ?, ?)",
        (source_id, content_hash, raw_content, int(changed)),
    )
    conn.commit()
    conn.close()


def update_snapshot_checked_at(snapshot_id):
    """Update the checked_at timestamp to now for an existing snapshot.

    Args:
        snapshot_id: The ID of the snapshot to update.
    """
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "UPDATE snapshots SET checked_at = CURRENT_TIMESTAMP WHERE id = ?",
        (snapshot_id,),
    )
    conn.commit()
    conn.close()
