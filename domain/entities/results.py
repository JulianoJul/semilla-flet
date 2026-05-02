"""
domain/entities/results.py — Composite result types.
"""

# --- IMPORTS ---
from __future__ import annotations

from dataclasses import dataclass
from typing import Optional

from domain.entities.badge_entity import BadgeEntity
from domain.entities.checkin import CheckIn
from domain.entities.streak import Streak


# --- DOMAIN ---
@dataclass(frozen=True)
class CompletionResult:
    checkin: CheckIn
    streak: Streak
    show_chest: bool
    new_badge: Optional[BadgeEntity] = None


@dataclass(frozen=True)
class StreakUpdateResult:
    streak: Streak
    shield_used: bool = False
    streak_reset: bool = False
