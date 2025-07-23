import httpx
from datetime import datetime
from collections import defaultdict
from typing import Any, Dict
from fastapi import HTTPException
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

BASE_URL = "https://blockchain.info"

# Headers para evitar problemas con la API
HEADERS = {
    "User-Agent": "BTC-Explorer/1.0",
    "Accept": "application/json"
}

async def get_address(address: str) -> Dict[str, Any]:
    """Get address information from blockchain.info API"""
    try:
        url = f"{BASE_URL}/rawaddr/{address}"
        logger.info(f"Fetching address data for: {address}")
        
        async with httpx.AsyncClient(timeout=30.0, headers=HEADERS) as client:
            resp = await client.get(url)
            resp.raise_for_status()
            data = resp.json()
            logger.info(f"Successfully fetched data for address: {address}")
            return data
    except httpx.HTTPStatusError as e:
        logger.error(f"HTTP error for address {address}: {e.response.status_code}")
        if e.response.status_code == 404:
            raise HTTPException(status_code=404, detail="Address not found")
        elif e.response.status_code == 429:
            raise HTTPException(status_code=429, detail="Rate limit exceeded. Please try again later.")
        raise HTTPException(status_code=e.response.status_code, detail=str(e))
    except httpx.TimeoutException:
        logger.error(f"Timeout while fetching address: {address}")
        raise HTTPException(status_code=504, detail="Request timeout. Please try again.")
    except Exception as e:
        logger.error(f"Unexpected error fetching address {address}: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error fetching address: {str(e)}")

async def get_transaction(txid: str) -> Dict[str, Any]:
    """Get transaction information from blockchain.info API"""
    try:
        url = f"{BASE_URL}/rawtx/{txid}"
        logger.info(f"Fetching transaction data for: {txid}")
        
        async with httpx.AsyncClient(timeout=30.0, headers=HEADERS) as client:
            resp = await client.get(url)
            resp.raise_for_status()
            data = resp.json()
            logger.info(f"Successfully fetched transaction: {txid}")
            return data
    except httpx.HTTPStatusError as e:
        logger.error(f"HTTP error for transaction {txid}: {e.response.status_code}")
        if e.response.status_code == 404:
            raise HTTPException(status_code=404, detail="Transaction not found")
        elif e.response.status_code == 429:
            raise HTTPException(status_code=429, detail="Rate limit exceeded. Please try again later.")
        raise HTTPException(status_code=e.response.status_code, detail=str(e))
    except httpx.TimeoutException:
        logger.error(f"Timeout while fetching transaction: {txid}")
        raise HTTPException(status_code=504, detail="Request timeout. Please try again.")
    except Exception as e:
        logger.error(f"Unexpected error fetching transaction {txid}: {str(e)}")
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
        async with httpx.AsyncClient(timeout=10.0, headers=HEADERS) as client:
            resp = await client.get(url)
            resp.raise_for_status()
            height = int(resp.text.strip())
            logger.info(f"Current block height: {height}")
            return {"block_height": height}
    except Exception as e:
        logger.error(f"Error fetching block height: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error fetching block height: {str(e)}")

async def get_btc_price_usd() -> Dict[str, Any]:
    """Get current BTC price in USD"""
    try:
        url = f"{BASE_URL}/ticker"
        async with httpx.AsyncClient(timeout=10.0, headers=HEADERS) as client:
            resp = await client.get(url)
            resp.raise_for_status()
            data = resp.json()
            usd_data = data.get("USD", {})
            price_info = {
                "USD": {
                    "price": usd_data.get("last", 0),
                    "symbol": usd_data.get("symbol", "$"),
                    "buy": usd_data.get("buy", 0),
                    "sell": usd_data.get("sell", 0)
                }
            }
            logger.info(f"Current BTC price: ${price_info['USD']['price']}")
            return price_info
    except Exception as e:
        logger.error(f"Error fetching BTC price: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error fetching BTC price: {str(e)}")
