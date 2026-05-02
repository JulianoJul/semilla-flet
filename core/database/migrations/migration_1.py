"""
core/database/migrations/migration_1.py — Schema + indices.
"""

# --- IMPORTS ---
from __future__ import annotations

import sqlite3


# --- SCHEMA ---
_TABLES = [
    """CREATE TABLE IF NOT EXISTS activities (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT NOT NULL, type TEXT NOT NULL,
        frequency_config TEXT, deadline TEXT,
        implementation_intention TEXT, coping_plan TEXT,
        created_at TEXT NOT NULL, is_archived INTEGER DEFAULT 0
    )""",
    """CREATE TABLE IF NOT EXISTS checkins (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        activity_id INTEGER NOT NULL REFERENCES activities(id),
        completed_at TEXT NOT NULL, notes TEXT
    )""",
    """CREATE TABLE IF NOT EXISTS today_intentions (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        date TEXT NOT NULL,
        activity_id INTEGER NOT NULL REFERENCES activities(id),
        order_index INTEGER NOT NULL
    )""",
    """CREATE TABLE IF NOT EXISTS streaks (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        activity_id INTEGER UNIQUE NOT NULL REFERENCES activities(id),
        current_count INTEGER DEFAULT 0, best_count INTEGER DEFAULT 0,
        last_checkin_date TEXT, shields_available INTEGER DEFAULT 1,
        weekly_completion_rate REAL DEFAULT 0.0,
        total_completions INTEGER DEFAULT 0
    )""",
    """CREATE TABLE IF NOT EXISTS badges (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        key TEXT UNIQUE NOT NULL, name TEXT NOT NULL,
        description TEXT, condition_type TEXT NOT NULL,
        condition_value TEXT NOT NULL, unlocked_at TEXT,
        icon_asset TEXT, emoji_placeholder TEXT
    )""",
    """CREATE TABLE IF NOT EXISTS ui_copy (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        key TEXT UNIQUE NOT NULL, value TEXT NOT NULL, context TEXT
    )""",
    """CREATE TABLE IF NOT EXISTS notification_copy (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        key TEXT UNIQUE NOT NULL, value TEXT NOT NULL,
        moment TEXT, activity_type TEXT
    )""",
    "CREATE TABLE IF NOT EXISTS settings (key TEXT PRIMARY KEY, value TEXT NOT NULL)",
    "CREATE TABLE IF NOT EXISTS gamification_params (key TEXT PRIMARY KEY, value TEXT NOT NULL)",
    "CREATE TABLE IF NOT EXISTS design_tokens (key TEXT PRIMARY KEY, value TEXT NOT NULL)",
]

_INDICES = [
    "CREATE INDEX IF NOT EXISTS idx_checkins_activity ON checkins(activity_id)",
    "CREATE INDEX IF NOT EXISTS idx_checkins_date ON checkins(completed_at)",
    "CREATE INDEX IF NOT EXISTS idx_today_date ON today_intentions(date)",
    "CREATE INDEX IF NOT EXISTS idx_today_activity ON today_intentions(activity_id)",
    "CREATE INDEX IF NOT EXISTS idx_streaks_activity ON streaks(activity_id)",
    "CREATE INDEX IF NOT EXISTS idx_activities_type ON activities(type)",
    "CREATE INDEX IF NOT EXISTS idx_activities_archived ON activities(is_archived)",
    "CREATE INDEX IF NOT EXISTS idx_badges_key ON badges(key)",
]


# --- ENTRY POINT ---
def run_migration(conn: sqlite3.Connection) -> None:
    for ddl in _TABLES:
        conn.execute(ddl)
    for idx in _INDICES:
        conn.execute(idx)
    from core.database.migrations.seed_data import seed_all
    seed_all(conn)
