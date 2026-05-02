# features/home/widgets/fresh_start_banner.py — Monday/month-start banner.

# --- IMPORTS ---
from __future__ import annotations

from datetime import date
from typing import Callable

import flet as ft

from core.design.neu_button import NeuButton
from core.design.neu_card import neu_card
from core.design.tokens import DesignTokens
from core.design.typography import TextStyles, make_text


class FreshStartBanner(ft.Container):
    def __init__(
        self,
        tokens: DesignTokens,
        on_ritual: Callable[[], None],
    ) -> None:
        copy_key = (
            "fresh_start_monday" if date.today().weekday() == 0
            else "fresh_start_month"
        )
        message = self._copy(copy_key)
        ritual_label = self._copy("ritual_button")

        controls: list[ft.Control] = [
            ft.Text("🌱", size=24),
            make_text(message, TextStyles.body),
        ]
        card = neu_card(
            content=ft.Column(
                controls=[
                    ft.Row(controls=controls, spacing=10),
                    ft.Container(height=8),
                    NeuButton(
                        label=ritual_label,
                        on_click=lambda e: on_ritual(),
                        tokens=tokens,
                        variant="secondary",
                    ),
                ],
                spacing=4,
            ),
            tokens=tokens,
            padding=16,
        )
        super().__init__(content=card)

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
