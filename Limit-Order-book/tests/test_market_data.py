from src.market_simulator import MarketSimulator


def test_market_history_is_recorded():

    simulator = MarketSimulator(
        starting_price=100.0,
        seed=42
    )

    simulator.run(10)

    assert len(simulator.history) == 10


def test_market_snapshot_contains_timestamp():

    simulator = MarketSimulator(
        starting_price=100.0,
        seed=42
    )

    simulator.run(5)

    assert simulator.history[0].timestamp == 0
    assert simulator.history[1].timestamp == 1
    assert simulator.history[4].timestamp == 4

def test_get_history():

    simulator = MarketSimulator(
        starting_price=100.0,
        seed=42
    )

    simulator.run(10)

    history = simulator.get_history()

    assert len(history) == 10

    assert history[0]["timestamp"] == 0
    assert history[1]["timestamp"] == 1

    assert "best_bid" in history[0]
    assert "best_ask" in history[0]
    assert "mid_price" in history[0]
    assert "spread" in history[0]
    assert "buy_volume" in history[0]
    assert "sell_volume" in history[0]