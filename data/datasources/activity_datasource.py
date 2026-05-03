# --- IMPORTS ---
from __future__ import annotations

from datetime import date

from core.database.db_helper import DBHelper
from data.datasources.activity_mappers import map_activity, map_checkin
from domain.entities.activity import Activity, ActivityType
from domain.entities.checkin import CheckIn


# --- DATASOURCE ---
class ActivityLocalDatasource:
    def __init__(self, db: DBHelper) -> None:
        self._db = db

    # --- READ ---
    def get_all(self) -> list[Activity]:
        conn = self._db.get_connection()
        rows = conn.execute(
            "SELECT * FROM activities WHERE is_archived = 0"
        ).fetchall()
        return [map_activity(r) for r in rows]

    def get_by_type(self, activity_type: ActivityType) -> list[Activity]:
        conn = self._db.get_connection()
        rows = conn.execute(
            "SELECT * FROM activities WHERE type = ? AND is_archived = 0",
            (activity_type.value,),
        ).fetchall()
        return [map_activity(r) for r in rows]

    # --- CREATE ---
    def create(self, a: Activity) -> Activity:
        conn = self._db.get_connection()
        freq = a.frequency_config.to_json() if a.frequency_config else None
        # Both inserts run in a single transaction — if the streak INSERT
        # fails the activity INSERT is also rolled back, avoiding orphaned rows.
        cur = conn.execute(
            "INSERT INTO activities (title, type, frequency_config, "
            "deadline, implementation_intention, coping_plan, created_at) "
            "VALUES (?, ?, ?, ?, ?, ?, ?)",
            (a.title, a.type.value, freq, a.deadline,
             a.implementation_intention, a.coping_plan, a.created_at),
        )
        new_id = cur.lastrowid
        conn.execute(
            "INSERT INTO streaks (activity_id) VALUES (?)", (new_id,),
        )
        conn.commit()
        return Activity(
            id=new_id, title=a.title, type=a.type,
            frequency_config=a.frequency_config, deadline=a.deadline,
            implementation_intention=a.implementation_intention,
            coping_plan=a.coping_plan, created_at=a.created_at,
        )
    # --- UPDATE ---
    def update(self, a: Activity) -> Activity:
        conn = self._db.get_connection()
        freq = a.frequency_config.to_json() if a.frequency_config else None
        conn.execute(
            "UPDATE activities SET title=?, type=?, frequency_config=?, "
            "deadline=?, implementation_intention=?, coping_plan=? "
            "WHERE id=?",
            (a.title, a.type.value, freq, a.deadline,
             a.implementation_intention, a.coping_plan, a.id),
        )
        conn.commit()
        return a

    def archive(self, activity_id: int) -> None:
        conn = self._db.get_connection()
        conn.execute(
            "UPDATE activities SET is_archived = 1 WHERE id = ?",
            (activity_id,),
        )
        conn.commit()
    # --- TODAY INTENTIONS ---
    def get_today_intentions(self) -> list[Activity]:
        from domain.entities.today_intention import TodayIntention
        conn = self._db.get_connection()
        today = date.today().isoformat()
        
        t_rows = conn.execute(
            "SELECT * FROM today_intentions WHERE date = ? ORDER BY order_index",
            (today,),
        ).fetchall()
        
        intentions = [
            TodayIntention(
                id=r["id"], date=r["date"], 
                activity_id=r["activity_id"], order_index=r["order_index"]
            )
            for r in t_rows
        ]
        
        activities = []
        for intention in intentions:
            a_row = conn.execute(
                "SELECT * FROM activities WHERE id = ? AND is_archived = 0", (intention.activity_id,)
            ).fetchone()
            if a_row:
                activities.append(map_activity(a_row))
                
        return activities

    def set_today_intentions(self, activity_ids: list[int]) -> None:
        conn = self._db.get_connection()
        today = date.today().isoformat()
        conn.execute(
            "DELETE FROM today_intentions WHERE date = ?", (today,),
        )
        for idx, aid in enumerate(activity_ids):
            conn.execute(
                "INSERT INTO today_intentions "
                "(date, activity_id, order_index) VALUES (?, ?, ?)",
                (today, aid, idx),
            )
        conn.commit()
    # --- CHECKINS ---
    def get_checkins(self, activity_id: int) -> list[CheckIn]:
        conn = self._db.get_connection()
        rows = conn.execute(
            "SELECT * FROM checkins WHERE activity_id = ? "
            "ORDER BY completed_at DESC", (activity_id,),
        ).fetchall()
        return [map_checkin(r) for r in rows]

    def create_checkin(self, c: CheckIn) -> CheckIn:
        conn = self._db.get_connection()
        cur = conn.execute(
            "INSERT INTO checkins (activity_id, completed_at, notes) "
            "VALUES (?, ?, ?)",
            (c.activity_id, c.completed_at, c.notes),
        )
        conn.commit()
        return CheckIn(
            id=cur.lastrowid, activity_id=c.activity_id,
            completed_at=c.completed_at, notes=c.notes,
        )

    def get_checkins_since(self, activity_id: int, since_date: str) -> list[CheckIn]:
        """Return all check-ins for *activity_id* on or after *since_date* (ISO date).

        Timestamps are stored as 'YYYY-MM-DD HH:MM:SS' UTC, so DATE(completed_at)
        extracts the date correctly without any timezone normalization needed.
        """
        conn = self._db.get_connection()
        rows = conn.execute(
            "SELECT * FROM checkins WHERE activity_id = ? "
            "AND DATE(completed_at) >= ? ORDER BY completed_at DESC",
            (activity_id, since_date),
        ).fetchall()
        return [map_checkin(r) for r in rows]
