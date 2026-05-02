# features/activity/create_activity_view.py — BottomSheet to create an activity.

# --- IMPORTS ---
from __future__ import annotations

from typing import Callable

import flet as ft

from core.design.colors import COLOR_BASE
from core.design.neu_button import NeuButton
from core.design.neu_card import neu_card
from core.design.tokens import DesignTokens
from core.design.typography import TextStyles, make_text


_TYPES = [("A", "Hábito diario"), ("B", "Horizonte"), ("C", "Semilla")]


class CreateActivityView(ft.BottomSheet):
    def __init__(
        self,
        tokens: DesignTokens,
        on_created: Callable[[], None],
        page: ft.Page,
    ) -> None:
        self._tokens = tokens
        self._on_created = on_created
        self._page = page
        self._selected_type = "A"
        self._error = ft.Text("", color=tokens.color_accent_alert, size=13)

        self._title_field = ft.TextField(
            hint_text=self._copy("activity_name_hint"),
            hint_style=ft.TextStyle(color=tokens.color_text_sub),
            color=tokens.color_text_main,
            border=ft.InputBorder.NONE,
            text_size=16,
        )
        self._deadline_field = ft.TextField(
            hint_text="YYYY-MM-DD",
            hint_style=ft.TextStyle(color=tokens.color_text_sub),
            color=tokens.color_text_main,
            border=ft.InputBorder.NONE,
            text_size=14,
            visible=False,
        )
        self._intention_field = ft.TextField(
            hint_text=self._copy("implementation_hint"),
            hint_style=ft.TextStyle(color=tokens.color_text_sub),
            color=tokens.color_text_main,
            border=ft.InputBorder.NONE,
            text_size=14,
            multiline=True,
            min_lines=2,
            max_lines=3,
        )
        self._type_row = self._build_type_row()
        self._column = ft.Column(
            controls=self._build_controls(),
            scroll=ft.ScrollMode.AUTO,
            spacing=12,
        )
        r = float(tokens.radius_large)
        super().__init__(
            use_safe_area=True,
            content=ft.Container(
                bgcolor=COLOR_BASE,
                padding=ft.padding.only(left=24, right=24, top=24, bottom=0),
                border_radius=ft.BorderRadius(r, r, 0, 0),
                content=ft.SafeArea(
                    content=self._column,
                    bottom=True,
                ),
            ),
        )

    def _build_controls(self) -> list[ft.Control]:
        controls: list[ft.Control] = [
            make_text(self._copy("new_activity_title"), TextStyles.heading2),
            ft.Container(height=4),
            self._type_row,
            ft.Container(height=4),
            neu_card(
                content=self._title_field, tokens=self._tokens,
                inset=True, padding=14,
            ),
        ]
        
        if self._selected_type == "B":
            self._deadline_field.visible = True
            controls.append(
                neu_card(
                    content=self._deadline_field, tokens=self._tokens,
                    inset=True, padding=14,
                )
            )
        
        controls.append(
            neu_card(
                content=self._intention_field, tokens=self._tokens,
                inset=True, padding=14,
            )
        )

        if self._error.value:
            controls.append(self._error)

        controls.append(ft.Container(height=8))
        
        controls.append(
            ft.Container(
                content=NeuButton(
                    label=self._copy("confirm_habit"),
                    on_click=self._handle_save,
                    tokens=self._tokens,
                ),
                padding=ft.padding.only(left=6, right=6, top=12, bottom=12),
                clip_behavior=ft.ClipBehavior.NONE,
            )
        )
        return controls

    def _build_type_row(self) -> ft.Row:
        def make_chip(code: str, label: str) -> ft.Control:
            selected = code == self._selected_type
            bg = self._tokens.color_primary if selected else self._tokens.color_base
            fg = self._tokens.color_shadow_light if selected else self._tokens.color_text_main
            r = float(self._tokens.radius_small)
            chip = ft.Container(
                content=ft.Text(label, color=fg, size=13, weight=ft.FontWeight.W_500),
                bgcolor=bg,
                border_radius=ft.BorderRadius(r, r, r, r),
                padding=ft.Padding(left=12, right=12, top=8, bottom=8),
            )
            return ft.GestureDetector(
                content=chip,
                on_tap=lambda e, c=code: self._select_type(c),
            )
        return ft.Row(
            controls=[make_chip(c, l) for c, l in _TYPES],
            spacing=8,
        )

    def _select_type(self, code: str) -> None:
        self._selected_type = code
        self._type_row.controls = self._build_type_row().controls
        self._column.controls = self._build_controls()
        try:
            self._column.update()
        except Exception:
            pass

    def _handle_save(self, e: ft.ControlEvent) -> None:
        title = (self._title_field.value or "").strip()
        if not title:
            self._error.value = "El nombre no puede estar vacío"
            self._column.controls = self._build_controls()
            try: self._column.update()
            except Exception: pass
            return
        deadline = (self._deadline_field.value or "").strip() or None
        intention = (self._intention_field.value or "").strip() or None
        try:
            from core.container import AppContainer
            res = AppContainer.instance().create_activity_uc.execute(
                title=title,
                activity_type=self._selected_type,
                deadline=deadline,
                implementation_intention=intention,
            )
            if res.is_failure():
                self._error.value = res.error or "Error"
                self._column.controls = self._build_controls()
                try: self._column.update()
                except Exception: pass
                return
        except Exception as exc:
            self._error.value = str(exc)
            self._column.controls = self._build_controls()
            try: self._column.update()
            except Exception: pass
            return
        self.open = False
        try: self._page.update()
        except Exception: pass
        self._on_created()

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
