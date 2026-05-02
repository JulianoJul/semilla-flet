"""
domain/entities/today_intention.py — TodayIntention entity.
"""

# --- IMPORTS ---
from __future__ import annotations

from dataclasses import dataclass
from typing import Optional


# --- DOMAIN ---
@dataclass(frozen=True)
class TodayIntention:
    id: Optional[int]
    date: str
    activity_id: int
    order_index: int
