from application.db.model.common import Position
from application.db.model.order import OrderModel
from application.db.model.taxi import TaxiModel, TaxiStatus
from application.db.util import with_session, with_readonly_session
from application.dto.dispatch import TaxiRegisterWorkerRequestDto, TaxiUpdateStatusRequestDto
from application.repositories.taxis import save_taxi, find_closest_available_taxi, find_taxi
from application.services.trip_service import update_trip_data
from infrastructure.config.logs import log

logger = log.getChild(__name__)


async def register_taxi(taxi_id: str, taxi_data: TaxiRegisterWorkerRequestDto) -> TaxiModel:
    taxi = TaxiModel(taxi_id=taxi_id, status=TaxiStatus.DELIVERED, cur=Position(x=taxi_data.cur_x, y=taxi_data.cur_y))
    await persist_taxi(taxi)
    return taxi


async def update_taxi_status(taxi_id: str, taxi_data: TaxiUpdateStatusRequestDto) -> TaxiModel | None:
    taxi = await find_taxi_by_id(taxi_id)
    if not taxi:
        logger.warn(f"Failed taxi status updated taxi_id: {taxi_id}")
        return taxi
    taxi.update_position(taxi_data)
    await persist_taxi(taxi)
    if taxi.order:
        await update_trip_data(taxi.order.order_id, taxi_data.waiting_time_units, taxi_data.travel_time_units)
    return taxi


@with_session
async def find_taxi_by_id(taxi_id: str, session) -> TaxiModel | None:
    return await find_taxi(session, taxi_id)


@with_session
async def persist_taxi(taxi: TaxiModel, session):
    return await save_taxi(session, taxi)

async def assign_taxi(order: OrderModel, taxi: TaxiModel) -> None:
    taxi.assign(order)
    await persist_taxi(taxi)

@with_readonly_session
async def find_closest_taxi(src_x: int, src_y: int, session) -> TaxiModel:
    return await find_closest_available_taxi(session, src_x, src_y)
