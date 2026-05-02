# features/home/widgets/habits_section.py — Section [A]: daily habits.

# --- IMPORTS ---
from __future__ import annotations

from typing import Callable

import flet as ft

from core.design.neu_card import neu_card
from core.design.tokens import DesignTokens
from core.design.typography import TextStyles, make_text
from domain.entities.activity import Activity


class HabitsSection(ft.Column):
    def __init__(
        self,
        tokens: DesignTokens,
        activities: list[Activity],
        on_select: Callable[[Activity], None],
        section_title: str = "Mis hábitos",
    ) -> None:
        super().__init__(spacing=12)
        self._tokens = tokens
        chips: list[ft.Control] = [
            self._habit_chip(a, on_select) for a in activities
        ]
        row: ft.Control = (
            ft.Row(controls=chips, scroll=ft.ScrollMode.AUTO, spacing=12)
            if activities else
            make_text("Sin hábitos aún — crea tu primera semilla", TextStyles.caption)
        )
        self.controls = [make_text(section_title, TextStyles.heading2), row]

    def _habit_chip(
        self, activity: Activity, on_select: Callable[[Activity], None],
    ) -> ft.Control:
        from features.gamification.streak_indicator import StreakIndicator
        card = neu_card(
            content=ft.Column(
                controls=[
                    ft.Text(
                        activity.title,
                        size=12,
                        color=self._tokens.color_text_main,
                        text_align=ft.TextAlign.CENTER,
                        no_wrap=False,
                        overflow=ft.TextOverflow.VISIBLE,
                    ),
                    StreakIndicator(activity_id=activity.id or 0, tokens=self._tokens),
                ],
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                spacing=6,
            ),
            tokens=self._tokens,
            radius_key="large",
            padding=12,
            width=90,
        )
        return ft.GestureDetector(
            content=card,
            on_tap=lambda e, a=activity: on_select(a),
        )
