# domain/entities/today_intention.py

from __future__ import annotations

from dataclasses import dataclass
from typing import Optional

@dataclass(frozen=True)
class TodayIntention:
    id: Optional[int]
    date: str
    activity_id: int
    order_index: int
