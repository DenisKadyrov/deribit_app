from sqlalchemy import desc, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.price import Price


class PriceRepository:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def add(self, price: Price) -> None:
        self.session.add(price)
        await self.session.commit()

    async def get_all(self, ticker: str) -> list[Price]:
        stmt = (
            select(Price)
            .where(Price.ticker == ticker)
            .order_by(Price.ts.asc())
        )
        result = await self.session.execute(stmt)
        return result.scalars().all()

    async def get_last(self, ticker: str) -> Price | None:
        stmt = (
            select(Price)
            .where(Price.ticker == ticker)
            .order_by(desc(Price.ts))
            .limit(1)
        )
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()

    async def get_by_date(self, ticker: str, ts_from: int, ts_to: int) -> list[Price]:
        stmt = (
            select(Price)
            .where(
                Price.ticker == ticker,
                Price.ts.between(ts_from, ts_to),
            )
            .order_by(Price.ts.asc())
        )
        result = await self.session.execute(stmt)
        return result.scalars().all()
