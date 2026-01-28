from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_session
from app.repositories.price import PriceRepository
from app.schemas.price import PriceOut
from app.services.price_service import PriceService

router = APIRouter()


async def get_price_service(
    session: AsyncSession = Depends(get_session),
) -> PriceService:
    repo = PriceRepository(session)
    return PriceService(repo)


async def ticker_lower(
    ticker: str = Query(
        ...,
        description="Currency ticker (case-insensitive), for example `btc` or `eth`.",
        examples=["btc"],
    ),
) -> str:
    return ticker.lower()


@router.get(
    "/all",
    response_model=list[PriceOut],
    summary="Get all saved prices for a ticker",
    description=(
        "Returns **all** index prices stored for the given `ticker`.\n\n"
    ),
)
async def get_all(
    ticker: str = Depends(ticker_lower),
    service: PriceService = Depends(get_price_service),
):
    return await service.get_all(ticker)


@router.get(
    "/last",
    response_model=PriceOut,
    summary="Get the latest saved price for a ticker",
    description=(
        "Returns **last** price stored for the given`ticker`.\n\n"
    ),
    responses={
        404: {
            "description": "No saved prices for the given ticker",
            "content": {
                "application/json": {
                    "example": {"detail": "No prices found"},
                }
            },
        }
    },
)
async def get_last(
    ticker: str = Depends(ticker_lower),
    service: PriceService = Depends(get_price_service),
):
    price = await service.get_last(ticker)
    if price is None:
        raise HTTPException(status_code=404, detail="No prices found")
    return price


@router.get(
    "/by-date",
    response_model=list[PriceOut],
    summary="Get prices for a ticker in a timestamp range",
    description=(
        "Return all prices for the given `ticker` by date"
    ),
    responses={
        400: {
            "description": "Invalid timestamp range",
            "content": {
                "application/json": {
                    "example": {"detail": "ts_from must be <= ts_to"},
                }
            },
        }
    },
)
async def get_by_date(
    ticker: str = Depends(ticker_lower),
    ts_from: int = Query(
        ...,
        description="start, soconds.",
        examples=[1738000000],
    ),
    ts_to: int = Query(
        ...,
        description="end, seconds",
        examples=[1738003600],
    ),
    service: PriceService = Depends(get_price_service),
):
    try:
        return await service.get_by_date(ticker, ts_from, ts_to)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
