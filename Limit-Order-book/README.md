# Limit Order Book & Market-Making Simulator

## Overview

A Python-based limit order book and exchange simulator designed
to investigate market microstructure and market-making behaviour.

The system implements:

- Limit orders
- Market orders
- Price-time priority
- Partial fills
- Order cancellation
- Multi-level market execution
- Synthetic order flow
- Market data collection
- Order-flow imbalance
- Return and volatility analysis
- Market-making
- Inventory management
- P&L
- Slippage analysis

## Architecture

Orders are submitted to a matching engine which interacts with
an order book containing bid and ask price levels.

The simulator generates synthetic order flow and records market
state after each timestep.

Experiments then analyse the resulting data.

## Research Questions

1. Does order-flow imbalance predict subsequent returns?
2. How does directional order flow affect prices?
3. How does quoted spread affect market-maker P&L?
4. How does order size affect execution price?
5. How does inventory affect market-maker risk?

## Methodology

Experiments are repeated across multiple random seeds to reduce
the risk of drawing conclusions from a single simulation path.

Results are evaluated using price returns, volatility,
correlation, P&L, inventory and drawdown.

## Limitations

This is a synthetic market model rather than a representation
of a real exchange.

The simulator does not model:

- Latency
- Hidden liquidity
- Queue cancellation dynamics
- Multiple market participants with heterogeneous strategies
- Real historical order-book data
- Transaction fees
- Adverse selection in a realistic way

These limitations are considered when interpreting results.