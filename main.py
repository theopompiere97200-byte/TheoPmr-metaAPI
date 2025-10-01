import os
from fastapi import FastAPI
from metaapi_cloud_sdk import MetaApi

app = FastAPI()

# Récupération des variables d'environnement
API_TOKEN = os.getenv("METAAPI_KEY")
ACCOUNT_ID = os.getenv("ACCOUNT_ID")

# Vérification que les variables sont bien définies
if not API_TOKEN or not ACCOUNT_ID:
    raise ValueError("⚠️ METAAPI_KEY ou ACCOUNT_ID non définis ! Vérifie tes variables Render")

# Initialisation du client MetaApi
client = MetaApi(API_TOKEN)

@app.get("/")
async def root():
    return {"status": "ok"}

@app.get("/account-info")
async def account_info():
    try:
        account = await client.metatrader_account_api.get_account(ACCOUNT_ID)
        # Synchronisation de l'état de l'account
        state = await account.get_state()  # compatible G2
        return {
            "balance": state.balance,
            "equity": state.equity,
            "margin": state.margin,
            "free_margin": state.freeMargin,
            "margin_level": state.marginLevel,
            "account_id": ACCOUNT_ID
        }
    except Exception as e:
        return {"error": f"Impossible de récupérer les données : {str(e)}"}
