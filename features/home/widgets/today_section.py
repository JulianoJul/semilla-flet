# features/home/widgets/today_section.py — Section [D]: today's focus activities.

# --- IMPORTS ---
from __future__ import annotations

from typing import Callable

import flet as ft

from core.asset_helper import get_sound_asset
from core.design.neu_card import neu_card
from core.design.tokens import DesignTokens
from core.design.typography import TextStyles, make_text
from domain.entities.activity import Activity


class TodaySection(ft.Column):
    def __init__(
        self,
        tokens: DesignTokens,
        activities: list[Activity],
        on_complete: Callable[[Activity], None],
        section_title: str = "Hoy cultivo",
    ) -> None:
        super().__init__(spacing=12)
        self._tokens = tokens
        self._on_complete = on_complete
        self._sound = get_sound_asset("complete")
        cards: list[ft.Control] = [
            self._activity_card(a) for a in activities[:3]
        ]
        self.controls = [make_text(section_title, TextStyles.heading2)] + cards
        if not activities:
            self.controls.append(
                make_text("Elige hasta 3 semillas para hoy", TextStyles.caption),
            )

    def _activity_card(self, activity: Activity) -> ft.Control:
        card = neu_card(
            content=ft.Row(
                controls=[
                    ft.Icon(ft.Icons.PARK_OUTLINED, color=self._tokens.color_primary, size=20),
                    ft.Text(
                        activity.title,
                        color=self._tokens.color_text_main,
                        size=16,
                        expand=True,
                    ),
                    ft.Icon(
                        ft.Icons.CHECK_CIRCLE_OUTLINE,
                        color=self._tokens.color_secondary, size=22,
                    ),
                ],
                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
            ),
            tokens=self._tokens,
            padding=16,
        )
        return ft.GestureDetector(
            content=card,
            on_tap=lambda e, a=activity: self._handle_complete(e, a),
        )

    def _handle_complete(self, e, activity: Activity) -> None:
        self._sound()
        self._on_complete(activity)
