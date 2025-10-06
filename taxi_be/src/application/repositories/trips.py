from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from application.db.model.trip import TripModel


async def save_trip(session: AsyncSession, trip: TripModel) -> None:
    session.add(trip)


async def find_trips(session: AsyncSession) -> list[TripModel]:
    res = await session.execute(select(TripModel))
    return list(res.scalars().all())
