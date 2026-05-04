# features/home/widgets/backlog_section.py — Section [C]: collapsible backlog.

# --- IMPORTS ---
from __future__ import annotations

from typing import Callable

import flet as ft

from core.design.neu_card import NeuCard
from core.design.tokens import DesignTokens
from core.design.typography import TextStyles, make_text
from domain.entities.activity import Activity


class BacklogSection(ft.Column):
    def __init__(
        self,
        tokens: DesignTokens,
        activities: list[Activity],
        on_elevate: Callable[[Activity], None],
        on_select: Callable[[Activity], None],
        section_title: str = "Semillas en espera",
    ) -> None:
        super().__init__(spacing=8)
        self._tokens = tokens
        self._activities = activities
        self._on_elevate = on_elevate
        self._on_select = on_select
        self._expanded = False
        self._list = ft.Container(
            content=ft.Column(controls=[], spacing=8),
            height=0,
            animate_size=ft.Animation(300, ft.AnimationCurve.EASE_IN_OUT),  # type: ignore
        )
        self._icon_container = ft.Container(content=ft.Icon(ft.Icons.EXPAND_MORE, color=tokens.color_text_sub, size=18))
        title_row = ft.GestureDetector(
            content=ft.Row(
                controls=[
                    make_text(section_title, TextStyles.label),
                    ft.Text(
                        f"Actividades pendientes: {len(activities)}",
                        size=11,
                        color=tokens.color_text_sub,
                        italic=True,
                    ),
                    ft.Container(expand=True),
                    self._icon_container,
                ],
                alignment=ft.MainAxisAlignment.START,
                vertical_alignment=ft.CrossAxisAlignment.CENTER,
            ),
            on_tap=self._toggle,
        )
        self.controls = [title_row, self._list]

    def _toggle(self, e: ft.TapEvent) -> None:
        self._expanded = not self._expanded
        self._list.height = None if self._expanded else 0
        
        new_icon = ft.Icons.EXPAND_LESS if self._expanded else ft.Icons.EXPAND_MORE
        self._icon_container.content = ft.Icon(new_icon, color=self._tokens.color_text_sub, size=18)
        
        if self._expanded:
            self._list.content = ft.Column(
                controls=[self._backlog_card(a) for a in self._activities],
                spacing=8,
            )
        try:
            self.update()
        except Exception: pass

    def _backlog_card(self, activity: Activity) -> ft.Control:
        return ft.Container(
            content=ft.Row(
                controls=[
                    ft.GestureDetector(
                        content=ft.Container(
                            content=ft.Text(
                                activity.title,
                                color=self._tokens.color_text_main,
                                size=15,
                            ),
                            expand=True,
                            padding=ft.Padding(14, 14, 0, 14),
                        ),
                        on_tap=lambda e: self._on_select(activity),
                        expand=True,
                    ),
                    ft.GestureDetector(
                        content=ft.Container(
                            content=ft.Icon(
                                ft.Icons.ARROW_UPWARD,
                                color=self._tokens.color_secondary,
                                size=18,
                            ),
                            padding=14,
                        ),
                        on_tap=lambda e: self._on_elevate(activity),
                    ),
                ],
            ),
            bgcolor=self._tokens.color_base,
            border_radius=ft.BorderRadius(12, 12, 12, 12),
            shadow=[
                ft.BoxShadow(
                    offset=ft.Offset(2, 2),
                    blur_radius=4.0,
                    color=NeuCard._with_opacity(self._tokens.shadow_dark_opacity * 0.4, self._tokens.color_shadow_dark),
                ),
                ft.BoxShadow(
                    offset=ft.Offset(-2, -2),
                    blur_radius=4.0,
                    color=NeuCard._with_opacity(self._tokens.shadow_light_opacity * 0.5, self._tokens.color_shadow_light),
                ),
            ],
        )
