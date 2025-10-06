from unittest.mock import AsyncMock, patch

import pytest

from worker.taxi_worker import *
import worker.taxi_worker as worker


@pytest.mark.asyncio
async def test_create_travel_context():
    ctx = create_travel_context(10, 20)
    assert ctx["cur_x"] == 10
    assert ctx["cur_y"] == 20
    assert ctx["status"] == TaxiState.PENDING_PICKUP
    assert ctx["waiting_time_units"] is None
    assert ctx["travel_time_units"] is None


def test_get_random_wait_time(monkeypatch):
    monkeypatch.setattr(settings, "min_sleep", 1)
    monkeypatch.setattr(settings, "max_sleep", 5)
    val = get_random_wait_time()
    assert 1 <= val <= 5


@pytest.mark.asyncio
async def test_poll_taxi_info_success():
    mock_session = AsyncMock()
    with patch("worker.taxi_worker.get_taxi_info", AsyncMock(return_value={"ok": True})) as mock_get:
        result = await poll_taxi_info(mock_session, "id123")
        assert result == {"ok": True}
        mock_get.assert_awaited_once()


@pytest.mark.asyncio
async def test_poll_taxi_info_failure_logs_warning(caplog):
    with patch("worker.taxi_worker.get_taxi_info", AsyncMock(side_effect=Exception("fail"))):
        result = await poll_taxi_info(AsyncMock(), "id123")
        assert result == {}
        assert "polling failed" in caplog.text


@pytest.mark.asyncio
async def test_travel_with_order(monkeypatch):
    info = {
        "cur_order_id": "order123",
        "src_x": 2,
        "src_y": 2,
        "dst_x": 3,
        "dst_y": 3,
    }
    global cur_y
    global cur_x
    cur_x = 3
    cur_y = 3

    monkeypatch.setattr(worker, "get_random_wait_time", lambda : 1)
    monkeypatch.setattr(worker, "poll_taxi_info", AsyncMock(return_value=info))
    monkeypatch.setattr(worker, "post_status", AsyncMock())
    monkeypatch.setattr(asyncio, "sleep", AsyncMock())

    mock_session = AsyncMock()
    result = await travel(mock_session, "worker-1")

    assert result["status"] == TaxiState.DELIVERED
    assert result["waiting_time_units"] > 0
    assert result["travel_time_units"] > 0
    assert cur_x == result["cur_x"]
    assert cur_y == result["cur_y"]


@pytest.mark.asyncio
async def test_travel_without_order(monkeypatch):
    monkeypatch.setattr(worker, "get_taxi_info", AsyncMock(return_value={"cur_order_id": None}))
    result = await travel(AsyncMock(), "worker-1")
    assert result is None
