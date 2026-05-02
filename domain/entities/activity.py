"""
domain/entities/activity.py — Activity entity + types.
"""

# --- IMPORTS ---
from __future__ import annotations

import json
from dataclasses import dataclass, field
from enum import Enum
from typing import Optional


# --- DOMAIN ---
class ActivityType(Enum):
    DAILY = "A"
    DEADLINE = "B"
    BACKLOG = "C"
    TODAY_FOCUS = "D"


@dataclass(frozen=True)
class FrequencyConfig:
    days_of_week: list[int] = field(default_factory=list)
    times_per_week: int = 7
    preferred_hour: Optional[int] = None

    def to_json(self) -> str:
        return json.dumps({
            "days_of_week": self.days_of_week,
            "times_per_week": self.times_per_week,
            "preferred_hour": self.preferred_hour,
        })

    @staticmethod
    def from_json(raw: Optional[str]) -> Optional[FrequencyConfig]:
        if not raw:
            return None
        data = json.loads(raw)
        return FrequencyConfig(
            days_of_week=data.get("days_of_week", []),
            times_per_week=data.get("times_per_week", 7),
            preferred_hour=data.get("preferred_hour"),
        )


@dataclass(frozen=True)
class Activity:
    id: Optional[int]
    title: str
    type: ActivityType
    frequency_config: Optional[FrequencyConfig]
    deadline: Optional[str]
    implementation_intention: Optional[str]
    coping_plan: Optional[str]
    created_at: str
    is_archived: bool = False
