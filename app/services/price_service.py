from typing import List
from app.repositories.price import PriceRepository
from app.schemas.price import PriceOut

class PriceService:
    def __init__(self, repo: PriceRepository):
        self.repo = repo

    async def get_all(self, ticker: str) -> List[PriceOut]:
        prices = await self.repo.get_all(ticker)
        return [PriceOut.from_orm(p) for p in prices]

    async def get_last(self, ticker: str) -> PriceOut:
        price = await self.repo.get_last(ticker)
        if price is None:
            return None
        return PriceOut.from_orm(price)

    async def get_by_date(self, ticker: str, ts_from: int, ts_to: int) -> List[PriceOut]:
        if ts_from > ts_to:
            raise ValueError("ts_from must be <= ts_to")
        prices = await self.repo.get_by_date(ticker, ts_from, ts_to)
        return [PriceOut.from_orm(p) for p in prices]
