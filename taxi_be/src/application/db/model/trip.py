from datetime import datetime

from sqlalchemy import String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from application.db.model.order import OrderModel
from application.db.model.taxi import TaxiModel
from infrastructure.db.config import Base, CommonMixin


class TripModel(CommonMixin, Base):
    trip_id: Mapped[str] = mapped_column(String(64), unique=True, index=True, nullable=False)
    order_id: Mapped[int | None] = mapped_column(
        ForeignKey("ordermodels.id"), unique=True, nullable=True
    )
    taxi_id: Mapped[int | None] = mapped_column(
        ForeignKey("taximodels.id"), unique=True, nullable=True
    )
    order: Mapped[OrderModel | None] = relationship(
        OrderModel,
        uselist=False,
        lazy="joined",
        cascade=None
    )
    taxi: Mapped[TaxiModel | None] = relationship(
        TaxiModel,
        uselist=False,
        lazy="joined",
        cascade=None
    )

    waiting_time: Mapped[datetime | None] = mapped_column(nullable=True)
    travel_time: Mapped[datetime | None] = mapped_column(nullable=True)
