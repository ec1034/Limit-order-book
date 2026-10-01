from src.order import Order, Side, OrderType
from src.order_book import OrderBook
from src.matching_engine import MatchingEngine


book = OrderBook()
engine = MatchingEngine(book)


orders = [
    Order(1, Side.SELL, OrderType.LIMIT, 100, 10, 1),
    Order(2, Side.SELL, OrderType.LIMIT, 101, 20, 2),
    Order(3, Side.SELL, OrderType.LIMIT, 102, 50, 3)
]


for order in orders:
    engine.submit_order(order)


for quantity in [10, 20, 30, 60, 80]:

    book = OrderBook()
    engine = MatchingEngine(book)

    for order in orders:

        new_order = Order(
            order.order_id,
            order.side,
            order.order_type,
            order.price,
            order.quantity,
            order.timestamp
        )

        engine.submit_order(new_order)

    market_buy = Order(
        100,
        Side.BUY,
        OrderType.MARKET,
        0,
        quantity,
        100
    )

    trades = engine.submit_order(
        market_buy
    )

    total_value = sum(
        trade.price * trade.quantity
        for trade in trades
    )

    total_quantity = sum(
        trade.quantity
        for trade in trades
    )

    if total_quantity > 0:

        average_price = (
            total_value / total_quantity
        )

        print(
            "Quantity:",
            quantity,
            "Average execution:",
            average_price
        )