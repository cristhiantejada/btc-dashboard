from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routers import address, tx

app = FastAPI(title="BTC Explorer API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"] ,
    allow_headers=["*"]
)

app.include_router(address.router, prefix="/api")
app.include_router(tx.router, prefix="/api")

@app.get("/api/health")
def health():
    return {"status": "ok"}
