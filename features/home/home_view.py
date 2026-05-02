# features/home/home_view.py — Main home screen.

# --- IMPORTS ---
from __future__ import annotations

import threading
from typing import Optional

import flet as ft

from core.design.colors import COLOR_BASE
from core.design.tokens import DesignTokens
from core.design.typography import TextStyles, make_text
from domain.entities.activity import Activity, ActivityType


class HomeView(ft.Column):
    def __init__(self, page: ft.Page) -> None:
        super().__init__(scroll=ft.ScrollMode.AUTO, expand=True, spacing=0)
        self._page = page
        self._tokens = self._load_tokens()
        self._body = ft.Column(spacing=20, expand=True)
        self.controls = [
            ft.Container(
                content=self._body,
                bgcolor=COLOR_BASE,
                padding=ft.Padding(left=20, right=20, top=24, bottom=24),
                expand=True,
            )
        ]
        page.floating_action_button = ft.FloatingActionButton(
            icon=ft.Icons.ADD,
            bgcolor=self._tokens.color_primary,
            on_click=self._open_create,
        )
        threading.Thread(target=self._load_data, daemon=True).start()

    def _load_tokens(self) -> DesignTokens:
        try:
            from core.database.db_helper import DBHelper
            return DesignTokens.load(DBHelper.instance())
        except Exception:
            return DesignTokens.defaults()

    def _load_data(self) -> None:
        try:
            from core.container import AppContainer
            c = AppContainer.instance()
            today_res = c.get_today_intentions_uc.execute()
            activities: list[Activity] = []
            fresh = False
            if today_res.is_success() and today_res.value is not None:
                activities, fresh = today_res.value

            daily_res = c.activity_repo.get_activities_by_type(ActivityType.DAILY)
            dl_res = c.activity_repo.get_activities_by_type(ActivityType.DEADLINE)
            bl_res = c.activity_repo.get_activities_by_type(ActivityType.BACKLOG)

            self._build_ui(
                today=activities, fresh=fresh,
                daily=daily_res.value or [],
                deadlines=dl_res.value or [],
                backlog=bl_res.value or [],
            )
        except Exception:
            pass

    def _build_ui(
        self,
        today: list[Activity],
        fresh: bool,
        daily: list[Activity],
        deadlines: list[Activity],
        backlog: list[Activity],
    ) -> None:
        from features.home.widgets.backlog_section import BacklogSection
        from features.home.widgets.deadlines_section import DeadlinesSection
        from features.home.widgets.fresh_start_banner import FreshStartBanner
        from features.home.widgets.habits_section import HabitsSection
        from features.home.widgets.plant_garden import PlantGarden
        from features.home.widgets.today_section import TodaySection

        controls: list[ft.Control] = [
            make_text(self._copy("home_title"), TextStyles.heading1),
            PlantGarden(self._tokens),
        ]
        if fresh:
            controls.append(FreshStartBanner(self._tokens, self._open_ritual))
        controls += [
            TodaySection(self._tokens, today, self._handle_complete,
                         section_title=self._copy("today_title")),
            HabitsSection(self._tokens, daily, self._handle_habit_tap,
                          section_title=self._copy("habits_title")),
            DeadlinesSection(self._tokens, deadlines,
                             section_title=self._copy("deadlines_title"),
                             horizon_prefix=self._copy("horizon_prefix")),
            BacklogSection(self._tokens, backlog, self._elevate_to_today,
                           section_title=self._copy("backlog_title")),
        ]
        self._body.controls = controls
        try: self._body.update()
        except Exception: pass

    def _handle_complete(self, activity: Activity) -> None:
        try:
            from core.container import AppContainer
            AppContainer.instance().complete_activity_uc.execute(
                activity_id=activity.id or 0,
            )
            threading.Thread(target=self._load_data, daemon=True).start()
        except Exception:
            pass

    def _handle_habit_tap(self, activity: Activity) -> None:
        pass  # future: open detail sheet

    def _elevate_to_today(self, activity: Activity) -> None:
        try:
            from core.container import AppContainer
            c = AppContainer.instance()
            res = c.activity_repo.get_today_intentions()
            current = res.value or []
            ids = [a.id or 0 for a in current]
            if activity.id not in ids:
                ids.append(activity.id or 0)
            c.activity_repo.set_today_intentions(ids[:3])
            threading.Thread(target=self._load_data, daemon=True).start()
        except Exception:
            pass

    def _open_ritual(self) -> None:
        from features.home.widgets.ritual_sheet import RitualSheet
        sheet = RitualSheet(self._tokens, self._handle_ritual, self._page)
        self._page.overlay.append(sheet)
        sheet.open = True
        try: self._page.update()
        except Exception: pass

    def _handle_ritual(self, ids: list[int]) -> None:
        try:
            from core.container import AppContainer
            AppContainer.instance().activity_repo.set_today_intentions(ids)
        except Exception:
            pass
        threading.Thread(target=self._load_data, daemon=True).start()

    def _open_create(self, e) -> None:
        from features.activity.create_activity_view import CreateActivityView
        sheet = CreateActivityView(
            tokens=self._tokens,
            on_created=lambda: threading.Thread(
                target=self._load_data, daemon=True,
            ).start(),
            page=self._page,
        )
        self._page.overlay.append(sheet)
        sheet.open = True
        try: self._page.update()
        except Exception: pass

    @staticmethod
    def _copy(key: str) -> str:
        try:
            from core.database.db_helper import DBHelper
            row = DBHelper.instance().get_connection().execute(
                "SELECT value FROM ui_copy WHERE key=?", (key,),
            ).fetchone()
            return row["value"] if row else key
        except Exception:
            return key
