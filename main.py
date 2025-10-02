from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import os
import asyncio
from metaapi_cloud_sdk import MetaApi
from datetime import datetime, timedelta

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
        accounts = await client.metatrader_account_api.get_accounts_with_infinite_scroll_pagination()
        
        if not accounts or len(accounts) == 0:
            raise HTTPException(
                status_code=404, 
                detail="Aucun compte MetaTrader trouve"
            )
        
        account = accounts[0]
        
        if account.state != "DEPLOYED":
            raise HTTPException(
                status_code=400,
                detail=f"Compte non deploye. Statut: {account.state}"
            )
        
        print(f"Connexion au compte {account.login}...")
        connection = account.get_rpc_connection()
        
        await connection.connect()
        print("Attente synchronisation...")
        
        try:
            await asyncio.wait_for(connection.wait_synchronized(), timeout=45.0)
            print("Synchronisation OK")
        except asyncio.TimeoutError:
            print("Timeout sync - recuperation partielle")
        
        account_info = await connection.get_account_information()
        
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
        raise HTTPException(status_code=500, detail=f"Erreur MetaApi: {str(e)}")

@app.get("/positions")
async def get_positions():
    try:
        print("Recuperation positions...")
        accounts = await client.metatrader_account_api.get_accounts_with_infinite_scroll_pagination()
        
        if not accounts or len(accounts) == 0:
            return {"success": False, "positions": [], "message": "Aucun compte"}
        
        account = accounts[0]
        connection = account.get_rpc_connection()
        
        await connection.connect()
        
        try:
            await asyncio.wait_for(connection.wait_synchronized(), timeout=45.0)
            print("Sync positions OK")
        except asyncio.TimeoutError:
            print("Timeout sync positions")
        
        positions = await connection.get_positions()
        print(f"{len(positions)} position(s) ouverte(s)")
        
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
        raise HTTPException(status_code=500, detail=f"Erreur positions: {str(e)}")

@app.get("/history")
async def get_history():
    try:
        print("Recuperation historique...")
        accounts = await client.metatrader_account_api.get_accounts_with_infinite_scroll_pagination()
        
        if not accounts or len(accounts) == 0:
            return {"success": False, "deals": [], "message": "Aucun compte"}
        
        account = accounts[0]
        connection = account.get_rpc_connection()
        
        await connection.connect()
        
        try:
            await asyncio.wait_for(connection.wait_synchronized(), timeout=45.0)
        except asyncio.TimeoutError:
            print("Timeout sync history")
        
        # Récupérer l'historique des 30 derniers jours
        start_time = datetime.now() - timedelta(days=30)
        deals = await connection.get_deals_by_time_range(start_time, datetime.now())
        
        print(f"{len(deals)} deal(s) dans l'historique")
        
        return {
            "success": True,
            "account_login": str(account.login),
            "total_deals": len(deals),
            "deals": [
                {
                    "id": deal.get("id"),
                    "type": deal.get("type"),
                    "symbol": deal.get("symbol"),
                    "volume": deal.get("volume"),
                    "price": deal.get("price"),
                    "profit": deal.get("profit"),
                    "commission": deal.get("commission"),
                    "swap": deal.get("swap"),
                    "time": deal.get("time"),
                    "entryType": deal.get("entryType")
                }
                for deal in deals
            ]
        }
        
    except Exception as e:
        print(f"Erreur historique: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Erreur historique: {str(e)}")
