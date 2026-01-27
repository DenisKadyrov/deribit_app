from sqlalchemy import select, desc
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.price import Price


class PriceRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def add(self, price: Price):
        self.session.add(price)
        await self.session.commit()

    async def get_all(self, ticker: str):
        stmt = select(Price).where(Price.ticker == ticker)
        result = await self.session.execute(stmt)
        return result.scalars().all()

    async def get_last(self, ticker: str):
        stmt = (
            select(Price)
            .where(Price.ticker == ticker)
            .order_by(desc(Price.timestamp))
            .limit(1)
        )
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()

    async def get_by_date(self, ticker: str, ts_from: int, ts_to: int):
        stmt = select(Price).where(
            Price.ticker == ticker,
            Price.timestamp.between(ts_from, ts_to)
        )
        result = await self.session.execute(stmt)
        return result.scalars().all()
