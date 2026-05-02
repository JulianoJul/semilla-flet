"""
domain/use_cases/complete_activity.py — Complete an activity check-in.
"""

# --- IMPORTS ---
from __future__ import annotations

from datetime import datetime, timezone

from core.result import Failure, Result, Success
from domain.entities.checkin import CheckIn
from domain.entities.results import CompletionResult
from domain.repositories.activity_repository import ActivityRepository
from domain.repositories.gamification_repository import GamificationRepository
from domain.use_cases.manage_streak import ManageStreakUseCase
from core.notifications.notification_service import NotificationService


# --- USE CASE ---
class CompleteActivityUseCase:
    def __init__(
        self,
        activity_repo: ActivityRepository,
        gamification_repo: GamificationRepository,
        manage_streak: ManageStreakUseCase,
        notification_service: NotificationService,
    ) -> None:
        self._activity_repo = activity_repo
        self._gamification_repo = gamification_repo
        self._manage_streak = manage_streak
        self._notification_service = notification_service

    def execute(
        self,
        activity_id: int,
        notes: str | None = None,
    ) -> Result[CompletionResult]:
        # --- CREATE CHECKIN ---
        now = datetime.now(timezone.utc).isoformat()
        checkin = CheckIn(
            id=None, activity_id=activity_id,
            completed_at=now, notes=notes,
        )
        checkin_res = self._activity_repo.create_checkin(checkin)
        if isinstance(checkin_res, Failure):
            return Failure(checkin_res.error)

        # --- UPDATE STREAK ---
        streak_res = self._manage_streak.execute(activity_id)
        if isinstance(streak_res, Failure):
            return Failure(streak_res.error)

        # --- CHECK BADGES ---
        badge_res = self._gamification_repo.check_and_unlock_badges(
            activity_id,
        )
        new_badge = None
        if isinstance(badge_res, Success):
            new_badge = badge_res.value

        # --- CHECK CHEST ---
        chest_res = self._gamification_repo.should_show_chest()
        show_chest = isinstance(chest_res, Success) and chest_res.value

        # --- NOTIFICATIONS ---
        self._notification_service.send_completion_feedback()

        return Success(CompletionResult(
            checkin=checkin_res.value,
            streak=streak_res.value.streak,
            show_chest=show_chest,
            new_badge=new_badge,
        ))
