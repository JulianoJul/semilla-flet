# features/activity/create_activity_view.py — BottomSheet to create an activity.

from __future__ import annotations
from typing import Any, Callable
import flet as ft
from core.design.colors import COLOR_BASE
from core.design.neu_card import NeuCard
from core.design.tokens import DesignTokens
from core.design.typography import TextStyles, make_text

_TYPES = [
    ("A", "Hábito"),
    ("B", "Horizonte"),
    ("C", "Semilla"),
    ("D", "Hoy"),
]


def _handle_bar(tokens: DesignTokens) -> ft.Control:
    """Drag handle bar — centred pill at the top of the sheet."""
    return ft.Container(
        content=ft.Container(
            width=48,
            height=6,
            bgcolor=tokens.color_shadow_dark,
            border_radius=ft.BorderRadius(3, 3, 3, 3),
            opacity=0.5,
        ),
        alignment=ft.Alignment(0, 0),
        padding=ft.Padding(left=0, right=0, top=8, bottom=12),
    )


def _ambient_shadow(tokens: DesignTokens) -> list[ft.BoxShadow]:
    """Soft ambient shadow for primary action buttons (not neumorphic)."""
    colour = NeuCard._with_opacity(tokens.shadow_ambient_opacity, tokens.color_primary)
    return [ft.BoxShadow(offset=ft.Offset(0, 4), blur_radius=10.0, color=colour)]


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
            filled=True,
            fill_color=tokens.color_base,
            border=ft.InputBorder.UNDERLINE,
            text_size=16,
            expand=True,
        )
        from datetime import datetime as _dt
        self._date_picker = ft.DatePicker(
            first_date=_dt.now(),
            on_change=self._handle_date_change,
        )
        self._page.overlay.append(self._date_picker)
        
        self._deadline_value = ""
        self._deadline_text = ft.Text(
            "Seleccionar fecha...",
            color=tokens.color_text_sub,
            size=14,
        )
        self._deadline_field = ft.GestureDetector( # type: ignore
            content=ft.Container(
                content=self._deadline_text,
                padding=ft.Padding(0, 8, 0, 8),
                bgcolor="transparent",
            ),
            on_tap=lambda e: self._open_date_picker(),
            mouse_cursor=ft.MouseCursor.CLICK,
        )
        self._intention_field = ft.TextField(
            hint_text=self._copy("implementation_hint") or "Cuándo y dónde lo harás...",
            hint_style=ft.TextStyle(color=tokens.color_text_sub),
            color=tokens.color_text_main,
            filled=True,
            fill_color=tokens.color_base,
            border=ft.InputBorder.UNDERLINE,
            text_size=14,
            multiline=True,
            min_lines=2,
            max_lines=3,
            expand=True,
        )
        self._coping_field = ft.TextField(
            hint_text=self._copy("coping_hint") or "Si surge un obstáculo, entonces...",
            hint_style=ft.TextStyle(color=tokens.color_text_sub),
            color=tokens.color_text_main,
            filled=True,
            fill_color=tokens.color_base,
            border=ft.InputBorder.UNDERLINE,
            text_size=14,
            multiline=True,
            min_lines=2,
            max_lines=3,
            expand=True,
        )

        from core.design.neu_checkbox import NeuCheckbox
        self._repeating_checkbox = NeuCheckbox(
            checked=False,
            on_change=lambda c: None,
            tokens=tokens,
            box_size=20.0,
        )
        
        repeating_row = ft.GestureDetector(
            content=ft.Row(
                controls=[
                    self._repeating_checkbox,
                    ft.Text("Este horizonte se repite", size=12, color=tokens.color_text_sub),
                ],
                spacing=8,
                vertical_alignment=ft.CrossAxisAlignment.CENTER,
            ),
            on_tap=self._toggle_repeating,
        )

        # Deadline card — visible solo para tipo B
        self._deadline_card = self._field_with_icon(
            field=ft.Column(
                controls=[
                    ft.Text(
                        "Fecha límite",
                        size=12,
                        color=tokens.color_text_sub,
                        weight=ft.FontWeight.W_500,
                    ),
                    self._deadline_field,
                    ft.Container(height=8),
                    repeating_row,
                ],
                spacing=4,
            ),
            icon=ft.Icons.CALENDAR_TODAY,
        )
        self._deadline_card.key = "deadline_active"
        
        self._deadline_container = ft.Container(
            content=self._deadline_card,
            height=0,
            opacity=0,
            animate_size=ft.Animation(400, ft.AnimationCurve.EASE_OUT),
            animate_opacity=ft.Animation(300, ft.AnimationCurve.EASE_IN_OUT),
            clip_behavior=ft.ClipBehavior.ANTI_ALIAS,
        )

        # Type selector
        self._type_chips_row = ft.Row(
            controls=self._build_chips(),
            spacing=8,
            scroll=ft.ScrollMode.AUTO,
        )

        # Primary confirm button (ambient shadow, not neumorphic per DESIGN.md)
        self._confirm_btn = self._primary_button(
            label=self._confirm_label(),
            on_click=self._handle_save,
        )
        self._confirm_wrapper = ft.Container(
            content=self._confirm_btn,
            clip_behavior=ft.ClipBehavior.NONE,
        )

        # Main scrollable column
        self._column = ft.Column(
            controls=[
                _handle_bar(tokens),
                # Header
                ft.Row(
                    controls=[
                        make_text(
                            self._copy("new_activity_title") or "Plantar nueva semilla",
                            TextStyles.heading2,
                        ),
                        ft.Container(expand=True),
                        # Close button — circular neumorphic
                        ft.GestureDetector(
                            content=ft.Container(
                                content=ft.Icon(
                                    ft.Icons.CLOSE,
                                    color=tokens.color_text_sub,
                                    size=18,
                                ),
                                width=40,
                                height=40,
                                border_radius=ft.BorderRadius(20, 20, 20, 20),
                                bgcolor=tokens.color_base,
                                shadow=[
                                    ft.BoxShadow(
                                        offset=ft.Offset(-2, -2),
                                        blur_radius=5.0,
                                        color=NeuCard._with_opacity(tokens.shadow_light_opacity, tokens.color_shadow_light),
                                    ),
                                    ft.BoxShadow(
                                        offset=ft.Offset(2, 2),
                                        blur_radius=5.0,
                                        color=NeuCard._with_opacity(tokens.shadow_dark_opacity, tokens.color_shadow_dark),
                                    ),
                                ],
                                alignment=ft.Alignment(0, 0),
                            ),
                            on_tap=self._handle_close,
                        ),
                    ],
                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                ),
                ft.Container(height=4),
                # Type selector label
                ft.Text(
                    "Tipo de actividad",
                    size=12,
                    color=tokens.color_text_sub,
                    weight=ft.FontWeight.W_500,
                ),
                self._type_chips_row,
                ft.Container(height=4),
                # Title field — well variant with icon
                self._field_with_icon(
                    field=ft.Column(
                        controls=[
                            ft.Text(
                                "Nombre *",
                                size=12,
                                color=tokens.color_text_sub,
                                weight=ft.FontWeight.W_500,
                            ),
                            self._title_field,
                        ],
                        spacing=4,
                    ),
                    icon=ft.Icons.EDIT_OUTLINED,
                ),
                # Deadline (animated)
                self._deadline_container,
                # Intention field
                self._field_with_icon(
                    field=ft.Column(
                        controls=[
                            ft.Text(
                                "Intención de implementación",
                                size=12,
                                color=tokens.color_text_sub,
                                weight=ft.FontWeight.W_500,
                            ),
                            self._intention_field,
                        ],
                        spacing=4,
                    ),
                    icon=ft.Icons.LIGHTBULB_OUTLINE,
                    multiline=True,
                ),
                # Coping field
                self._field_with_icon(
                    field=ft.Column(
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
                    icon=ft.Icons.SHIELD_OUTLINED,
                    multiline=True,
                ),
                self._error,
                ft.Container(height=8),
                # Sticky footer with gradient fade
                ft.Container(
                    content=self._confirm_wrapper,
                    gradient=ft.LinearGradient(
                        begin=ft.Alignment(0, -1),
                        end=ft.Alignment(0, 1),
                        colors=["#00E8EDEA", "#E8EDEA", "#E8EDEA"],
                    ),
                    padding=ft.Padding(left=0, right=0, top=16, bottom=0),
                    clip_behavior=ft.ClipBehavior.NONE,
                ),
                ft.Container(height=16),
            ],
            scroll=ft.ScrollMode.AUTO,
            spacing=12,
        )

        r = float(tokens.radius_large)
        super().__init__(
            scrollable=True,
            content=ft.Container(
                content=self._column,
                padding=ft.Padding(left=24, right=24, top=0, bottom=24),
                bgcolor=tokens.color_base,
                border_radius=ft.BorderRadius(r, r, 0, 0),
            ),
        )

    # --- FIELD WRAPPER ---
    def _field_with_icon(
        self,
        field: ft.Control,
        icon: Any,
        multiline: bool = False,
    ) -> ft.Container:
        t = self._tokens
        return NeuCard(
            content=ft.Row(
                controls=[
                    ft.Icon(icon, color=t.color_text_sub, size=18),
                    field if not isinstance(field, ft.Column) else ft.Container(content=field, expand=True),
                ],
                spacing=10,
                vertical_alignment=ft.CrossAxisAlignment.START if multiline else ft.CrossAxisAlignment.CENTER,
                expand=True,
            ),
            tokens=t,
            variant="well",
            padding=14,
        )

    # --- PRIMARY BUTTON ---
    def _primary_button(self, label: str, on_click: Callable[..., Any]) -> ft.Container:
        t = self._tokens
        r = float(t.radius_standard)
        return ft.Container(
            content=ft.Text(
                label,
                color="#FFFFFF",
                size=16,
                weight=ft.FontWeight.W_600,
                text_align=ft.TextAlign.CENTER,
            ),
            bgcolor=t.color_primary,
            border_radius=ft.BorderRadius(r, r, r, r),
            padding=ft.Padding(left=24, right=24, top=14, bottom=14),
            shadow=_ambient_shadow(t),
            on_click=on_click,
            ink=True,
            animate_scale=ft.Animation(150, ft.AnimationCurve.EASE_OUT),
            expand=True,
        )

    # --- CHIPS ---
    def _build_chips(self) -> list[ft.Control]:
        chips: list[ft.Control] = []
        for code, label in _TYPES:
            selected = code == self._selected_type
            r_full = 999.0
            if selected:
                chip = ft.Container(
                    content=ft.Text(
                        label,
                        color="#FFFFFF",
                        size=13,
                        weight=ft.FontWeight.W_500,
                    ),
                    bgcolor=self._tokens.color_primary,
                    border_radius=ft.BorderRadius(r_full, r_full, r_full, r_full),
                    padding=ft.Padding(left=16, right=16, top=8, bottom=8),
                    shadow=[
                        ft.BoxShadow(
                            offset=ft.Offset(-2, -2),
                            blur_radius=4.0,
                            color=NeuCard._with_opacity(self._tokens.shadow_light_opacity * 0.5, self._tokens.color_shadow_light),
                        ),
                        ft.BoxShadow(
                            offset=ft.Offset(2, 2),
                            blur_radius=4.0,
                            color=NeuCard._with_opacity(self._tokens.shadow_dark_opacity * 0.4, self._tokens.color_shadow_dark),
                        ),
                    ],
                    on_click=lambda e, c=code: self._select_type(c),
                    ink=True,
                )
            else:
                chip = ft.GestureDetector(
                    content=NeuCard(
                        content=ft.Text(
                            label,
                            color=self._tokens.color_text_main,
                            size=13,
                            weight=ft.FontWeight.W_400,
                        ),
                        tokens=self._tokens,
                        radius_key="full",
                        variant="default",
                        padding=ft.Padding(left=16, right=16, top=8, bottom=8),  # type: ignore
                    ),
                    on_tap=lambda e, c=code: self._select_type(c),
                )
            chips.append(chip)
        return chips

    def _select_type(self, code: str) -> None:
        self._selected_type = code
        self._type_chips_row.controls = self._build_chips()
        if code == "B":
            self._deadline_container.height = None
            self._deadline_container.opacity = 1.0
        else:
            self._deadline_container.height = 0
            self._deadline_container.opacity = 0.0
        self._confirm_wrapper.content = self._primary_button(
            label=self._confirm_label(),
            on_click=self._handle_save,
        )
        try:
            self._page.update()
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

    def _open_date_picker(self) -> None:
        self._date_picker.open = True
        try:
            self._page.update()
        except Exception:
            pass

    def _handle_date_change(self, e) -> None:
        if self._date_picker.value:
            date_str = self._date_picker.value.strftime("%Y-%m-%d")
            self._deadline_value = date_str
            self._deadline_text.value = date_str
            self._deadline_text.color = self._tokens.color_text_main
            try:
                self._page.update()
            except Exception:
                pass

    def _toggle_repeating(self, e: ft.TapEvent) -> None:
        self._repeating_checkbox.checked = not self._repeating_checkbox.checked
        self._repeating_checkbox._apply_state()
        try:
            self._repeating_checkbox.update()
        except Exception:
            pass

    def _handle_save(self, e: ft.ControlEvent) -> None:
        title = (self._title_field.value or "").strip()
        if not title:
            self._error.value = "El nombre no puede estar vacío"
            try:
                self._page.update()
            except Exception:
                pass
            return
        deadline = self._deadline_value.strip() or None
        intention = (self._intention_field.value or "").strip() or None
        coping = (self._coping_field.value or "").strip() or None

        if deadline and self._selected_type == "B":
            import re
            if not re.match(r"^\d{4}-\d{2}-\d{2}$", deadline):
                self._error.value = "Fecha inválida. Usa el formato YYYY-MM-DD"
                try:
                    self._page.update()
                except Exception:
                    pass
                return

        is_repeating = False
        if self._selected_type == "B":
            is_repeating = self._repeating_checkbox.checked
        elif self._selected_type == "A":
            is_repeating = True

        from domain.entities.activity import FrequencyConfig
        freq_config = FrequencyConfig(is_repeating=is_repeating) if (is_repeating or self._selected_type == "B") else None

        try:
            from core.container import AppContainer
            res = AppContainer.instance().create_activity_uc.execute(
                title=title,
                activity_type=self._selected_type,
                frequency_config=freq_config,
                deadline=deadline,
                implementation_intention=intention,
                coping_plan=coping,
            )
            if res.is_failure():
                self._error.value = res.error or "Error"
                try:
                    self._page.update()
                except Exception:
                    pass
                return
        except Exception as exc:
            self._error.value = str(exc)
            try:
                self._page.update()
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
