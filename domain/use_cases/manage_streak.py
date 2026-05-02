"""
domain/use_cases/manage_streak.py — Full streak logic.
"""

# --- IMPORTS ---
from __future__ import annotations

from datetime import date, datetime, timedelta, timezone

from core.result import Failure, Result, Success
from domain.entities.results import StreakUpdateResult
from domain.entities.streak import Streak
from domain.repositories.gamification_repository import GamificationRepository


# --- USE CASE ---
class ManageStreakUseCase:
    def __init__(self, gamification_repo: GamificationRepository) -> None:
        self._repo = gamification_repo

    def execute(self, activity_id: int) -> Result[StreakUpdateResult]:
        streak_res = self._repo.get_streak(activity_id)
        if isinstance(streak_res, Failure):
            return Failure(streak_res.error)

        streak = streak_res.value
        today = date.today()
        shield_used = False
        streak_reset = False

        last = self._parse_date(streak.last_checkin_date)
        gap = (today - last).days if last else None

        # --- CALCULATE NEW COUNT ---
        if gap is None or gap == 0:
            new_count = max(streak.current_count, 1)
        elif gap == 1:
            new_count = streak.current_count + 1
        elif gap == 2 and self._within_grace(today):
            new_count = streak.current_count + 1
        elif streak.shields_available > 0:
            shield_res = self._repo.use_shield(activity_id)
            shield_used = isinstance(shield_res, Success) and shield_res.value
            new_count = streak.current_count + 1 if shield_used else 1
            streak_reset = not shield_used
        else:
            new_count = 1
            streak_reset = True

        # --- WEEKLY RATE ---
        week_rate = self._calc_weekly_rate(streak, today)
        new_best = max(streak.best_count, new_count)
        total = streak.total_completions + 1

        updated = Streak(
            id=streak.id, activity_id=activity_id,
            current_count=new_count, best_count=new_best,
            last_checkin_date=today.isoformat(),
            shields_available=streak.shields_available - (1 if shield_used else 0),
            weekly_completion_rate=week_rate,
            total_completions=total,
        )

        save_res = self._repo.update_streak(updated)
        if isinstance(save_res, Failure):
            return Failure(save_res.error)

        return Success(StreakUpdateResult(
            streak=save_res.value,
            shield_used=shield_used,
            streak_reset=streak_reset,
        ))

    def _within_grace(self, today: date) -> bool:
        grace_res = self._repo.get_setting("grace_period_hours")
        if isinstance(grace_res, Failure):
            return False
        grace_hours = int(grace_res.value)
        now = datetime.now(timezone.utc)
        return now.hour < grace_hours

    @staticmethod
    def _parse_date(date_str: str | None) -> date | None:
        if not date_str:
            return None
        try:
            return date.fromisoformat(date_str)
        except ValueError:
            return None

    @staticmethod
    def _calc_weekly_rate(streak: Streak, today: date) -> float:
        week_start = today - timedelta(days=today.weekday())
        days_in_week = min((today - week_start).days + 1, 7)
        if days_in_week == 0:
            return 0.0
        completed = min(streak.current_count, days_in_week)
        return round(completed / days_in_week, 2)
