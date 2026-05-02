# core/design/neu_button.py — NeuButton with pressed/disabled states.

# --- IMPORTS ---
from __future__ import annotations

from typing import Callable, Optional

import flet as ft

from core.design.colors import check_contrast
from core.design.tokens import DesignTokens


# --- COMPONENT ---
class NeuButton(ft.Container):
    def __init__(
        self,
        label: str,
        on_click: Callable[..., None],
        tokens: Optional[DesignTokens] = None,
        variant: str = "primary",
        disabled: bool = False,
    ) -> None:
        t = tokens or DesignTokens.defaults()
        text_color = t.color_shadow_light if variant == "primary" else t.color_text_main
        bg = t.color_primary if variant == "primary" else t.color_base
        check_contrast(text_color, bg)

        r = float(t.radius_standard)
        super().__init__(
            content=ft.Text(
                label,
                color=text_color,
                weight=ft.FontWeight.W_600,
                size=16,
                text_align=ft.TextAlign.CENTER,
            ),
            bgcolor=bg,
            border_radius=ft.BorderRadius(r, r, r, r),
            padding=ft.Padding(left=24, right=24, top=14, bottom=14),
            shadow=self._shadows(t) if not disabled else None,
            opacity=0.4 if disabled else 1.0,
            on_click=None if disabled else lambda e: on_click(e),
        )

    @staticmethod
    def _shadows(t: DesignTokens) -> list[ft.BoxShadow]:
        o = t.shadow_offset
        return [
            ft.BoxShadow(
                offset=ft.Offset(-o, -o),
                blur_radius=float(t.shadow_blur),
                color=ft.colors.with_opacity(
                    t.shadow_light_opacity, t.color_shadow_light,
                ),
            ),
            ft.BoxShadow(
                offset=ft.Offset(o, o),
                blur_radius=float(t.shadow_blur),
                color=ft.colors.with_opacity(
                    t.shadow_dark_opacity, t.color_shadow_dark,
                ),
            ),
        ]
