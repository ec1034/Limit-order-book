import pandas as pd

from src.order_book import OrderBook
from src.matching_engine import MatchingEngine
from src.market_simulator import MarketSimulator
from src.market_maker import MarketMaker


simulator = MarketSimulator(
    starting_price=100.0,
    seed=42,
    buy_probability=0.5
)

book = OrderBook()
engine = MatchingEngine(book)

maker = MarketMaker(
    engine=engine,
    order_book=book,
    spread=1.0,
    order_size=10,
    max_inventory=100
)

results = []

for _ in range(5000):

    simulator.step()

    if simulator.current_price is not None:

        maker.submit_quotes(
            simulator.current_price
        )

        pnl = maker.mark_to_market(
            simulator.current_price
        )

        results.append({
            "timestamp": simulator.timestamp,
            "price": simulator.current_price,
            "inventory": maker.inventory,
            "cash": maker.cash,
            "pnl": pnl
        })


df = pd.DataFrame(results)

print(df.tail())

print()
print("Final inventory:", maker.inventory)
print("Final cash:", maker.cash)
print("Final P&L:", df["pnl"].iloc[-1])

df.to_csv(
    "results/market_maker_results.csv",
    index=False
)