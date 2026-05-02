"""
domain/use_cases/get_today_intentions.py — Get today's focus activities.
"""

# --- IMPORTS ---
from __future__ import annotations

from datetime import date

from core.result import Failure, Result, Success
from domain.entities.activity import Activity
from domain.repositories.activity_repository import ActivityRepository


# --- USE CASE ---
class GetTodayIntentionsUseCase:
    def __init__(self, activity_repo: ActivityRepository) -> None:
        self._activity_repo = activity_repo

    def execute(self) -> Result[tuple[list[Activity], bool]]:
        result = self._activity_repo.get_today_intentions()
        if isinstance(result, Failure):
            return Failure(result.error)

        fresh_start = self._is_fresh_start()
        return Success((result.value, fresh_start))

    @staticmethod
    def _is_fresh_start() -> bool:
        today = date.today()
        is_monday = today.weekday() == 0
        is_first = today.day == 1
        return is_monday or is_first
