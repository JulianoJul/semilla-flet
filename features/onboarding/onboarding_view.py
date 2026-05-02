# features/onboarding/onboarding_view.py — 3-step onboarding with fade transitions.

# --- IMPORTS ---
from __future__ import annotations

from typing import Callable

import flet as ft

from core.design.colors import COLOR_BASE
from core.design.tokens import DesignTokens


# --- VIEW ---
class OnboardingView(ft.Column):
    def __init__(
        self,
        page: ft.Page,
        on_complete: Callable[[ft.Page], None],
    ) -> None:
        super().__init__(expand=True)
        self._page = page
        self._on_complete = on_complete
        self._step = 0
        self._tokens = self._load_tokens()
        self._switcher = ft.AnimatedSwitcher(
            content=self._build_step(0),
            transition=ft.AnimatedSwitcherTransition.FADE,
            duration=350,
            expand=True,
        )
        self.controls = [self._switcher]
        self.expand = True
        self.horizontal_alignment = ft.CrossAxisAlignment.CENTER

    def _load_tokens(self) -> DesignTokens:
        try:
            from core.database.db_helper import DBHelper
            return DesignTokens.load(DBHelper.instance())
        except Exception:
            return DesignTokens.defaults()

    def _build_step(self, step: int) -> ft.Control:
        from features.onboarding.step_archetype import StepArchetype
        from features.onboarding.step_first_seed import StepFirstSeed
        from features.onboarding.step_pact import StepPact

        if step == 0:
            return StepArchetype(tokens=self._tokens, on_done=self._next)
        elif step == 1:
            return StepFirstSeed(
                tokens=self._tokens,
                on_done=self._next,
                page=self._page,
            )
        return StepPact(
            tokens=self._tokens,
            on_done=self._complete,
        )

    def _next(self) -> None:
        self._step += 1
        self._switcher.content = self._build_step(self._step)
        self._switcher.update()

    def _complete(self) -> None:
        self._on_complete(self._page)
