# features/gamification/streak_indicator.py — Compact streak display widget.

from __future__ import annotations
import flet as ft
from core.design.tokens import DesignTokens


class StreakIndicator(ft.Container):
    """
    Muestra: 🔥 N  ⬡×N  [ring]
    Todo en una Row con fuentes reducidas y tight=True para no desbordar el chip.
    """

    def __init__(
        self,
        activity_id: int,
        tokens: DesignTokens,
    ) -> None:
        streak = self._load(activity_id)
        t = tokens

        fire = ft.Text("🔥", size=14)
        count = ft.Text(
            str(streak["current"]),
            size=16,
            weight=ft.FontWeight.BOLD,
            color=t.color_primary,
        )
        shield_icon = ft.Text("⬡", size=12, color=t.color_text_sub)
        shield_count = ft.Text(
            f"×{streak['shields']}",
            size=12,
            color=t.color_text_sub,
        )
        ring = ft.ProgressRing(
            value=streak["weekly_rate"],
            width=18,
            height=18,
            stroke_width=2,
            color=t.color_secondary,
            bgcolor=t.color_shadow_dark + "44",
        )

        row = ft.Row(
            controls=[fire, count, shield_icon, shield_count, ring],
            spacing=3,
            tight=True,
        )

        super().__init__(
            content=row,
            padding=ft.Padding(left=0, right=0, top=2, bottom=0),
            clip_behavior=ft.ClipBehavior.HARD_EDGE,
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
        return {"current": 0, "shields": 1, "weekly_rate": 0.0}
