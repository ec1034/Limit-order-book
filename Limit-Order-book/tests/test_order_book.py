from src.order import Order, Side, OrderType
from src.order_book import OrderBook


def test_add_orders():

    book = OrderBook()

    buy_order = Order(
        order_id=1,
        side=Side.BUY,
        order_type=OrderType.LIMIT,
        price=100.0,
        quantity=50,
        timestamp=1
    )

    sell_order = Order(
        order_id=2,
        side=Side.SELL,
        order_type=OrderType.LIMIT,
        price=101.0,
        quantity=50,
        timestamp=2
    )

    book.add_order(buy_order)
    book.add_order(sell_order)

    assert book.best_bid() == 100.0
    assert book.best_ask() == 101.0
    assert book.spread() == 1.0

def test_best_prices():

    book = OrderBook()

    book.add_order(Order(
        order_id=1,
        side=Side.BUY,
        order_type=OrderType.LIMIT,
        price=99.0,
        quantity=10,
        timestamp=1
    ))

    book.add_order(Order(
        order_id=2,
        side=Side.BUY,
        order_type=OrderType.LIMIT,
        price=101.0,
        quantity=10,
        timestamp=2
    ))

    book.add_order(Order(
        order_id=3,
        side=Side.SELL,
        order_type=OrderType.LIMIT,
        price=103.0,
        quantity=10,
        timestamp=3
    ))

    book.add_order(Order(
        order_id=4,
        side=Side.SELL,
        order_type=OrderType.LIMIT,
        price=102.0,
        quantity=10,
        timestamp=4
    ))

    assert book.best_bid() == 101.0
    assert book.best_ask() == 102.0
    assert book.spread() == 1.0

def test_cancel_order():

    book = OrderBook()

    order = Order(
        order_id=1,
        side=Side.BUY,
        order_type=OrderType.LIMIT,
        price=100.0,
        quantity=50,
        timestamp=1
    )

    book.add_order(order)

    assert book.best_bid() == 100.0

    result = book.cancel_order(1)

    assert result is True
    assert book.best_bid() is None


def test_cancel_nonexistent_order():

    book = OrderBook()

    result = book.cancel_order(999)

    assert result is False

def test_cancel_preserves_other_orders():

    book = OrderBook()

    first_order = Order(
        order_id=1,
        side=Side.BUY,
        order_type=OrderType.LIMIT,
        price=100.0,
        quantity=50,
        timestamp=1
    )

    second_order = Order(
        order_id=2,
        side=Side.BUY,
        order_type=OrderType.LIMIT,
        price=100.0,
        quantity=30,
        timestamp=2
    )

    book.add_order(first_order)
    book.add_order(second_order)

    result = book.cancel_order(1)

    assert result is True

    assert book.best_bid() == 100.0
    assert len(book.bids[100.0]) == 1
    assert book.bids[100.0][0].order_id == 2