from application.db.model.common import Position
from application.db.model.taxi import TaxiModel, TaxiStatus
from application.db.util import with_session, with_readonly_session
from application.dto.dispatch import TaxiRegisterWorkerRequestDto
from application.repositories.taxis import save_taxi, find_closest_available_taxi


@with_session
async def register_taxi(taxi_id: str, taxi_data: TaxiRegisterWorkerRequestDto, session) -> TaxiModel:
    taxi = TaxiModel(taxi_id=taxi_id, status=TaxiStatus.DELIVERED, cur=Position(x=taxi_data.cur_x, y=taxi_data.cur_y))
    await save_taxi(session, taxi)
    return taxi


@with_readonly_session
async def find_closest_taxi(src_x: int, src_y: int, session) -> TaxiModel:
    return await find_closest_available_taxi(session, src_x, src_y)
