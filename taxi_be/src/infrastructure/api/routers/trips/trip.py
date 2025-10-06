from fastapi import APIRouter

from application.dto.dispatch import TripResponseDto, TripPositionResponseDto
from application.views.trips import to_trip_dtos, all_trips, to_trip_position_dtos

router = APIRouter(
    prefix="/trip",
    tags=["Trip"]
)


@router.get("/", status_code=200)
async def get_trips() -> list[TripResponseDto]:
    return to_trip_dtos(await all_trips())


@router.get("/positions", status_code=200)
async def get_trip_positions() -> list[TripPositionResponseDto]:
    return to_trip_position_dtos(await all_trips())
