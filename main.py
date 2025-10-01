import os
from fastapi import FastAPI
from metaapi_cloud_sdk import MetaApi

app = FastAPI()

# Lecture des variables d'environnement
API_TOKEN = os.getenv("METAAPI_KEY")
ACCOUNT_ID = os.getenv("ACCOUNT_ID")

# Vérification immédiate pour Render
if not API_TOKEN or not ACCOUNT_ID:
    print("⚠️ METAAPI_KEY ou ACCOUNT_ID non définis ! Vérifie tes variables Render")

# Initialisation du client MetaApi
client = MetaApi(API_TOKEN)

@app.get("/")
async def root():
    return {"status": "ok"}

@app.get("/account-info")
async def account_info():
    # Vérifie que le compte est défini
    if not ACCOUNT_ID:
        return {"error": "Pas de numéro de compte défini"}

    try:
        # Récupère l'objet compte
        account = await client.metatrader_account_api.get_account(ACCOUNT_ID)

        # Assure-toi que le compte est en ligne
        account_state = await account.get_historical_state('latest')

        # Retourne les infos essentielles
        return {
            "balance": account_state.get('balance', None),
            "equity": account_state.get('equity', None),
            "account_id": ACCOUNT_ID,
            "status": "success"
        }

    except Exception as e:
        # Si erreur MetaApi
        return {"error": str(e)}
