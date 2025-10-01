# backend_metaapi.py
import os
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from metaapi_cloud_sdk import MetaApi

app = FastAPI(title="MetaApi Bridge - Backend")

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Clé API
API_TOKEN = os.getenv("METAAPI_KEY", "52c3348b-3e48-473e-88fd-d37734190a3b")
client = MetaApi(API_TOKEN)

@app.get("/")
async def root():
    return {"status": "ok", "service": "MetaApi Bridge", "version": "1.0.0"}

@app.get("/account-info")
async def get_account_info():
    try:
        accounts = await client.metatrader_account_api.get_accounts()
        if not accounts:
            raise HTTPException(status_code=404, detail="Aucun compte MetaTrader trouvé")
        
        account = accounts[0]
        connection = account.get_rpc_connection()
        await connection.connect()
        await connection.wait_synchronized()
        info = await connection.get_account_information()
        
        return {
            "success": True,
            "account_login": getattr(account, 'login', 'N/A'),
            "broker": info.get("broker", "Unknown"),
            "currency": info.get("currency", "USD"),
            "server": info.get("server", "Unknown"),
            "balance": info.get("balance", 0),
            "equity": info.get("equity", 0),
            "margin": info.get("margin", 0),
            "freeMargin": info.get("freeMargin", 0),
            "leverage": info.get("leverage", 0),
            "profit": info.get("profit", 0)
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erreur MetaApi: {str(e)}")

@app.get("/positions")
async def get_positions():
    try:
        accounts = await client.metatrader_account_api.get_accounts()
        if not accounts:
            return {"success": False, "positions": [], "message": "Aucun compte"}
        
        account = accounts[0]
        connection = account.get_rpc_connection()
        await connection.connect()
        await connection.wait_synchronized()
        
        positions = await connection.get_positions()
        return {
            "success": True,
            "account_login": getattr(account, 'login', 'N/A'),
            "total_positions": len(positions),
            "positions": positions
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erreur: {str(e)}")

if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
