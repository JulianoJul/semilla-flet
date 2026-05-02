"""
data/datasources/chest_logic.py — Chest drop probability with pity timer.
"""

# --- IMPORTS ---
from __future__ import annotations

import random
import sqlite3
from datetime import date


# --- LOGIC ---
def check_chest_drop(conn: sqlite3.Connection) -> bool:
    rate = _read(conn, "gamification_params", "chest_drop_rate", "0.4")
    pity = _read(conn, "gamification_params", "pity_timer_days", "3")
    last = _read(conn, "settings", "last_chest_date", "")

    days_since = _days_since(last, int(pity))
    prob = 1.0 if days_since >= int(pity) else float(rate)
    return random.random() < prob


# --- HELPERS ---
def _read(conn: sqlite3.Connection, table: str, key: str, default: str) -> str:
    row = conn.execute(
        f"SELECT value FROM {table} WHERE key = ?", (key,),
    ).fetchone()
    return row["value"] if row else default


def _days_since(last_str: str, default: int) -> int:
    if not last_str:
        return default
    try:
        return (date.today() - date.fromisoformat(last_str)).days
    except ValueError:
        return default
