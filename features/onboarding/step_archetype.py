# features/onboarding/step_archetype.py — Step 1: user archetype selection.

# --- IMPORTS ---
from __future__ import annotations

from typing import Callable

import flet as ft

from core.design.neu_card import neu_card
from core.design.tokens import DesignTokens
from core.design.typography import TextStyles, make_text


_ARCHETYPES = {
    "archetype_1": "sembrador",
    "archetype_2": "jardinero",
    "archetype_3": "podador",
}


class StepArchetype(ft.Column):
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
        question = self._copy("onboarding_question_1")
        cards: list[ft.Control] = [
            self._archetype_card(k) for k in _ARCHETYPES
        ]
        self.controls = (
            [ft.Container(height=40), make_text(question, TextStyles.heading2),
             ft.Container(height=8)]
            + cards
        )

    def _archetype_card(self, key: str) -> ft.Control:
        label = self._copy(key)
        card = neu_card(
            content=ft.Text(
                label, size=17,
                color=self._tokens.color_text_main,
                text_align=ft.TextAlign.CENTER,
            ),
            tokens=self._tokens,
            padding=18,
            width=300,
        )
        return ft.GestureDetector(
            content=card,
            on_tap=lambda e, k=key: self._select(k),
        )

    def _select(self, key: str) -> None:
        try:
            from core.database.db_helper import DBHelper
            conn = DBHelper.instance().get_connection()
            conn.execute(
                "INSERT OR REPLACE INTO settings (key,value) VALUES (?,?)",
                ("user_archetype", _ARCHETYPES.get(key, key)),
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
