from uuid import uuid4

import pytest

from application.db.model.common import TaxiStatus
from application.db.model.order import OrderModel, OrderState
from application.db.model.taxi import TaxiModel


@pytest.fixture
def order_model():
    order = OrderModel(
        order_id=str(uuid4()),
        user_id="user123",
        state=OrderState.PLACED,
        src_x=1, src_y=2,
        dst_x=3, dst_y=4
    )
    order.id = 1
    return order


@pytest.fixture
def taxi_model():
    taxi = TaxiModel(
        taxi_id=str(uuid4()),
        status=TaxiStatus.DELIVERED,
        cur_x=0,
        cur_y=0
    )
    taxi.id = 10
    return taxi

