from typing import List

from application.db.model.taxi import TaxiModel
from application.db.util import with_session
from application.dto.dispatch import TaxiResponseDto
from application.repositories.taxis import find_taxis, find_taxi


@with_session
async def all_taxis(session) -> List[TaxiModel]:
    return await find_taxis(session)


@with_session
async def get_taxi(taxi_id: str, session) -> TaxiModel:
    return await find_taxi(session, taxi_id)


def to_taxi_dto(taxi: TaxiModel) -> TaxiResponseDto | None:
    if not taxi:
        return None
    return TaxiResponseDto(
        taxi_id=taxi.taxi_id,
        cur_order_id=taxi.order.order_id if taxi.order_id else None,
        status=taxi.status,
        cur_x=taxi.cur.x if taxi.cur else None,
        cur_y=taxi.cur.y if taxi.cur else None,
        src_x=taxi.order.src.x if taxi.order_id else None,
        src_y=taxi.order.src.y if taxi.order_id else None,
        dst_x=taxi.order.dst.x if taxi.order_id else None,
        dst_y=taxi.order.dst.y if taxi.order_id else None,
    )


def to_taxi_dtos(taxis: list[TaxiModel]) -> list[TaxiResponseDto]:
    return [to_taxi_dto(taxi) for taxi in taxis]
