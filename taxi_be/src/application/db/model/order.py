import uuid
from enum import StrEnum

from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, composite

from application.db.model.common import Position
from infrastructure.db.config import Base, CommonMixin


class OrderState(StrEnum):
    PLACED = "PLACED"
    CANCELED = "CANCELED"
    CLOSED = "CLOSED"


class OrderModel(CommonMixin, Base):
    order_id: Mapped[str] = mapped_column(String(64), unique=True, index=True, nullable=False)
    user_id: Mapped[str] = mapped_column(String(128), index=True, nullable=False)
    state: Mapped[OrderState] = mapped_column(String(32), nullable=False, index=True)

    src_x: Mapped[int] = mapped_column(nullable=False)
    src_y: Mapped[int] = mapped_column(nullable=False)
    dst_x: Mapped[int] = mapped_column(nullable=False)
    dst_y: Mapped[int] = mapped_column(nullable=False)

    src = composite(Position, src_x, src_y)
    dst = composite(Position, dst_x, dst_y)

    def cancel(self):
        self.state = OrderState.CANCELED

    def close(self):
        self.state = OrderState.CLOSED

    @staticmethod
    def create(dto: "PlaceOrderRequestDto") -> "OrderModel":
        return OrderModel(
            order_id=str(uuid.uuid4()),
            user_id=dto.user_id,
            state=OrderState.PLACED,
            src_x=dto.src_x,
            src_y=dto.src_y,
            dst_x=dto.dst_x,
            dst_y=dto.dst_y,
        )
