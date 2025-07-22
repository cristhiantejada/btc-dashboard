import os
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv

from blockchain_api import (
    get_address_info,
    get_transaction_info,
    get_latest_block_height,
    get_btc_price_usd,
)

load_dotenv()

allowed_origins = [origin.strip() for origin in os.getenv("ALLOWED_ORIGINS", "").split(',') if origin.strip()]

app = FastAPI(title="BTC Explorer API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins or ["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/healthz")
async def health_check():
    return {"status": "ok"}

@app.get("/api/address/{addr}")
async def address_info(addr: str):
    return await get_address_info(addr)

@app.get("/api/tx/{txid}")
async def transaction_info(txid: str):
    return await get_transaction_info(txid)

@app.get("/api/stats/blockheight")
async def latest_block_height():
    return await get_latest_block_height()

@app.get("/api/price")
async def btc_price_usd():
    return await get_btc_price_usd()

