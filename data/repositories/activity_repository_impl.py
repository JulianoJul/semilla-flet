"""
data/repositories/activity_repository_impl.py — Concrete ActivityRepository.
"""

# --- IMPORTS ---
from __future__ import annotations

from core.result import Failure, Result, Success
from data.datasources.activity_datasource import ActivityLocalDatasource
from domain.entities.activity import Activity, ActivityType
from domain.entities.checkin import CheckIn
from domain.repositories.activity_repository import ActivityRepository


# --- IMPLEMENTATION ---
class ActivityRepositoryImpl(ActivityRepository):
    def __init__(self, ds: ActivityLocalDatasource) -> None:
        self._ds = ds

    def get_all_activities(self) -> Result[list[Activity]]:
        try:
            return Success(self._ds.get_all())
        except Exception as e:
            return Failure(f"Error al obtener actividades: {e}")

    def get_activities_by_type(
        self, activity_type: ActivityType,
    ) -> Result[list[Activity]]:
        try:
            return Success(self._ds.get_by_type(activity_type))
        except Exception as e:
            return Failure(f"Error filtrando actividades: {e}")

    def create_activity(self, activity: Activity) -> Result[Activity]:
        try:
            return Success(self._ds.create(activity))
        except Exception as e:
            return Failure(f"Error al crear actividad: {e}")

    def update_activity(self, activity: Activity) -> Result[Activity]:
        try:
            return Success(self._ds.update(activity))
        except Exception as e:
            return Failure(f"Error al actualizar actividad: {e}")

    def archive_activity(self, activity_id: int) -> Result[None]:
        try:
            self._ds.archive(activity_id)
            return Success(None)
        except Exception as e:
            return Failure(f"Error al archivar actividad: {e}")

    def get_today_intentions(self) -> Result[list[Activity]]:
        try:
            return Success(self._ds.get_today_intentions())
        except Exception as e:
            return Failure(f"Error al obtener intenciones: {e}")

    def set_today_intentions(
        self, activity_ids: list[int],
    ) -> Result[None]:
        try:
            self._ds.set_today_intentions(activity_ids)
            return Success(None)
        except Exception as e:
            return Failure(f"Error al guardar intenciones: {e}")

    def get_checkins_for_activity(
        self, activity_id: int,
    ) -> Result[list[CheckIn]]:
        try:
            return Success(self._ds.get_checkins(activity_id))
        except Exception as e:
            return Failure(f"Error al obtener check-ins: {e}")

    def create_checkin(self, checkin: CheckIn) -> Result[CheckIn]:
        try:
            return Success(self._ds.create_checkin(checkin))
        except Exception as e:
            return Failure(f"Error al crear check-in: {e}")

    def get_checkins_since(
        self, activity_id: int, since_date: str,
    ) -> Result[list[CheckIn]]:
        try:
            return Success(self._ds.get_checkins_since(activity_id, since_date))
        except Exception as e:
            return Failure(f"Error al obtener check-ins desde fecha: {e}")
