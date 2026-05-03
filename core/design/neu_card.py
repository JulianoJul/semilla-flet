# core/design/neu_card.py — NeuCard component factory.

# --- IMPORTS ---
from __future__ import annotations
from dataclasses import field
from typing import Any, Optional

import flet as ft

from core.design.tokens import DesignTokens


# --- COMPONENT ---
@ft.control
class NeuCard(ft.Container):
    """
    Neumorphic card control with visual variants:
      - "default": standard outer neumorphic shadows
      - "pressed": reduced shadows (simulates physical depression, scale 0.98)
      - "well":    very subtle outer shadows (for text field wrappers)
      - "inset":   true inset shadow effect
    """
    tokens: DesignTokens = field(default_factory=DesignTokens.defaults)
    radius_key: str = "standard"
    variant: str = "default"
    inset: bool = False

    @staticmethod
    def _with_opacity(opacity: float, color: str) -> str:
        """Return an #AARRGGBB hex string merging *color* (#RRGGBB) with *opacity* [0-1]."""
        c = color.lstrip("#")
        if len(c) == 3:
            c = "".join(ch * 2 for ch in c)
        aa = format(round(opacity * 255), "02X")
        return f"#{aa}{c.upper()}"

    def init(self) -> None:
        super().init()
        t = self.tokens
        
        radius_map = {
            "small": t.radius_small,
            "standard": t.radius_standard,
            "large": t.radius_large,
            "full": 999,
        }
        r = float(radius_map.get(self.radius_key, t.radius_standard))
        o = t.shadow_offset

        self.bgcolor = t.color_base
        self.border_radius = ft.BorderRadius(r, r, r, r)
        self.clip_behavior = ft.ClipBehavior.NONE

        if self.padding is None:
            self.padding = 16

        # Determine shadow and scale based on variant and inset flag
        if self.inset:
            self.shadow = [
                ft.BoxShadow(
                    offset=ft.Offset(o, o),
                    blur_radius=float(t.shadow_blur // 2),
                    color=self._with_opacity(t.shadow_dark_opacity, t.color_shadow_dark),
                ),
                ft.BoxShadow(
                    offset=ft.Offset(-o, -o),
                    blur_radius=float(t.shadow_blur // 2),
                    color=self._with_opacity(t.shadow_light_opacity, t.color_shadow_light),
                ),
            ]
            self.scale = 1.0
        elif self.variant == "pressed":
            self.shadow = [
                ft.BoxShadow(
                    offset=ft.Offset(-2, -2),
                    blur_radius=4.0,
                    color=self._with_opacity(t.shadow_light_opacity * 0.6, t.color_shadow_light),
                ),
                ft.BoxShadow(
                    offset=ft.Offset(2, 2),
                    blur_radius=4.0,
                    color=self._with_opacity(t.shadow_dark_opacity * 0.6, t.color_shadow_dark),
                ),
            ]
            self.scale = 0.98
        elif self.variant == "well":
            self.shadow = [
                ft.BoxShadow(
                    offset=ft.Offset(-1, -1),
                    blur_radius=3.0,
                    color=self._with_opacity(0.2, t.color_shadow_dark),
                ),
                ft.BoxShadow(
                    offset=ft.Offset(1, 1),
                    blur_radius=3.0,
                    color=self._with_opacity(0.5, t.color_shadow_light),
                ),
            ]
            self.scale = 1.0
        else:  # "default"
            self.shadow = [
                ft.BoxShadow(
                    offset=ft.Offset(-o, -o),
                    blur_radius=float(t.shadow_blur),
                    color=self._with_opacity(t.shadow_light_opacity, t.color_shadow_light),
                ),
                ft.BoxShadow(
                    offset=ft.Offset(o, o),
                    blur_radius=float(t.shadow_blur),
                    color=self._with_opacity(t.shadow_dark_opacity, t.color_shadow_dark),
                ),
            ]
            self.scale = 1.0

# Provide proxy functions strictly to avoid breaking imports
# until all consumers are refactored. We'll delete these later.
def _with_opacity(opacity: float, color: str) -> str:
    return NeuCard._with_opacity(opacity, color)

def neu_card(content: ft.Control, **kwargs: Any) -> ft.Container:
    return NeuCard(content=content, **kwargs)

def neu_card_variant(content: ft.Control, **kwargs: Any) -> ft.Container:
    return NeuCard(content=content, **kwargs)
