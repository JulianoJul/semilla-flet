# features/activity/create_activity_view.py — BottomSheet to create an activity.

from __future__ import annotations
from typing import Any, Callable
import flet as ft
from core.design.colors import COLOR_BASE
from core.design.neu_button import NeuButton
from core.design.neu_card import neu_card
from core.design.tokens import DesignTokens
from core.design.typography import TextStyles, make_text

_TYPES = [
    ("A", "Hábito"),
    ("B", "Horizonte"),
    ("C", "Semilla"),
    ("D", "Hoy"),
]


class CreateActivityView(ft.BottomSheet):
    def __init__(
        self,
        tokens: DesignTokens,
        on_created: Callable[[], Any],
        page: ft.Page,
    ) -> None:
        self._tokens = tokens
        self._on_created = on_created
        self._page = page
        self._selected_type = "A"
        self._error = ft.Text("", color=tokens.color_accent_alert, size=13)

        self._title_field = ft.TextField(
            hint_text=self._copy("activity_name_hint") or "Nombre de tu semilla...",
            hint_style=ft.TextStyle(color=tokens.color_text_sub),
            color=tokens.color_text_main,
            border=ft.InputBorder.NONE,
            text_size=16,
            expand=True,
        )
        self._deadline_field = ft.TextField(
            hint_text="YYYY-MM-DD",
            hint_style=ft.TextStyle(color=tokens.color_text_sub),
            color=tokens.color_text_main,
            border=ft.InputBorder.NONE,
            text_size=14,
            expand=True,
        )
        self._intention_field = ft.TextField(
            hint_text=self._copy("implementation_hint") or "Intención de implementación...",
            hint_style=ft.TextStyle(color=tokens.color_text_sub),
            color=tokens.color_text_main,
            border=ft.InputBorder.NONE,
            text_size=14,
            multiline=True,
            min_lines=2,
            max_lines=3,
            expand=True,
        )
        self._coping_field = ft.TextField(
            hint_text=self._copy("coping_hint") or "Si me resulta difícil, puedo...",
            hint_style=ft.TextStyle(color=tokens.color_text_sub),
            color=tokens.color_text_main,
            border=ft.InputBorder.NONE,
            text_size=14,
            multiline=True,
            min_lines=2,
            max_lines=3,
            expand=True,
        )

        # Deadline card — visible solo para tipo B
        self._deadline_card = neu_card(
            content=ft.Column(
                controls=[
                    ft.Text(
                        "Fecha límite",
                        size=12,
                        color=tokens.color_text_sub,
                        weight=ft.FontWeight.W_500,
                    ),
                    self._deadline_field,
                ],
                spacing=4,
            ),
            tokens=self._tokens,
            inset=True,
            padding=14,
        )
        self._deadline_wrapper = ft.AnimatedSwitcher(
            content=ft.Container(key="empty_deadline"),
            transition=ft.AnimatedSwitcherTransition.FADE,
            duration=200,
        )

        # Type selector
        self._type_chips_row = ft.Row(
            controls=self._build_chips(),
            spacing=8,
            scroll=ft.ScrollMode.AUTO,
        )

        # Confirm button — recreated on type change
        self._confirm_btn = NeuButton(
            label=self._confirm_label(),
            on_click=self._handle_save,
            tokens=self._tokens,
        )
        self._confirm_wrapper = ft.Container(
            content=self._confirm_btn,
            clip_behavior=ft.ClipBehavior.NONE,
        )

        # Main scrollable column
        self._column = ft.Column(
            controls=[
                # Header
                ft.Row(
                    controls=[
                        make_text(
                            self._copy("new_activity_title") or "Plantar nueva semilla",
                            TextStyles.heading2,
                        ),
                        ft.Container(expand=True),
                        ft.IconButton(
                            icon=ft.Icons.CLOSE,
                            icon_color=tokens.color_text_sub,
                            on_click=self._handle_close,
                            icon_size=20,
                        ),
                    ],
                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                ),
                ft.Container(height=4),
                # Type selector
                ft.Text(
                    "Tipo de semilla",
                    size=12,
                    color=tokens.color_text_sub,
                    weight=ft.FontWeight.W_500,
                ),
                self._type_chips_row,
                ft.Container(height=4),
                # Title field
                neu_card(
                    content=ft.Column(
                        controls=[
                            ft.Text(
                                "Nombre",
                                size=12,
                                color=tokens.color_text_sub,
                                weight=ft.FontWeight.W_500,
                            ),
                            self._title_field,
                        ],
                        spacing=4,
                    ),
                    tokens=self._tokens,
                    inset=True,
                    padding=14,
                ),
                # Deadline (animated)
                self._deadline_wrapper,
                # Intention field
                neu_card(
                    content=ft.Column(
                        controls=[
                            ft.Text(
                                "Intención",
                                size=12,
                                color=tokens.color_text_sub,
                                weight=ft.FontWeight.W_500,
                            ),
                            self._intention_field,
                        ],
                        spacing=4,
                    ),
                    tokens=self._tokens,
                    inset=True,
                    padding=14,
                ),
                # Coping field
                neu_card(
                    content=ft.Column(
                        controls=[
                            ft.Text(
                                "Plan de afrontamiento",
                                size=12,
                                color=tokens.color_text_sub,
                                weight=ft.FontWeight.W_500,
                            ),
                            self._coping_field,
                        ],
                        spacing=4,
                    ),
                    tokens=self._tokens,
                    inset=True,
                    padding=14,
                ),
                self._error,
                ft.Container(height=8),
                self._confirm_wrapper,
                ft.Container(height=16),
            ],
            scroll=ft.ScrollMode.AUTO,
            spacing=12,
        )

        r = float(tokens.radius_large)
        # Asegurar que h sea un número (800 por defecto) para evitar TypeError
        h = getattr(self._page, "height", 800) or 800
        super().__init__(
            use_safe_area=True,
            content=ft.Container(
                height=max(500, h * 0.85),
                bgcolor=COLOR_BASE,
                padding=ft.Padding(left=24, right=24, top=20, bottom=0),
                border_radius=ft.BorderRadius(r, r, 0, 0),
                content=ft.SafeArea(
                    content=self._column,
                    bottom=True,
                ),
            ),
        )

    # --- CHIPS ---
    def _build_chips(self) -> list[ft.Control]:
        chips: list[ft.Control] = []
        for code, label in _TYPES:
            selected = code == self._selected_type
            bg = self._tokens.color_primary if selected else self._tokens.color_base
            fg = self._tokens.color_shadow_light if selected else self._tokens.color_text_main
            r = float(self._tokens.radius_small)
            chip = ft.GestureDetector(
                content=ft.Container(
                    content=ft.Text(
                        label,
                        color=fg,
                        size=13,
                        weight=ft.FontWeight.W_500,
                    ),
                    bgcolor=bg,
                    border_radius=ft.BorderRadius(r, r, r, r),
                    padding=ft.Padding(left=14, right=14, top=8, bottom=8),
                    shadow=[
                        ft.BoxShadow(
                            offset=ft.Offset(2, 2),
                            blur_radius=4,
                            color="#33B8BDB9",
                        )
                    ] if selected else None,
                ),
                on_tap=lambda e, c=code: self._select_type(c),
            )
            chips.append(chip)
        return chips

    def _select_type(self, code: str) -> None:
        self._selected_type = code
        self._type_chips_row.controls = self._build_chips()
        if code == "B":
            self._deadline_wrapper.content = self._deadline_card
        else:
            self._deadline_wrapper.content = ft.Container(key="empty_deadline")
        self._confirm_btn = NeuButton(
            label=self._confirm_label(),
            on_click=self._handle_save,
            tokens=self._tokens,
        )
        self._confirm_wrapper.content = self._confirm_btn
        try:
            self._column.update()
        except Exception:
            pass

    def _confirm_label(self) -> str:
        labels = {
            "A": self._copy("confirm_a") or "Plantar hábito",
            "B": self._copy("confirm_b") or "Establecer meta",
            "C": self._copy("confirm_c") or "Guardar semilla",
            "D": self._copy("confirm_d") or "Cultivar hoy",
        }
        return labels.get(self._selected_type, "Guardar")

    # --- ACTIONS ---
    def _handle_close(self, e: object) -> None:
        self.open = False
        try:
            self._page.update()
        except Exception:
            pass

    def _handle_save(self, e: ft.ControlEvent) -> None:
        title = (self._title_field.value or "").strip()
        if not title:
            self._error.value = "El nombre no puede estar vacío"
            try:
                self._column.update()
            except Exception:
                pass
            return
        deadline = (self._deadline_field.value or "").strip() or None
        intention = (self._intention_field.value or "").strip() or None
        coping = (self._coping_field.value or "").strip() or None

        if deadline and self._selected_type == "B":
            import re
            if not re.match(r"^\d{4}-\d{2}-\d{2}$", deadline):
                self._error.value = "Fecha inválida. Usa el formato YYYY-MM-DD"
                try:
                    self._column.update()
                except Exception:
                    pass
                return

        try:
            from core.container import AppContainer
            res = AppContainer.instance().create_activity_uc.execute(
                title=title,
                activity_type=self._selected_type,
                deadline=deadline,
                implementation_intention=intention,
                coping_plan=coping,
            )
            if res.is_failure():
                self._error.value = res.error or "Error"
                try:
                    self._column.update()
                except Exception:
                    pass
                return
        except Exception as exc:
            self._error.value = str(exc)
            try:
                self._column.update()
            except Exception:
                pass
            return

        self.open = False
        try:
            self._page.update()
        except Exception:
            pass
        self._on_created()

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
