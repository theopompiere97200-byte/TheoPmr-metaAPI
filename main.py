import os
from fastapi import FastAPI
from metaapi_cloud_sdk import MetaApi
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# ✅ Vérifier les variables d'environnement
API_TOKEN = os.getenv("METAAPI_KEY")
ACCOUNT_ID = os.getenv("ACCOUNT_ID")

if not API_TOKEN or not ACCOUNT_ID:
    raise Exception("⚠️ METAAPI_KEY ou ACCOUNT_ID non définis ! Vérifie tes variables Render")

# CORS (optionnel si tu appelles depuis ton front)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # ou ton front exact
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialisation du client MetaApi
client = MetaApi(API_TOKEN)

@app.get("/")
async def root():
    return {"status": "online"}

@app.get("/account-info")
async def account_info():
    try:
        # Obtenir l'état actuel du compte
        account = await client.metatrader_account_api.get_account(ACCOUNT_ID)
        state = await account.get_state()  # méthode correcte pour obtenir balance/equity

        return {
            "balance": state.balance,
            "equity": state.equity,
            "account_id": ACCOUNT_ID
        }
    except Exception as e:
        return {"error": f"Impossible de récupérer les données : {str(e)}"}
