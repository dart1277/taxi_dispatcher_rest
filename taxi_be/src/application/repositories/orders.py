from sqlalchemy import select

from application.db.model.order import OrderModel
from infrastructure.db.config import AsyncSession


async def save_order(session: AsyncSession, order: OrderModel) -> None:
    session.add(order)


async def update_order(session: AsyncSession, order: OrderModel) -> OrderModel:
    order_model = await session.merge(order)
    return order_model


async def find_orders(session: AsyncSession) -> list[OrderModel]:
    res = await session.execute(select(OrderModel))
    return list(res.scalars().all())


async def find_order(session: AsyncSession, order_id: str) -> OrderModel | None:
    res = await session.execute(select(OrderModel).filter_by(order_id=order_id))
    return res.scalars().one_or_none()
