import pandas as pd
import matplotlib.pyplot as plt


df = pd.read_csv(
    "results/market_maker_results.csv"
)

plt.plot(
    df["timestamp"],
    df["pnl"]
)

plt.xlabel("Time")
plt.ylabel("P&L")
plt.title("Market Maker P&L")

plt.show()