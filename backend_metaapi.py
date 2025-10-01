from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import os
from metaapi_cloud_sdk import MetaApi

app = FastAPI(title="MetaApi Bridge pour Base44")

# Activer CORS pour toutes les requêtes (obligatoire pour Base44)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Clé API MetaApi depuis Render (variable d'environnement)
API_TOKEN = os.getenv("METAAPI_KEY")
client = MetaApi(API_TOKEN)

# UUID de ton compte MetaApi
ACCOUNT_ID = "52c3348b-3e48-473e-88fd-d37734190a3b"


@app.get("/")
async def root():
    return {"status": "online ✅", "service": "MetaApi Bridge pour Base44"}


@app.get("/accounts")
async def get_accounts():
    """Liste tous les comptes MetaApi liés à ton token"""
    try:
        accounts = await client.metatrader_account_api.get_metatrader_accounts()
        return [
            {
                "id": a.id,
                "login": a.login,
                "type": a.type,
                "server": a.server,
                "state": a.state
            }
            for a in accounts
        ]
    except Exception as e:
        return {"error": str(e)}


@app.get("/account-info")
async def account_info():
    """Infos détaillées du compte principal"""
    try:
        account = await client.metatrader_account_api.get_account(ACCOUNT_ID)
        connection = account.get_rpc_connection()
        await connection.connect()
        await connection.wait_synchronized()
        info = await connection.get_account_information()
        return {
            "success": True,
            "login": account.login,
            "server": account.server,
            "balance": info.get("balance", 0),
            "equity": info.get("equity", 0),
            "margin": info.get("margin", 0),
            "freeMargin": info.get("freeMargin", 0),
            "leverage": info.get("leverage", 0),
            "profit": info.get("profit", 0),
            "currency": info.get("currency", "USD"),
        }
    except Exception as e:
        return {"error": str(e)}


@app.get("/positions")
async def get_positions():
    """Liste toutes les positions ouvertes du compte principal"""
    try:
        account = await client.metatrader_account_api.get_account(ACCOUNT_ID)
        connection = account.get_rpc_connection()
        await connection.connect()
        await connection.wait_synchronized()
        positions = await connection.get_positions()
        return {
            "success": True,
            "positions": [
                {
                    "id": pos.get("id"),
                    "symbol": pos.get("symbol"),
                    "type": pos.get("type"),
                    "volume": pos.get("volume"),
                    "openPrice": pos.get("openPrice"),
                    "currentPrice": pos.get("currentPrice"),
                    "profit": pos.get("profit"),
                    "stopLoss": pos.get("stopLoss"),
                    "takeProfit": pos.get("takeProfit"),
                    "openTime": pos.get("time")
                }
                for pos in positions
            ]
        }
    except Exception as e:
        return {"error": str(e)}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "backend_metaapi:app",
        host="0.0.0.0",
        port=int(os.environ.get("PORT", 8000)),
        reload=True
    )
