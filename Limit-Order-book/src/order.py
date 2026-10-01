from dataclasses import dataclass
from enum import Enum


class Side(Enum):
    BUY = "BUY"
    SELL = "SELL"


class OrderType(Enum):
    LIMIT = "LIMIT"
    MARKET = "MARKET"


@dataclass
class Order:
    order_id: int
    side: Side
    order_type: OrderType
    price: float
    quantity: int
    timestamp: int
    remaining_quantity: int = 0

    def __post_init__(self):
        self.remaining_quantity = self.quantity