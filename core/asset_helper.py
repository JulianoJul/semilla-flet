"""
core/asset_helper.py — Placeholder system for all project assets.
Every asset has a graceful fallback; no missing file ever causes an error.
"""

# --- IMPORTS ---
from __future__ import annotations

import logging
from pathlib import Path
from typing import Any, Callable, Optional

import flet as ft

logger = logging.getLogger(__name__)

# --- CONSTANTS ---
_PLANT_EMOJIS = ["🌱", "🌿", "🍀", "🌳", "🌲", "🌴"]

_BADGE_EMOJI_MAP: dict[str, str] = {
    "jardinero": "🧑‍🌾",
    "resiliente": "🛡️",
    "mañanas": "☀️",
    "constancia": "⚡",
    "primer_brote": "🌱",
    "racha_7": "🔥",
    "racha_21": "💪",
    "racha_30": "🏆",
    "racha_60": "🌟",
    "racha_100": "👑",
}

from typing import Any

_ICON_FALLBACK_MAP: dict[str, Any] = {
    "home": ft.Icons.HOME_OUTLINED,
    "add": ft.Icons.ADD_CIRCLE_OUTLINE,
    "check": ft.Icons.CHECK_CIRCLE_OUTLINE,
    "streak": ft.Icons.LOCAL_FIRE_DEPARTMENT_OUTLINED,
    "badge": ft.Icons.EMOJI_EVENTS_OUTLINED,
    "settings": ft.Icons.SETTINGS_OUTLINED,
    "plant": ft.Icons.PARK_OUTLINED,
    "calendar": ft.Icons.CALENDAR_TODAY_OUTLINED,
    "backlog": ft.Icons.LIST_ALT_OUTLINED,
    "shield": ft.Icons.SHIELD_OUTLINED,
    "chest": ft.Icons.REDEEM_OUTLINED,
}


# --- HELPERS ---
def get_asset(
    path: str,
    placeholder_fn: Callable[..., ft.Control],
    **kwargs: Any,
) -> ft.Control:
    return ft.Image(src=path, error_content=placeholder_fn(**kwargs), **kwargs)


# --- PLANT ASSETS ---
def get_plant_stage_asset(stage: int) -> ft.Control:
    # ASSET: imagen PNG de planta en etapa {stage}
    # Debe ser: planta en estado de crecimiento stage (0–5)
    # Etapas: 0=semilla, 1=brote, 2=planta joven,
    #         3=arbusto, 4=árbol, 5=árbol maduro
    # Formato esperado: PNG, 80×80 a 200×200 px
    # Estilo: ilustración flat, paleta verde suave (#7FAF8C)
    asset_path = f"assets/plants/stage_{stage}.png"
    size = 80 + (stage * 20)
    clamped = min(max(stage, 0), len(_PLANT_EMOJIS) - 1)
    emoji = _PLANT_EMOJIS[clamped]
    esize = 24 + (clamped * 10)
    fallback = ft.Text(emoji, size=float(esize))
    
    img = ft.Image(src=asset_path, width=size, height=size, error_content=fallback)
    return ft.Container(content=img, width=size, height=size, alignment=ft.Alignment(0, 0))


# --- BADGE ASSETS ---
def get_badge_asset(badge_key: str, emoji: Optional[str] = None) -> ft.Control:
    # ASSET: icono PNG/SVG de insignia {badge_key}
    # Dimensiones: 48×48 px, fondo transparente
    # Estilo: icono monocromático con COLOR_PRIMARY (#2E4A3E)
    asset_path = f"assets/badges/{badge_key}.png"
    fallback_emoji = emoji or _BADGE_EMOJI_MAP.get(badge_key, "🏅")
    fallback = ft.Text(fallback_emoji, size=40.0)
    return ft.Image(src=asset_path, width=48, height=48, error_content=fallback)


# --- SOUND ASSETS ---
def get_sound_asset(name: str) -> Callable[[], None]:
    # ASSET: archivo MP3 de sonido {name}
    # Archivos esperados: complete.mp3, chest.mp3,
    #                     streak.mp3, shield.mp3, reset.mp3
    # Formato: MP3, 44100 Hz, mono, < 2s de duración
    # Si no existe: función silenciosa con log de debug
    def _play() -> None:
        logger.debug("SOUND: playing %s", name)
    return _play


# --- ICON ASSETS ---
def get_icon_asset(name: str, size: float = 24.0) -> ft.Control:
    # ASSET: archivo SVG de icono {name}
    # Dimensiones: 24×24 px, viewBox estándar
    # Estilo: line icons, stroke-width 1.5, COLOR_PRIMARY
    svg_path = f"assets/icons/{name}.svg"
    fallback_icon = _ICON_FALLBACK_MAP.get(name, ft.Icons.HELP_OUTLINE)
    fallback = ft.Icon(fallback_icon, size=size, color="#2E4A3E")
    return ft.Image(src=svg_path, width=size, height=size, error_content=fallback)
