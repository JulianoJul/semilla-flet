"""
core/container.py — Simple dependency injection container.
"""

# --- IMPORTS ---
from __future__ import annotations

from typing import Optional

from core.database.db_helper import DBHelper
from data.datasources.activity_datasource import ActivityLocalDatasource
from data.datasources.gamification_datasource import (
    GamificationLocalDatasource,
)
from data.repositories.activity_repository_impl import ActivityRepositoryImpl
from data.repositories.gamification_repository_impl import (
    GamificationRepositoryImpl,
)
from core.notifications.notification_service import NotificationService
from domain.use_cases.complete_activity import CompleteActivityUseCase
from domain.use_cases.create_activity import CreateActivityUseCase
from domain.use_cases.get_today_intentions import GetTodayIntentionsUseCase
from domain.use_cases.manage_streak import ManageStreakUseCase


# --- SINGLETON ---
class AppContainer:
    _instance: Optional[AppContainer] = None

    def __init__(self, db_helper: Optional[DBHelper] = None) -> None:
        db = db_helper or DBHelper.instance()

        # --- DATASOURCES ---
        activity_ds = ActivityLocalDatasource(db)
        gamification_ds = GamificationLocalDatasource(db)

        # --- REPOSITORIES ---
        self.activity_repo = ActivityRepositoryImpl(activity_ds)
        self.gamification_repo = GamificationRepositoryImpl(gamification_ds)

        self.notification_service = NotificationService()

        self.manage_streak_uc = ManageStreakUseCase(self.gamification_repo)

        self.create_activity_uc = CreateActivityUseCase(
            self.activity_repo, self.gamification_repo,
        )
        self.complete_activity_uc = CompleteActivityUseCase(
            self.activity_repo, self.gamification_repo,
            self.manage_streak_uc, self.notification_service,
        )
        self.get_today_intentions_uc = GetTodayIntentionsUseCase(
            self.activity_repo,
        )

    @classmethod
    def instance(
        cls, db_helper: Optional[DBHelper] = None,
    ) -> AppContainer:
        if cls._instance is None:
            cls._instance = cls(db_helper)
        return cls._instance

    @classmethod
    def _reset(cls) -> None:
        cls._instance = None
