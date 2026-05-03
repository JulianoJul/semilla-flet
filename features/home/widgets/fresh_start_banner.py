# features/home/widgets/fresh_start_banner.py — Monday/month-start banner.

# --- IMPORTS ---
from __future__ import annotations

from datetime import date
from typing import Callable

import flet as ft

from core.design.neu_card import NeuCard
from core.design.tokens import DesignTokens
from core.design.typography import TextStyles, make_text


class FreshStartBanner(ft.Container):
    def __init__(
        self,
        tokens: DesignTokens,
        on_ritual: Callable[[], None],
    ) -> None:
        t = tokens
        copy_key = (
            "fresh_start_monday" if date.today().weekday() == 0
            else "fresh_start_month"
        )
        message = self._copy(copy_key)
        ritual_label = self._copy("ritual_button")

        # ── Circular icon neumorphic ─────────────────────────────
        icon_container = ft.Container(
            content=ft.Icon(ft.Icons.WB_SUNNY_OUTLINED, color=t.color_primary, size=24),
            width=48,
            height=48,
            border_radius=ft.BorderRadius(24, 24, 24, 24),
            bgcolor=t.color_base,
            shadow=[
                ft.BoxShadow(
                    offset=ft.Offset(-2, -2),
                    blur_radius=5.0,
                    color=NeuCard._with_opacity(t.shadow_light_opacity * 0.8, t.color_shadow_light),
                ),
                ft.BoxShadow(
                    offset=ft.Offset(2, 2),
                    blur_radius=5.0,
                    color=NeuCard._with_opacity(t.shadow_dark_opacity * 0.5, t.color_shadow_dark),
                ),
            ],
            alignment=ft.Alignment(0, 0),
        )

        # ── Message row ─────────────────────────────────────────
        message_col = ft.Column(
            controls=[
                ft.Text(
                    "Un nuevo día para crecer",
                    size=14,
                    weight=ft.FontWeight.W_500,
                    color=t.color_text_main,
                ),
                ft.Text(
                    message,
                    size=12,
                    color=t.color_text_sub,
                ),
            ],
            spacing=2,
            expand=True,
        )

        info_row = ft.Row(
            controls=[icon_container, message_col],
            spacing=14,
            vertical_alignment=ft.CrossAxisAlignment.CENTER,
        )

        # ── Ritual button — pill neumorphic ──────────────────────
        r_full = 999.0
        ritual_btn = ft.GestureDetector(
            content=ft.Container(
                content=ft.Row(
                    controls=[
                        ft.Text(
                            ritual_label,
                            size=13,
                            weight=ft.FontWeight.W_500,
                            color=t.color_text_main,
                        ),
                        ft.Icon(ft.Icons.ARROW_FORWARD, color=t.color_text_sub, size=16),
                    ],
                    spacing=6,
                    tight=True,
                ),
                bgcolor=t.color_base,
                border_radius=ft.BorderRadius(r_full, r_full, r_full, r_full),
                padding=ft.Padding(left=14, right=14, top=8, bottom=8),
                shadow=[
                    ft.BoxShadow(
                        offset=ft.Offset(-2, -2),
                        blur_radius=5.0,
                        color=NeuCard._with_opacity(t.shadow_light_opacity, t.color_shadow_light),
                    ),
                    ft.BoxShadow(
                        offset=ft.Offset(2, 2),
                        blur_radius=5.0,
                        color=NeuCard._with_opacity(t.shadow_dark_opacity, t.color_shadow_dark),
                    ),
                ],
            ),
            on_tap=lambda e: on_ritual(),
        )

        card = NeuCard(
            content=ft.Column(
                controls=[
                    ft.Row(
                        controls=[info_row, ritual_btn],
                        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                        vertical_alignment=ft.CrossAxisAlignment.CENTER,
                    ),
                ],
                spacing=0,
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
