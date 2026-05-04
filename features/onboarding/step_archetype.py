# features/onboarding/step_archetype.py — Step 1: user archetype selection.

# --- IMPORTS ---
from __future__ import annotations

from typing import Callable

import flet as ft

from core.design.neu_card import NeuCard
from core.design.tokens import DesignTokens
from core.design.typography import TextStyles, make_text


_ARCHETYPES = {
    "archetype_1": ("sembrador", "🌱"),
    "archetype_2": ("jardinero", "🌿"),
    "archetype_3": ("podador", "✂️"),
}


class StepArchetype(ft.Column):
    def __init__(
        self,
        tokens: DesignTokens,
        on_done: Callable[[], None],
    ) -> None:
        super().__init__(
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            alignment=ft.MainAxisAlignment.CENTER,
            spacing=24,
            expand=True,
        )
        self._tokens = tokens
        self._on_done = on_done
        question = self._copy("onboarding_question_1")

        # ── Progress dots ──────────────────────────────────────────
        r_small = float(tokens.radius_small)
        progress_dots = ft.Row(
            controls=[
                ft.Container(
                    width=24, height=6,
                    bgcolor=tokens.color_primary,
                    border_radius=ft.BorderRadius(r_small, r_small, r_small, r_small),
                ),
                ft.Container(
                    width=6, height=6,
                    bgcolor=tokens.color_text_sub,
                    border_radius=ft.BorderRadius(r_small, r_small, r_small, r_small),
                    opacity=0.3,
                ),
                ft.Container(
                    width=6, height=6,
                    bgcolor=tokens.color_text_sub,
                    border_radius=ft.BorderRadius(r_small, r_small, r_small, r_small),
                    opacity=0.3,
                ),
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            spacing=8,
        )

        cards: list[ft.Control] = [
            self._archetype_card(k, icon) for k, (_, icon) in _ARCHETYPES.items()
        ]

        self.controls = (
            [
                ft.Container(height=20),
                progress_dots,
                ft.Container(height=20),
                make_text(question, TextStyles.heading2),
                ft.Container(height=8)
            ]
            + cards
        )

    def _archetype_card(self, key: str, icon: str) -> ft.Control:
        t = self._tokens
        label = self._copy(key)

        icon_circle = ft.Container(
            content=ft.Text(icon, size=24),
            width=48,
            height=48,
            border_radius=ft.BorderRadius(24, 24, 24, 24),
            bgcolor=t.color_base,
            shadow=[
                ft.BoxShadow(
                    offset=ft.Offset(2, 2),
                    blur_radius=4.0,
                    color=NeuCard._with_opacity(t.shadow_dark_opacity * 0.5, t.color_shadow_dark),
                ),
                ft.BoxShadow(
                    offset=ft.Offset(-2, -2),
                    blur_radius=4.0,
                    color=NeuCard._with_opacity(t.shadow_light_opacity * 0.5, t.color_shadow_light),
                ),
            ],
            alignment=ft.Alignment(0, 0),
        )

        card = NeuCard(
            content=ft.Row(
                controls=[
                    icon_circle,
                    ft.Text(
                        label,
                        size=16,
                        color=t.color_text_main,
                        weight=ft.FontWeight.W_500,
                        expand=True,
                    ),
                    ft.Icon(ft.Icons.ARROW_FORWARD_IOS, size=14, color=t.color_text_sub),
                ],
                spacing=16,
                vertical_alignment=ft.CrossAxisAlignment.CENTER,
            ),
            tokens=t,
            padding=16,
            width=320,
        )

        container = ft.Container(
            content=card,
            animate_scale=ft.Animation(150, ft.AnimationCurve.EASE_OUT),
            scale=1.0,
        )

        def _on_tap_down(e) -> None:
            container.scale = 0.96
            try: container.update()
            except Exception: pass

        def _on_tap_up(e) -> None:
            container.scale = 1.0
            try: container.update()
            except Exception: pass
            self._select(key)

        def _on_tap_cancel(e) -> None:
            container.scale = 1.0
            try: container.update()
            except Exception: pass

        return ft.GestureDetector(
            content=container,
            on_tap_down=_on_tap_down,
            on_tap_up=_on_tap_up,
            on_tap_cancel=_on_tap_cancel,
        )

    def _select(self, key: str) -> None:
        try:
            from core.database.db_helper import DBHelper
            conn = DBHelper.instance().get_connection()
            archetype_val = _ARCHETYPES.get(key, (key, ""))[0]
            conn.execute(
                "INSERT OR REPLACE INTO settings (key,value) VALUES (?,?)",
                ("user_archetype", archetype_val),
            )
            conn.commit()
        except Exception:
            pass
        self._on_done()

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
