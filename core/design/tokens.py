# core/design/tokens.py — DesignTokens loaded from design_tokens table.

# --- IMPORTS ---
from __future__ import annotations

from dataclasses import dataclass
from typing import Optional

from core.design.colors import (
    COLOR_ACCENT_ALERT, COLOR_BASE, COLOR_PRIMARY,
    COLOR_SECONDARY, COLOR_SHADOW_DARK, COLOR_SHADOW_LIGHT,
    COLOR_TEXT_MAIN, COLOR_TEXT_SUB,
)


# --- DOMAIN ---
@dataclass
class DesignTokens:
    radius_small: int = 10
    radius_standard: int = 16
    radius_large: int = 24
    shadow_blur: int = 8
    shadow_offset: int = 4
    shadow_dark_opacity: float = 0.4
    shadow_light_opacity: float = 0.8
    color_base: str = COLOR_BASE
    color_shadow_dark: str = COLOR_SHADOW_DARK
    color_shadow_light: str = COLOR_SHADOW_LIGHT
    color_primary: str = COLOR_PRIMARY
    color_secondary: str = COLOR_SECONDARY
    color_text_main: str = COLOR_TEXT_MAIN
    color_text_sub: str = COLOR_TEXT_SUB
    color_accent_alert: str = COLOR_ACCENT_ALERT

    @staticmethod
    def load(db: object) -> DesignTokens:  # type: ignore[override]
        try:
            from core.database.db_helper import DBHelper
            assert isinstance(db, DBHelper)
            conn = db.get_connection()
            rows = conn.execute("SELECT key, value FROM design_tokens").fetchall()
            data = {r["key"]: r["value"] for r in rows}
            return DesignTokens(
                radius_small=int(data.get("radius_small", 10)),
                radius_standard=int(data.get("radius_standard", 16)),
                radius_large=int(data.get("radius_large", 24)),
                shadow_blur=int(data.get("shadow_blur", 8)),
                shadow_offset=int(data.get("shadow_offset", 4)),
                shadow_dark_opacity=float(data.get("shadow_dark_opacity", 0.4)),
                shadow_light_opacity=float(data.get("shadow_light_opacity", 0.8)),
                color_base=f"#{data.get('color_base', 'E8EDEA')}",
                color_shadow_dark=f"#{data.get('color_shadow_dark', 'B8BDB9')}",
                color_shadow_light=f"#{data.get('color_shadow_light', 'FFFFFF')}",
                color_primary=f"#{data.get('color_primary', '2E4A3E')}",
                color_secondary=f"#{data.get('color_secondary', '7FAF8C')}",
                color_text_main=f"#{data.get('color_text_main', '1A2E25')}",
                color_text_sub=f"#{data.get('color_text_sub', '4A6358')}",
                color_accent_alert=f"#{data.get('color_accent_alert', 'C17A3A')}",
            )
        except Exception:
            return DesignTokens()

    @staticmethod
    def defaults() -> DesignTokens:
        return DesignTokens()
