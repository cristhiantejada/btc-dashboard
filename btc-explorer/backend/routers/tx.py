from fastapi import APIRouter
from services import blockchain_api

router = APIRouter(prefix="/tx", tags=["tx"])

@router.get("/{txid}")
async def get_tx(txid: str):
    return await blockchain_api.get_transaction(txid)
