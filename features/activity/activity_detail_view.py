# features/activity/activity_detail_view.py — Detail/edit sheet for an activity.

from __future__ import annotations

from typing import Callable, Any

import flet as ft

from core.design.colors import COLOR_BASE
from core.design.neu_button import NeuButton
from core.design.neu_card import neu_card
from core.design.tokens import DesignTokens
from core.design.typography import TextStyles, make_text
from domain.entities.activity import Activity


class ActivityDetailView(ft.BottomSheet):
    """
    Bottom sheet con el detalle completo de un hábito/actividad.
    Muestra: título, estadísticas de racha, historial de check-ins,
    intención de implementación, plan de afrontamiento, y botones
    de acción (completar hoy / archivar).
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

        # ── HEADER ──────────────────────────────────────────────
        header = ft.Row(
            controls=[
                ft.Column(
                    controls=[
                        ft.Text(
                            activity.title,
                            size=22,
                            weight=ft.FontWeight.BOLD,
                            color=t.color_text_main,
                        ),
                        ft.Text(
                            self._type_label(activity.type.value),
                            size=13,
                            color=t.color_text_sub,
                        ),
                    ],
                    spacing=2,
                    expand=True,
                ),
                ft.IconButton(
                    icon=ft.Icons.CLOSE,
                    icon_color=t.color_text_sub,
                    on_click=self._handle_close,
                    icon_size=20,
                ),
            ],
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
        )

        # ── STREAK STATS ────────────────────────────────────────
        stats_card = neu_card(
            content=ft.Row(
                controls=[
                    self._stat_col("🔥", str(streak["current"]), "Racha"),
                    self._divider(),
                    self._stat_col("🏆", str(streak["best"]), "Mejor"),
                    self._divider(),
                    self._stat_col("✅", str(streak["total"]), "Total"),
                    self._divider(),
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
        weekly_card = neu_card(
            content=ft.Column(
                controls=[
                    ft.Row(
                        controls=[
                            ft.Text(
                                "Progreso semanal",
                                size=13,
                                color=t.color_text_sub,
                                weight=ft.FontWeight.W_500,
                            ),
                            ft.Container(expand=True),
                            ft.Text(
                                f"{int(weekly_rate * 100)}%",
                                size=13,
                                color=t.color_primary,
                                weight=ft.FontWeight.BOLD,
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
                ],
                spacing=8,
            ),
            tokens=t,
            padding=16,
        )

        # ── IMPLEMENTATION INTENTION ────────────────────────────
        intention_controls: list[ft.Control] = []
        if activity.implementation_intention:
            intention_controls.append(
                neu_card(
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
                neu_card(
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

        # ── ACTION BUTTONS ───────────────────────────────────────
        already_done_today = self._completed_today()

        complete_btn = NeuButton(
            label="✅  Ya completada hoy" if already_done_today else "✅  Marcar como completada",
            on_click=self._handle_complete,
            tokens=t,
            disabled=already_done_today,
        )

        archive_btn = ft.TextButton(
            content=ft.Text("Archivar semilla", color=t.color_accent_alert),
            on_click=self._handle_archive,
        )

        # ── LAYOUT ──────────────────────────────────────────────
        sections: list[ft.Control] = [
            header,
            ft.Divider(color=t.color_shadow_dark + "55", height=1),
            stats_card,
            weekly_card,
            *deadline_controls,
            *intention_controls,
            *([neu_card(
                content=ft.Column(controls=checkin_controls, spacing=8),
                tokens=t,
                padding=16,
            )] if checkin_controls else []),
            ft.Container(height=8),
            complete_btn,
            ft.Container(
                content=archive_btn,
                alignment=ft.Alignment(0, 0),
            ),
            ft.Container(height=16),
        ]

        # Asegurar que h sea un número (800 por defecto) para evitar TypeError
        h = getattr(self._page, "height", 800) or 800
        content = ft.Container(
            height=max(500, h * 0.85),
            bgcolor=COLOR_BASE,
            padding=ft.Padding(left=24, right=24, top=20, bottom=0),
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
                ft.Text(emoji, size=20),
                ft.Text(
                    value,
                    size=18,
                    weight=ft.FontWeight.BOLD,
                    color=self._tokens.color_primary,
                ),
                ft.Text(label, size=11, color=self._tokens.color_text_sub),
            ],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=2,
        )

    def _divider(self) -> ft.Control:
        return ft.VerticalDivider(
            color=self._tokens.color_shadow_dark + "55",
            width=1,
        )

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
        """Devuelve True si ya hay un check-in hoy para esta actividad."""
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
        """Devuelve lista de timestamps de los últimos check-ins."""
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
