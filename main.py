from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import os
import asyncio
from metaapi_cloud_sdk import MetaApi

app = FastAPI()

# Autoriser Base44 ou n'importe quel front
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # tu peux mettre l'URL de ton front si tu veux plus de sécurité
    allow_methods=["*"],
    allow_headers=["*"],
)

# Récupérer le token et l'UUID depuis les variables d'environnement
METAAPI_KEY = os.getenv("METAAPI_KEY")  # ton User Token MetaApi
ACCOUNT_ID = os.getenv("ACCOUNT_ID")    # l'UUID du compte MT5

# Créer le client MetaApi
client = MetaApi(METAAPI_KEY)

@app.get("/")
async def root():
    return {"status": "ok"}

@app.get("/account-info")
async def account_info():
    try:
        account = await client.metatrader_account_api.get_account(ACCOUNT_ID)
        # Refresh pour s'assurer que l'info est à jour
        await account.wait_connected()
        balance = await account.get_balance()
        equity = await account.get_equity()
        return {
            "balance": balance,
            "equity": equity,
            "account_id": ACCOUNT_ID
        }
    except Exception as e:
        return {"error": str(e)}

# Pour lancer en local : uvicorn main:app --reload
