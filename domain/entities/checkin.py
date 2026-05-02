"""
domain/entities/checkin.py — CheckIn entity.
"""

# --- IMPORTS ---
from __future__ import annotations

from dataclasses import dataclass
from typing import Optional


# --- DOMAIN ---
@dataclass(frozen=True)
class CheckIn:
    id: Optional[int]
    activity_id: int
    completed_at: str
    notes: Optional[str] = None
