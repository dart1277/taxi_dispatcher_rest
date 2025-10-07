import pytest

from application.db.model.common import TaxiStatus
from application.dto.dispatch import TaxiUpdateStatusRequestDto


def test_taxi_assign(order_model, taxi_model):
    taxi_model.assign(order_model)
    assert taxi_model.order_id == order_model.id
    assert taxi_model.status == TaxiStatus.PENDING_PICKUP


def test_taxi_update_position_valid_with_order(order_model, taxi_model):
    taxi_model.assign(order_model)
    dto = TaxiUpdateStatusRequestDto(
        cur_x=50,
        cur_y=60,
        status=TaxiStatus.DELIVERED,
        waiting_time_units=None,
        travel_time_units=None
    )

    taxi_model.update_position(dto)
    assert taxi_model.cur_x == 50
    assert taxi_model.cur_y == 60
    assert taxi_model.status == TaxiStatus.DELIVERED

    assert taxi_model.order_id is None


def test_taxi_update_position_invalid_status_no_order(taxi_model):
    dto = TaxiUpdateStatusRequestDto(
        cur_x=5,
        cur_y=5,
        status=TaxiStatus.PICKUP,
        waiting_time_units=None,
        travel_time_units=None
    )
    with pytest.raises(RuntimeError, match="Invalid taxi status"):
        taxi_model.update_position(dto)


def test_taxi_update_position_offline_without_order_ok(taxi_model):
    dto = TaxiUpdateStatusRequestDto(
        cur_x=10,
        cur_y=20,
        status=TaxiStatus.OFFLINE,
        waiting_time_units=None,
        travel_time_units=None
    )
    taxi_model.update_position(dto)
    assert taxi_model.cur_x == 10
    assert taxi_model.cur_y == 20
    assert taxi_model.status == TaxiStatus.OFFLINE
