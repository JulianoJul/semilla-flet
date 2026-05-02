"""
data/datasources/activity_mappers.py — Row-to-entity mappers.
"""

# --- IMPORTS ---
from __future__ import annotations

from domain.entities.activity import Activity, ActivityType, FrequencyConfig
from domain.entities.checkin import CheckIn


# --- MAPPERS ---
def map_activity(row: dict) -> Activity:
    return Activity(
        id=row["id"], title=row["title"],
        type=ActivityType(row["type"]),
        frequency_config=FrequencyConfig.from_json(
            row["frequency_config"],
        ),
        deadline=row["deadline"],
        implementation_intention=row["implementation_intention"],
        coping_plan=row["coping_plan"],
        created_at=row["created_at"],
        is_archived=bool(row["is_archived"]),
    )


def map_checkin(row: dict) -> CheckIn:
    return CheckIn(
        id=row["id"], activity_id=row["activity_id"],
        completed_at=row["completed_at"], notes=row["notes"],
    )
