"""
domain/repositories/activity_repository.py — Abstract activity repository.
"""

# --- IMPORTS ---
from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Optional

from core.result import Failure, Result, Success
from domain.entities.activity import Activity, ActivityType
from domain.entities.checkin import CheckIn


# --- ABSTRACT ---
class ActivityRepository(ABC):

    @abstractmethod
    def get_all_activities(self) -> Result[list[Activity]]: ...

    @abstractmethod
    def get_activities_by_type(
        self, activity_type: ActivityType,
    ) -> Result[list[Activity]]: ...

    @abstractmethod
    def create_activity(self, activity: Activity) -> Result[Activity]: ...

    @abstractmethod
    def update_activity(self, activity: Activity) -> Result[Activity]: ...

    @abstractmethod
    def archive_activity(self, activity_id: int) -> Result[None]: ...

    @abstractmethod
    def get_today_intentions(self) -> Result[list[Activity]]: ...

    @abstractmethod
    def set_today_intentions(
        self, activity_ids: list[int],
    ) -> Result[None]: ...

    @abstractmethod
    def get_checkins_for_activity(
        self, activity_id: int,
    ) -> Result[list[CheckIn]]: ...

    @abstractmethod
    def create_checkin(self, checkin: CheckIn) -> Result[CheckIn]: ...
