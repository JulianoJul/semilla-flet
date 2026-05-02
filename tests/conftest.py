"""
tests/conftest.py — Shared fixtures for all test suites.
BD en memoria (:memory:) para aislamiento total entre tests.
"""
# --- IMPORTS ---
from __future__ import annotations

import pytest


# --- FIXTURES ---
@pytest.fixture
def db_helper():
    """In-memory SQLite DBHelper instance, fully migrated."""
    from core.database.db_helper import DBHelper

    db = DBHelper.instance(db_path=":memory:")
    db.init_db()
    yield db
    DBHelper._reset()


@pytest.fixture
def container(db_helper):
    """AppContainer wired to the in-memory DB."""
    from core.container import AppContainer

    c = AppContainer.instance(db_helper=db_helper)
    yield c
    AppContainer._reset()


@pytest.fixture
def sample_activity(container):
    """A single Activity of type 'A' created via use case."""
    result = container.create_activity_uc.execute(
        title="Test habit",
        activity_type="A",
    )
    return result.get_or_raise()
