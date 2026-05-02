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
        streak = self._load_streak(activity.id or 0)
        card = neu_card(
            content=ft.Column(
                controls=[
                    ft.Text(
                        activity.title[:12] + ("…" if len(activity.title) > 12 else ""),
                        size=13,
                        text_align=ft.TextAlign.CENTER,
                    ),
                    ft.ProgressRing(
                        value=min(streak / 7.0, 1.0),
                        width=32, height=32, stroke_width=3,
                    ),
                    ft.Text(
                        f"🔥 {streak}",
                        size=11,
                        text_align=ft.TextAlign.CENTER,
                    ),
                ],
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                spacing=6,
            ),
            radius_key="large",
            padding=12,
            width=90,
            height=110,
        )
        return ft.GestureDetector(
            content=card,
            on_tap=lambda e, a=activity: on_select(a),
        )

    def _load_streak(self, activity_id: int) -> int:
        try:
            from core.database.db_helper import DBHelper
            row = DBHelper.instance().get_connection().execute(
                "SELECT current_count FROM streaks WHERE activity_id=?",
                (activity_id,),
            ).fetchone()
            return int(row["current_count"]) if row else 0
        except Exception:
            return 0
