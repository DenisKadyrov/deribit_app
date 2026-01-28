from decimal import Decimal

from sqlalchemy.ext.asyncio import AsyncSession

from app.models.price import Price


async def seed_prices(session: AsyncSession) -> None:
    session.add_all(
        [
            Price(ticker="btc", price=Decimal("100.00000000"), ts=1),
            Price(ticker="btc", price=Decimal("101.00000000"), ts=2),
            Price(ticker="eth", price=Decimal("200.00000000"), ts=3),
        ]
    )
    await session.commit()


async def test_get_all_requires_ticker(client):
    resp = await client.get("/api/v1/prices/all")
    assert resp.status_code == 422


async def test_get_all_returns_all_rows_for_ticker(client, db_session: AsyncSession):
    await seed_prices(db_session)

    resp = await client.get("/api/v1/prices/all", params={"ticker": "BTC"})
    assert resp.status_code == 200

    data = resp.json()
    assert isinstance(data, list)
    assert [row["ts"] for row in data] == [1, 2]
    assert all(row["ticker"] == "btc" for row in data)


async def test_get_last_returns_latest_row(client, db_session: AsyncSession):
    await seed_prices(db_session)

    resp = await client.get("/api/v1/prices/last", params={"ticker": "btc"})
    assert resp.status_code == 200

    data = resp.json()
    assert data["ticker"] == "btc"
    assert data["ts"] == 2


async def test_get_last_404_when_no_rows(client):
    resp = await client.get("/api/v1/prices/last", params={"ticker": "btc"})
    assert resp.status_code == 404
    assert resp.json()["detail"] == "No prices found"


async def test_get_by_date_filters_interval(client, db_session: AsyncSession):
    await seed_prices(db_session)

    resp = await client.get(
        "/api/v1/prices/by-date",
        params={"ticker": "btc", "ts_from": 2, "ts_to": 10},
    )
    assert resp.status_code == 200
    data = resp.json()
    assert [row["ts"] for row in data] == [2]


async def test_get_by_date_400_on_wrong_interval(client):
    resp = await client.get(
        "/api/v1/prices/by-date",
        params={"ticker": "btc", "ts_from": 10, "ts_to": 2},
    )
    assert resp.status_code == 400
    assert resp.json()["detail"] == "ts_from must be <= ts_to"
