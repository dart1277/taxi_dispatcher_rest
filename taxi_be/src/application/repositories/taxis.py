from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession

from application.db.model.taxi import TaxiModel, TaxiStatus


async def save_taxi(session: AsyncSession, taxi: TaxiModel) -> None:
    session.add(taxi)


async def find_taxis(session: AsyncSession) -> list[TaxiModel]:
    res = await session.execute(select(TaxiModel))
    return list(res.scalars().all())


async def find_taxi(session: AsyncSession, taxi_id: str) -> TaxiModel | None:
    res = await session.execute(select(TaxiModel).filter_by(taxi_id=taxi_id))
    return res.scalars().one_or_none()


async def find_closest_available_taxi(session: AsyncSession, src_x: int, src_y: int) -> TaxiModel:
    distance = func.abs(TaxiModel.cur_x - src_x) + func.abs(TaxiModel.cur_y - src_y)

    stmt = (
        select(TaxiModel)
        .where(TaxiModel.status == TaxiStatus.DELIVERED)
        .order_by(distance)
        .limit(1)
    )

    result = await session.execute(stmt)
    return result.scalar_one_or_none()
