# core/design/neu_button.py — NeuButton component.

# --- IMPORTS ---
from __future__ import annotations
from dataclasses import field

import flet as ft

from core.design.colors import check_contrast
from core.design.neu_card import NeuCard
from core.design.tokens import DesignTokens


# --- COMPONENT ---
@ft.control
class NeuButton(ft.Container):
    label: str = ""
    variant: str = "primary"
    disabled_state: bool = False
    tokens: DesignTokens = field(default_factory=DesignTokens.defaults)

    def init(self) -> None:
        super().init()
        t = self.tokens
        text_color = t.color_shadow_light if self.variant == "primary" else t.color_text_main
        bg = t.color_primary if self.variant == "primary" else t.color_base
        check_contrast(text_color, bg)

        r = float(t.radius_standard)
        
        self.content = ft.Text(
            self.label,
            color=text_color,
            weight=ft.FontWeight.W_600,
            size=16,
            text_align=ft.TextAlign.CENTER,
        )
        self.bgcolor = bg
        self.border_radius = ft.BorderRadius(r, r, r, r)
        self.padding = ft.Padding(left=24, right=24, top=14, bottom=14)
        
        if not self.disabled_state:
            o = t.shadow_offset
            self.shadow = [
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
            self.opacity = 1.0
            self.ink = True
        else:
            self.shadow = None
            self.opacity = 0.4
            self.on_click = None
            self.ink = False
            
        self.clip_behavior = ft.ClipBehavior.NONE
