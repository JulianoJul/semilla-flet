# core/result.py — Result[T] sealed type for error handling.

# --- IMPORTS ---
from __future__ import annotations

from dataclasses import dataclass
from typing import Callable, Generic, Optional, TypeVar

# --- TYPE VARS ---
T = TypeVar("T")
U = TypeVar("U")


# --- DOMAIN ---
@dataclass(frozen=True)
class Success(Generic[T]):
    value: T
    error: Optional[str] = None

    def is_success(self) -> bool:
        return True

    def is_failure(self) -> bool:
        return False

    def fold(
        self,
        on_success: Callable[[T], U],
        on_failure: Callable[[str], U],
    ) -> U:
        return on_success(self.value)

    def map(self, fn: Callable[[T], U]) -> "Result[U]":
        try:
            return Success(fn(self.value))
        except Exception as exc:  # noqa: BLE001
            return Failure(str(exc))

    def get_or_none(self) -> Optional[T]:
        return self.value

    def get_or_raise(self) -> T:
        return self.value


@dataclass(frozen=True)
class Failure(Generic[T]):
    error: str
    value: Optional[T] = None  # Always None; present so Result[T] union has .value

    def is_success(self) -> bool:
        return False

    def is_failure(self) -> bool:
        return True

    def fold(
        self,
        on_success: Callable[[T], U],
        on_failure: Callable[[str], U],
    ) -> U:
        return on_failure(self.error)

    def map(self, fn: Callable[[T], U]) -> "Result[U]":
        return Failure(self.error)

    def get_or_none(self) -> Optional[T]:
        return None

    def get_or_raise(self) -> T:
        raise RuntimeError(self.error)


# --- PUBLIC API ---
Result = Success[T] | Failure[T]
