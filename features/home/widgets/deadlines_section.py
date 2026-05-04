# features/home/widgets/deadlines_section.py — Section [B]: deadline activities.

# --- IMPORTS ---
from __future__ import annotations

from datetime import date
from typing import Optional

import flet as ft

from core.design.neu_card import NeuCard
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


def _neu_shadows(t: DesignTokens) -> list[ft.BoxShadow]:
    o = t.shadow_offset
    return [
        ft.BoxShadow(
            offset=ft.Offset(-o, -o),
            blur_radius=float(t.shadow_blur),
            color=NeuCard._with_opacity(t.shadow_light_opacity, t.color_shadow_light),
        ),
        ft.BoxShadow(
            offset=ft.Offset(o, o),
            blur_radius=float(t.shadow_blur),
            color=NeuCard._with_opacity(t.shadow_dark_opacity, t.color_shadow_dark),
        ),
    ]


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
        t = self._tokens
        days = _days_remaining(activity.deadline)
        urgent = days is not None and days <= 3

        if days is None:
            horizon_text = "Sin fecha definida"
            days_display = "?"
        elif days < 0:
            horizon_text = "Horizonte superado"
            days_display = "!"
        elif days == 0:
            horizon_text = "¡Hoy es el día!"
            days_display = "0"
        else:
            horizon_text = f"{prefix} {days} días"
            days_display = str(days)

        text_color = t.color_accent_alert if urgent else t.color_primary
        r = float(t.radius_standard)

        # ── Circular days indicator ──────────────────────────────
        day_circle = ft.Container(
            content=ft.Column(
                controls=[
                    ft.Text(
                        days_display,
                        size=18,
                        weight=ft.FontWeight.BOLD,
                        color=text_color,
                        text_align=ft.TextAlign.CENTER,
                    ),
                    ft.Text(
                        "días",
                        size=10,
                        color=t.color_text_sub,
                        text_align=ft.TextAlign.CENTER,
                    ),
                ],
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                spacing=0,
                tight=True,
            ),
            width=52,
            height=52,
            border_radius=ft.BorderRadius(26, 26, 26, 26),
            bgcolor=t.color_base,
            shadow=[
                ft.BoxShadow(
                    offset=ft.Offset(2, 2),
                    blur_radius=4.0,
                    color=NeuCard._with_opacity(t.shadow_dark_opacity * 0.6, t.color_shadow_dark),
                ),
                ft.BoxShadow(
                    offset=ft.Offset(-2, -2),
                    blur_radius=4.0,
                    color=NeuCard._with_opacity(t.shadow_light_opacity * 0.6, t.color_shadow_light),
                ),
            ],
            alignment=ft.Alignment(0, 0),
        )

        # ── Text column ─────────────────────────────────────────
        info_col = ft.Column(
            controls=[
                ft.Text(
                    activity.title,
                    color=t.color_text_main,
                    size=15,
                    weight=ft.FontWeight.W_500,
                    overflow=ft.TextOverflow.ELLIPSIS,
                ),
                ft.Row(
                    controls=[
                        ft.Icon(ft.Icons.CALENDAR_TODAY, color=t.color_text_sub, size=12),
                        ft.Text(horizon_text, color=t.color_text_sub, size=12),
                    ],
                    spacing=4,
                ),
            ],
            spacing=4,
            expand=True,
        )

        card_content = ft.Row(
            controls=[day_circle, info_col],
            spacing=14,
            vertical_alignment=ft.CrossAxisAlignment.CENTER,
        )

        # ── Base card ────────────────────────────────────────────
        base_card = ft.Container(
            content=card_content,
            bgcolor=t.color_base,
            border_radius=ft.BorderRadius(r, r, r, r),
            padding=ft.Padding(left=20 if urgent else 16, right=16, top=14, bottom=14),
            shadow=_neu_shadows(t),
            clip_behavior=ft.ClipBehavior.NONE,
        )

        if not urgent:
            return base_card

        # ── Urgent: Stack with left accent bar ───────────────────
        accent_bar = ft.Container(
            width=4,
            bgcolor=t.color_accent_alert,
            border_radius=ft.BorderRadius(r, 0, 0, r),
        )

        return ft.Stack(
            controls=[
                # Card with extra left padding for the bar
                base_card,
                # Accent bar pinned to the left
                ft.Container(
                    content=accent_bar,
                    width=4,
                    alignment=ft.Alignment(-1, 0),
                ),
            ],
        )
