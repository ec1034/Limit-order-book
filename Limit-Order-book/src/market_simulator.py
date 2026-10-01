import random

from src.order import Order, Side, OrderType
from src.order_book import OrderBook
from src.matching_engine import MatchingEngine
from src.metrics import MarketSnapshot


class MarketSimulator:

    def __init__(
    self,
    starting_price=100.0,
    seed=None,
    buy_probability=0.5
    ):

        self.starting_price = starting_price
        self.current_price = starting_price
        self.buy_probability = buy_probability

        self.order_id = 1
        self.timestamp = 0

        if seed is not None:
            random.seed(seed)

        self.order_book = OrderBook()
        self.engine = MatchingEngine(self.order_book)

        self.trades = []
        self.history = []

    def generate_order(self):

        if random.random() < self.buy_probability:
            side = Side.BUY
        else:
            side = Side.SELL

        order_type = random.choice([
            OrderType.LIMIT,
            OrderType.MARKET
        ])

        quantity = random.randint(1, 20)

        if order_type == OrderType.LIMIT:

            price_change = random.uniform(-1.0, 1.0)

            price = round(
                self.current_price + price_change,
                2
            )

        else:

            price = 0

        order = Order(
            order_id=self.order_id,
            side=side,
            order_type=order_type,
            price=price,
            quantity=quantity,
            timestamp=self.timestamp
        )

        self.order_id += 1
        self.timestamp += 1

        return order

    def step(self):

        order = self.generate_order()

        new_trades = self.engine.submit_order(order)

        self.trades.extend(new_trades)

        if new_trades:

            last_trade = new_trades[-1]

            self.current_price = last_trade.price

        best_bid = self.order_book.best_bid()
        best_ask = self.order_book.best_ask()

        if best_bid is not None and best_ask is not None:
            mid_price = (best_bid + best_ask) / 2
            spread = best_ask - best_bid
        else:
            mid_price = None
            spread = None

        trade_price = None
        trade_volume = 0
        buy_volume = 0
        sell_volume = 0

        for trade in new_trades:

            trade_price = trade.price
            trade_volume += trade.quantity

            if trade.buy_order_id == order.order_id:
                buy_volume += trade.quantity

            if trade.sell_order_id == order.order_id:
                sell_volume += trade.quantity

        snapshot = MarketSnapshot(
            timestamp=self.timestamp - 1,
            best_bid=best_bid,
            best_ask=best_ask,
            mid_price=mid_price,
            spread=spread,
            trade_price=trade_price,
            trade_volume=trade_volume,
            buy_volume=buy_volume,
            sell_volume=sell_volume
        )

        self.history.append(snapshot)

        return order, new_trades

    def run(self, steps):

        for _ in range(steps):

            self.step()

    def get_mid_price(self):

        bid = self.order_book.best_bid()
        ask = self.order_book.best_ask()

        if bid is None or ask is None:
            return None

        return (bid + ask) / 2

    def get_history(self):

        data = []

        for snapshot in self.history:

            data.append({
                "timestamp": snapshot.timestamp,
                "best_bid": snapshot.best_bid,
                "best_ask": snapshot.best_ask,
                "mid_price": snapshot.mid_price,
                "spread": snapshot.spread,
                "trade_price": snapshot.trade_price,
                "trade_volume": snapshot.trade_volume,
                "buy_volume": snapshot.buy_volume,
                "sell_volume": snapshot.sell_volume
            })

        return data