# features/gamification/streak_indicator.py — Compact streak display widget.

# --- IMPORTS ---
from __future__ import annotations

import flet as ft

from core.design.tokens import DesignTokens


class StreakIndicator(ft.Container):
    """Row: 🔥 N | shield ⬡ | weekly ring."""

    def __init__(
        self,
        activity_id: int,
        tokens: DesignTokens,
    ) -> None:
        streak = self._load(activity_id)
        controls: list[ft.Control] = [
            ft.Text("🔥", size=18),
            ft.Text(
                str(streak["current"]),
                size=22, weight=ft.FontWeight.BOLD,
                color=tokens.color_primary,
            ),
            ft.Container(width=8),
            ft.Text("⬡", size=16, color=tokens.color_text_sub),
            ft.Text(
                f"×{streak['shields']}",
                size=14, color=tokens.color_text_sub,
            ),
            ft.Container(width=8),
            ft.ProgressRing(
                value=streak["weekly_rate"],
                width=26, height=26, stroke_width=3,
            ),
        ]
        super().__init__(
            content=ft.Row(controls=controls, spacing=4),
        )

    @staticmethod
    def _load(activity_id: int) -> dict:
        try:
            from core.database.db_helper import DBHelper
            row = DBHelper.instance().get_connection().execute(
                "SELECT current_count, shields_available, weekly_completion_rate "
                "FROM streaks WHERE activity_id=?",
                (activity_id,),
            ).fetchone()
            if row:
                return {
                    "current": row["current_count"],
                    "shields": row["shields_available"],
                    "weekly_rate": float(row["weekly_completion_rate"] or 0),
                }
        except Exception:
            pass
        return {"current": 0, "shields": 0, "weekly_rate": 0.0}
