# main.py - Backend MindTrader pour connexion MT5 simplifiée
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import os
from metaapi_cloud_sdk import MetaApi
import asyncio
from datetime import datetime

app = FastAPI()

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Configuration MetaApi
METAAPI_TOKEN = os.getenv("METAAPI_TOKEN")
if not METAAPI_TOKEN:
    raise ValueError("❌ METAAPI_TOKEN manquant")

meta_api = MetaApi(METAAPI_TOKEN)

# Modèles
class MT5ConnectionRequest(BaseModel):
    user_email: str
    account_number: str
    server: str
    password: str
    nickname: str = None

# Stockage temporaire (utiliser une vraie DB en production)
connections_store = {}

# Endpoints
@app.get("/")
async def root():
    return {"message": "🚀 MindTrader Backend MT5", "version": "1.0"}

@app.post("/api/connect-mt5")
async def connect_mt5(request: MT5ConnectionRequest):
    try:
        # Créer compte MetaApi
        account = await meta_api.metatrader_account_api.create_account({
            'name': request.nickname or f"MT5-{request.account_number}",
            'type': 'cloud',
            'login': request.account_number,
            'password': request.password,
            'server': request.server,
            'platform': 'mt5',
            'magic': 0
        })
        
        # Déployer et connecter
        await account.deploy()
        await account.wait_connected()
        
        connection = account.get_streaming_connection()
        await connection.connect()
        await connection.wait_synchronized()
        
        account_info = await connection.get_account_information()
        
        return {
            "success": True,
            "connection": {
                "id": account.id,
                "account_number": request.account_number,
                "server": request.server,
                "balance": account_info.get('balance', 0),
                "equity": account_info.get('equity', 0),
                "currency": account_info.get('currency', 'USD'),
                "status": "connected"
            }
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/sync-positions/{metaapi_account_id}")
async def sync_positions(metaapi_account_id: str):
    try:
        account = await meta_api.metatrader_account_api.get_account(metaapi_account_id)
        connection = account.get_streaming_connection()
        await connection.connect()
        await connection.wait_synchronized()
        
        positions = await connection.get_positions()
        account_info = await connection.get_account_information()
        
        return {
            "success": True,
            "positions": positions,
            "account": account_info
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/account-history/{metaapi_account_id}")
async def get_history(metaapi_account_id: str):
    try:
        account = await meta_api.metatrader_account_api.get_account(metaapi_account_id)
        connection = account.get_streaming_connection()
        await connection.connect()
        await connection.wait_synchronized()
        
        history = await connection.get_deals(
            start_time=datetime.now().replace(day=1),
            limit=1000
        )
        
        return {"success": True, "trades": history}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
