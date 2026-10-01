from src.order import Order, Side, OrderType


class MarketMaker:

    def __init__(
        self,
        engine,
        order_book,
        spread=1.0,
        order_size=10,
        max_inventory=100
    ):

        self.engine = engine
        self.order_book = order_book

        self.spread = spread
        self.order_size = order_size
        self.max_inventory = max_inventory

        self.inventory = 0
        self.cash = 0.0

        self.order_id = 1000000
        self.timestamp = 0

    def quote(self, mid_price):

        bid_price = mid_price - self.spread / 2
        ask_price = mid_price + self.spread / 2

        return bid_price, ask_price

    def submit_quotes(self, mid_price):

        bid_price, ask_price = self.quote(
            mid_price
        )

        trades = []

        if self.inventory < self.max_inventory:

            buy_order = Order(
                order_id=self.order_id,
                side=Side.BUY,
                order_type=OrderType.LIMIT,
                price=bid_price,
                quantity=self.order_size,
                timestamp=self.timestamp
            )

            self.order_id += 1

            new_trades = self.engine.submit_order(
                buy_order
            )

            trades.extend(new_trades)

            for trade in new_trades:

                self.inventory += trade.quantity
                self.cash -= (
                    trade.price * trade.quantity
                )

        if self.inventory > -self.max_inventory:

            sell_order = Order(
                order_id=self.order_id,
                side=Side.SELL,
                order_type=OrderType.LIMIT,
                price=ask_price,
                quantity=self.order_size,
                timestamp=self.timestamp
            )

            self.order_id += 1

            new_trades = self.engine.submit_order(
                sell_order
            )

            trades.extend(new_trades)

            for trade in new_trades:

                self.inventory -= trade.quantity
                self.cash += (
                    trade.price * trade.quantity
                )

        self.timestamp += 1

        return trades

    def mark_to_market(self, price):

        return (
            self.cash +
            self.inventory * price
        )

    def reset(self):

        self.inventory = 0
        self.cash = 0.0