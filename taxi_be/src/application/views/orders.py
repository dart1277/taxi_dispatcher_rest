from application.db.model.order import OrderModel
from application.db.util import with_session
from application.dto.dispatch import OrderResponseDto
from application.repositories.orders import find_orders


@with_session
async def all_orders(session) -> list[OrderModel]:
    return await find_orders(session)


def to_order_dto(order: OrderModel) -> OrderResponseDto:
    return OrderResponseDto(
        order_id=order.order_id,
        user_id=order.user_id,
        state=order.state,
        src_x=order.src.x,
        src_y=order.src.y,
        dst_x=order.dst.x,
        dst_y=order.dst.y,
    )


def to_order_dtos(orders: list[OrderModel]) -> list[OrderResponseDto]:
    return [to_order_dto(order) for order in orders]
