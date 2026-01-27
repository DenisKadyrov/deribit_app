from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_session
from app.repositories.price import PriceRepository
from app.services.price_service import PriceService
from app.schemas.price import PriceOut

from typing import List

router = APIRouter()

async def get_price_service(session: AsyncSession = Depends(get_session)) -> PriceService:
    repo = PriceRepository(session)
    return PriceService(repo)

async def ticker_lower(ticker: str = Query(..., description="Currency ticker")) -> str:
    return ticker.lower()


@router.get("/all", response_model=List[PriceOut])
async def get_all(ticker: str = Depends(ticker_lower), service: PriceService = Depends(get_price_service)):
    return await service.get_all(ticker)


@router.get("/last", response_model=PriceOut)
async def get_last(ticker: str = Depends(ticker_lower), service: PriceService = Depends(get_price_service)):
    price = await service.get_last(ticker)
    if price is None:
        raise HTTPException(status_code=404, detail="No prices found")
    return price


@router.get("/by-date", response_model=List[PriceOut])
async def get_by_date(
    ticker: str = Depends(ticker_lower),
    ts_from: int = Query(...),
    ts_to: int = Query(...),
    service: PriceService = Depends(get_price_service),
):
    try:
        return await service.get_by_date(ticker, ts_from, ts_to)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
