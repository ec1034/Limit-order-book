import math


class MarketSnapshot:

    def __init__(
        self,
        timestamp,
        best_bid,
        best_ask,
        mid_price,
        spread,
        trade_price,
        trade_volume,
        buy_volume,
        sell_volume
    ):

        self.timestamp = timestamp
        self.best_bid = best_bid
        self.best_ask = best_ask
        self.mid_price = mid_price
        self.spread = spread
        self.trade_price = trade_price
        self.trade_volume = trade_volume
        self.buy_volume = buy_volume
        self.sell_volume = sell_volume


def calculate_returns(prices):

    returns = []

    for i in range(1, len(prices)):

        previous_price = prices[i - 1]
        current_price = prices[i]

        if previous_price is None or current_price is None:
            continue

        return_value = (
            current_price - previous_price
        ) / previous_price

        returns.append(return_value)

    return returns


def calculate_log_returns(prices):

    log_returns = []

    for i in range(1, len(prices)):

        previous_price = prices[i - 1]
        current_price = prices[i]

        if previous_price is None or current_price is None:
            continue

        log_return = math.log(
            current_price / previous_price
        )

        log_returns.append(log_return)

    return log_returns


def calculate_volatility(returns):

    if len(returns) < 2:
        return 0.0

    mean = sum(returns) / len(returns)

    squared_differences = []

    for value in returns:

        difference = value - mean
        squared_differences.append(difference ** 2)

    variance = (
        sum(squared_differences)
        / (len(returns) - 1)
    )

    return math.sqrt(variance)

def calculate_order_flow_imbalance(buy_volume, sell_volume):

    total_volume = buy_volume + sell_volume

    if total_volume == 0:
        return 0.0

    return (
        (buy_volume - sell_volume)
        / total_volume)

def calculate_correlation(x, y):

    if len(x) != len(y):
        raise ValueError("Lists must have the same length")

    if len(x) < 2:
        return 0.0

    mean_x = sum(x) / len(x)
    mean_y = sum(y) / len(y)

    numerator = 0.0
    squared_x = 0.0
    squared_y = 0.0

    for i in range(len(x)):

        difference_x = x[i] - mean_x
        difference_y = y[i] - mean_y

        numerator += difference_x * difference_y

        squared_x += difference_x ** 2
        squared_y += difference_y ** 2

    denominator = (
        squared_x * squared_y
    ) ** 0.5

    if denominator == 0:
        return 0.0

    return numerator / denominator

def calculate_max_drawdown(values):

    if len(values) == 0:
        return 0.0

    peak = values[0]
    max_drawdown = 0.0

    for value in values:

        if value > peak:
            peak = value

        drawdown = value - peak

        if drawdown < max_drawdown:
            max_drawdown = drawdown

    return max_drawdown