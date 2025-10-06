from fastapi import APIRouter
from fastapi.exceptions import HTTPException

from application.db.model.common import TaxiStatus
from application.dto.dispatch import TaxiResponseDto, TaxiUpdateStatusRequestDto, TaxiRegisterWorkerRequestDto
from application.services.order_service import close_order
from application.services.taxi_service import register_taxi, find_closest_taxi, update_taxi_status
from application.views.taxis import to_taxi_dtos, all_taxis, to_taxi_dto, get_taxi

router = APIRouter(
    prefix="/taxi",
    tags=["Taxi"]
)


@router.get("/", status_code=200)
async def get_taxis() -> list[TaxiResponseDto]:
    return to_taxi_dtos(await all_taxis())


@router.put("/status/{taxi_id}", status_code=202)
async def put_taxi_status(taxi_id: str, status: TaxiUpdateStatusRequestDto) -> None:
    taxi = await update_taxi_status(taxi_id, status)
    if taxi and status.status == TaxiStatus.DELIVERED:
        await close_order(taxi.order.order_id)
    if not taxi:
        raise HTTPException(status_code=404, detail="Not found")


@router.post("/register/{taxi_id}", status_code=202)
async def register_taxi_worker(taxi_id: str, taxi_data: TaxiRegisterWorkerRequestDto) -> TaxiResponseDto:
    return to_taxi_dto(await register_taxi(taxi_id, taxi_data))


@router.get("/closest", status_code=200)
async def get_closest_taxi(src_x: int, src_y: int) -> TaxiResponseDto:
    taxi = await find_closest_taxi(src_x, src_y)
    if not taxi:
        raise HTTPException(status_code=404, detail="Not found")
    return to_taxi_dto(taxi)


@router.get("/{taxi_id}", status_code=200)
async def poll_taxi(taxi_id: str) -> TaxiResponseDto:
    taxi = await get_taxi(taxi_id)
    if not taxi:
        raise HTTPException(status_code=404, detail="Not found")
    return to_taxi_dto(taxi)
