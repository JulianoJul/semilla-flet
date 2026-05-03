# features/home/widgets/today_section.py — Section [D]: today's focus activities.

from __future__ import annotations
from typing import Callable

import flet as ft

from core.design.neu_card import neu_card
from core.design.tokens import DesignTokens
from core.design.typography import TextStyles, make_text
from domain.entities.activity import Activity


class TodaySection(ft.Column):
    """
    Muestra las actividades de hoy.
    El TAP abre el detalle (on_complete callback); la racha sube
    desde ActivityDetailView, NO automáticamente al pulsar aquí.
    """

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

        cards: list[ft.Control] = [
            self._activity_card(a) for a in activities[:3]
        ]
        self.controls = [make_text(section_title, TextStyles.heading2)] + cards
        if not activities:
            self.controls.append(
                make_text(
                    "Elige hasta 3 semillas para hoy 🌱",
                    TextStyles.caption,
                )
            )

    def _activity_card(self, activity: Activity) -> ft.Control:
        already_done = self._completed_today(activity.id or 0)

        done_icon = ft.Icon(
            ft.Icons.CHECK_CIRCLE if already_done else ft.Icons.CHECK_CIRCLE_OUTLINE,
            color=(
                self._tokens.color_secondary if already_done
                else self._tokens.color_text_sub
            ),
            size=22,
        )

        card = neu_card(
            content=ft.Row(
                controls=[
                    ft.Icon(
                        ft.Icons.PARK_OUTLINED,
                        color=self._tokens.color_primary,
                        size=20,
                    ),
                    ft.Text(
                        activity.title,
                        color=self._tokens.color_text_main,
                        size=16,
                        expand=True,
                        overflow=ft.TextOverflow.ELLIPSIS,
                        max_lines=1,
                    ),
                    done_icon,
                ],
                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
            ),
            tokens=self._tokens,
            padding=16,
        )

        return ft.GestureDetector(
            content=card,
            # Tap → abre detalle; el detalle tiene el botón de completar
            on_tap=lambda e, a=activity: self._on_complete(a),
        )

    @staticmethod
    def _completed_today(activity_id: int) -> bool:
        try:
            from datetime import date
            from core.database.db_helper import DBHelper
            today = date.today().isoformat()
            row = DBHelper.instance().get_connection().execute(
                "SELECT COUNT(*) as c FROM checkins "
                "WHERE activity_id=? AND DATE(completed_at)=?",
                (activity_id, today),
            ).fetchone()
            return int(row["c"]) > 0
        except Exception:
            return False
