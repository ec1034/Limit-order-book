from src.order import Order, Side, OrderType
from src.trade import Trade


class MatchingEngine:

    def __init__(self, order_book):

        self.order_book = order_book
        self.next_trade_id = 1

    def submit_order(self, order):

        trades = []

        if order.side == Side.BUY:
            trades = self._match_buy_order(order)
        else:
            trades = self._match_sell_order(order)

        if order.remaining_quantity > 0:

            if order.order_type == OrderType.LIMIT:
                self.order_book.add_order(order)

        return trades

    def _match_buy_order(self, order):

        trades = []

        while order.remaining_quantity > 0:

            best_ask = self.order_book.best_ask()

            if best_ask is None:
                break

            if order.order_type == OrderType.LIMIT:
                if order.price < best_ask:
                    break

            ask_queue = self.order_book.asks[best_ask]

            resting_order = ask_queue[0]

            traded_quantity = min(
                order.remaining_quantity,
                resting_order.remaining_quantity
            )

            trade = Trade(
                trade_id=self.next_trade_id,
                buy_order_id=order.order_id,
                sell_order_id=resting_order.order_id,
                price=best_ask,
                quantity=traded_quantity,
                timestamp=order.timestamp
            )

            trades.append(trade)

            self.next_trade_id += 1

            order.remaining_quantity -= traded_quantity
            resting_order.remaining_quantity -= traded_quantity

            if resting_order.remaining_quantity == 0:

                ask_queue.pop(0)

                if len(ask_queue) == 0:
                    del self.order_book.asks[best_ask]

        return trades

    def _match_sell_order(self, order):

        trades = []

        while order.remaining_quantity > 0:

            best_bid = self.order_book.best_bid()

            if best_bid is None:
                break

            if order.order_type == OrderType.LIMIT:
                if order.price > best_bid:
                    break

            bid_queue = self.order_book.bids[best_bid]

            resting_order = bid_queue[0]

            traded_quantity = min(
                order.remaining_quantity,
                resting_order.remaining_quantity
            )

            trade = Trade(
                trade_id=self.next_trade_id,
                buy_order_id=resting_order.order_id,
                sell_order_id=order.order_id,
                price=best_bid,
                quantity=traded_quantity,
                timestamp=order.timestamp
            )

            trades.append(trade)

            self.next_trade_id += 1

            order.remaining_quantity -= traded_quantity
            resting_order.remaining_quantity -= traded_quantity

            if resting_order.remaining_quantity == 0:

                bid_queue.pop(0)

                if len(bid_queue) == 0:
                    del self.order_book.bids[best_bid]

        return trades

