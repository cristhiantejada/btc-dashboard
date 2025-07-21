from fastapi import APIRouter, Response
from services import blockchain_api
from utils.formatters import volume_to_csv

router = APIRouter(prefix="/address", tags=["address"])

@router.get("/{address}")
async def get_address(address: str):
    data = await blockchain_api.get_address(address)
    return {
        "balance": data.get("final_balance", 0) / 1e8,
        "total_received": data.get("total_received", 0) / 1e8,
        "total_sent": data.get("total_sent", 0) / 1e8,
        "tx_count": data.get("n_tx", 0),
        "txs": data.get("txs", [])
    }

@router.get("/{address}/volume-daily")
async def volume_daily(address: str):
    return await blockchain_api.get_daily_volume(address)

@router.get("/{address}/export-csv")
async def export_csv(address: str):
    data = await blockchain_api.get_daily_volume(address)
    csv_data = volume_to_csv(data)
    return Response(content=csv_data, media_type="text/csv")
