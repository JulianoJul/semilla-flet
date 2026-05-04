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
        self._emoji = ft.Text("🏅", size=36)
        self._name = ft.Text("", size=18, weight=ft.FontWeight.BOLD, color=tokens.color_text_main, text_align=ft.TextAlign.CENTER)
        self._description = ft.Text("", size=12, color=tokens.color_text_sub, text_align=ft.TextAlign.CENTER)
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
                tight=True,
            ),
            tokens=tokens,
            radius_key="large",
            padding=16,
            width=200,
        )
        super().__init__(
            content=card,
            bgcolor="#B3000000",
            alignment=ft.Alignment(0, 0),
            left=0,
            top=0,
            right=0,
            bottom=0,
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
