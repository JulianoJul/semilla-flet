# features/home/widgets/deadlines_section.py — Section [B]: deadline activities.

# --- IMPORTS ---
from __future__ import annotations

from datetime import date
from typing import Optional

import flet as ft

from core.design.neu_card import neu_card
from core.design.tokens import DesignTokens
from core.design.typography import TextStyles, make_text
from domain.entities.activity import Activity


def _days_remaining(deadline: Optional[str]) -> Optional[int]:
    if not deadline:
        return None
    try:
        return (date.fromisoformat(deadline[:10]) - date.today()).days
    except ValueError:
        return None


class DeadlinesSection(ft.Column):
    def __init__(
        self,
        tokens: DesignTokens,
        activities: list[Activity],
        section_title: str = "Horizontes",
        horizon_prefix: str = "Horizonte en",
    ) -> None:
        super().__init__(spacing=12)
        self._tokens = tokens
        cards: list[ft.Control] = [
            self._deadline_card(a, horizon_prefix) for a in activities
        ]
        self.controls = [make_text(section_title, TextStyles.heading2)] + cards

    def _deadline_card(self, activity: Activity, prefix: str) -> ft.Control:
        days = _days_remaining(activity.deadline)
        urgent = days is not None and days <= 2
        if days is None:
            horizon_text = "Sin fecha definida"
        elif days < 0:
            horizon_text = "Horizonte superado"
        elif days == 0:
            horizon_text = "\u00a1Hoy es el d\u00eda!"
        else:
            horizon_text = f"{prefix} {days} d\u00edas"

        text_color = (
            self._tokens.color_accent_alert if urgent
            else self._tokens.color_text_sub
        )
        return neu_card(
            content=ft.Column(
                controls=[
                    ft.Text(
                        activity.title,
                        color=self._tokens.color_text_main,
                        size=16,
                        weight=ft.FontWeight.W_500,
                        overflow=ft.TextOverflow.VISIBLE,
                    ),
                    ft.Row(
                        controls=[
                            ft.Icon(ft.Icons.CALENDAR_TODAY, color=text_color, size=14),
                            ft.Text(horizon_text, color=text_color, size=13),
                        ],
                        spacing=4,
                    ),
                ],
                spacing=6,
            ),
            tokens=self._tokens,
            padding=16,
        )
