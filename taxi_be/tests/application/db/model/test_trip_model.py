from datetime import datetime

from application.db.model.trip import TripModel


def test_trip_start(order_model, taxi_model):
    trip = TripModel.start(order_model, taxi_model)
    assert trip.trip_id == order_model.order_id
    assert trip.taxi_id == taxi_model.id
    assert trip.order_id == order_model.id
    assert isinstance(trip.start_time, datetime)


def test_trip_update_details():
    trip = TripModel(
        trip_id="trip-1",
        order_id=1,
        taxi_id=1,
        waiting_time=None,
        travel_time=None
    )
    trip.update_details(waiting_time_units=12.5, travel_time_units=25.0)
    assert trip.waiting_time == 12.5
    assert trip.travel_time == 25.0


def test_trip_update_details_partial():
    trip = TripModel(
        trip_id="trip-2",
        order_id=2,
        taxi_id=2
    )
    trip.update_details(waiting_time_units=None, travel_time_units=30.0)
    assert trip.travel_time == 30.0
    assert trip.waiting_time is None
