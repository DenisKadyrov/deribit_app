from fastapi import FastAPI

from app.api.v1.prices import router as api_router

app = FastAPI(title="Deribit Prices API")

app.include_router(api_router, prefix="/api/v1/prices")
