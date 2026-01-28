from decimal import Decimal

from pydantic import BaseModel, Field
from pydantic import ConfigDict

from app.models.price import Price


class PriceOut(BaseModel):
    """Price DTO returned by the public API."""

    ticker: str = Field(
        ...,
        description="Currency ticker (lowercase), for example `btc` or `eth`.",
        examples=["btc"],
    )
    price: Decimal = Field(
        ...,
        description="Index price of the currency on Deribit.",
        examples=["100000.00000000"],
    )
    ts: int = Field(
        ...,
        description="Unix timestamp in seconds when the price was fetched.",
        examples=[1738000000],
    )

    model_config = ConfigDict(
        json_schema_extra={
            "example": {"ticker": "btc", "price": "100000.00000000", "ts": 1738000000}
        }
    )

    @classmethod
    def from_orm(cls, price: Price) -> "PriceOut":
        return cls(ticker=price.ticker, price=price.price, ts=price.ts)
