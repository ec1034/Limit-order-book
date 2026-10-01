import pandas as pd

from src.order_book import OrderBook
from src.matching_engine import MatchingEngine
from src.market_simulator import MarketSimulator
from src.market_maker import MarketMaker


results = []


for spread in [
    0.2,
    0.5,
    1.0,
    2.0,
    5.0
]:

    simulator = MarketSimulator(
        starting_price=100.0,
        seed=42,
        buy_probability=0.5
    )

    book = OrderBook()
    engine = MatchingEngine(book)

    maker = MarketMaker(
        engine,
        book,
        spread=spread,
        order_size=10,
        max_inventory=100
    )

    for _ in range(5000):

        simulator.step()

        maker.submit_quotes(
            simulator.current_price
        )

    pnl = maker.mark_to_market(
        simulator.current_price
    )

    results.append({
        "spread": spread,
        "final_pnl": pnl,
        "inventory": maker.inventory
    })


df = pd.DataFrame(results)

print(df)

df.to_csv(
    "results/spread_results.csv",
    index=False
)