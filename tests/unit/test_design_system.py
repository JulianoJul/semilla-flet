# tests/unit/test_design_system.py — Tests for contrast and token loading.

import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", ".."))

import pytest
import warnings


def test_text_colors_pass_wcag_aa():
    from core.design.colors import check_contrast, COLOR_TEXT_MAIN, COLOR_TEXT_SUB
    COLOR_BASE = "#E8EDEA"
    r1 = check_contrast(COLOR_TEXT_MAIN, COLOR_BASE)
    assert r1 >= 4.5, f"COLOR_TEXT_MAIN fails WCAG AA: {r1:.2f}:1"
    r2 = check_contrast(COLOR_TEXT_SUB, COLOR_BASE)
    assert r2 >= 4.5, f"COLOR_TEXT_SUB fails WCAG AA: {r2:.2f}:1"


def test_primary_on_base_contrast():
    from core.design.colors import check_contrast, COLOR_PRIMARY
    COLOR_BASE = "#E8EDEA"
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        ratio = check_contrast(COLOR_PRIMARY, COLOR_BASE)
    # Primary is used for icons/accents, not small text — 3:1 minimum
    assert ratio >= 3.0, f"COLOR_PRIMARY on base too low: {ratio:.2f}:1"


def test_default_tokens_loadable():
    from core.design.tokens import DesignTokens
    t = DesignTokens.defaults()
    assert t.radius_standard > 0
    assert t.shadow_blur > 0
    assert t.color_base.startswith("#")


def test_make_text_returns_ft_text():
    import flet as ft
    from core.design.typography import make_text, TextStyles
    t = make_text("Hola", TextStyles.heading1)
    assert isinstance(t, ft.Text)
    assert t.value == "Hola"
