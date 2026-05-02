"""
domain/repositories/gamification_repository.py — Abstract gamification repository.
"""

# --- IMPORTS ---
from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Optional

from core.result import Result
from domain.entities.badge_entity import BadgeEntity
from domain.entities.streak import Streak


# --- ABSTRACT ---
class GamificationRepository(ABC):

    @abstractmethod
    def get_streak(self, activity_id: int) -> Result[Streak]: ...

    @abstractmethod
    def update_streak(self, streak: Streak) -> Result[Streak]: ...

    @abstractmethod
    def use_shield(self, activity_id: int) -> Result[bool]: ...

    @abstractmethod
    def get_unlocked_badges(self) -> Result[list[BadgeEntity]]: ...

    @abstractmethod
    def check_and_unlock_badges(
        self, activity_id: int,
    ) -> Result[Optional[BadgeEntity]]: ...

    @abstractmethod
    def should_show_chest(self) -> Result[bool]: ...

    @abstractmethod
    def get_ui_copy(self, key: str) -> Result[str]: ...

    @abstractmethod
    def get_setting(self, key: str) -> Result[str]: ...

    @abstractmethod
    def set_setting(self, key: str, value: str) -> Result[None]: ...
