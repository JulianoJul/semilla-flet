# core/design/neu_card.py — NeuCard component factory.

# --- IMPORTS ---
from __future__ import annotations

from typing import Optional

import flet as ft

from core.design.tokens import DesignTokens


# --- FACTORY ---
def neu_card(
    content: ft.Control,
    tokens: Optional[DesignTokens] = None,
    radius_key: str = "standard",
    padding: int = 16,
    width: Optional[int] = None,
    height: Optional[int] = None,
    inset: bool = False,
) -> ft.Container:
    t = tokens or DesignTokens.defaults()
    radius_map = {
        "small": t.radius_small,
        "standard": t.radius_standard,
        "large": t.radius_large,
    }
    r = float(radius_map.get(radius_key, t.radius_standard))
    o = t.shadow_offset

    if inset:
        shadows: list[ft.BoxShadow] = [
            ft.BoxShadow(
                offset=ft.Offset(o, o),
                blur_radius=float(t.shadow_blur // 2),
                color=ft.Colors.with_opacity(
                    t.shadow_dark_opacity, t.color_shadow_dark,
                ),
            ),
            ft.BoxShadow(
                offset=ft.Offset(-o, -o),
                blur_radius=float(t.shadow_blur // 2),
                color=ft.Colors.with_opacity(
                    t.shadow_light_opacity, t.color_shadow_light,
                ),
            ),
        ]
    else:
        shadows = [
            ft.BoxShadow(
                offset=ft.Offset(-o, -o),
                blur_radius=float(t.shadow_blur),
                color=ft.Colors.with_opacity(
                    t.shadow_light_opacity, t.color_shadow_light,
                ),
            ),
            ft.BoxShadow(
                offset=ft.Offset(o, o),
                blur_radius=float(t.shadow_blur),
                color=ft.Colors.with_opacity(
                    t.shadow_dark_opacity, t.color_shadow_dark,
                ),
            ),
        ]

    return ft.Container(
        content=content,
        bgcolor=t.color_base,
        border_radius=ft.BorderRadius(r, r, r, r),
        padding=padding,
        width=width,
        height=height,
        shadow=shadows,
        clip_behavior=ft.ClipBehavior.NONE,
    )
