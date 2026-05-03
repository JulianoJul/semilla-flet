# features/gamification/badge_celebration.py — Badge unlock overlay.

# --- IMPORTS ---
from __future__ import annotations

from typing import Optional

import flet as ft

from core.design.neu_card import NeuCard
from core.design.tokens import DesignTokens
from core.design.typography import TextStyles, make_text
from domain.entities.badge_entity import BadgeEntity


class BadgeCelebration(ft.Container):
    """
    Full-overlay celebration shown when a badge is unlocked.
    Add to page.overlay and set visible=True to trigger.
    """

    def __init__(
        self,
        tokens: DesignTokens,
        page: ft.Page,
    ) -> None:
        self._tokens = tokens
        self._page = page
        self._emoji = ft.Text("🏅", size=64)
        self._name = make_text("", TextStyles.heading2)
        self._description = make_text("", TextStyles.body)
        card = NeuCard(
            content=ft.Column(
                controls=[
                    ft.Container(
                        content=self._emoji,
                        alignment=ft.Alignment(0, 0),
                    ),
                    ft.Container(height=12),
                    self._name,
                    ft.Container(height=4),
                    self._description,
                ],
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                spacing=0,
            ),
            tokens=tokens,
            radius_key="large",
            padding=32,
            width=280,
        )
        super().__init__(
            content=card,
            bgcolor="#B3000000",  # ~70% opaque black (#AARRGGBB)
            alignment=ft.Alignment(0, 0),
            expand=True,
            visible=False,
            animate_opacity=300,
            opacity=0.0,
        )

    def show(self, badge: BadgeEntity) -> None:
        self._emoji.value = badge.emoji_placeholder or "🏅"
        self._name.value = badge.name
        self._description.value = badge.description or ""
        self.visible = True
        self.opacity = 1.0
        try:
            self._emoji.update()
            self._name.update()
            self._description.update()
            self.update()
        except Exception:
            pass
        async def hide() -> None:
            import asyncio
            await asyncio.sleep(3.0)
            self.opacity = 0.0
            try: self.update()
            except Exception: pass
            await asyncio.sleep(0.4)
            self.visible = False
            try: self.update()
            except Exception: pass
            page = self._page
            if page is None:
                return
            if self in page.overlay:
                page.overlay.remove(self)
                try: page.update()
                except Exception: pass
        self._page.run_task(hide)
