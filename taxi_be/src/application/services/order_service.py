from application.db.model.order import OrderModel
from application.db.util import with_session
from application.dto.dispatch import PlaceOrderRequestDto
from application.repositories.orders import save_order, find_order, update_order
from application.services.taxi_service import find_closest_taxi, assign_taxi
from application.services.trip_service import start_trip
from infrastructure.config.logs import log

logger = log.getChild(__name__)


async def place_order(dto: PlaceOrderRequestDto) -> OrderModel:
    order = OrderModel.create(dto)
    await save_placed_order(order)
    await try_assign_taxi(order)
    return order


async def try_assign_taxi(order: OrderModel) -> None:
    taxi = None
    try:
        taxi = await find_closest_taxi(order.src.x, order.src.y)
        if taxi:
            await assign_taxi(order, taxi)
            await start_new_trip(order, taxi)
            logger.info(f"Taxi assigned to order: {order.order_id}")
    except Exception as e:
        logger.warn(f"Taxi assignment failed {str(e)}")
    if not taxi:
        logger.warn(f"No available taxi found for order {order.order_id}, order canceled")
        await cancel_order(order)


async def start_new_trip(order, taxi):
    trip = await start_trip(order, taxi)
    if trip:
        logger.info(f"Trip {trip.trip_id} started")


@with_session
async def save_placed_order(order: OrderModel, session) -> None:
    await save_order(session, order)


@with_session
async def close_order(order_id: str, session) -> OrderModel:
    order = await find_order(session, order_id)
    if order:
        order.close()
        order = await update_order(session, order)
    return order


@with_session
async def cancel_order(order: OrderModel, session) -> OrderModel:
    order.cancel()
    order = await update_order(session, order)
    return order
