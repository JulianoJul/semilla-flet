"""
domain/entities/badge_entity.py — BadgeEntity.
"""

# --- IMPORTS ---
from __future__ import annotations

from dataclasses import dataclass
from typing import Optional


# --- DOMAIN ---
@dataclass(frozen=True)
class BadgeEntity:
    id: Optional[int]
    key: str
    name: str
    description: Optional[str]
    condition_type: str
    condition_value: str
    unlocked_at: Optional[str] = None
    icon_asset: Optional[str] = None
    emoji_placeholder: Optional[str] = "🏅"
