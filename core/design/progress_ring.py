# core/design/progress_ring.py — Neumorphic Progress Ring

# --- IMPORTS ---
from __future__ import annotations
from dataclasses import field

import flet as ft

from core.design.neu_card import NeuCard
from core.design.tokens import DesignTokens


@ft.control
class NeuProgressRing(ft.Stack):
    value: float = 0.0
    ring_size: float = 64.0
    stroke_width: float = 8.0
    tokens: DesignTokens = field(default_factory=DesignTokens.defaults)

    def init(self) -> None:
        super().init()
        self.width = self.ring_size
        self.height = self.ring_size

        t = self.tokens

        # Inset shadow track container
        track = ft.Container(
            width=self.ring_size,
            height=self.ring_size,
            border_radius=ft.BorderRadius(
                self.ring_size / 2,
                self.ring_size / 2,
                self.ring_size / 2,
                self.ring_size / 2,
            ),
            bgcolor=t.color_base,
            border=ft.Border(
                top=ft.BorderSide(self.stroke_width, t.color_base),
                right=ft.BorderSide(self.stroke_width, t.color_base),
                bottom=ft.BorderSide(self.stroke_width, t.color_base),
                left=ft.BorderSide(self.stroke_width, t.color_base),
            ),
            shadow=[
                ft.BoxShadow(
                    offset=ft.Offset(2, 2),
                    blur_radius=4.0,
                    color=NeuCard._with_opacity(t.shadow_dark_opacity * 0.7, t.color_shadow_dark),
                ),
                ft.BoxShadow(
                    offset=ft.Offset(-2, -2),
                    blur_radius=4.0,
                    color=NeuCard._with_opacity(t.shadow_light_opacity * 0.7, t.color_shadow_light),
                ),
            ],
        )

        ring = ft.ProgressRing(
            value=self.value,
            stroke_width=self.stroke_width,
            color=t.color_secondary,
            bgcolor=ft.Colors.TRANSPARENT,
            width=self.ring_size,
            height=self.ring_size,
        )

        self.controls = [track, ring]
