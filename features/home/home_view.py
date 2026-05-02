"""
features/home/home_view.py — Stub (Phase 7).
"""
# --- IMPORTS ---
from __future__ import annotations
import flet as ft


# --- VIEW ---
class HomeView(ft.Column):
    def __init__(self, page: ft.Page) -> None:
        super().__init__()
        self.controls = [
            ft.Text(
                "🌱 Semilla — Home (Fase 7)",
                size=24,
                color="#1A2E25",
                weight=ft.FontWeight.BOLD,
            )
        ]
