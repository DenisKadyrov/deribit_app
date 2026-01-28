from fastapi import FastAPI

from app.api.v1.prices import router as api_router


app = FastAPI(
    title="Deribit Prices API",
    version="1.0.0",
)

app.include_router(api_router, prefix="/api/v1/prices", tags=["prices"])
