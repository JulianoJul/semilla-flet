"""
features/onboarding/onboarding_view.py — Stub (Phase 6).
"""
# --- IMPORTS ---
from __future__ import annotations
from typing import Callable
import flet as ft


# --- VIEW ---
class OnboardingView(ft.Column):
    def __init__(
        self,
        page: ft.Page,
        on_complete: Callable[[ft.Page], None],
    ) -> None:
        super().__init__()
        self._page = page
        self._on_complete = on_complete
        self.controls = [
            ft.Text(
                "🌱 Semilla — Onboarding (Fase 6)",
                size=24,
                color="#1A2E25",
                weight=ft.FontWeight.BOLD,
            ),
            ft.ElevatedButton(
                "Continuar →",
                on_click=lambda _: on_complete(page),
            ),
        ]
