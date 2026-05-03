# tests/unit/test_streak.py — Unit tests for ManageStreakUseCase.

import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", ".."))

import pytest
import dataclasses
from datetime import date, timedelta

from core.database.db_helper import DBHelper
from core.container import AppContainer


@pytest.fixture(autouse=True)
def fresh_db(tmp_path):
    db_file = str(tmp_path / "test.db")
    DBHelper._reset()
    AppContainer._reset()
    db = DBHelper.instance(db_path=db_file)
    db.init_db()
    yield db
    DBHelper._reset()
    AppContainer._reset()


def _make_activity(title: str = "Test") -> int:
    c = AppContainer.instance()
    res = c.create_activity_uc.execute(title=title, activity_type="A")
    assert res.is_success()
    return res.get_or_raise().id or 0


def _wind_back_one_day(activity_id: int) -> None:
    """Move last_checkin_date back one day to simulate time passing."""
    c = AppContainer.instance()
    s = c.gamification_repo.get_streak(activity_id).get_or_raise()
    yesterday = (date.today() - timedelta(days=1)).isoformat()
    c.gamification_repo.update_streak(
        dataclasses.replace(s, last_checkin_date=yesterday)
    )


def test_first_completion_starts_streak():
    aid = _make_activity()
    res = AppContainer.instance().complete_activity_uc.execute(activity_id=aid)
    assert res.is_success()
    assert res.get_or_raise().streak.current_count == 1
    assert res.get_or_raise().streak.total_completions == 1


def test_consecutive_completions_grow_streak():
    aid = _make_activity()
    c = AppContainer.instance()
    r = None
    for i in range(3):
        r = c.complete_activity_uc.execute(activity_id=aid)
        assert r.is_success()
        _wind_back_one_day(aid)
    assert r is not None and r.get_or_raise().streak.current_count == 3


def test_best_count_updates():
    aid = _make_activity()
    c = AppContainer.instance()
    for _ in range(5):
        c.complete_activity_uc.execute(activity_id=aid)
        _wind_back_one_day(aid)
    streak = c.gamification_repo.get_streak(activity_id=aid)
    assert streak.get_or_raise().best_count == 5


def test_empty_title_fails():
    c = AppContainer.instance()
    res = c.create_activity_uc.execute(title="  ", activity_type="A")
    assert res.is_failure()


def test_today_intentions_returned():
    aid = _make_activity("Meditar")
    AppContainer.instance().activity_repo.set_today_intentions([aid])
    res = AppContainer.instance().get_today_intentions_uc.execute()
    assert res.is_success()
    activities, fresh = res.get_or_raise()
    assert any(a.id == aid for a in activities)

