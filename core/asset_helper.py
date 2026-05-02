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

_ICON_FALLBACK_MAP: dict[str, ft.icons] = {
    "home": ft.icons.HOME_OUTLINED,
    "add": ft.icons.ADD_CIRCLE_OUTLINE,
    "check": ft.icons.CHECK_CIRCLE_OUTLINE,
    "streak": ft.icons.LOCAL_FIRE_DEPARTMENT_OUTLINED,
    "badge": ft.icons.EMOJI_EVENTS_OUTLINED,
    "settings": ft.icons.SETTINGS_OUTLINED,
    "plant": ft.icons.PARK_OUTLINED,
    "calendar": ft.icons.CALENDAR_TODAY_OUTLINED,
    "backlog": ft.icons.LIST_ALT_OUTLINED,
    "shield": ft.icons.SHIELD_OUTLINED,
    "chest": ft.icons.REDEEM_OUTLINED,
}


# --- HELPERS ---
def get_asset(
    path: str,
    placeholder_fn: Callable[..., ft.Control],
    **kwargs: Any,
) -> ft.Control:
    if Path(path).exists():
        return ft.Image(src=path, **kwargs)
    return placeholder_fn(**kwargs)


# --- PLANT ASSETS ---
def get_plant_stage_asset(stage: int) -> ft.Control:
    # ASSET: imagen PNG de planta en etapa {stage}
    # Debe ser: planta en estado de crecimiento stage (0–5)
    # Etapas: 0=semilla, 1=brote, 2=planta joven,
    #         3=arbusto, 4=árbol, 5=árbol maduro
    # Formato esperado: PNG, 80×80 a 200×200 px
    # Estilo: ilustración flat, paleta verde suave (#7FAF8C)
    asset_path = f"assets/plants/stage_{stage}.png"
    if Path(asset_path).exists():
        size = 80 + (stage * 20)
        return ft.Image(src=asset_path, width=size, height=size)

    # PLACEHOLDER: emoji que escala con el estado de crecimiento
    clamped = min(max(stage, 0), len(_PLANT_EMOJIS) - 1)
    emoji = _PLANT_EMOJIS[clamped]
    size = 24 + (clamped * 10)
    return ft.Text(emoji, size=float(size))


# --- BADGE ASSETS ---
def get_badge_asset(badge_key: str, emoji: Optional[str] = None) -> ft.Control:
    # ASSET: icono PNG/SVG de insignia {badge_key}
    # Dimensiones: 48×48 px, fondo transparente
    # Estilo: icono monocromático con COLOR_PRIMARY (#2E4A3E)
    asset_path = f"assets/badges/{badge_key}.png"
    if Path(asset_path).exists():
        return ft.Image(src=asset_path, width=48, height=48)

    # PLACEHOLDER: emoji temático por tipo de insignia
    fallback_emoji = emoji or _BADGE_EMOJI_MAP.get(badge_key, "🏅")
    return ft.Text(fallback_emoji, size=40.0)


# --- SOUND ASSETS ---
def get_sound_asset(name: str) -> Callable[[], None]:
    # ASSET: archivo MP3 de sonido {name}
    # Archivos esperados: complete.mp3, chest.mp3,
    #                     streak.mp3, shield.mp3, reset.mp3
    # Formato: MP3, 44100 Hz, mono, < 2s de duración
    # Si no existe: función silenciosa con log de debug
    sound_path = Path(f"assets/sounds/{name}.mp3")
    if sound_path.exists():
        def _play() -> None:
            logger.debug("SOUND: playing %s", name)
        return _play

    def _noop() -> None:
        logger.debug("SOUND: placeholder — asset not found: %s.mp3", name)

    return _noop


# --- ICON ASSETS ---
def get_icon_asset(name: str, size: float = 24.0) -> ft.Control:
    # ASSET: archivo SVG de icono {name}
    # Dimensiones: 24×24 px, viewBox estándar
    # Estilo: line icons, stroke-width 1.5, COLOR_PRIMARY
    svg_path = f"assets/icons/{name}.svg"
    if Path(svg_path).exists():
        return ft.Image(src=svg_path, width=size, height=size)

    # PLACEHOLDER: ft.Icon con el ícono Flet más cercano
    fallback = _ICON_FALLBACK_MAP.get(name, ft.icons.HELP_OUTLINE)
    return ft.Icon(name=fallback, size=size, color="#2E4A3E")
