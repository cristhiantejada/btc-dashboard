import httpx
from datetime import datetime
from collections import defaultdict

BASE_URL = "https://blockchain.info"

async def get_address(address: str):
    url = f"{BASE_URL}/rawaddr/{address}?cors=true"
    async with httpx.AsyncClient() as client:
        resp = await client.get(url)
        resp.raise_for_status()
        return resp.json()

async def get_transaction(txid: str):
    url = f"{BASE_URL}/rawtx/{txid}?cors=true"
    async with httpx.AsyncClient() as client:
        resp = await client.get(url)
        resp.raise_for_status()
        return resp.json()

async def get_daily_volume(address: str):
    data = await get_address(address)
    volume_by_date = defaultdict(int)
    for tx in data.get("txs", []):
        date = datetime.utcfromtimestamp(tx.get("time")).strftime("%Y-%m-%d")
        volume_by_date[date] += tx.get("result", 0) / 1e8
    # sort dates
    return [{"date": d, "volume": v} for d, v in sorted(volume_by_date.items())]
