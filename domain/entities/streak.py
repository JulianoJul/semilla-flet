"""
domain/entities/streak.py — Streak entity.
"""

# --- IMPORTS ---
from __future__ import annotations

from dataclasses import dataclass
from typing import Optional


# --- DOMAIN ---
@dataclass(frozen=True)
class Streak:
    id: Optional[int]
    activity_id: int
    current_count: int = 0
    best_count: int = 0
    last_checkin_date: Optional[str] = None
    shields_available: int = 1
    weekly_completion_rate: float = 0.0
    total_completions: int = 0
    weekly_streak_count: int = 0
