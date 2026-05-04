"""
domain/use_cases/create_activity.py — Create a new activity.
"""

# --- IMPORTS ---
from __future__ import annotations

from datetime import datetime, timedelta, timezone
from typing import Optional

from core.result import Failure, Result, Success
from domain.entities.activity import Activity, ActivityType, FrequencyConfig
from domain.entities.checkin import CheckIn
from domain.repositories.activity_repository import ActivityRepository
from domain.repositories.gamification_repository import GamificationRepository


# --- USE CASE ---
class CreateActivityUseCase:
    def __init__(
        self,
        activity_repo: ActivityRepository,
        gamification_repo: GamificationRepository,
    ) -> None:
        self._activity_repo = activity_repo
        self._gamification_repo = gamification_repo

    def execute(
        self,
        title: str,
        activity_type: str,
        frequency_config: Optional[FrequencyConfig] = None,
        deadline: Optional[str] = None,
        implementation_intention: Optional[str] = None,
        coping_plan: Optional[str] = None,
    ) -> Result[Activity]:
        # --- VALIDATION ---
        title = title.strip()
        if not title:
            return Failure("El título no puede estar vacío")

        act_type = ActivityType(activity_type)

        # --- MAX INTENTIONS CHECK ---
        if act_type == ActivityType.TODAY_FOCUS:
            max_res = self._gamification_repo.get_setting(
                "max_today_intentions",
            )
            if isinstance(max_res, Success):
                max_val = int(max_res.value)
                current = self._activity_repo.get_today_intentions()
                if isinstance(current, Success) and len(current.value) >= max_val:
                    return Failure(
                        f"Máximo {max_val} intenciones de hoy"
                    )

        # --- CREATE ---
        # Store timestamps as 'YYYY-MM-DD HH:MM:SS' (SQLite-safe, unambiguous UTC).
        now = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S")
        activity = Activity(
            id=None, title=title, type=act_type,
            frequency_config=frequency_config,
            deadline=deadline,
            implementation_intention=implementation_intention,
            coping_plan=coping_plan, created_at=now,
        )
        result = self._activity_repo.create_activity(activity)
        if isinstance(result, Failure):
            return result

        # --- ENDOWED PROGRESS ---
        created = result.value
        # if act_type in (ActivityType.DAILY, ActivityType.DEADLINE):
        #     self._add_endowed_checkins(created)

        return result

    def _add_endowed_checkins(self, activity: Activity) -> None:
        ep_res = self._gamification_repo.get_setting(
            "endowed_progress_checkins",
        )
        count = int(ep_res.value) if isinstance(ep_res, Success) else 2
        # Each endowed check-in is placed on a distinct past day (not today)
        # to avoid polluting morning_completions or same-day duplicate logic.
        for i in range(count):
            days_ago = count - i  # e.g. count=2 → 2 days ago, 1 day ago
            past_ts = (
                datetime.now(timezone.utc) - timedelta(days=days_ago)
            ).strftime("%Y-%m-%d 12:00:00")
            checkin = CheckIn(
                id=None, activity_id=activity.id or 0,
                completed_at=past_ts, notes="endowed",
            )
            self._activity_repo.create_checkin(checkin)
