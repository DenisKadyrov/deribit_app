import asyncio
import time
from decimal import Decimal

import aiohttp

from app.celery_app import celery_app
from app.clients.deribit_client import DeribitClient
from app.core.config import settings
from app.core.sync_database import SessionLocal
from app.models.price import Price


@celery_app.task(
    bind=True,
    autoretry_for=(Exception,),
    retry_kwargs={"max_retries": 3, "countdown": 5},
)
def fetch_and_store_prices(self) -> None:
    """
    Asychronously sending query to deribit and sinchronously writing data to db
    """
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    try:
        btc, eth, ts = loop.run_until_complete(_fetch_prices())
    finally:
        loop.close()

    _store_prices_sync(btc=btc, eth=eth, ts=ts)


async def _fetch_prices() -> tuple[Decimal, Decimal, int]:
    async with aiohttp.ClientSession() as session:
        client = DeribitClient(settings.DERIBIT_URL, session)
        btc, eth = await asyncio.gather(
            client.get_index_price("btc"),
            client.get_index_price("eth"),
        )

    ts = int(time.time())

    return Decimal(btc), Decimal(eth), ts


def _store_prices_sync(*, btc: Decimal, eth: Decimal, ts: int):
    with SessionLocal() as session:
        session.add_all(
            [
                Price(ticker="btc", price=btc, ts=ts),
                Price(ticker="eth", price=eth, ts=ts),
            ]
        )
        session.commit()
