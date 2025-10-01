from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import os
from metaapi_cloud_sdk import MetaApi

# ✅ Initialisation FastAPI
app = FastAPI(title="MetaApi Bridge pour MindTrader")

# ✅ CORS obligatoire pour Base44
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ✅ Clé API MetaApi (⚠️ à mettre dans Render → Environment Variables)
API_TOKEN = os.getenv("METAAPI_KEY")
if not API_TOKEN:
    raise Exception("⚠️ Variable d'environnement METAAPI_KEY manquante !")

client = MetaApi(API_TOKEN)

# 🔹 Root
@app.get("/")
async def root():
    return {
        "status": "online ✅",
        "service": "MetaApi Bridge pour MindTrader"
    }

# 🔹 Healthcheck pour Render
@app.get("/healthz")
async def healthz():
    return {"status": "healthy 🟢"}

# 🔹 Infos du compte MT5
@app.get("/account-info")
async def get_account_info():
    try:
        accounts = await client.metatrader_account_api.get_accounts_list()
        
        if not accounts:
            raise HTTPException(status_code=404, detail="Aucun compte trouvé")
        
        deployed_accounts = [a for a in accounts if a.state == 'DEPLOYED']
        if not deployed_accounts:
            raise HTTPException(status_code=503, detail="Aucun compte déployé")
        
        account = deployed_accounts[0]
        connection = account.get_rpc_connection()
        
        await connection.connect()
        await connection.wait_synchronized()
        
        account_info = await connection.get_account_information()
        
        return {
            "success": True,
            "account_login": account.login,
            "broker": account_info.get("broker", "Unknown"),
            "currency": account_info.get("currency", "USD"),
            "server": account_info.get("server", "Unknown"),
            "balance": account_info.get("balance", 0),
            "equity": account_info.get("equity", 0),
            "margin": account_info.get("margin", 0),
            "freeMargin": account_info.get("freeMargin", 0),
            "leverage": account_info.get("leverage", 0),
            "profit": account_info.get("profit", 0)
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# 🔹 Positions ouvertes
@app.get("/positions")
async def get_positions():
    try:
        accounts = await client.metatrader_account_api.get_accounts_list()
        
        if not accounts:
            return {"positions": []}
        
        deployed_accounts = [a for a in accounts if a.state == 'DEPLOYED']
        if not deployed_accounts:
            return {"positions": []}
        
        account = deployed_accounts[0]
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
        raise HTTPException(status_code=500, detail=str(e))

# ✅ Lancement (Render utilise cette commande automatiquement)
if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
