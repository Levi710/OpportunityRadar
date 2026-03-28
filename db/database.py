"""SQLite database connection and table initialization for OpportunityRadar."""

import sqlite3
import os
from pathlib import Path
from loguru import logger

DB_PATH = Path(os.getenv("DATABASE_PATH", str(Path(__file__).resolve().parent.parent / "opportunityradar.db")))


def get_connection():
    """Create and return a SQLite connection with row factory enabled.

    Returns:
        sqlite3.Connection: A connection to the local SQLite database.
    """
    conn = sqlite3.connect(str(DB_PATH))
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    """Create the sources, snapshots, and student_profiles tables if they do not already exist.

    This is safe to call multiple times — it uses IF NOT EXISTS and checks column existence.
    """
    # Ensure parent directory exists (critical if a custom DATABASE_PATH is used in a volume)
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    
    logger.info("Initializing database at {}", DB_PATH)
    conn = get_connection()
    cursor = conn.cursor()

    # --- 1. Create Tables (Base Schema) ---
    
    # Sources table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS sources (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            url TEXT NOT NULL UNIQUE,
            css_selector TEXT NOT NULL,
            is_js_rendered BOOLEAN DEFAULT 0,
            active BOOLEAN DEFAULT 1,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
    """)

    # Snapshots table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS snapshots (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            source_id INTEGER NOT NULL,
            content_hash TEXT NOT NULL,
            raw_content TEXT,
            checked_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            changed BOOLEAN DEFAULT 0,
            FOREIGN KEY (source_id) REFERENCES sources(id)
        );
    """)

    # Student Profiles table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS student_profiles (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            email TEXT UNIQUE NOT NULL,
            name TEXT,
            branch TEXT NOT NULL,
            year INTEGER NOT NULL,
            college TEXT,
            update_count INTEGER DEFAULT 0,
            verified BOOLEAN DEFAULT 0,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
    """)

    # --- 2. Migrations (Updates to Existing Tables) ---

    # Sources: Add category and tags
    cursor = conn.execute("PRAGMA table_info(sources)")
    columns = [row[1] for row in cursor.fetchall()]
    if "category" not in columns:
        conn.execute("ALTER TABLE sources ADD COLUMN category TEXT DEFAULT 'general'")
        logger.info("Added category column to sources table")
    if "tags" not in columns:
        conn.execute("ALTER TABLE sources ADD COLUMN tags TEXT DEFAULT '[\"all\"]'")
        logger.info("Added tags column to sources table")

    # Student Profiles: Add update_count (for users who already had the table from V2)
    cursor = conn.execute("PRAGMA table_info(student_profiles)")
    columns = [row[1] for row in cursor.fetchall()]
    if "update_count" not in columns:
        conn.execute("ALTER TABLE student_profiles ADD COLUMN update_count INTEGER DEFAULT 0")
        logger.info("Added update_count column to student_profiles table")

    conn.commit()
    conn.close()
    logger.info("Database initialized at {}", DB_PATH)
