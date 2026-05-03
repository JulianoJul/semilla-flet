"""
domain/use_cases/manage_streak.py — Full streak logic.
"""

# --- IMPORTS ---
from __future__ import annotations

from datetime import date, datetime, timedelta, timezone

from core.result import Failure, Result, Success
from domain.entities.results import StreakUpdateResult
from domain.entities.streak import Streak
from domain.repositories.activity_repository import ActivityRepository
from domain.repositories.gamification_repository import GamificationRepository


# --- USE CASE ---
class ManageStreakUseCase:
    def __init__(
        self,
        gamification_repo: GamificationRepository,
        activity_repo: ActivityRepository,
    ) -> None:
        self._repo = gamification_repo
        self._activity_repo = activity_repo

    def execute(self, activity_id: int) -> Result[StreakUpdateResult]:
        streak_res = self._repo.get_streak(activity_id)
        if isinstance(streak_res, Failure):
            return Failure(streak_res.error)

        streak = streak_res.value
        today = date.today()
        shield_used = False
        streak_reset = False

        # --- WEEKLY SHIELD REGENERATION ---
        # If we are in a new week compared to the last check-in, restore shields.
        self._maybe_refresh_shields(streak, today, activity_id)
        # Re-fetch streak to get updated shields_available after potential refresh.
        streak_res2 = self._repo.get_streak(activity_id)
        if isinstance(streak_res2, Success):
            streak = streak_res2.value

        last = self._parse_date(streak.last_checkin_date)
        gap = (today - last).days if last else None

        # --- CALCULATE NEW COUNT ---
        if gap is None or gap == 0:
            new_count = max(streak.current_count, 1)
        elif gap == 1:
            new_count = streak.current_count + 1
        elif gap == 2 and self._within_grace(today):
            # Grace period: first hours of day allow registering yesterday's
            # check-in (gap==2 means today minus last recorded day = 2).
            new_count = streak.current_count + 1
        elif streak.shields_available > 0:
            shield_res = self._repo.use_shield(activity_id)
            shield_used = isinstance(shield_res, Success) and shield_res.value
            new_count = streak.current_count + 1 if shield_used else 1
            streak_reset = not shield_used
        else:
            new_count = 1
            streak_reset = True

        # --- WEEKLY STREAK COUNT ---
        new_weekly_streak_count = streak.weekly_streak_count
        if last is not None:
            last_week_start = last - timedelta(days=last.weekday())
            this_week_start = today - timedelta(days=today.weekday())
            weeks_diff = (this_week_start - last_week_start).days // 7
            if weeks_diff == 1:
                # Consecutive week
                if streak.weekly_completion_rate >= 0.8:
                    new_weekly_streak_count += 1
                else:
                    new_weekly_streak_count = 0
            elif weeks_diff > 1:
                # Missed full week(s)
                new_weekly_streak_count = 0

        # --- WEEKLY RATE (real query) ---
        week_rate = self._calc_weekly_rate(activity_id, today)
        new_best = max(streak.best_count, new_count)
        # Don't inflate total_completions on same-day duplicate check-ins.
        total = streak.total_completions + (0 if gap == 0 else 1)

        updated = Streak(
            id=streak.id, activity_id=activity_id,
            current_count=new_count, best_count=new_best,
            last_checkin_date=today.isoformat(),
            shields_available=streak.shields_available - (1 if shield_used else 0),
            weekly_completion_rate=week_rate,
            total_completions=total,
            weekly_streak_count=new_weekly_streak_count,
        )

        save_res = self._repo.update_streak(updated)
        if isinstance(save_res, Failure):
            return Failure(save_res.error)

        return Success(StreakUpdateResult(
            streak=save_res.value,
            shield_used=shield_used,
            streak_reset=streak_reset,
        ))

    # --- WEEKLY SHIELD REFRESH ---
    def _maybe_refresh_shields(
        self, streak: Streak, today: date, activity_id: int,
    ) -> None:
        """Replenish shields if a new week has started since the last check-in."""
        last = self._parse_date(streak.last_checkin_date)
        if last is None:
            return
        last_week_start = last - timedelta(days=last.weekday())
        this_week_start = today - timedelta(days=today.weekday())
        if this_week_start <= last_week_start:
            return  # Still same week — nothing to restore.
        shields_res = self._repo.get_setting("shields_per_week")
        shields_per_week = int(shields_res.value) if isinstance(shields_res, Success) else 1
        if streak.shields_available >= shields_per_week:
            return  # Already at or above weekly maximum — no restore needed.
        restored = Streak(
            id=streak.id, activity_id=streak.activity_id,
            current_count=streak.current_count,
            best_count=streak.best_count,
            last_checkin_date=streak.last_checkin_date,
            shields_available=shields_per_week,
            weekly_completion_rate=streak.weekly_completion_rate,
            total_completions=streak.total_completions,
            weekly_streak_count=streak.weekly_streak_count,
        )
        self._repo.update_streak(restored)

    # --- REAL WEEKLY RATE ---
    def _calc_weekly_rate(self, activity_id: int, today: date) -> float:
        """Count distinct days with a check-in in the current ISO week."""
        week_start = today - timedelta(days=today.weekday())
        days_in_week = min((today - week_start).days + 1, 7)
        if days_in_week == 0:
            return 0.0
        checkins_res = self._activity_repo.get_checkins_since(
            activity_id, week_start.isoformat(),
        )
        if isinstance(checkins_res, Failure):
            return 0.0
        # Count distinct calendar days (ISO date prefix of completed_at).
        # The check-in for today is already in the DB when this runs, so
        # distinct_days already includes today — no +1 needed.
        distinct_days = len({c.completed_at[:10] for c in checkins_res.value})
        completed = min(distinct_days, days_in_week)
        return round(completed / days_in_week, 2)

    # --- GRACE PERIOD ---
    def _within_grace(self, today: date) -> bool:
        grace_res = self._repo.get_setting("grace_period_hours")
        if isinstance(grace_res, Failure):
            return False
        grace_hours = int(grace_res.value)
        now = datetime.now()
        return now.hour < grace_hours

    @staticmethod
    def _parse_date(date_str: str | None) -> date | None:
        if not date_str:
            return None
        try:
            return date.fromisoformat(date_str)
        except ValueError:
            return None
