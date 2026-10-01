from src.order import Order, Side, OrderType
from src.order_book import OrderBook
from src.matching_engine import MatchingEngine


def test_orders_match():

    book = OrderBook()
    engine = MatchingEngine(book)

    sell_order = Order(
        order_id=1,
        side=Side.SELL,
        order_type=OrderType.LIMIT,
        price=100.0,
        quantity=50,
        timestamp=1
    )

    buy_order = Order(
        order_id=2,
        side=Side.BUY,
        order_type=OrderType.LIMIT,
        price=100.0,
        quantity=50,
        timestamp=2
    )

    engine.submit_order(sell_order)

    trades = engine.submit_order(buy_order)

    assert len(trades) == 1
    assert trades[0].price == 100.0
    assert trades[0].quantity == 50

    assert buy_order.remaining_quantity == 0
    assert sell_order.remaining_quantity == 0
def test_partial_fill():

    book = OrderBook()
    engine = MatchingEngine(book)

    sell_order = Order(
        order_id=1,
        side=Side.SELL,
        order_type=OrderType.LIMIT,
        price=100.0,
        quantity=100,
        timestamp=1
    )

    buy_order = Order(
        order_id=2,
        side=Side.BUY,
        order_type=OrderType.LIMIT,
        price=100.0,
        quantity=40,
        timestamp=2
    )

    engine.submit_order(sell_order)

    trades = engine.submit_order(buy_order)

    assert len(trades) == 1
    assert trades[0].quantity == 40

    assert buy_order.remaining_quantity == 0
    assert sell_order.remaining_quantity == 60

def test_price_time_priority():

    book = OrderBook()
    engine = MatchingEngine(book)

    first_buy = Order(
        order_id=1,
        side=Side.BUY,
        order_type=OrderType.LIMIT,
        price=100.0,
        quantity=50,
        timestamp=1
    )

    second_buy = Order(
        order_id=2,
        side=Side.BUY,
        order_type=OrderType.LIMIT,
        price=100.0,
        quantity=50,
        timestamp=2
    )

    sell_order = Order(
        order_id=3,
        side=Side.SELL,
        order_type=OrderType.LIMIT,
        price=100.0,
        quantity=60,
        timestamp=3
    )

    engine.submit_order(first_buy)
    engine.submit_order(second_buy)

    trades = engine.submit_order(sell_order)

    assert trades[0].buy_order_id == 1
    assert trades[0].quantity == 50

    assert trades[1].buy_order_id == 2
    assert trades[1].quantity == 10

def test_market_buy_multiple_levels():

    book = OrderBook()
    engine = MatchingEngine(book)

    sell1 = Order(
        order_id=1,
        side=Side.SELL,
        order_type=OrderType.LIMIT,
        price=100.0,
        quantity=50,
        timestamp=1
    )

    sell2 = Order(
        order_id=2,
        side=Side.SELL,
        order_type=OrderType.LIMIT,
        price=101.0,
        quantity=70,
        timestamp=2
    )

    sell3 = Order(
        order_id=3,
        side=Side.SELL,
        order_type=OrderType.LIMIT,
        price=102.0,
        quantity=100,
        timestamp=3
    )

    engine.submit_order(sell1)
    engine.submit_order(sell2)
    engine.submit_order(sell3)

    market_buy = Order(
        order_id=4,
        side=Side.BUY,
        order_type=OrderType.MARKET,
        price=0,
        quantity=150,
        timestamp=4
    )

    trades = engine.submit_order(market_buy)

    assert len(trades) == 3

    assert trades[0].price == 100.0
    assert trades[0].quantity == 50

    assert trades[1].price == 101.0
    assert trades[1].quantity == 70

    assert trades[2].price == 102.0
    assert trades[2].quantity == 30

    assert market_buy.remaining_quantity == 0

def test_market_buy_runs_out_of_liquidity():

    book = OrderBook()
    engine = MatchingEngine(book)

    sell1 = Order(
        order_id=1,
        side=Side.SELL,
        order_type=OrderType.LIMIT,
        price=100.0,
        quantity=50,
        timestamp=1
    )

    sell2 = Order(
        order_id=2,
        side=Side.SELL,
        order_type=OrderType.LIMIT,
        price=101.0,
        quantity=30,
        timestamp=2
    )

    engine.submit_order(sell1)
    engine.submit_order(sell2)

    market_buy = Order(
        order_id=3,
        side=Side.BUY,
        order_type=OrderType.MARKET,
        price=0,
        quantity=100,
        timestamp=3
    )

    trades = engine.submit_order(market_buy)

    assert len(trades) == 2
    assert market_buy.remaining_quantity == 20

def test_market_order_does_not_rest():

    book = OrderBook()
    engine = MatchingEngine(book)

    market_buy = Order(
        order_id=1,
        side=Side.BUY,
        order_type=OrderType.MARKET,
        price=0,
        quantity=100,
        timestamp=1
    )

    trades = engine.submit_order(market_buy)

    assert len(trades) == 0
    assert market_buy.remaining_quantity == 100

    assert book.best_bid() is None

def test_market_sell_multiple_levels():

    book = OrderBook()
    engine = MatchingEngine(book)

    buy1 = Order(
        order_id=1,
        side=Side.BUY,
        order_type=OrderType.LIMIT,
        price=100.0,
        quantity=50,
        timestamp=1
    )

    buy2 = Order(
        order_id=2,
        side=Side.BUY,
        order_type=OrderType.LIMIT,
        price=99.0,
        quantity=70,
        timestamp=2
    )

    buy3 = Order(
        order_id=3,
        side=Side.BUY,
        order_type=OrderType.LIMIT,
        price=98.0,
        quantity=100,
        timestamp=3
    )

    engine.submit_order(buy1)
    engine.submit_order(buy2)
    engine.submit_order(buy3)

    market_sell = Order(
        order_id=4,
        side=Side.SELL,
        order_type=OrderType.MARKET,
        price=0,
        quantity=150,
        timestamp=4
    )

    trades = engine.submit_order(market_sell)

    assert len(trades) == 3

    assert trades[0].price == 100.0
    assert trades[0].quantity == 50

    assert trades[1].price == 99.0
    assert trades[1].quantity == 70

    assert trades[2].price == 98.0
    assert trades[2].quantity == 30

    assert market_sell.remaining_quantity == 0