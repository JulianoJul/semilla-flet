# core/design/colors.py — Color constants + WCAG contrast helpers.

# --- IMPORTS ---
from __future__ import annotations

import logging
import warnings

logger = logging.getLogger(__name__)

# --- CONSTANTS ---
COLOR_BASE          = "#E8EDEA"
COLOR_SHADOW_DARK   = "#B8BDB9"
COLOR_SHADOW_LIGHT  = "#FFFFFF"
COLOR_PRIMARY       = "#2E4A3E"
COLOR_SECONDARY     = "#7FAF8C"
COLOR_TEXT_MAIN     = "#1A2E25"
COLOR_TEXT_SUB      = "#4A6358"
COLOR_ACCENT_ALERT  = "#C17A3A"


# --- HELPERS ---
def _luminance(hex_color: str) -> float:
    h = hex_color.lstrip("#")
    r, g, b = (int(h[i:i+2], 16) / 255.0 for i in (0, 2, 4))
    def lin(c: float) -> float:
        return c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4
    return 0.2126 * lin(r) + 0.7152 * lin(g) + 0.0722 * lin(b)


def check_contrast(fg: str, bg: str) -> float:
    l1 = _luminance(fg) + 0.05
    l2 = _luminance(bg) + 0.05
    ratio = max(l1, l2) / min(l1, l2)
    if ratio < 4.5:
        warnings.warn(
            f"Contrast {ratio:.2f}:1 below WCAG AA ({fg} on {bg})",
            stacklevel=2,
        )
    return ratio
