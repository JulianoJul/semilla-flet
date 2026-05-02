# core/notifications/notification_service.py — Local notification scheduling.

# --- IMPORTS ---
from __future__ import annotations

import logging

logger = logging.getLogger(__name__)


# --- SERVICE ---
class NotificationService:
    """Sends local notifications via plyer (gracefully degrades if unavailable)."""

    def __init__(self) -> None:
        self._plyer_ok = self._check_plyer()

    @staticmethod
    def _check_plyer() -> bool:
        try:
            from plyer import notification  # type: ignore[import]
            return True
        except Exception:
            return False

    def schedule_morning(self, title: str, message: str) -> None:
        self._notify(title=title, message=message)

    def schedule_evening(self, title: str, message: str) -> None:
        self._notify(title=title, message=message)

    def _notify(self, title: str, message: str, timeout: int = 5) -> None:
        if not self._plyer_ok:
            logger.debug("plyer unavailable — notification skipped: %s", title)
            return
        try:
            from plyer import notification as plyer_notif  # type: ignore[import]
            plyer_notif.notify(
                title=title,
                message=message,
                app_name="Semilla",
                timeout=timeout,
            )
        except Exception as exc:
            logger.warning("Notification failed: %s", exc)

    def send_streak_reminder(self, activity_title: str) -> None:
        title = self._copy("notification_morning_title") or "Semilla"
        msg = (
            self._copy("notification_streak_reminder") or
            f"Recuerda: {activity_title}"
        )
        self._notify(title=title, message=msg)

    def send_completion_feedback(self) -> None:
        title = self._copy("notification_evening_title") or "¡Bien hecho!"
        msg = self._copy("notification_completion") or "Tu jardín crece 🌱"
        self._notify(title=title, message=msg)

    @staticmethod
    def _copy(key: str) -> str:
        try:
            from core.database.db_helper import DBHelper
            row = DBHelper.instance().get_connection().execute(
                "SELECT value FROM notification_copy WHERE key=?", (key,),
            ).fetchone()
            return row["value"] if row else ""
        except Exception:
            return ""
