import os
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from metaapi_cloud_sdk import MetaApi

# Initialisation FastAPI
app = FastAPI()

# Configuration CORS pour Base44
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # autorise toutes les origines, tu peux mettre l'URL exacte de Base44 si tu veux
    allow_credentials=False,  # évite le conflit
    allow_methods=["*"],
    allow_headers=["*"],
)

# Récupération des variables d'environnement
API_TOKEN = os.getenv("METAAPI_KEY")
ACCOUNT_ID = os.getenv("ACCOUNT_ID")

if not API_TOKEN or not ACCOUNT_ID:
    print("⚠️ METAAPI_KEY ou ACCOUNT_ID non définis ! Vérifie tes variables Render")

# Initialisation MetaApi
client = MetaApi(API_TOKEN)

@app.get("/")
async def root():
    return {"status": "online"}

@app.get("/account-info")
async def account_info():
    if not ACCOUNT_ID:
        return {"error": "Pas de numéro de compte défini"}

    try:
        # Récupération du compte MetaTrader
        account = await client.metatrader_account_api.get_account(ACCOUNT_ID)
        # Récupération des informations de balance et equity
        await account.wait_connected()
        state = await account.get_state()
        return {
            "balance": state.balance,
            "equity": state.equity,
            "account_id": ACCOUNT_ID
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Impossible de récupérer les données : {str(e)}")
