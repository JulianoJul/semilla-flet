# core/design/animations.py — Animation helpers, max 600ms.

# --- IMPORTS ---
from __future__ import annotations

import flet as ft


# --- HELPERS ---
def fade_in(content: ft.Control, duration: int = 300) -> ft.AnimatedSwitcher:
    return ft.AnimatedSwitcher(
        content=content,
        transition=ft.AnimatedSwitcherTransition.FADE,
        duration=duration,
        reverse_duration=150,
    )


def scale_pop(control: ft.Control) -> ft.Container:
    return ft.Container(
        content=control,
        animate_scale=ft.animation.Animation(
            duration=250,
            curve=ft.AnimationCurve.BOUNCE_OUT,
        ),
        scale=1.0,
    )


def slide_up(content: ft.Control, duration: int = 350) -> ft.AnimatedContainer:
    return ft.AnimatedContainer(
        content=content,
        animate=ft.animation.Animation(
            duration=duration,
            curve=ft.AnimationCurve.EASE_OUT,
        ),
        height=None,
    )


def pulse_scale(container: ft.Container, target: float = 1.1) -> None:
    container.scale = target
    container.update()


def reset_scale(container: ft.Container) -> None:
    container.scale = 1.0
    container.update()
