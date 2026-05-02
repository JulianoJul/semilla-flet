"""
data/datasources/gamification_datasource.py — Streaks, badges, settings.
"""

# --- IMPORTS ---
from __future__ import annotations

from typing import Optional

from core.database.db_helper import DBHelper
from data.datasources.chest_logic import check_chest_drop
from data.datasources.gamification_mappers import map_badge, map_streak
from domain.entities.badge_entity import BadgeEntity
from domain.entities.streak import Streak

from datetime import datetime, timezone


# --- DATASOURCE ---
class GamificationLocalDatasource:
    def __init__(self, db: DBHelper) -> None:
        self._db = db

    # --- STREAKS ---
    def get_streak(self, activity_id: int) -> Streak:
        conn = self._db.get_connection()
        row = conn.execute(
            "SELECT * FROM streaks WHERE activity_id = ?",
            (activity_id,),
        ).fetchone()
        if row is None:
            return Streak(id=None, activity_id=activity_id)
        return map_streak(row)

    def save_streak(self, s: Streak) -> Streak:
        conn = self._db.get_connection()
        conn.execute(
            "UPDATE streaks SET current_count=?, best_count=?, "
            "last_checkin_date=?, shields_available=?, "
            "weekly_completion_rate=?, total_completions=? "
            "WHERE activity_id=?",
            (s.current_count, s.best_count, s.last_checkin_date,
             s.shields_available, s.weekly_completion_rate,
             s.total_completions, s.activity_id),
        )
        conn.commit()
        return self.get_streak(s.activity_id)

    def use_shield(self, activity_id: int) -> bool:
        conn = self._db.get_connection()
        row = conn.execute(
            "SELECT shields_available FROM streaks WHERE activity_id=?",
            (activity_id,),
        ).fetchone()
        if row is None or row["shields_available"] <= 0:
            return False
        conn.execute(
            "UPDATE streaks SET shields_available = shields_available - 1 "
            "WHERE activity_id = ?", (activity_id,),
        )
        conn.commit()
        return True

    # --- BADGES ---
    def get_unlocked_badges(self) -> list[BadgeEntity]:
        conn = self._db.get_connection()
        rows = conn.execute(
            "SELECT * FROM badges WHERE unlocked_at IS NOT NULL",
        ).fetchall()
        return [map_badge(r) for r in rows]

    def check_and_unlock(self, activity_id: int) -> Optional[BadgeEntity]:
        streak = self.get_streak(activity_id)
        conn = self._db.get_connection()
        locked = conn.execute(
            "SELECT * FROM badges WHERE unlocked_at IS NULL",
        ).fetchall()
        now = datetime.now(timezone.utc).isoformat()
        for row in locked:
            if self._badge_met(row, streak):
                conn.execute(
                    "UPDATE badges SET unlocked_at=? WHERE id=?",
                    (now, row["id"]),
                )
                conn.commit()
                updated = conn.execute(
                    "SELECT * FROM badges WHERE id=?", (row["id"],),
                ).fetchone()
                return map_badge(updated)
        return None

    @staticmethod
    def _badge_met(row: dict, streak: Streak) -> bool:
        ctype, cval = row["condition_type"], int(row["condition_value"])
        if ctype == "total_completions":
            return streak.total_completions >= cval
        if ctype == "streak":
            return streak.current_count >= cval
        if ctype == "shield_used":
            return streak.shields_available < 1
        return False

    # --- CHEST ---
    def should_show_chest(self) -> bool:
        conn = self._db.get_connection()
        showed = check_chest_drop(conn)
        if showed:
            self.set_setting("last_chest_date", datetime.now().strftime("%Y-%m-%d"))
        return showed

    # --- SETTINGS & COPY ---
    def get_ui_copy(self, key: str) -> Optional[str]:
        conn = self._db.get_connection()
        row = conn.execute(
            "SELECT value FROM ui_copy WHERE key = ?", (key,),
        ).fetchone()
        return row["value"] if row else None

    def get_setting(self, key: str) -> Optional[str]:
        conn = self._db.get_connection()
        row = conn.execute(
            "SELECT value FROM settings WHERE key = ?", (key,),
        ).fetchone()
        return row["value"] if row else None

    def set_setting(self, key: str, value: str) -> None:
        conn = self._db.get_connection()
        conn.execute(
            "INSERT OR REPLACE INTO settings (key, value) VALUES (?, ?)",
            (key, value),
        )
        conn.commit()
