from application.db.model.order import OrderModel

from application.db.model.order import OrderState


def test_order_states():
    order = OrderModel()
    order.cancel()
    assert order.state == OrderState.CANCELED

    order.close()
    assert order.state == OrderState.CLOSED