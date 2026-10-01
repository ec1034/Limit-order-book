import pandas as pd

from src.market_simulator import MarketSimulator


def run_experiment(buy_probability):

    simulator = MarketSimulator(
        starting_price=100.0,
        seed=42,
        buy_probability=buy_probability
    )

    simulator.run(5000)

    history = simulator.get_history()

    df = pd.DataFrame(history)

    df = df.dropna(subset=["mid_price"])

    starting_price = df["mid_price"].iloc[0]
    ending_price = df["mid_price"].iloc[-1]

    return {
        "buy_probability": buy_probability,
        "starting_price": starting_price,
        "ending_price": ending_price,
        "price_change": ending_price - starting_price,
        "return": (
            ending_price - starting_price
        ) / starting_price
    }


results = []

for probability in [0.3, 0.5, 0.7]:

    result = run_experiment(probability)

    results.append(result)


df = pd.DataFrame(results)

print(df)

df.to_csv(
    "results/regime_results.csv",
    index=False
)