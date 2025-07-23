import httpx
from datetime import datetime
from collections import defaultdict
from typing import Any, Dict
from fastapi import HTTPException

BASE_URL = "https://blockchain.info"

async def get_address(address: str) -> Dict[str, Any]:
    """Get address information from blockchain.info API"""
    try:
        url = f"{BASE_URL}/rawaddr/{address}?cors=true"
        async with httpx.AsyncClient(timeout=30.0) as client:
            resp = await client.get(url)
            resp.raise_for_status()
            return resp.json()
    except httpx.HTTPStatusError as e:
        if e.response.status_code == 404:
            raise HTTPException(status_code=404, detail="Address not found")
        raise HTTPException(status_code=e.response.status_code, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching address: {str(e)}")

async def get_transaction(txid: str) -> Dict[str, Any]:
    """Get transaction information from blockchain.info API"""
    try:
        url = f"{BASE_URL}/rawtx/{txid}?cors=true"
        async with httpx.AsyncClient(timeout=30.0) as client:
            resp = await client.get(url)
            resp.raise_for_status()
            return resp.json()
    except httpx.HTTPStatusError as e:
        if e.response.status_code == 404:
            raise HTTPException(status_code=404, detail="Transaction not found")
        raise HTTPException(status_code=e.response.status_code, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching transaction: {str(e)}")

async def get_daily_volume(address: str) -> list:
    """Calculate daily transaction volume for an address"""
    data = await get_address(address)
    volume_by_date = defaultdict(float)
    
    for tx in data.get("txs", []):
        if tx.get("time"):
            date = datetime.utcfromtimestamp(tx.get("time")).strftime("%Y-%m-%d")
            # Calculate the net effect on the address
            result = tx.get("result", 0)
            volume_by_date[date] += abs(result / 1e8)
    
    # Sort by date and return
    return [{"date": d, "volume": v} for d, v in sorted(volume_by_date.items())]

async def get_latest_block_height() -> Dict[str, Any]:
    """Get the latest block height"""
    try:
        url = f"{BASE_URL}/q/getblockcount"
        async with httpx.AsyncClient(timeout=10.0) as client:
            resp = await client.get(url)
            resp.raise_for_status()
            return {"block_height": int(resp.text.strip())}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching block height: {str(e)}")

async def get_btc_price_usd() -> Dict[str, Any]:
    """Get current BTC price in USD"""
    try:
        url = f"{BASE_URL}/ticker"
        async with httpx.AsyncClient(timeout=10.0) as client:
            resp = await client.get(url)
            resp.raise_for_status()
            data = resp.json()
            usd_data = data.get("USD", {})
            return {
                "USD": {
                    "price": usd_data.get("last", 0),
                    "symbol": usd_data.get("symbol", "$"),
                    "buy": usd_data.get("buy", 0),
                    "sell": usd_data.get("sell", 0)
                }
            }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching BTC price: {str(e)}")
