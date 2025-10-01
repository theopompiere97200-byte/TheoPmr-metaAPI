# main.py
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import os
from metaapi_cloud_sdk import MetaApi

app = FastAPI(title="MetaApi Bridge pour MindTrader")

# ✅ CONFIGURATION CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,  # important pour éviter les conflits avec Base44
    allow_methods=["*"],
    allow_headers=["*"],
)

# 🔑 Clé API MetaApi
API_TOKEN = os.getenv("METAAPI_KEY")
if not API_TOKEN:
    raise Exception("Veuillez définir la variable d'environnement METAAPI_KEY")

client = MetaApi(API_TOKEN)

@app.get("/")
async def root():
    return {
        "status": "ok",
        "service": "MetaApi Bridge pour MindTrader",
        "version": "1.0.0"
    }

@app.get("/account-info")
async def get_account_info():
    try:
        accounts = await client.metatrader_account_api.get_accounts()
        if not accounts:
            raise HTTPException(status_code=404, detail="Aucun compte MetaTrader trouvé sur MetaApi")
        account = accounts[0]

        connection = account.get_rpc_connection()
        await connection.connect()
        await connection.wait_synchronized()
        account_info = await connection.get_account_information()

        return {
            "success": True,
            "account_login": getattr(account, 'login', 'N/A'),
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
        raise HTTPException(status_code=500, detail=f"Erreur MetaApi: {str(e)}")

@app.get("/positions")
async def get_positions():
    try:
        accounts = await client.metatrader_account_api.get_accounts()
        if not accounts:
            return {"success": False, "positions": [], "message": "Aucun compte trouvé"}
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

@app.get("/history")
async def get_history(days: int = 30):
    from datetime import datetime, timedelta
    try:
        accounts = await client.metatrader_account_api.get_accounts()
        if not accounts:
            return {"success": False, "deals": [], "message": "Aucun compte trouvé"}
        account = accounts[0]
        connection = account.get_rpc_connection()
        await connection.connect()
        await connection.wait_synchronized()
        start_time = datetime.now() - timedelta(days=days)
        deals = await connection.get_deals_by_time_range(start_time, datetime.now())
        return {"success": True, "account_login": getattr(account, 'login', 'N/A'), "total_deals": len(deals), "deals": deals}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erreur: {str(e)}")

if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
