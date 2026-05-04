"""
Semilla — Entry point.
No gestionas tareas. Cultivas tu día.
"""

# --- IMPORTS ---
from __future__ import annotations

import logging
import sys
from pathlib import Path

import flet as ft

# --- CONSTANTS ---
COLOR_BASE = "#E8EDEA"

logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
)
logger = logging.getLogger(__name__)


# --- BOOTSTRAP ---
def _ensure_sys_path() -> None:
    root = str(Path(__file__).parent)
    if root not in sys.path:
        sys.path.insert(0, root)


def _init_database() -> bool:
    try:
        from core.database.db_helper import DBHelper

        db = DBHelper.instance()
        db.init_db()
        return True
    except Exception as exc:  # noqa: BLE001
        logger.error("DB init failed: %s", exc)
        return False


def _is_onboarding_complete() -> bool:
    try:
        from core.database.db_helper import DBHelper

        db = DBHelper.instance()
        conn = db.get_connection()
        row = conn.execute(
            "SELECT value FROM settings WHERE key = ?",
            ("onboarding_complete",),
        ).fetchone()
        return row is not None and row["value"] == "1"
    except Exception as exc:  # noqa: BLE001
        logger.warning("Could not read onboarding flag: %s", exc)
        return False


# --- ROUTING ---
def _navigate_to_home(page: ft.Page) -> None:
    from features.home.home_view import HomeView

    page.controls.clear()
    page.add(HomeView(page=page))
    page.update()


def _navigate_to_onboarding(page: ft.Page) -> None:
    from features.onboarding.onboarding_view import OnboardingView

    page.controls.clear()
    page.add(OnboardingView(page=page, on_complete=_navigate_to_home))
    page.update()


# --- MAIN ---
def main(page: ft.Page) -> None:
    # --- PAGE SETUP ---
    page.title = "Semilla"
    page.bgcolor = COLOR_BASE
    page.padding = 0
    page.spacing = 0
    page.fonts = {
        "Inter": "https://fonts.gstatic.com/s/inter/v13/UcCO3FwrK3iLTeHuS_fvQtMwCp50KnMw2boKoduKmMEVuLyfAZ9hiJ-Ek-_EeA.woff2"
    }
    page.theme_mode = ft.ThemeMode.LIGHT
    page.theme = ft.Theme(
        font_family="Inter",
        use_material3=True,
        bottom_sheet_theme=ft.BottomSheetTheme(
            bgcolor=COLOR_BASE,
            elevation=0,
        )
    )

    # --- DB INIT ---
    if not _init_database():
        page.add(
            ft.Text(
                "Error al iniciar la base de datos.",
                color="#C17A3A",
                size=16,
            )
        )
        page.update()
        return

    # --- ROUTING ---
    if _is_onboarding_complete():
        _navigate_to_home(page)
    else:
        _navigate_to_onboarding(page)


if __name__ == "__main__":
    _ensure_sys_path()
    ft.app(main, assets_dir="assets")
