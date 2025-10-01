import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from metaapi_cloud_sdk import MetaApi

app = FastAPI()

# ⚠️ Variables d'environnement
API_TOKEN = os.getenv("METAAPI_KEY")
ACCOUNT_ID = os.getenv("ACCOUNT_ID")

if not API_TOKEN or not ACCOUNT_ID:
    print("⚠️ METAAPI_KEY ou ACCOUNT_ID non définis ! Vérifie tes variables Render")

client = MetaApi(API_TOKEN)

# ⚡ CORS simplifié pour Base44
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    return {"status": "online"}

@app.get("/account-info")
async def account_info():
    if not ACCOUNT_ID:
        return {"error": "Pas de numéro de compte défini"}
    try:
        # Récupère simplement le compte MetaTrader
        account = await client.metatrader_account_api.get_account(ACCOUNT_ID)

        # Utilisation sécurisée avec getattr() pour éviter les erreurs
        balance = getattr(account, "balance", None)
        equity = getattr(account, "equity", None)

        return {
            "balance": balance,
            "equity": equity,
            "account_id": ACCOUNT_ID
        }
    except Exception as e:
        return {"error": f"Impossible de récupérer les données : {str(e)}"}
