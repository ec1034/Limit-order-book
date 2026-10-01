import pandas as pd
import matplotlib.pyplot as plt


df = pd.read_csv(
    "results/market_maker_results.csv"
)

plt.plot(
    df["timestamp"],
    df["inventory"]
)

plt.xlabel("Time")
plt.ylabel("Inventory")
plt.title("Market Maker Inventory")

plt.show()