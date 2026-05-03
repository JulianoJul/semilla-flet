# core/design/neu_checkbox.py — Neumorphic custom checkbox component.

# --- IMPORTS ---
from __future__ import annotations
from dataclasses import field
from typing import Callable, Optional

import flet as ft

from core.design.neu_card import NeuCard
from core.design.tokens import DesignTokens

# --- COMPONENT ---
@ft.control
class NeuCheckbox(ft.Container):
    checked: bool = False
    on_change: Optional[Callable[[bool], None]] = None
    tokens: DesignTokens = field(default_factory=DesignTokens.defaults)
    box_size: float = 28.0

    def init(self) -> None:
        super().init()
        self.width = self.box_size
        self.height = self.box_size
        self.border_radius = ft.BorderRadius(6, 6, 6, 6)
        self.on_click = self._toggle
        self.ink = True
        self.animate_scale = ft.Animation(150, ft.AnimationCurve.EASE_OUT)
        self._apply_state()

    def _apply_state(self) -> None:
        t = self.tokens
        if self.checked:
            self.bgcolor = t.color_primary
            self.shadow = [
                ft.BoxShadow(
                    offset=ft.Offset(-2, -2),
                    blur_radius=4.0,
                    color=NeuCard._with_opacity(t.shadow_light_opacity * 0.7, t.color_shadow_light),
                ),
                ft.BoxShadow(
                    offset=ft.Offset(2, 2),
                    blur_radius=4.0,
                    color=NeuCard._with_opacity(t.shadow_dark_opacity * 0.6, t.color_shadow_dark),
                ),
            ]
            self.content = ft.Icon(
                ft.Icons.CHECK,
                size=self.box_size * 0.6,
                color="#FFFFFF",
            )
        else:
            self.bgcolor = t.color_base
            self.shadow = [
                ft.BoxShadow(
                    offset=ft.Offset(2, 2),
                    blur_radius=4.0,
                    color=NeuCard._with_opacity(t.shadow_dark_opacity * 0.5, t.color_shadow_dark),
                ),
                ft.BoxShadow(
                    offset=ft.Offset(-2, -2),
                    blur_radius=4.0,
                    color=NeuCard._with_opacity(t.shadow_light_opacity * 0.7, t.color_shadow_light),
                ),
            ]
            self.content = None

    def _toggle(self, e: object) -> None:
        self.checked = not self.checked
        self._apply_state()
        try:
            self.update()
        except Exception:
            pass
        if self.on_change:
            self.on_change(self.checked)

    @property
    def value(self) -> bool:
        return self.checked
