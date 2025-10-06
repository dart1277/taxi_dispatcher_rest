from application.db.model.order import OrderModel
from application.db.util import with_session
from application.dto.dispatch import PlaceOrderRequestDto
from application.repositories.orders import save_order, find_order, update_order


@with_session
async def place_order(dto: PlaceOrderRequestDto, session) -> OrderModel:
    order = OrderModel.create(dto)
    await save_order(session, order)
    return order


@with_session
async def close_order(order_id: str, session) -> OrderModel:
    order = await find_order(session, order_id)
    order.close()
    order = await update_order(session, order)
    return order


@with_session
async def cancel_order(order_id: str, session) -> OrderModel:
    order = await find_order(session, order_id)
    order.cancel()
    order = await update_order(session, order)
    return order
