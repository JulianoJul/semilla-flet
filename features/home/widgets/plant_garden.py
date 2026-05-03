# features/home/widgets/plant_garden.py — Visual plant garden widget.

# --- IMPORTS ---
from __future__ import annotations

import flet as ft

from core.asset_helper import get_plant_stage_asset
from core.design.neu_card import NeuCard
from core.design.tokens import DesignTokens


_STAGE_LABELS = [
    ("Semilla dormida", "Planta tu primera intención."),
    ("Primer brote", "Tus hábitos empiezan a crecer."),
    ("Pequeña planta", "Estás construyendo consistencia."),
    ("Planta joven", "Tu jardín florece día a día."),
    ("Árbol maduro", "Una racha impresionante."),
    ("Jardín frondoso", "¡Maestro del cultivo! 🌟"),
]


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
            content=None,
            animate_scale=ft.Animation(400, ft.AnimationCurve.BOUNCE_OUT),  # type: ignore
            scale=1.0,
            alignment=ft.Alignment(0, 0),
        )
        self._stage_label = ft.Text(
            "",
            size=16,
            weight=ft.FontWeight.W_600,
            color=tokens.color_primary,
            text_align=ft.TextAlign.CENTER,
        )
        self._stage_sub = ft.Text(
            "",
            size=13,
            color=tokens.color_text_sub,
            text_align=ft.TextAlign.CENTER,
        )
        self._progress_bar = ft.ProgressBar(
            value=0.0,
            color=tokens.color_secondary,
            bgcolor=tokens.color_shadow_dark + "44",
            height=6,
            border_radius=ft.BorderRadius(3, 3, 3, 3),
        )

        t = tokens
        card_content = ft.Column(
            controls=[
                ft.Container(
                    content=self._plant_container,
                    alignment=ft.Alignment(0, 0),
                    height=130,
                ),
                self._stage_label,
                self._stage_sub,
                ft.Container(height=8),
                # Inset progress track
                ft.Container(
                    content=self._progress_bar,
                    padding=ft.Padding(left=2, right=2, top=2, bottom=2),
                    border_radius=ft.BorderRadius(5, 5, 5, 5),
                    bgcolor=t.color_base,
                    shadow=[
                        ft.BoxShadow(
                            offset=ft.Offset(1, 1),
                            blur_radius=3.0,
                            color=NeuCard._with_opacity(t.shadow_dark_opacity * 0.5, t.color_shadow_dark),
                        ),
                        ft.BoxShadow(
                            offset=ft.Offset(-1, -1),
                            blur_radius=3.0,
                            color=NeuCard._with_opacity(t.shadow_light_opacity * 0.5, t.color_shadow_light),
                        ),
                    ],
                ),
            ],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=6,
        )

        # Gradient background via Stack
        r = float(tokens.radius_large)
        gradient_bg = ft.Container(
            gradient=ft.LinearGradient(
                begin=ft.Alignment(-1, -1),
                end=ft.Alignment(1, 1),
                colors=[tokens.gradient_subtle_start, tokens.gradient_subtle_end],
            ),
            border_radius=ft.BorderRadius(r, r, r, r),
            expand=True,
        )

        card = ft.Container(
            content=ft.Stack(
                controls=[
                    gradient_bg,
                    ft.Container(
                        content=card_content,
                        padding=24,
                    ),
                ],
            ),
            border_radius=ft.BorderRadius(r, r, r, r),
            shadow=[
                ft.BoxShadow(
                    offset=ft.Offset(-t.shadow_offset, -t.shadow_offset),
                    blur_radius=float(t.shadow_blur),
                    color=NeuCard._with_opacity(t.shadow_light_opacity, t.color_shadow_light),
                ),
                ft.BoxShadow(
                    offset=ft.Offset(t.shadow_offset, t.shadow_offset),
                    blur_radius=float(t.shadow_blur),
                    color=NeuCard._with_opacity(t.shadow_dark_opacity, t.color_shadow_dark),
                ),
            ],
            clip_behavior=ft.ClipBehavior.ANTI_ALIAS,
        )

        super().__init__(content=card)
        self.load()

    def load(self) -> None:
        total = self._fetch_total()
        stage = _stage_from_completions(total)
        self._plant_container.content = get_plant_stage_asset(stage)
        label, sub = _STAGE_LABELS[stage]
        self._stage_label.value = label
        self._stage_sub.value = sub
        # Progress within current stage
        thresholds = [0, 3, 7, 15, 30, 100, 100]
        low = thresholds[stage]
        high = thresholds[stage + 1] if stage < 5 else 100
        span = high - low
        progress = (total - low) / span if span > 0 else 1.0
        self._progress_bar.value = max(0.0, min(1.0, progress))

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
        from core.design.animations import pulse_scale, reset_scale
        pulse_scale(self._plant_container, target=1.25)
        async def _reset():
            import asyncio
            await asyncio.sleep(0.5)
            reset_scale(self._plant_container)
        if self.page:
            self.page.run_task(_reset)  # type: ignore
