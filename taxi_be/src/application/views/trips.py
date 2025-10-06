from typing import List

from application.db.model.order import OrderState
from application.db.model.trip import TripModel
from application.db.util import with_session
from application.dto.dispatch import TripResponseDto, TripPositionResponseDto
from application.repositories.trips import find_trips


@with_session
async def all_trips(session) -> List[TripModel]:
    return await find_trips(session)


def to_trip_dto(trip: TripModel) -> TripResponseDto:
    return TripResponseDto(
        cur_x=trip.taxi.cur.x if trip.taxi_id else None,
        cur_y=trip.taxi.cur.y if trip.taxi_id else None,
        src_x=trip.order.src.x if trip.order_id else None,
        src_y=trip.order.src.y if trip.order_id else None,
        dst_x=trip.order.dst.x if trip.order_id else None,
        dst_y=trip.order.dst.y if trip.order_id else None,
        taxi_id=trip.taxi.taxi_id if trip.taxi_id else None,
        order_id=trip.order.order_id if trip.order_id else None,
        user_id=trip.order.user_id if trip.order_id else None,
        waiting_time=trip.waiting_time if trip.waiting_time else None,
        travel_time=trip.travel_time if trip.travel_time else None,
    )


def to_trip_position_dtos(trips: list[TripModel]) -> list[TripPositionResponseDto]:
    return [
        TripPositionResponseDto(taxi_id=trip.taxi.taxi_id if trip.taxi_id else None,
                                user_id=trip.order.user_id if trip.order_id else None,
                                x=trip.taxi.cur.x if trip.taxi_id else None,
                                y=trip.taxi.cur.y if trip.taxi_id else None)
        for trip in trips if trip.order_id and trip.order.state == OrderState.PLACED]


def to_trip_dtos(trips: list[TripModel]) -> list[TripResponseDto]:
    return [to_trip_dto(trip) for trip in trips]
