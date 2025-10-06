from typing import Annotated, Optional

from pydantic import Field, EmailStr, constr, field_validator

from application.db.model.taxi import TaxiStatus
from application.dto.base import DtoBaseModel
from infrastructure.config.settings import settings

IdField = Annotated[str, constr(min_length=1)]
TaxiPositionXField = Annotated[int, Field(..., ge=settings.min_pos_x, le=settings.max_pos_x)]
TaxiPositionYField = Annotated[int, Field(..., ge=settings.min_pos_y, le=settings.max_pos_y)]


class TaxiResponseDto(DtoBaseModel):
    taxi_id: IdField
    cur_order_id: IdField | None = None
    cur_x: TaxiPositionXField
    cur_y: TaxiPositionYField
    src_x: TaxiPositionXField | None = None
    src_y: TaxiPositionYField | None = None
    dst_x: TaxiPositionXField | None = None
    dst_y: TaxiPositionYField | None = None
    status: str


class TripResponseDto(DtoBaseModel):
    cur_x: TaxiPositionXField | None = None
    cur_y: TaxiPositionYField | None = None
    src_x: TaxiPositionXField | None = None
    src_y: TaxiPositionYField | None = None
    dst_x: TaxiPositionXField | None = None
    dst_y: TaxiPositionYField | None = None
    taxi_id: IdField | None = None
    order_id: IdField | None = None
    user_id: EmailStr | None = None
    waiting_time: float | None = None
    travel_time: float | None = None


class TripPositionResponseDto(DtoBaseModel):
    x: TaxiPositionXField | None = None
    y: TaxiPositionYField | None = None
    taxi_id: IdField
    user_id: EmailStr | None = None


class OrderResponseDto(DtoBaseModel):
    order_id: IdField
    user_id: EmailStr
    state: str
    src_x: TaxiPositionXField
    src_y: TaxiPositionYField
    dst_x: TaxiPositionXField
    dst_y: TaxiPositionYField


class PlaceOrderRequestDto(DtoBaseModel):
    user_id: EmailStr
    src_x: TaxiPositionXField
    src_y: TaxiPositionYField
    dst_x: TaxiPositionXField
    dst_y: TaxiPositionYField


class TaxiUpdateStatusRequestDto(DtoBaseModel):
    cur_x: TaxiPositionXField
    cur_y: TaxiPositionYField
    status: TaxiStatus
    waiting_time_units: Optional[Annotated[float, Field(ge=0)]]
    travel_time_units: Optional[Annotated[float, Field(ge=0)]]

    @field_validator("status", mode="before")
    def coerce_enum(cls, v):
        if isinstance(v, str):
            return TaxiStatus(v)
        return v


class TaxiRegisterWorkerRequestDto(DtoBaseModel):
    cur_x: TaxiPositionXField
    cur_y: TaxiPositionYField
