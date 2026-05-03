"""
core/database/migrations/migration_2.py — Add weekly_streak_count to streaks.

Adds the `weekly_streak_count` column used by the 'constancia' badge
to track consecutive ISO weeks where weekly_completion_rate >= 0.8.
Uses ALTER TABLE ... ADD COLUMN which is safe to run on an existing DB
because the column may already exist (guarded by a try/except).
"""

# --- IMPORTS ---
from __future__ import annotations

import logging
import sqlite3

logger = logging.getLogger(__name__)


# --- MIGRATION ---
def run_migration(conn: sqlite3.Connection) -> None:
    try:
        conn.execute(
            "ALTER TABLE streaks ADD COLUMN weekly_streak_count INTEGER DEFAULT 0"
        )
        conn.commit()
        logger.info("migration_2: added weekly_streak_count to streaks")
    except sqlite3.OperationalError as exc:
        # Column already exists — idempotent, safe to ignore.
        if "duplicate column name" in str(exc).lower():
            logger.debug("migration_2: weekly_streak_count already exists, skipping")
        else:
            raise
