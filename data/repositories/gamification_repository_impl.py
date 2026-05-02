"""
data/repositories/gamification_repository_impl.py — Concrete GamificationRepository.
"""

# --- IMPORTS ---
from __future__ import annotations

from typing import Optional

from core.result import Failure, Result, Success
from data.datasources.gamification_datasource import (
    GamificationLocalDatasource,
)
from domain.entities.badge_entity import BadgeEntity
from domain.entities.streak import Streak
from domain.repositories.gamification_repository import (
    GamificationRepository,
)


# --- IMPLEMENTATION ---
class GamificationRepositoryImpl(GamificationRepository):
    def __init__(self, ds: GamificationLocalDatasource) -> None:
        self._ds = ds

    def get_streak(self, activity_id: int) -> Result[Streak]:
        try:
            return Success(self._ds.get_streak(activity_id))
        except Exception as e:
            return Failure(f"Error al obtener racha: {e}")

    def update_streak(self, streak: Streak) -> Result[Streak]:
        try:
            return Success(self._ds.save_streak(streak))
        except Exception as e:
            return Failure(f"Error al actualizar racha: {e}")

    def use_shield(self, activity_id: int) -> Result[bool]:
        try:
            return Success(self._ds.use_shield(activity_id))
        except Exception as e:
            return Failure(f"Error al usar escudo: {e}")

    def get_unlocked_badges(self) -> Result[list[BadgeEntity]]:
        try:
            return Success(self._ds.get_unlocked_badges())
        except Exception as e:
            return Failure(f"Error al obtener insignias: {e}")

    def check_and_unlock_badges(
        self, activity_id: int,
    ) -> Result[Optional[BadgeEntity]]:
        try:
            return Success(self._ds.check_and_unlock(activity_id))
        except Exception as e:
            return Failure(f"Error al verificar insignias: {e}")

    def should_show_chest(self) -> Result[bool]:
        try:
            return Success(self._ds.should_show_chest())
        except Exception as e:
            return Failure(f"Error al verificar cofre: {e}")

    def get_ui_copy(self, key: str) -> Result[str]:
        try:
            val = self._ds.get_ui_copy(key)
            if val is None:
                return Failure(f"UI copy no encontrado: {key}")
            return Success(val)
        except Exception as e:
            return Failure(f"Error al leer ui_copy: {e}")

    def get_setting(self, key: str) -> Result[str]:
        try:
            val = self._ds.get_setting(key)
            if val is None:
                return Failure(f"Setting no encontrado: {key}")
            return Success(val)
        except Exception as e:
            return Failure(f"Error al leer setting: {e}")

    def set_setting(self, key: str, value: str) -> Result[None]:
        try:
            self._ds.set_setting(key, value)
            return Success(None)
        except Exception as e:
            return Failure(f"Error al guardar setting: {e}")
