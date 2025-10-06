from application.db.model.order import OrderModel
from application.db.model.taxi import TaxiModel
from application.db.model.trip import TripModel
from application.db.util import with_session
from application.repositories.trips import find_trip, save_trip
from infrastructure.config.logs import log

logger = log.getChild(__name__)


async def start_trip(order: OrderModel, taxi: TaxiModel) -> TripModel:
    trip = TripModel.start(order, taxi)
    await persist_trip(trip)
    return trip


async def update_trip_data(trip_id: str, waiting_time_units: float, travel_time_units: float) -> None:
    trip = await find_trip_by_id(trip_id)
    if not trip:
        logger.warn(f"Failed to find trip with id {trip_id}")
        return
    trip.update_details(waiting_time_units, travel_time_units)
    await persist_trip(trip)


@with_session
async def find_trip_by_id(trip_id: str, session) -> TripModel | None:
    return await find_trip(session, trip_id)


@with_session
async def persist_trip(trip: TripModel, session) -> None:
    await save_trip(session, trip)
