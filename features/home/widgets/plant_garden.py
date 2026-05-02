# features/home/widgets/plant_garden.py — Visual plant garden widget.

# --- IMPORTS ---
from __future__ import annotations

import threading

import flet as ft

from core.asset_helper import get_plant_stage_asset
from core.design.neu_card import neu_card
from core.design.tokens import DesignTokens


def _stage_from_completions(total: int) -> int:
    if total >= 100: return 5
    if total >= 30:  return 4
    if total >= 15:  return 3
    if total >= 7:   return 2
    if total >= 3:   return 1
    return 0


class PlantGarden(ft.Container):
    def __init__(self, tokens: DesignTokens) -> None:
        self._tokens = tokens
        self._plant_container = ft.Container(
            content=get_plant_stage_asset(0),
            animate_scale=ft.Animation(400, ft.AnimationCurve.BOUNCE_OUT),
            scale=1.0,
            alignment=ft.Alignment(0, 0),
        )
        card = neu_card(
            content=ft.Column(
                controls=[
                    ft.Container(
                        content=self._plant_container,
                        alignment=ft.Alignment(0, 0),
                        height=140,
                    ),
                ],
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            ),
            tokens=tokens,
            radius_key="large",
            padding=24,
        )
        super().__init__(content=card)
        self.load()

    def load(self) -> None:
        total = self._fetch_total()
        stage = _stage_from_completions(total)
        self._plant_container.content = get_plant_stage_asset(stage)

    def _fetch_total(self) -> int:
        try:
            from core.database.db_helper import DBHelper
            conn = DBHelper.instance().get_connection()
            row = conn.execute(
                "SELECT COALESCE(SUM(total_completions),0) as t FROM streaks",
            ).fetchone()
            return int(row["t"])
        except Exception:
            return 0

    def celebrate(self) -> None:
        self._plant_container.scale = 1.25
        try: self._plant_container.update()
        except Exception: pass
        def reset() -> None:
            import time; time.sleep(0.5)
            self._plant_container.scale = 1.0
            try: self._plant_container.update()
            except Exception: pass
        threading.Thread(target=reset, daemon=True).start()
