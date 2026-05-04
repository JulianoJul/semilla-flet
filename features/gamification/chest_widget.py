# features/gamification/chest_widget.py — Animated chest drop dialog.

# --- IMPORTS ---
from __future__ import annotations

from typing import Any, Callable, Optional

import flet as ft

from core.design.neu_button import NeuButton
from core.design.neu_card import NeuCard
from core.design.tokens import DesignTokens
from core.design.typography import TextStyles, make_text


class ChestWidget(ft.AlertDialog):
    """Modal shown when gamification triggers a chest drop."""

    def __init__(
        self,
        tokens: DesignTokens,
        on_open: Callable[[], Any],
        page: ft.Page,
    ) -> None:
        self._tokens = tokens
        self._page = page
        self._reward_text = ft.Text("", size=15, color=tokens.color_text_main)
        self._chest_icon = ft.Container(
            content=ft.Text("🪴", size=64),
            animate_scale=ft.Animation(800, ft.AnimationCurve.ELASTIC_OUT),  # type: ignore
            scale=0.8,
            alignment=ft.Alignment(0, 0),
            height=85,
        )
        super().__init__(
            modal=True,
            title=make_text(self._copy("chest_title"), TextStyles.heading2),
            content=ft.Column(
                controls=[
                    self._chest_icon,
                    ft.Container(height=8),
                    self._reward_text,
                ],
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                spacing=4,
                tight=True,
            ),
            actions=[
                NeuButton(
                    label=self._copy("chest_open_label"),
                    on_click=lambda e: self._open_chest(on_open),
                    tokens=tokens,
                ),
            ],
            bgcolor=tokens.color_base,
        )

    def _open_chest(self, callback: Callable[[], Any]) -> None:
        self.actions = []
        self._chest_icon.scale = 1.2
        try:
            self._chest_icon.update()
            self.update()
        except Exception:
            pass
        async def animate() -> None:
            import asyncio
            await asyncio.sleep(0.4)
            self._chest_icon.content = ft.Text("🌟", size=64)
            self._chest_icon.scale = 1.0
            reward = self._pick_reward()
            self._reward_text.value = reward
            try:
                self._chest_icon.update()
                self._reward_text.update()
            except Exception: pass
            await asyncio.sleep(1.0)
            self.open = False
            try: self._page.update()
            except Exception: pass
            callback()
        self._page.run_task(animate)

    @staticmethod
    def _pick_reward() -> str:
        try:
            from core.database.db_helper import DBHelper
            conn = DBHelper.instance().get_connection()
            row = conn.execute(
                "SELECT value FROM ui_copy WHERE key LIKE 'chest_reward%' "
                "ORDER BY RANDOM() LIMIT 1",
            ).fetchone()
            return row["value"] if row else "¡Un pequeño regalo para ti! 🌱"
        except Exception:
            return "¡Un pequeño regalo para ti! 🌱"

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
