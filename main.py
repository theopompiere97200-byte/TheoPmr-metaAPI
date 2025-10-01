import os
from fastapi import FastAPI
from metaapi_cloud_sdk import MetaApi

app = FastAPI()

# Lecture des variables d'environnement
API_TOKEN = os.getenv("METAAPI_KEY")
ACCOUNT_ID = os.getenv("ACCOUNT_ID")

# Vérification des variables
if not API_TOKEN or not ACCOUNT_ID:
    print("⚠️ METAAPI_KEY ou ACCOUNT_ID non définis ! Vérifie tes variables Render")

client = MetaApi(API_TOKEN)

@app.get("/")
async def root():
    return {"status": "ok"}

@app.get("/account-info")
async def account_info():
    if not ACCOUNT_ID:
        return {"error": "Pas de numéro de compte défini"}

    try:
        account = await client.metatrader_account_api.get_account(ACCOUNT_ID)
        # Charger l'état de compte
        state = await account.get_state()
        return {
            "balance": state.balance,
            "equity": state.equity,
            "account_id": ACCOUNT_ID
        }
    except Exception as e:
        return {"error": f"Impossible de récupérer les données : {str(e)}"}
