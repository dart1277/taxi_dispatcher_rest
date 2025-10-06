from application.db.model.common import Position, TaxiStatus
from application.db.model.order import OrderModel
from infrastructure.db.config import Base, CommonMixin
from sqlalchemy import String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, composite, relationship


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

    def update_position(self, data: "TaxiUpdateStatusRequestDto") -> None:

        if not self.order_id and data.status != TaxiStatus.DELIVERED and data.status != TaxiStatus.OFFLINE:
            raise RuntimeError(f"Invalid taxi status of {self.taxi_id} {data.status}")

        self.status = data.status
        self.cur_x = data.cur_x
        self.cur_y = data.cur_y
        if self.order_id and data.status == TaxiStatus.DELIVERED:
            self.order_id = None

    def assign(self, order: OrderModel):
        self.order_id = order.id
        self.status = TaxiStatus.PENDING_PICKUP
