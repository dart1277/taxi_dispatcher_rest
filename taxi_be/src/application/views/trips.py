from typing import List

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
        taxi_id=trip.taxi_id,
        order_id=trip.order_id,
        user_id=trip.order.user_id if trip.order_id else None,
        waiting_time=trip.waiting_time.isoformat() if trip.waiting_time else None,
        travel_time=trip.travel_time.isoformat() if trip.travel_time else None,
    )


def to_trip_position_dtos(trips: list[TripModel]) -> list[TripPositionResponseDto]:
    return [
        TripPositionResponseDto(taxi_id=trip.taxi_id,
                                user_id=trip.order.user_id if trip.order else None,
                                x=trip.taxi.cur.x if trip.taxi else None,
                                y=trip.taxi.cur.y if trip.taxi else None)
        for trip in trips]


def to_trip_dtos(trips: list[TripModel]) -> list[TripResponseDto]:
    return [to_trip_dto(trip) for trip in trips]
