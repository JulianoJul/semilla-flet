# features/home/widgets/habits_section.py — Section [A]: daily habits.

from __future__ import annotations
from typing import Callable
import flet as ft
from core.design.neu_card import NeuCard
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

        if not activities:
            empty = make_text(
                "Sin hábitos aún — crea tu primera semilla 🌱",
                TextStyles.caption,
            )
            self.controls = [make_text(section_title, TextStyles.heading2), empty]
            return

        chips: list[ft.Control] = [
            self._habit_chip(a, on_select) for a in activities
        ]
        row = ft.Row(
            controls=chips,
            scroll=ft.ScrollMode.AUTO,
            spacing=12,
        )
        self.controls = [make_text(section_title, TextStyles.heading2), row]

    def _habit_chip(
        self,
        activity: Activity,
        on_select: Callable[[Activity], None],
    ) -> ft.Control:
        from features.gamification.streak_indicator import StreakIndicator

        indicator = StreakIndicator(
            activity_id=activity.id or 0,
            tokens=self._tokens,
        )

        # Título truncado a 2 líneas máximo
        title = ft.Text(
            activity.title,
            size=13,
            color=self._tokens.color_text_main,
            text_align=ft.TextAlign.CENTER,
            max_lines=2,
            overflow=ft.TextOverflow.ELLIPSIS,
            no_wrap=False,
        )

        card_content = ft.Column(
            controls=[title, indicator],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=6,
            tight=True,
        )

        card = NeuCard(
            content=card_content,
            tokens=self._tokens,
            radius_key="large",
            padding=12,
            width=125,   # Un poco más ancho para evitar que se corten los indicadores
            height=90,   # Altura fija para consistencia visual
        )

        return ft.GestureDetector(
            content=card,
            on_tap=lambda e, a=activity: on_select(a),
        )
