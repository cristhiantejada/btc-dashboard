import os
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv

from routers import address, tx

load_dotenv()

# Configure CORS origins from environment variable
allowed_origins = [origin.strip() for origin in os.getenv("ALLOWED_ORIGINS", "http://localhost:5173").split(',') if origin.strip()]

app = FastAPI(
    title="BTC Explorer API",
    description="API for exploring Bitcoin addresses and transactions",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=True,
    allow_methods=["GET"],
    allow_headers=["*"],
)

# Include routers
app.include_router(address.router, prefix="/api")
app.include_router(tx.router, prefix="/api")

@app.get("/")
async def root():
    return {"message": "BTC Explorer API", "docs": "/docs"}

@app.get("/healthz")
async def health_check():
    return {"status": "ok"}

@app.get("/api/stats/blockheight")
async def latest_block_height():
    from services.blockchain_api import get_latest_block_height
    return await get_latest_block_height()

@app.get("/api/price")
async def btc_price_usd():
    from services.blockchain_api import get_btc_price_usd
    return await get_btc_price_usd()

