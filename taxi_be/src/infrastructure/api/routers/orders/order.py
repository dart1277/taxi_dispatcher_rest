from fastapi import APIRouter

from application.dto.dispatch import OrderResponseDto, PlaceOrderRequestDto
from application.services.order_service import place_order, cancel_order
from application.views.orders import to_order_dtos, all_orders, to_order_dto

router = APIRouter(
    prefix="/order",
    tags=["Order"]
)


@router.get("/", status_code=200)
async def get_orders() -> list[OrderResponseDto]:
    return to_order_dtos(await all_orders())


@router.post("/", status_code=201)
async def post_place_order(order_dto: PlaceOrderRequestDto) -> OrderResponseDto:
    order = await place_order(order_dto)
    return to_order_dto(order)
