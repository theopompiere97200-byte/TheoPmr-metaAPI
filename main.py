from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import os
import asyncio
from metaapi_cloud_sdk import MetaApi

app = FastAPI(title="MetaApi Bridge pour MindTrader")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

API_TOKEN = os.getenv("METAAPI_KEY", "52c3348b-3e48-473e-88fd-d37734190a3b")
client = MetaApi(API_TOKEN)

@app.get("/")
async def root():
    return {
        "status": "ok",
        "message": "MetaApi backend is running",
        "version": "1.0.0"
    }

@app.get("/account-info")
async def get_account_info():
    try:
        print("Recuperation des comptes MetaApi...")
        accounts = await client.metatrader_account_api.get_accounts()
        
        if not accounts or len(accounts) == 0:
            raise HTTPException(
                status_code=404, 
                detail="Aucun compte MetaTrader trouve sur votre compte MetaApi"
            )
        
        print(f"{len(accounts)} compte(s) trouve(s)")
        account = accounts[0]
        
        if account.state != "DEPLOYED":
            raise HTTPException(
                status_code=400,
                detail=f"Le compte n'est pas deploye. Statut actuel: {account.state}"
            )
        
        print(f"Connexion au compte {account.login}...")
        connection = account.get_rpc_connection()
        
        await connection.connect()
        print("Attente de la synchronisation...")
        
        try:
            await asyncio.wait_for(connection.wait_synchronized(), timeout=30.0)
            print("Synchronisation complete !")
        except asyncio.TimeoutError:
            print("Timeout synchronisation, tentative de recuperation quand meme...")
        
        print("Recuperation des donnees du compte...")
        account_info = await connection.get_account_information()
        
        print(f"Balance: {account_info.get('balance', 'N/A')}")
        print(f"Equity: {account_info.get('equity', 'N/A')}")
        
        return {
            "success": True,
            "account_login": str(account.login),
            "account_id": account.id,
            "broker": account_info.get("broker", "Unknown"),
            "currency": account_info.get("currency", "USD"),
            "server": account_info.get("server", "Unknown"),
            "balance": account_info.get("balance", 0),
            "equity": account_info.get("equity", 0),
            "margin": account_info.get("margin", 0),
            "freeMargin": account_info.get("freeMargin", 0),
            "leverage": account_info.get("leverage", 0),
            "profit": account_info.get("profit", 0),
            "state": account.state
        }
        
    except HTTPException:
        raise
    except Exception as e:
        print(f"Erreur: {str(e)}")
        raise HTTPException(
            status_code=500, 
            detail=f"Erreur MetaApi: {str(e)}"
        )

@app.get("/positions")
async def get_positions():
    try:
        print("Recuperation des comptes...")
        accounts = await client.metatrader_account_api.get_accounts()
        
        if not accounts or len(accounts) == 0:
            return {
                "success": False, 
                "positions": [], 
                "message": "Aucun compte trouve"
            }
        
        account = accounts[0]
        print(f"Connexion au compte {account.login}...")
        connection = account.get_rpc_connection()
        
        await connection.connect()
        
        try:
            await asyncio.wait_for(connection.wait_synchronized(), timeout=30.0)
        except asyncio.TimeoutError:
            print("Timeout synchronisation positions")
        
        print("Recuperation des positions...")
        positions = await connection.get_positions()
        print(f"{len(positions)} position(s) trouvee(s)")
        
        return {
            "success": True,
            "account_login": str(account.login),
            "total_positions": len(positions),
            "positions": [
                {
                    "id": pos.get("id"),
                    "symbol": pos.get("symbol"),
                    "type": pos.get("type"),
                    "volume": pos.get("volume"),
                    "openPrice": pos.get("openPrice"),
                    "currentPrice": pos.get("currentPrice"),
                    "profit": pos.get("profit"),
                    "swap": pos.get("swap"),
                    "commission": pos.get("commission"),
                    "stopLoss": pos.get("stopLoss"),
                    "takeProfit": pos.get("takeProfit"),
                    "openTime": pos.get("time")
                }
                for pos in positions
            ]
        }
        
    except Exception as e:
        print(f"Erreur positions: {str(e)}")
        raise HTTPException(
            status_code=500, 
            detail=f"Erreur positions: {str(e)}"
        )
