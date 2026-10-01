import pandas as pd

from src.market_simulator import MarketSimulator
from src.metrics import calculate_order_flow_imbalance


simulator = MarketSimulator(
    starting_price=100.0,
    seed=42
)

simulator.run(1000)

history = simulator.get_history()

df = pd.DataFrame(history)

df["ofi"] = df.apply(
    lambda row: calculate_order_flow_imbalance(
        row["buy_volume"],
        row["sell_volume"]
    ),
    axis=1
)

df["next_mid_price"] = df["mid_price"].shift(-1)

df["next_return"] = (
    df["next_mid_price"] - df["mid_price"]
) / df["mid_price"]


print(df.head(10))

print()
print("Number of observations:", len(df))

print()
print("Average spread:", df["spread"].mean())

print()
print("Average trade volume:", df["trade_volume"].mean())

print()
print("Average OFI:", df["ofi"].mean())

print()
print("OFI / next return correlation:")

print(
    df["ofi"].corr(df["next_return"])
)