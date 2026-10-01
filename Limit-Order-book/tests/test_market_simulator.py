from src.market_simulator import MarketSimulator
from src.order import Side, OrderType


def test_simulator_creates_orders():

    simulator = MarketSimulator(
        starting_price=100.0,
        seed=42
    )

    order, trades = simulator.step()

    assert order.order_id == 1
    assert order.timestamp == 0
    assert order.quantity > 0


def test_simulator_runs_multiple_steps():

    simulator = MarketSimulator(
        starting_price=100.0,
        seed=42
    )

    simulator.run(100)

    assert simulator.order_id == 101
    assert simulator.timestamp == 100

def test_mid_price():

    simulator = MarketSimulator(
        starting_price=100.0,
        seed=42
    )

    simulator.order_book.add_order(
        simulator.generate_order()
    )