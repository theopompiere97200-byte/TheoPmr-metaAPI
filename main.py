import os
from fastapi import FastAPI
from metaapi_cloud_sdk import MetaApi

app = FastAPI()

# Récupération des variables d'environnement
API_TOKEN = os.getenv("METAAPI_KEY")
ACCOUNT_ID = os.getenv("ACCOUNT_ID")

# Vérification que les variables existent
if not API_TOKEN or not ACCOUNT_ID:
    print("⚠️ METAAPI_KEY ou ACCOUNT_ID non définis ! Vérifie tes variables Render")

# Création du client MetaApi
client = MetaApi(API_TOKEN)

@app.get("/")
async def root():
    return {"status": "ok"}

@app.get("/account-info")
async def account_info():
    if not ACCOUNT_ID:
        return {"error": "Pas de numéro de compte défini"}
    
    # Récupération des informations du compte MT5 via MetaApi
    account = await client.metatrader_account_api.get_account(ACCOUNT_ID)
    
    return {
        "balance": account.balance,
        "equity": account.equity,
        "account_id": ACCOUNT_ID
    }
