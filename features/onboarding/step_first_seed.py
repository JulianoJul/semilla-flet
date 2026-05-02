# features/onboarding/step_first_seed.py — Step 2: create first habit.

# --- IMPORTS ---
from __future__ import annotations

from typing import Callable

import flet as ft

from core.design.neu_button import NeuButton
from core.design.neu_card import neu_card
from core.design.tokens import DesignTokens
from core.design.typography import TextStyles, make_text


class StepFirstSeed(ft.Column):
    def __init__(
        self,
        tokens: DesignTokens,
        on_done: Callable[[], None],
        page: ft.Page,
    ) -> None:
        super().__init__(
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            alignment=ft.MainAxisAlignment.CENTER,
            spacing=24,
            expand=True,
        )
        self._tokens = tokens
        self._on_done = on_done
        self._field = ft.TextField(
            hint_text=self._copy("first_seed_hint"),
            hint_style=ft.TextStyle(color=tokens.color_text_sub),
            color=tokens.color_text_main,
            border=ft.InputBorder.NONE,
            text_size=16,
            multiline=False,
        )
        self._error = ft.Text("", color=tokens.color_accent_alert, size=13)
        controls: list[ft.Control] = [
            ft.Container(height=40),
            make_text(self._copy("first_seed_title"), TextStyles.heading2),
            ft.Container(height=8),
            neu_card(content=self._field, tokens=tokens, inset=True, width=300, padding=16),
            self._error,
            NeuButton(
                label=self._copy("confirm_habit"),
                on_click=self._handle_confirm,
                tokens=tokens,
            ),
        ]
        self.controls = controls

    def _handle_confirm(self, e: ft.ControlEvent) -> None:
        title = (self._field.value or "").strip()
        if not title:
            self._error.value = "Escribe el nombre de tu hábito"
            try: self._error.update()
            except Exception: pass
            return
        try:
            from core.container import AppContainer
            result = AppContainer.instance().create_activity_uc.execute(
                title=title, activity_type="A",
            )
            if result.is_failure():
                self._error.value = result.error or "Error desconocido"
                try: self._error.update()
                except Exception: pass
                return
        except Exception as exc:
            self._error.value = str(exc)
            try: self._error.update()
            except Exception: pass
            return
        self._on_done()

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
