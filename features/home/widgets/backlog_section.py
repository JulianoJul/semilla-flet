# features/home/widgets/backlog_section.py — Section [C]: collapsible backlog.

# --- IMPORTS ---
from __future__ import annotations

from typing import Callable

import flet as ft

from core.design.neu_card import neu_card
from core.design.tokens import DesignTokens
from core.design.typography import TextStyles, make_text
from domain.entities.activity import Activity


class BacklogSection(ft.Column):
    def __init__(
        self,
        tokens: DesignTokens,
        activities: list[Activity],
        on_elevate: Callable[[Activity], None],
        section_title: str = "Semillas en espera",
    ) -> None:
        super().__init__(spacing=8)
        self._tokens = tokens
        self._activities = activities
        self._on_elevate = on_elevate
        self._expanded = False
        self._list = ft.Container(
            content=ft.Column(controls=[], spacing=8),
            height=0,
            animate=ft.Animation(300, ft.AnimationCurve.EASE_IN_OUT),
        )
        title_row = ft.GestureDetector(
            content=ft.Row(
                controls=[
                    make_text(section_title, TextStyles.label),
                    ft.Icon(ft.Icons.EXPAND_MORE, color=tokens.color_text_sub, size=18),
                ],
            ),
            on_tap=self._toggle,
        )
        self.controls = [title_row, self._list]

    def _toggle(self, e: ft.TapEvent) -> None:
        self._expanded = not self._expanded
        self._list.height = len(self._activities) * 72 if self._expanded else 0
        if self._expanded:
            self._list.content = ft.Column(
                controls=[self._backlog_card(a) for a in self._activities],
                spacing=8,
            )
        try: self._list.update()
        except Exception: pass

    def _backlog_card(self, activity: Activity) -> ft.Control:
        card = neu_card(
            content=ft.Row(
                controls=[
                    ft.Text(
                        activity.title,
                        color=self._tokens.color_text_main,
                        size=15,
                        expand=True,
                    ),
                    ft.Icon(
                        ft.Icons.ARROW_UPWARD,
                        color=self._tokens.color_secondary, size=18,
                    ),
                ],
            ),
            tokens=self._tokens,
            padding=14,
        )
        return ft.GestureDetector(
            content=card,
            on_long_press=lambda e, a=activity: self._on_elevate(a),
        )
