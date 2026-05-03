# features/home/widgets/ritual_sheet.py — Bottom sheet for selecting today's seeds.

# --- IMPORTS ---
from __future__ import annotations

from typing import Callable

import flet as ft

from core.design.colors import COLOR_BASE
from core.design.neu_button import NeuButton
from core.design.tokens import DesignTokens
from core.design.typography import TextStyles, make_text
from domain.entities.activity import Activity, ActivityType


class RitualSheet(ft.BottomSheet):
    def __init__(
        self,
        tokens: DesignTokens,
        on_confirm: Callable[[list[int]], None],
        page: ft.Page,
    ) -> None:
        self._tokens = tokens
        self._on_confirm = on_confirm
        self._page = page
        self._max = self._load_max()
        self._activities = self._load_candidates()
        self._selected: set[int] = set()
        self._error = ft.Text("", color=tokens.color_accent_alert, size=13)
        self._checkboxes: dict[int, ft.Checkbox] = {}
        rows: list[ft.Control] = [self._activity_row(a) for a in self._activities]

        r = float(tokens.radius_large)
        super().__init__(
            use_safe_area=True,
            content=ft.Container(
                bgcolor=COLOR_BASE,
                padding=24,
                border_radius=ft.BorderRadius(r, r, 0, 0),
                content=ft.SafeArea(
                    ft.Column(
                        controls=[
                            make_text(self._copy("today_title"), TextStyles.heading2),
                            ft.Container(height=8),
                            *rows,
                            self._error,
                            ft.Container(height=8),
                            NeuButton(
                                label=self._copy("ritual_button"),
                                on_click=self._handle_confirm,
                                tokens=tokens,
                            ),
                        ],
                        scroll=ft.ScrollMode.AUTO,
                        spacing=10,
                    ),
                    bottom=True,
                ),
            ),
        )

    def _activity_row(self, activity: Activity) -> ft.Control:
        cb = ft.Checkbox(
            label=activity.title,
            label_style=ft.TextStyle(color=self._tokens.color_text_main, size=15),
            active_color=self._tokens.color_primary,
            check_color=self._tokens.color_shadow_light,
        )
        aid = activity.id or 0
        self._checkboxes[aid] = cb
        cb.on_change = lambda e, a=activity: self._toggle(e, a)
        return cb

    def _toggle(self, e, activity: Activity) -> None:
        aid = activity.id or 0
        cb = self._checkboxes.get(aid)
        checked = bool(cb.value) if cb else False
        if checked:
            if len(self._selected) >= self._max:
                if cb:
                    cb.value = False
                    try: cb.update()
                    except Exception: pass
                self._error.value = f"Máximo {self._max} semillas"
                try: self._error.update()
                except Exception: pass
                return
            self._selected.add(aid)
        else:
            self._selected.discard(aid)
        self._error.value = ""
        try: self._error.update()
        except Exception: pass

    def _handle_confirm(self, e: ft.ControlEvent) -> None:
        self._on_confirm(list(self._selected))
        self.open = False
        try: self._page.update()
        except Exception: pass

    def _load_candidates(self) -> list[Activity]:
        try:
            from core.container import AppContainer
            repo = AppContainer.instance().activity_repo
            res_daily = repo.get_activities_by_type(ActivityType.DAILY)
            res_deadline = repo.get_activities_by_type(ActivityType.DEADLINE)
            
            daily = res_daily.value or []
            deadline = res_deadline.value or []
            return daily + deadline
        except Exception:
            return []

    def _load_max(self) -> int:
        try:
            from core.database.db_helper import DBHelper
            row = DBHelper.instance().get_connection().execute(
                "SELECT value FROM settings WHERE key='max_today_intentions'",
            ).fetchone()
            return int(row["value"]) if row else 3
        except Exception:
            return 3

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
