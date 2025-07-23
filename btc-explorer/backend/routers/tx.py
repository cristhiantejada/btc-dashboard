from fastapi import APIRouter
from services import blockchain_api

router = APIRouter(prefix="/tx", tags=["transactions"])

@router.get("/{txid}")
async def get_transaction(txid: str):
    """Get transaction details by transaction ID"""
    data = await blockchain_api.get_transaction(txid)
    
    # Format the response
    return {
        "txid": data.get("hash"),
        "size": data.get("size"),
        "weight": data.get("weight"),
        "fee": data.get("fee", 0) / 1e8 if data.get("fee") else 0,
        "time": data.get("time"),
        "block_height": data.get("block_height"),
        "inputs": [
            {
                "address": inp.get("prev_out", {}).get("addr") if inp.get("prev_out") else None,
                "value": inp.get("prev_out", {}).get("value", 0) / 1e8 if inp.get("prev_out") else 0
            }
            for inp in data.get("inputs", [])
        ],
        "outputs": [
            {
                "address": out.get("addr"),
                "value": out.get("value", 0) / 1e8,
                "spent": out.get("spent", False)
            }
            for out in data.get("out", [])
        ]
    }
