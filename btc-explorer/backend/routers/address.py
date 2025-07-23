from fastapi import APIRouter, Response
from services import blockchain_api
from utils.formatters import volume_to_csv

router = APIRouter(prefix="/address", tags=["address"])

@router.get("/{address}")
async def get_address(address: str):
    data = await blockchain_api.get_address(address)
    
    # Ensure numeric values are always valid
    final_balance = data.get("final_balance", 0)
    total_received = data.get("total_received", 0)
    total_sent = data.get("total_sent", 0)
    
    # Convert to BTC and handle None values
    balance_btc = (final_balance / 1e8) if final_balance is not None else 0
    received_btc = (total_received / 1e8) if total_received is not None else 0
    sent_btc = (total_sent / 1e8) if total_sent is not None else 0
    
    return {
        "balance": balance_btc,
        "total_received": received_btc,
        "total_sent": sent_btc,
        "tx_count": data.get("n_tx", 0) or 0,
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
