import os
from fastapi import FastAPI
from metaapi_cloud_sdk import MetaApi

app = FastAPI()

# Récupère les variables d'environnement
API_TOKEN = os.getenv("METAAPI_KEY")
ACCOUNT_ID = os.getenv("ACCOUNT_ID")

# Vérifie que les variables sont bien définies
if not API_TOKEN or not ACCOUNT_ID:
    print("⚠️ METAAPI_KEY ou ACCOUNT_ID non définis ! Vérifie tes variables Render")

# Initialise le client MetaApi
client = MetaApi(API_TOKEN)

@app.get("/")
async def root():
    return {"status": "ok"}

@app.get("/account-info")
async def account_info():
    if not ACCOUNT_ID:
        return {"error": "Pas de numéro de compte défini"}
    try:
        # Récupère l'objet compte
        account = await client.metatrader_account_api.get_account(ACCOUNT_ID)
        # Récupère l'état du compte pour obtenir balance et equity
        state = await account.get_state()
        return {
            "balance": state.get('balance', None),
            "equity": state.get('equity', None),
            "account_id": ACCOUNT_ID
        }
    except Exception as e:
        # Retourne l'erreur si quelque chose ne va pas
        return {"error": str(e)}
