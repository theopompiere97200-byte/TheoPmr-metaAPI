# main.py
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import os
from metaapi_cloud_sdk import MetaApi

app = FastAPI(title="MetaApi Bridge pour MindTrader")

# CORS pour autoriser toutes les requêtes depuis Base44
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Clé API MetaApi
API_TOKEN = os.getenv("METAAPI_KEY", "52c3348b-3e48-473e-88fd-d37734190a3b")
client = MetaApi(API_TOKEN)

@app.get("/")
async def root():
    return {"status": "ok", "service": "MetaApi Bridge pour MindTrader", "version": "1.0.0"}

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
            "equity": info.get("e
