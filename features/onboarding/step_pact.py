# features/onboarding/step_pact.py — Step 3: self-compassion pact.

# --- IMPORTS ---
from __future__ import annotations

from typing import Callable

import flet as ft

from core.design.neu_button import NeuButton
from core.design.neu_card import neu_card
from core.design.tokens import DesignTokens
from core.design.typography import TextStyles, make_text


class StepPact(ft.Column):
    def __init__(
        self,
        tokens: DesignTokens,
        on_done: Callable[[], None],
    ) -> None:
        super().__init__(
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            alignment=ft.MainAxisAlignment.CENTER,
            spacing=24,
            expand=True,
        )
        self._tokens = tokens
        self._on_done = on_done
        self._accepted = False
        self._checkbox = ft.Checkbox(
            active_color=tokens.color_primary,
            check_color=tokens.color_shadow_light,
        )
        self._checkbox.on_change = self._handle_check

        pact_row = ft.Row(
            controls=[
                self._checkbox,
                ft.Text(
                    self._copy("pact_text"),
                    color=tokens.color_text_main,
                    size=14,
                    expand=True,
                ),
            ],
            vertical_alignment=ft.CrossAxisAlignment.CENTER,
        )

        self._btn_container = ft.Container()
        self._rebuild_btn(disabled=True)

        controls: list[ft.Control] = [
            ft.Container(height=40),
            make_text(self._copy("pact_title"), TextStyles.heading2),
            ft.Container(height=8),
            neu_card(content=pact_row, tokens=tokens, padding=20, width=300),
            self._btn_container,
        ]
        self.controls = controls

    def _rebuild_btn(self, disabled: bool) -> None:
        self._btn_container.content = NeuButton(
            label=self._copy("confirm_pact"),
            on_click=self._handle_confirm,
            tokens=self._tokens,
            disabled=disabled,
        )

    def _handle_check(self, e) -> None:
        self._accepted = bool(self._checkbox.value)
        self._rebuild_btn(disabled=not self._accepted)
        try: self._btn_container.update()
        except Exception: pass

    def _handle_confirm(self, e: ft.ControlEvent) -> None:
        if not self._accepted:
            return
        try:
            from core.database.db_helper import DBHelper
            conn = DBHelper.instance().get_connection()
            for key in ("compassion_pact_accepted", "onboarding_complete"):
                conn.execute(
                    "INSERT OR REPLACE INTO settings (key,value) VALUES (?,?)",
                    (key, "1"),
                )
            conn.commit()
        except Exception:
            pass
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
