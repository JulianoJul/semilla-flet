# features/onboarding/step_first_seed.py — Step 2: create first habit.

# --- IMPORTS ---
from __future__ import annotations

from typing import Callable

import flet as ft

from core.design.neu_card import NeuCard
from core.design.tokens import DesignTokens
from core.design.typography import TextStyles, make_text


def _ambient_shadow(tokens: DesignTokens) -> list[ft.BoxShadow]:
    colour = NeuCard._with_opacity(tokens.shadow_ambient_opacity, tokens.color_primary)
    return [ft.BoxShadow(offset=ft.Offset(0, 4), blur_radius=10.0, color=colour)]


class StepFirstSeed(ft.Column):
    def __init__(
        self,
        tokens: DesignTokens,
        on_done: Callable[[], None],
        page: ft.Page,
    ) -> None:
        super().__init__(
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            alignment=ft.MainAxisAlignment.CENTER,
            spacing=24,
            expand=True,
        )
        self._tokens = tokens
        self._on_done = on_done
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
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            spacing=8,
        )

        self._field = ft.TextField(
            hint_text=self._copy("first_seed_hint"),
            hint_style=ft.TextStyle(color=t.color_text_sub),
            color=t.color_text_main,
            border=ft.InputBorder.NONE,
            text_size=16,
            multiline=False,
            expand=True,
        )

        field_wrapper = NeuCard(
            content=ft.Row(
                controls=[
                    ft.Icon(ft.Icons.EDIT_OUTLINED, color=t.color_text_sub, size=18),
                    self._field,
                ],
                spacing=10,
                vertical_alignment=ft.CrossAxisAlignment.CENTER,
            ),
            tokens=t,
            variant="well",
            padding=16,
            width=320,
        )

        self._error = ft.Text("", color=t.color_accent_alert, size=13)

        r_std = float(t.radius_standard)
        confirm_btn = ft.Container(
            content=ft.Text(
                self._copy("confirm_habit"),
                color="#FFFFFF",
                size=16,
                weight=ft.FontWeight.W_600,
                text_align=ft.TextAlign.CENTER,
            ),
            bgcolor=t.color_primary,
            border_radius=ft.BorderRadius(r_std, r_std, r_std, r_std),
            padding=ft.Padding(left=24, right=24, top=14, bottom=14),
            shadow=_ambient_shadow(t),
            on_click=self._handle_confirm,
            ink=True,
            width=320,
        )

        self.controls = [
            ft.Container(height=20),
            progress_dots,
            ft.Container(height=20),
            make_text(self._copy("first_seed_title"), TextStyles.heading2),
            ft.Container(height=8),
            field_wrapper,
            self._error,
            confirm_btn,
        ]

    def _handle_confirm(self, e) -> None:
        title = (self._field.value or "").strip()
        if not title:
            self._error.value = "Escribe el nombre de tu hábito"
            try: self._error.update()
            except Exception: pass
            return
        try:
            from core.container import AppContainer
            result = AppContainer.instance().create_activity_uc.execute(
                title=title, activity_type="A",
            )
            if result.is_failure():
                self._error.value = result.error or "Error desconocido"
                try: self._error.update()
                except Exception: pass
                return
        except Exception as exc:
            self._error.value = str(exc)
            try: self._error.update()
            except Exception: pass
            return
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
