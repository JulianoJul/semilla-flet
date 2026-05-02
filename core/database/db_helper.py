"""
core/database/db_helper.py — Singleton SQLite helper.
"""

# --- IMPORTS ---
from __future__ import annotations

import logging
import sqlite3
from pathlib import Path
from typing import Optional

logger = logging.getLogger(__name__)

_DEFAULT_DB = str(Path(__file__).parent.parent.parent / "semilla.db")


# --- SINGLETON ---
class DBHelper:
    _instance: Optional[DBHelper] = None
    _db_path: str = _DEFAULT_DB
    _conn: Optional[sqlite3.Connection] = None

    def __new__(cls) -> DBHelper:
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    @classmethod
    def instance(cls, db_path: Optional[str] = None) -> DBHelper:
        if db_path is not None:
            cls._db_path = db_path
            cls._instance = None
            cls._conn = None
        return cls()

    @classmethod
    def _reset(cls) -> None:
        if cls._conn is not None:
            cls._conn.close()
            cls._conn = None
        cls._instance = None
        cls._db_path = _DEFAULT_DB

    # --- CONNECTION ---
    def get_connection(self) -> sqlite3.Connection:
        if self._db_path == ":memory:":
            if DBHelper._conn is None:
                DBHelper._conn = self._make_conn()
            return DBHelper._conn
        return self._make_conn()

    def _make_conn(self) -> sqlite3.Connection:
        conn = sqlite3.connect(self._db_path)
        conn.row_factory = sqlite3.Row
        conn.execute("PRAGMA foreign_keys = ON")
        conn.execute("PRAGMA journal_mode = WAL")
        return conn

    # --- MIGRATION ---
    def init_db(self) -> None:
        from core.database.migrations.migration_1 import run_migration

        conn = self.get_connection()
        try:
            run_migration(conn)
            conn.commit()
            logger.info("DB initialized at %s", self._db_path)
        except Exception:
            conn.rollback()
            raise
        finally:
            if self._db_path != ":memory:":
                conn.close()
