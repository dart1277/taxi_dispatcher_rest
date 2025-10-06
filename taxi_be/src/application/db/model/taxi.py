from enum import StrEnum

from sqlalchemy import String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, composite, relationship

from application.db.model.common import Position
from application.db.model.order import OrderModel
from infrastructure.db.config import Base, CommonMixin


class TaxiStatus(StrEnum):
    OFFLINE = "OFFLINE"
    DELIVERED = "DELIVERED"  # DELIVERED is an alias for IDLE, this might need to be changed in the future
    PENDING_PICKUP = "PENDING_PICKUP"
    PICKUP = "PICKUP"
    DRIVING = "DRIVING"


class TaxiModel(CommonMixin, Base):
    taxi_id: Mapped[str] = mapped_column(String(64), unique=True, index=True, nullable=False)
    status: Mapped[TaxiStatus] = mapped_column(String(32), nullable=False, index=True)
    order_id: Mapped[int | None] = mapped_column(
        ForeignKey("ordermodels.id"), unique=True, nullable=True
    )
    order: Mapped[OrderModel | None] = relationship(
        OrderModel,
        uselist=False,
        lazy="joined",
        cascade=None
    )
    cur_x: Mapped[int | None] = mapped_column(nullable=True)
    cur_y: Mapped[int | None] = mapped_column(nullable=True)

    cur = composite(Position, cur_x, cur_y)
