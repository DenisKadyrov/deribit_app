from decimal import Decimal

from pydantic import BaseModel

from app.models.price import Price


class PriceOut(BaseModel):
    ticker: str
    price: Decimal
    ts: int

    @classmethod
    def from_orm(cls, price: Price) -> "PriceOut":
        return cls(ticker=price.ticker, price=price.price, ts=price.ts)
