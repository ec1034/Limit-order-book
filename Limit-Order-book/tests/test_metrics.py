from src.metrics import (
    calculate_returns,
    calculate_log_returns,
    calculate_volatility,
    calculate_order_flow_imbalance,
    calculate_correlation,
    calculate_max_drawdown
)


def test_calculate_returns():

    prices = [100.0, 101.0, 102.0]

    returns = calculate_returns(prices)

    assert len(returns) == 2
    assert returns[0] == 0.01
    assert returns[1] == (102.0 - 101.0) / 101.0


def test_calculate_log_returns():

    prices = [100.0, 101.0, 102.0]

    returns = calculate_log_returns(prices)

    assert len(returns) == 2
    assert returns[0] > 0
    assert returns[1] > 0


def test_calculate_volatility():

    returns = [0.01, -0.01, 0.01, -0.01]

    volatility = calculate_volatility(returns)

    assert volatility > 0

def test_order_flow_imbalance():

    imbalance = calculate_order_flow_imbalance(
        buy_volume=80,
        sell_volume=20
    )

    assert imbalance == 0.6


def test_order_flow_imbalance_balanced():

    imbalance = calculate_order_flow_imbalance(
        buy_volume=50,
        sell_volume=50
    )

    assert imbalance == 0.0


def test_order_flow_imbalance_no_volume():

    imbalance = calculate_order_flow_imbalance(
        buy_volume=0,
        sell_volume=0
    )

    assert imbalance == 0.0

def test_correlation():

    x = [1, 2, 3, 4, 5]
    y = [2, 4, 6, 8, 10]

    correlation = calculate_correlation(x, y)

    assert abs(correlation - 1.0) < 0.000001

def test_max_drawdown():

    values = [
        100,
        110,
        105,
        90,
        95
    ]

    drawdown = calculate_max_drawdown(
        values
    )

    assert drawdown == -20