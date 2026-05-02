# core/design/typography.py — Text styles with guaranteed contrast.

# --- IMPORTS ---
from __future__ import annotations

from core.design.colors import COLOR_TEXT_MAIN, COLOR_TEXT_SUB, check_contrast

import flet as ft

COLOR_BASE = "#E8EDEA"
_WEIGHT = {
    "bold": ft.FontWeight.BOLD,
    "w600": ft.FontWeight.W_600,
    "w500": ft.FontWeight.W_500,
    "normal": ft.FontWeight.NORMAL,
}


# --- STYLES ---
class TextStyles:
    heading1    = dict(size=28, weight="bold",   color=COLOR_TEXT_MAIN)
    heading2    = dict(size=22, weight="w600",   color=COLOR_TEXT_MAIN)
    body        = dict(size=16, weight="normal", color=COLOR_TEXT_MAIN)
    caption     = dict(size=13, weight="normal", color=COLOR_TEXT_SUB)
    label       = dict(size=14, weight="w500",   color=COLOR_TEXT_MAIN)
    button_text = dict(size=16, weight="w600",   color=COLOR_TEXT_MAIN)

    @classmethod
    def verify_all(cls) -> None:
        for style in [cls.heading1, cls.heading2, cls.body,
                      cls.caption, cls.label, cls.button_text]:
            check_contrast(str(style["color"]), COLOR_BASE)


# --- FACTORY ---
def make_text(content: str, style: dict) -> ft.Text:
    weight = _WEIGHT.get(str(style.get("weight", "normal")), ft.FontWeight.NORMAL)
    return ft.Text(
        value=content,
        size=float(style.get("size", 16)),
        color=str(style.get("color", COLOR_TEXT_MAIN)),
        weight=weight,
    )
