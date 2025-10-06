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
        ForeignKey("taximodels.id"), nullable=True
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

    start_time: Mapped[datetime | None] = mapped_column(nullable=True)
    waiting_time: Mapped[float | None] = mapped_column(nullable=True)
    travel_time: Mapped[float | None] = mapped_column(nullable=True)

    def update_details(self, waiting_time_units: float, travel_time_units: float) -> None:
        if waiting_time_units:
            self.waiting_time = waiting_time_units
        if travel_time_units:
            self.travel_time = travel_time_units

    @classmethod
    def start(cls, order: OrderModel, taxi: TaxiModel) -> "TripModel":
        return cls(
            trip_id=order.order_id,
            taxi_id=taxi.id,
            order_id=order.id,
            start_time=datetime.now()
        )
