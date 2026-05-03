# features/activity/activity_detail_view.py — Detail/edit sheet for an activity.

from __future__ import annotations

from typing import Callable, Any

import flet as ft

from core.design.colors import COLOR_BASE
from core.design.neu_card import NeuCard
from core.design.tokens import DesignTokens
from core.design.typography import TextStyles, make_text
from domain.entities.activity import Activity


def _handle_bar(tokens: DesignTokens) -> ft.Control:
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
    colour = NeuCard._with_opacity(tokens.shadow_ambient_opacity, tokens.color_primary)
    return [ft.BoxShadow(offset=ft.Offset(0, 4), blur_radius=10.0, color=colour)]


_DAYS = ["L", "M", "M", "J", "V", "S", "D"]


class ActivityDetailView(ft.BottomSheet):
    """
    Bottom sheet con el detalle completo de un hábito/actividad.
    """

    def __init__(
        self,
        activity: Activity,
        tokens: DesignTokens,
        page: ft.Page,
        on_complete: Callable[[Activity], None],
        on_archived: Callable[[], Any],
        on_dismiss: Callable[[], Any],
    ) -> None:
        self._activity = activity
        self._tokens = tokens
        self._page = page
        self._on_complete = on_complete
        self._on_archived = on_archived
        self._on_dismiss = on_dismiss

        t = tokens
        r = float(t.radius_large)

        streak = self._load_streak()
        checkins = self._load_checkins()

        # ── HANDLE ──────────────────────────────────────────────
        handle = _handle_bar(t)

        # ── HEADER ──────────────────────────────────────────────
        header = ft.Row(
            controls=[
                ft.Container(width=40),  # Spacer
                ft.Column(
                    controls=[
                        ft.Text(
                            activity.title,
                            size=20,
                            weight=ft.FontWeight.BOLD,
                            color=t.color_text_main,
                            text_align=ft.TextAlign.CENTER,
                        ),
                        ft.Text(
                            self._type_label(activity.type.value),
                            size=12,
                            color=t.color_text_sub,
                            text_align=ft.TextAlign.CENTER,
                        ),
                    ],
                    spacing=2,
                    expand=True,
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                ),
                # Close button — circular neumorphic
                ft.GestureDetector(
                    content=ft.Container(
                        content=ft.Icon(ft.Icons.CLOSE, color=t.color_text_sub, size=18),
                        width=40,
                        height=40,
                        border_radius=ft.BorderRadius(20, 20, 20, 20),
                        bgcolor=t.color_base,
                        shadow=[
                            ft.BoxShadow(
                                offset=ft.Offset(-2, -2),
                                blur_radius=5.0,
                                color=NeuCard._with_opacity(t.shadow_light_opacity, t.color_shadow_light),
                            ),
                            ft.BoxShadow(
                                offset=ft.Offset(2, 2),
                                blur_radius=5.0,
                                color=NeuCard._with_opacity(t.shadow_dark_opacity, t.color_shadow_dark),
                            ),
                        ],
                        alignment=ft.Alignment(0, 0),
                    ),
                    on_tap=self._handle_close,
                ),
            ],
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
            vertical_alignment=ft.CrossAxisAlignment.CENTER,
        )

        # ── HERO ICON ───────────────────────────────────────────
        hero_icon = ft.Container(
            content=ft.Text(
                self._type_emoji(activity.type.value),
                size=44,
                text_align=ft.TextAlign.CENTER,
            ),
            width=96,
            height=96,
            border_radius=ft.BorderRadius(48, 48, 48, 48),
            bgcolor=t.color_base,
            shadow=[
                ft.BoxShadow(
                    offset=ft.Offset(3, 3),
                    blur_radius=6.0,
                    color=NeuCard._with_opacity(t.shadow_dark_opacity * 0.6, t.color_shadow_dark),
                ),
                ft.BoxShadow(
                    offset=ft.Offset(-3, -3),
                    blur_radius=6.0,
                    color=NeuCard._with_opacity(t.shadow_light_opacity * 0.6, t.color_shadow_light),
                ),
            ],
            alignment=ft.Alignment(0, 0),
        )

        hero_row = ft.Row(
            controls=[hero_icon],
            alignment=ft.MainAxisAlignment.CENTER,
        )

        # ── STREAK STATS ────────────────────────────────────────
        stats_card = NeuCard(
            content=ft.Row(
                controls=[
                    self._stat_col("🔥", str(streak["current"]), "Racha"),
                    ft.VerticalDivider(
                        color=t.color_shadow_dark + "30",
                        width=1,
                    ),
                    self._stat_col("🏆", str(streak["best"]), "Mejor"),
                    ft.VerticalDivider(
                        color=t.color_shadow_dark + "30",
                        width=1,
                    ),
                    self._stat_col("✅", str(streak["total"]), "Total"),
                    ft.VerticalDivider(
                        color=t.color_shadow_dark + "30",
                        width=1,
                    ),
                    self._stat_col("⬡", str(streak["shields"]), "Escudos"),
                ],
                alignment=ft.MainAxisAlignment.SPACE_AROUND,
            ),
            tokens=t,
            padding=16,
            radius_key="standard",
        )

        # ── WEEKLY PROGRESS ─────────────────────────────────────
        weekly_rate = streak["weekly_rate"]
        completed_days = round(weekly_rate * 7)

        day_indicators = ft.Row(
            controls=[
                ft.Container(
                    content=ft.Text(
                        day,
                        size=10,
                        color="#FFFFFF" if idx < completed_days else t.color_text_sub,
                        text_align=ft.TextAlign.CENTER,
                        weight=ft.FontWeight.W_500,
                    ),
                    width=24,
                    height=24,
                    border_radius=ft.BorderRadius(12, 12, 12, 12),
                    bgcolor=t.color_secondary if idx < completed_days else t.color_base,
                    shadow=[
                        ft.BoxShadow(
                            offset=ft.Offset(1, 1),
                            blur_radius=3.0,
                            color=NeuCard._with_opacity(0.3, t.color_shadow_dark),
                        ),
                    ] if idx < completed_days else [
                        ft.BoxShadow(
                            offset=ft.Offset(1, 1),
                            blur_radius=2.0,
                            color=NeuCard._with_opacity(t.shadow_dark_opacity * 0.4, t.color_shadow_dark),
                        ),
                        ft.BoxShadow(
                            offset=ft.Offset(-1, -1),
                            blur_radius=2.0,
                            color=NeuCard._with_opacity(t.shadow_light_opacity * 0.4, t.color_shadow_light),
                        ),
                    ],
                    alignment=ft.Alignment(0, 0),
                )
                for idx, day in enumerate(_DAYS)
            ],
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
        )

        weekly_card = NeuCard(
            content=ft.Column(
                controls=[
                    ft.Row(
                        controls=[
                            ft.Column(
                                controls=[
                                    ft.Text(
                                        "Progreso semanal",
                                        size=13,
                                        color=t.color_text_sub,
                                        weight=ft.FontWeight.W_500,
                                    ),
                                    ft.Text(
                                        f"{completed_days} de 7 días completados",
                                        size=12,
                                        color=t.color_text_sub,
                                    ),
                                ],
                                spacing=2,
                                expand=True,
                            ),
                            ft.Text(
                                f"{int(weekly_rate * 100)}%",
                                size=20,
                                weight=ft.FontWeight.BOLD,
                                color=t.color_primary,
                            ),
                        ],
                    ),
                    ft.ProgressBar(
                        value=weekly_rate,
                        color=t.color_secondary,
                        bgcolor=t.color_shadow_dark + "44",
                        height=8,
                        border_radius=ft.BorderRadius(4, 4, 4, 4),
                    ),
                    day_indicators,
                ],
                spacing=12,
            ),
            tokens=t,
            padding=20,
        )

        # ── IMPLEMENTATION INTENTION ────────────────────────────
        intention_controls: list[ft.Control] = []
        if activity.implementation_intention:
            intention_controls.append(
                NeuCard(
                    content=ft.Column(
                        controls=[
                            ft.Text(
                                "🎯 Intención",
                                size=12,
                                color=t.color_text_sub,
                                weight=ft.FontWeight.W_500,
                            ),
                            ft.Text(
                                activity.implementation_intention,
                                size=15,
                                color=t.color_text_main,
                            ),
                        ],
                        spacing=6,
                    ),
                    tokens=t,
                    padding=16,
                )
            )
        if activity.coping_plan:
            intention_controls.append(
                NeuCard(
                    content=ft.Column(
                        controls=[
                            ft.Text(
                                "🛡️ Plan de afrontamiento",
                                size=12,
                                color=t.color_text_sub,
                                weight=ft.FontWeight.W_500,
                            ),
                            ft.Text(
                                activity.coping_plan,
                                size=15,
                                color=t.color_text_main,
                            ),
                        ],
                        spacing=6,
                    ),
                    tokens=t,
                    padding=16,
                )
            )

        # ── DEADLINE ────────────────────────────────────────────
        deadline_controls: list[ft.Control] = []
        if activity.deadline:
            from datetime import date as _date
            try:
                days = (_date.fromisoformat(activity.deadline[:10]) - _date.today()).days
                if days < 0:
                    dl_text = "Horizonte superado"
                    dl_color = t.color_accent_alert
                elif days == 0:
                    dl_text = "¡Hoy es el día!"
                    dl_color = t.color_accent_alert
                else:
                    dl_text = f"Horizonte en {days} días ({activity.deadline[:10]})"
                    dl_color = t.color_text_sub
            except ValueError:
                dl_text = activity.deadline
                dl_color = t.color_text_sub

            deadline_controls.append(
                ft.Row(
                    controls=[
                        ft.Icon(ft.Icons.CALENDAR_TODAY, color=dl_color, size=14),
                        ft.Text(dl_text, size=13, color=dl_color),
                    ],
                    spacing=6,
                )
            )

        # ── RECENT CHECK-INS ────────────────────────────────────
        checkin_controls: list[ft.Control] = []
        if checkins:
            checkin_controls.append(
                ft.Text(
                    "Últimos registros",
                    size=13,
                    color=t.color_text_sub,
                    weight=ft.FontWeight.W_500,
                )
            )
            for ci in checkins[:5]:
                date_str = ci[:10] if len(ci) >= 10 else ci
                time_str = ci[11:16] if len(ci) >= 16 else ""
                checkin_controls.append(
                    ft.Row(
                        controls=[
                            ft.Icon(
                                ft.Icons.CHECK_CIRCLE,
                                color=t.color_secondary,
                                size=14,
                            ),
                            ft.Text(
                                f"{date_str}  {time_str}",
                                size=13,
                                color=t.color_text_main,
                            ),
                        ],
                        spacing=6,
                    )
                )

        # ── ACTION BUTTONS (sticky footer with gradient) ─────────
        already_done_today = self._completed_today()
        r_std = float(t.radius_standard)

        # Primary complete button — ambient shadow (not neumorphic per DESIGN.md)
        complete_btn = ft.Container(
            content=ft.Row(
                controls=[
                    ft.Icon(ft.Icons.CHECK_CIRCLE_OUTLINE, color="#FFFFFF", size=20),
                    ft.Text(
                        "Ya completada hoy" if already_done_today else "Marcar como completada",
                        color="#FFFFFF",
                        size=15,
                        weight=ft.FontWeight.W_600,
                    ),
                ],
                alignment=ft.MainAxisAlignment.CENTER,
                spacing=8,
            ),
            bgcolor=t.color_primary,
            border_radius=ft.BorderRadius(r_std, r_std, r_std, r_std),
            padding=ft.Padding(left=24, right=24, top=14, bottom=14),
            shadow=_ambient_shadow(t) if not already_done_today else None,
            opacity=0.5 if already_done_today else 1.0,
            on_click=None if already_done_today else self._handle_complete,
            ink=not already_done_today,
        )

        archive_btn = ft.Container(
            content=ft.Text(
                "Archivar semilla",
                color=t.color_accent_alert,
                size=14,
                text_align=ft.TextAlign.CENTER,
            ),
            alignment=ft.Alignment(0, 0),
            padding=ft.Padding(left=0, right=0, top=8, bottom=0),
            on_click=self._handle_archive,
            ink=True,
        )

        footer = ft.Container(
            content=ft.Column(
                controls=[complete_btn, archive_btn],
                spacing=4,
            ),
            gradient=ft.LinearGradient(
                begin=ft.Alignment(0, -1),
                end=ft.Alignment(0, 1),
                colors=["#00E8EDEA", "#E8EDEA", "#E8EDEA"],
            ),
            padding=ft.Padding(left=0, right=0, top=16, bottom=0),
        )

        # ── LAYOUT ──────────────────────────────────────────────
        sections: list[ft.Control] = [
            handle,
            header,
            hero_row,
            stats_card,
            weekly_card,
            *deadline_controls,
            *intention_controls,
            *([NeuCard(
                content=ft.Column(controls=checkin_controls, spacing=8),
                tokens=t,
                padding=16,
            )] if checkin_controls else []),
            ft.Container(height=4),
            footer,
            ft.Container(height=16),
        ]

        h = getattr(self._page, "height", 800) or 800
        content = ft.Container(
            height=max(500, h * 0.85),
            bgcolor=COLOR_BASE,
            padding=ft.Padding(left=24, right=24, top=0, bottom=0),
            border_radius=ft.BorderRadius(r, r, 0, 0),
            content=ft.SafeArea(
                content=ft.Column(
                    controls=sections,
                    scroll=ft.ScrollMode.AUTO,
                    spacing=14,
                ),
                bottom=True,
            ),
        )

        super().__init__(
            use_safe_area=True,
            content=content,
            on_dismiss=lambda e: on_dismiss(),
        )

    # ── HELPERS ─────────────────────────────────────────────────

    def _stat_col(self, emoji: str, value: str, label: str) -> ft.Control:
        return ft.Column(
            controls=[
                ft.Text(emoji, size=20, text_align=ft.TextAlign.CENTER),
                ft.Text(
                    value,
                    size=18,
                    weight=ft.FontWeight.BOLD,
                    color=self._tokens.color_primary,
                    text_align=ft.TextAlign.CENTER,
                ),
                ft.Text(
                    label,
                    size=11,
                    color=self._tokens.color_text_sub,
                    text_align=ft.TextAlign.CENTER,
                ),
            ],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=2,
            expand=True,
        )

    @staticmethod
    def _type_emoji(type_value: str) -> str:
        return {"A": "🌱", "B": "🎯", "C": "💤", "D": "⭐"}.get(type_value, "🌿")

    def _handle_close(self, e: object) -> None:
        self.open = False
        try:
            self._page.update()
        except Exception:
            pass
        self._on_dismiss()

    def _handle_complete(self, e: object) -> None:
        self.open = False
        try:
            self._page.update()
        except Exception:
            pass
        self._on_complete(self._activity)

    def _handle_archive(self, e: object) -> None:
        try:
            from core.container import AppContainer
            AppContainer.instance().activity_repo.archive_activity(
                self._activity.id or 0
            )
        except Exception:
            pass
        self.open = False
        try:
            self._page.update()
        except Exception:
            pass
        self._on_archived()

    def _completed_today(self) -> bool:
        try:
            from datetime import date
            from core.database.db_helper import DBHelper
            today = date.today().isoformat()
            row = DBHelper.instance().get_connection().execute(
                "SELECT COUNT(*) as c FROM checkins "
                "WHERE activity_id=? AND DATE(completed_at)=?",
                (self._activity.id or 0, today),
            ).fetchone()
            return int(row["c"]) > 0
        except Exception:
            return False

    def _load_streak(self) -> dict:
        try:
            from core.database.db_helper import DBHelper
            row = DBHelper.instance().get_connection().execute(
                "SELECT current_count, best_count, total_completions, "
                "shields_available, weekly_completion_rate "
                "FROM streaks WHERE activity_id=?",
                (self._activity.id or 0,),
            ).fetchone()
            if row:
                return {
                    "current": row["current_count"],
                    "best": row["best_count"],
                    "total": row["total_completions"],
                    "shields": row["shields_available"],
                    "weekly_rate": float(row["weekly_completion_rate"] or 0),
                }
        except Exception:
            pass
        return {"current": 0, "best": 0, "total": 0, "shields": 1, "weekly_rate": 0.0}

    def _load_checkins(self) -> list[str]:
        try:
            from core.database.db_helper import DBHelper
            rows = DBHelper.instance().get_connection().execute(
                "SELECT completed_at FROM checkins "
                "WHERE activity_id=? ORDER BY completed_at DESC LIMIT 10",
                (self._activity.id or 0,),
            ).fetchall()
            return [r["completed_at"] for r in rows]
        except Exception:
            return []

    @staticmethod
    def _type_label(type_value: str) -> str:
        return {
            "A": "🌱 Hábito diario",
            "B": "🎯 Horizonte",
            "C": "💤 Semilla en espera",
            "D": "⭐ Enfoque de hoy",
        }.get(type_value, "Actividad")
