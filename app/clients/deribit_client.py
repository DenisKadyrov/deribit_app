import aiohttp
import asyncio

from core.config import settings
from core.database import AsyncSessionLocal 


class DeribitClient:
  def __init__(self, base_url: str):
    self.base_url = base_url

  async def get_index_price(self, currency: str) -> float:
    url = f"{self.base_url}/public/get_index_price"
    params = {"index_name": f"{currency.lower()}_usd"}

    async with aiohttp.ClientSession() as session:
      async with session.get(url, params=params) as resp:
        data = await resp.json()
        return data["result"]["index_price"]


async def main():
  deribit_client = DeribitClient(settings.DERIBIT_URL)
  res = await deribit_client.get_index_price("eth")
  print(res)

if __name__ == "__main__":
    asyncio.run(main())
