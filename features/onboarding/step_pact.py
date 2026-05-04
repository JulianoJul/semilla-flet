# features/onboarding/step_pact.py — Step 3: self-compassion pact.

# --- IMPORTS ---
from __future__ import annotations

from typing import Callable

import flet as ft

from core.design.neu_card import NeuCard
from core.design.neu_checkbox import NeuCheckbox
from core.design.tokens import DesignTokens
from core.design.typography import TextStyles, make_text


def _ambient_shadow(tokens: DesignTokens) -> list[ft.BoxShadow]:
    colour = NeuCard._with_opacity(tokens.shadow_ambient_opacity, tokens.color_primary)
    return [ft.BoxShadow(offset=ft.Offset(0, 4), blur_radius=10.0, color=colour)]


def _disabled_shadow(tokens: DesignTokens) -> list[ft.BoxShadow]:
    t = tokens
    return [
        ft.BoxShadow(
            offset=ft.Offset(1, 1),
            blur_radius=3.0,
            color=NeuCard._with_opacity(t.shadow_dark_opacity * 0.4, t.color_shadow_dark),
        ),
        ft.BoxShadow(
            offset=ft.Offset(-1, -1),
            blur_radius=3.0,
            color=NeuCard._with_opacity(t.shadow_light_opacity * 0.4, t.color_shadow_light),
        ),
    ]


class StepPact(ft.Column):
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
        self._accepted = False
        t = tokens

        # ── Progress dots ──────────────────────────────────────────
        r_small = float(tokens.radius_small)
        progress_dots = ft.Row(
            controls=[
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
                ft.Container(
                    width=24, height=6,
                    bgcolor=tokens.color_primary,
                    border_radius=ft.BorderRadius(r_small, r_small, r_small, r_small),
                ),
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            spacing=8,
        )

        self._checkbox = NeuCheckbox(
            checked=False,
            on_change=self._handle_check,
            tokens=tokens,
            box_size=28.0,
        )

        pact_row = ft.Row(
            controls=[
                self._checkbox,
                ft.Text(
                    self._copy("pact_text"),
                    color=tokens.color_text_main,
                    size=14,
                    expand=True,
                ),
            ],
            vertical_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=16,
        )

        self._btn_container = ft.Container(width=320)
        self._rebuild_btn(disabled=True)

        controls: list[ft.Control] = [
            ft.Container(height=20),
            progress_dots,
            ft.Container(height=20),
            make_text(self._copy("pact_title"), TextStyles.heading2),
            ft.Container(height=8),
            NeuCard(content=pact_row, tokens=tokens, padding=20, width=320),
            self._btn_container,
        ]
        self.controls = controls

    def _rebuild_btn(self, disabled: bool) -> None:
        t = self._tokens
        r = float(t.radius_standard)
        
        self._btn_container.content = ft.Container(
            content=ft.Text(
                self._copy("confirm_pact"),
                color="#FFFFFF" if not disabled else t.color_text_sub,
                size=16,
                weight=ft.FontWeight.W_600,
                text_align=ft.TextAlign.CENTER,
            ),
            bgcolor=t.color_primary if not disabled else t.color_base,
            border_radius=ft.BorderRadius(r, r, r, r),
            padding=ft.Padding(left=24, right=24, top=14, bottom=14),
            shadow=_ambient_shadow(t) if not disabled else _disabled_shadow(t),
            opacity=1.0 if not disabled else 0.6,
            on_click=self._handle_confirm if not disabled else None,
            ink=not disabled,
            animate_scale=ft.Animation(150, ft.AnimationCurve.EASE_OUT),
            width=320,
        )

    def _handle_check(self, checked: bool) -> None:
        self._accepted = checked
        self._rebuild_btn(disabled=not self._accepted)
        try: self._btn_container.update()
        except Exception: pass

    def _handle_confirm(self, e) -> None:
        if not self._accepted:
            return
        try:
            from core.database.db_helper import DBHelper
            conn = DBHelper.instance().get_connection()
            for key in ("compassion_pact_accepted", "onboarding_complete"):
                conn.execute(
                    "INSERT OR REPLACE INTO settings (key,value) VALUES (?,?)",
                    (key, "1"),
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
