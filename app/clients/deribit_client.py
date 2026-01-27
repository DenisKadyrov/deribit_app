from aiohttp import ClientSession


class DeribitClient:
    def __init__(self, base_url: str, session: ClientSession):
        self.base_url = base_url
        self.session = session

    async def get_index_price(self, currency: str) -> float:
        url = f"{self.base_url}/public/get_index_price"
        params = {"index_name": f"{currency.lower()}_usd"}

        async with self.session.get(url, params=params) as resp:
            data = await resp.json()
            return data["result"]["index_price"]
