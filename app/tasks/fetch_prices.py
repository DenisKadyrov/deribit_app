import asyncio
import time
from decimal import Decimal
import aiohttp

from app.celery_app import celery_app
from app.core.database import AsyncSessionLocal
from app.models.price import Price
from app.clients.deribit_client import DeribitClient
from app.core.config import settings


@celery_app.task(
    bind=True,
    autoretry_for=(Exception,),
    retry_kwargs={"max_retries": 3, "countdown": 5},
)
def fetch_and_store_prices(self):
    asyncio.run(_fetch_and_store())


async def _fetch_and_store():
    async with aiohttp.ClientSession() as session:
        client = DeribitClient(settings.DERIBIT_URL, session)
        btc = await client.get_index_price("btc")
        eth = await client.get_index_price("eth")

    ts = int(time.time())

    async with AsyncSessionLocal() as session:
        session.add_all(
            [
                Price(ticker="btc", price=Decimal(btc), ts=ts),
                Price(ticker="eth", price=Decimal(eth), ts=ts),
            ]
        )
        await session.commit()
