import os
from typing import Any, Dict

import httpx
from dotenv import load_dotenv

load_dotenv()

BASE_URL = os.getenv("BLOCKCHAIN_API_URL", "https://blockchain.info")

async def get_address_info(address: str) -> Dict[str, Any]:
    url = f"{BASE_URL}/rawaddr/{address}"
    async with httpx.AsyncClient() as client:
        resp = await client.get(url)
        resp.raise_for_status()
        return resp.json()

async def get_transaction_info(txid: str) -> Dict[str, Any]:
    url = f"{BASE_URL}/rawtx/{txid}"
    params = {"format": "json"}
    async with httpx.AsyncClient() as client:
        resp = await client.get(url, params=params)
        resp.raise_for_status()
        return resp.json()

async def get_latest_block_height() -> Dict[str, Any]:
    url = f"{BASE_URL}/q/getblockcount"
    async with httpx.AsyncClient() as client:
        resp = await client.get(url)
        resp.raise_for_status()
        return {"block_height": int(resp.text)}

async def get_btc_price_usd() -> Dict[str, Any]:
    url = f"{BASE_URL}/ticker"
    async with httpx.AsyncClient() as client:
        resp = await client.get(url)
        resp.raise_for_status()
        data = resp.json()
        usd = data.get("USD", {})
        return {"USD": usd}
