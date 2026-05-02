"""
data/datasources/gamification_mappers.py — Row-to-entity mappers.
"""

# --- IMPORTS ---
from __future__ import annotations

from domain.entities.badge_entity import BadgeEntity
from domain.entities.streak import Streak


# --- MAPPERS ---
def map_streak(row: dict) -> Streak:
    return Streak(
        id=row["id"], activity_id=row["activity_id"],
        current_count=row["current_count"],
        best_count=row["best_count"],
        last_checkin_date=row["last_checkin_date"],
        shields_available=row["shields_available"],
        weekly_completion_rate=row["weekly_completion_rate"],
        total_completions=row["total_completions"],
    )


def map_badge(row: dict) -> BadgeEntity:
    return BadgeEntity(
        id=row["id"], key=row["key"], name=row["name"],
        description=row["description"],
        condition_type=row["condition_type"],
        condition_value=row["condition_value"],
        unlocked_at=row["unlocked_at"],
        icon_asset=row["icon_asset"],
        emoji_placeholder=row["emoji_placeholder"],
    )
