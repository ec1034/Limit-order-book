from collections import defaultdict

from src.order import Order, Side


class OrderBook:

    def __init__(self):
        self.bids = defaultdict(list)
        self.asks = defaultdict(list)

    def add_order(self, order):

        if order.side == Side.BUY:
            self.bids[order.price].append(order)

        else:
            self.asks[order.price].append(order)

    def best_bid(self):

        if not self.bids:
            return None

        return max(self.bids.keys())

    def best_ask(self):

        if not self.asks:
            return None

        return min(self.asks.keys())

    def spread(self):

        bid = self.best_bid()
        ask = self.best_ask()

        if bid is None or ask is None:
            return None

        return ask - bid

    def cancel_order(self, order_id):

        for price, orders in self.bids.items():

            for order in orders:

                if order.order_id == order_id:

                    orders.remove(order)

                    if len(orders) == 0:
                        del self.bids[price]

                    return True

        for price, orders in self.asks.items():

            for order in orders:

                if order.order_id == order_id:

                    orders.remove(order)

                    if len(orders) == 0:
                        del self.asks[price]

                    return True

        return False