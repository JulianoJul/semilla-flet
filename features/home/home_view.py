# features/home/home_view.py — Main home screen.

from __future__ import annotations
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
                padding=ft.Padding(left=20, right=20, top=24, bottom=80),
                expand=True,
            )
        ]
        # FAB para crear nueva actividad
        page.floating_action_button = ft.FloatingActionButton(
            icon=ft.Icons.ADD,
            bgcolor=self._tokens.color_primary,
            foreground_color=self._tokens.color_shadow_light,
            on_click=self._open_create,
            tooltip="Nueva semilla",
        )
        page.floating_action_button_location = ft.FloatingActionButtonLocation.END_FLOAT
        self._page.run_task(self._load_data)

    def _load_tokens(self) -> DesignTokens:
        try:
            from core.database.db_helper import DBHelper
            return DesignTokens.load(DBHelper.instance())
        except Exception:
            return DesignTokens.defaults()

    async def _load_data(self) -> None:
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
                today=activities,
                fresh=fresh,
                daily=daily_res.value or [],
                deadlines=dl_res.value or [],
                backlog=bl_res.value or [],
            )
        except Exception as exc:
            import logging
            logging.getLogger(__name__).error("HomeView load error: %s", exc)

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

        self._garden = PlantGarden(self._tokens)

        controls: list[ft.Control] = [
            make_text(self._copy("home_title"), TextStyles.heading1),
            self._garden,
        ]

        if fresh:
            controls.append(
                FreshStartBanner(self._tokens, self._open_ritual)
            )

        # Sección "Hoy cultivo" — tap abre detalle, racha NO sube aquí
        controls.append(
            TodaySection(
                self._tokens,
                today,
                on_complete=self._handle_today_tap,
                section_title=self._copy("today_title"),
            )
        )

        # Sección "Mis hábitos" — tap abre detalle
        controls.append(
            HabitsSection(
                self._tokens,
                daily,
                on_select=self._handle_habit_tap,
                section_title=self._copy("habits_title"),
            )
        )

        # Sección "Horizontes"
        controls.append(
            DeadlinesSection(
                self._tokens,
                deadlines,
                on_select=self._handle_today_tap,
                section_title=self._copy("deadlines_title"),
                horizon_prefix=self._copy("horizon_prefix"),
            )
        )

        # Sección "Semillas en espera" — colapsable, elevate con tap
        controls.append(
            BacklogSection(
                self._tokens,
                backlog,
                on_elevate=self._elevate_to_today,
                on_select=self._handle_today_tap,
                section_title=self._copy("backlog_title"),
            )
        )

        self._body.controls = controls
        try:
            self._body.update()
        except Exception:
            pass

    # ── COMPLETAR ─────────────────────────────────────────────────
    # La racha se incrementa SOLO desde este método (llamado por ActivityDetailView)
    def _complete_activity(self, activity: Activity) -> None:
        try:
            from core.container import AppContainer
            res = AppContainer.instance().complete_activity_uc.execute(
                activity_id=activity.id or 0,
            )
            if res.is_success() and res.value:
                result = res.value
                if hasattr(self, "_garden"):
                    self._garden.celebrate()
                    
                snack = ft.SnackBar(
                    content=ft.Text(
                        f"✅ {activity.title} completada hoy",
                        color="#FFFFFF",
                    ),
                    bgcolor=self._tokens.color_primary,
                    duration=2000,
                )
                self._page.overlay.append(snack)
                snack.open = True
                
                def after_chest():
                    if result.new_badge is not None:
                        self._show_badge(result.new_badge)
                    self._page.run_task(self._load_data)

                if result.show_chest:
                    self._show_chest(on_finish=after_chest)
                else:
                    after_chest()
            else:
                self._page.run_task(self._load_data)
        except Exception as exc:
            import logging
            logging.getLogger(__name__).error("Complete error: %s", exc)

    def _handle_today_tap(self, activity: Activity) -> None:
        """Tap en card de 'Hoy cultivo' → abre detalle."""
        self._open_detail(activity)

    def _handle_habit_tap(self, activity: Activity) -> None:
        """Tap en chip de hábito → abre detalle."""
        self._open_detail(activity)

    # ── DETALLE ───────────────────────────────────────────────────
    def _open_detail(self, activity: Activity) -> None:
        from features.activity.activity_detail_view import ActivityDetailView

        sheet = ActivityDetailView(
            activity=activity,
            tokens=self._tokens,
            page=self._page,
            on_complete=self._complete_activity,   # ← racha sube aquí
            on_archived=lambda: self._page.run_task(self._load_data),
            on_dismiss=lambda: self._page.run_task(self._load_data),
        )
        self._page.overlay.append(sheet)
        sheet.open = True
        try:
            self._page.update()
        except Exception:
            pass

    # ── CHEST / BADGE ─────────────────────────────────────────────
    def _show_chest(self, on_finish=None) -> None:
        from features.gamification.chest_widget import ChestWidget
        
        def handle_open():
            if on_finish:
                on_finish()
            else:
                self._page.run_task(self._load_data)
                
        dialog = ChestWidget(
            tokens=self._tokens,
            on_open=handle_open,
            page=self._page,
        )
        self._page.overlay.append(dialog)
        dialog.open = True
        try:
            self._page.update()
        except Exception:
            pass

    def _show_badge(self, badge: object) -> None:
        from features.gamification.badge_celebration import BadgeCelebration
        overlay = BadgeCelebration(tokens=self._tokens, page=self._page)
        self._page.overlay.append(overlay)
        try:
            self._page.update()
        except Exception:
            pass
        overlay.show(badge)  # type: ignore[arg-type]

    # ── BACKLOG → HOY ─────────────────────────────────────────────
    def _elevate_to_today(self, activity: Activity) -> None:
        try:
            from core.container import AppContainer
            c = AppContainer.instance()
            res = c.activity_repo.get_today_intentions()
            current = res.value or []
            ids = [a.id or 0 for a in current]

            if activity.id in ids:
                return

            max_res = c.gamification_repo.get_setting("max_today_intentions")
            max_intentions = int(max_res.value) if max_res.is_success() and max_res.value is not None else 3

            if len(ids) >= max_intentions:
                snack = ft.SnackBar(
                    content=ft.Text(
                        f"Ya tienes {max_intentions} semillas para hoy 🌱"
                    ),
                    duration=2500,
                )
                self._page.overlay.append(snack)
                snack.open = True
                try:
                    self._page.update()
                except Exception:
                    pass
                return

            ids.append(activity.id or 0)
            c.activity_repo.set_today_intentions(ids[:max_intentions])

            if activity.type == ActivityType.BACKLOG:
                updated = Activity(
                    id=activity.id, title=activity.title, type=ActivityType.TODAY_FOCUS,
                    frequency_config=activity.frequency_config, deadline=activity.deadline,
                    implementation_intention=activity.implementation_intention,
                    coping_plan=activity.coping_plan, created_at=activity.created_at,
                    is_archived=activity.is_archived
                )
                c.activity_repo.update_activity(updated)

            snack = ft.SnackBar(
                content=ft.Text(f"☀️ {activity.title} añadida a hoy"),
                bgcolor=self._tokens.color_primary,
                duration=2000,
            )
            self._page.overlay.append(snack)
            snack.open = True
            self._page.run_task(self._load_data)
        except Exception:
            pass

    # ── RITUAL ────────────────────────────────────────────────────
    def _open_ritual(self) -> None:
        from features.home.widgets.ritual_sheet import RitualSheet
        sheet = RitualSheet(self._tokens, self._handle_ritual, self._page)
        self._page.overlay.append(sheet)
        sheet.open = True
        try:
            self._page.update()
        except Exception:
            pass

    def _handle_ritual(self, ids: list[int]) -> None:
        try:
            from core.container import AppContainer
            AppContainer.instance().activity_repo.set_today_intentions(ids)
        except Exception:
            pass
        self._page.run_task(self._load_data)

    # ── CREATE ────────────────────────────────────────────────────
    def _open_create(self, e: object) -> None:
        from features.activity.create_activity_view import CreateActivityView

        def handle_dismiss(ev: object) -> None:
            if sheet in self._page.overlay:
                self._page.overlay.remove(sheet)
                try:
                    self._page.update()
                except Exception:
                    pass

        sheet = CreateActivityView(
            tokens=self._tokens,
            on_created=lambda: self._page.run_task(self._load_data),
            page=self._page,
        )
        sheet.on_dismiss = handle_dismiss
        self._page.overlay.append(sheet)
        sheet.open = True
        try:
            self._page.update()
        except Exception:
            pass

    # ── COPY ──────────────────────────────────────────────────────
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
