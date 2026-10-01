import pandas as pd
import numpy as np

from src.market_simulator import MarketSimulator


def calculate_volatility(prices):

    returns = []

    for i in range(1, len(prices)):

        previous = prices[i - 1]
        current = prices[i]

        returns.append(
            (current - previous) / previous
        )

    if len(returns) < 2:
        return 0.0

    return np.std(returns, ddof=1)


results = []

for probability in [0.3, 0.5, 0.7]:

    simulator = MarketSimulator(
        starting_price=100.0,
        seed=42,
        buy_probability=probability
    )

    simulator.run(5000)

    history = simulator.get_history()

    df = pd.DataFrame(history)

    df = df.dropna(
        subset=["mid_price"]
    )

    volatility = calculate_volatility(
        df["mid_price"].tolist()
    )

    results.append({
        "buy_probability": probability,
        "volatility": volatility
    })


results_df = pd.DataFrame(results)

print(results_df)

results_df.to_csv(
    "results/volatility_results.csv",
    index=False
)