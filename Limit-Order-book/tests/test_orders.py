from src.order import Order, Side, OrderType


def test_create_order():

    order = Order(
        order_id=1,
        side=Side.BUY,
        order_type=OrderType.LIMIT,
        price=100.0,
        quantity=50,
        timestamp=1
    )

    assert order.order_id == 1
    assert order.side == Side.BUY
    assert order.order_type == OrderType.LIMIT
    assert order.price == 100.0
    assert order.quantity == 50
    assert order.remaining_quantity == 50