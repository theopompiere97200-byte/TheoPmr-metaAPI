import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from metaapi_cloud_sdk import MetaApi

app = FastAPI()

# ⚠️ Vérification des variables d'environnement
API_TOKEN = os.getenv("METAAPI_KEY")
ACCOUNT_ID = os.getenv("ACCOUNT_ID")

if not API_TOKEN or not ACCOUNT_ID:
    print("⚠️ METAAPI_KEY ou ACCOUNT_ID non définis ! Vérifie tes variables Render")

# Création du client MetaApi
client = MetaApi(API_TOKEN)

# ⚡ Correction CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Autorise toutes les origines (Base44 inclus)
    allow_credentials=False,  # False pour éviter conflit
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
        account = await client.metatrader_account_api.get_account(ACCOUNT_ID)
        state = await account.get_state_async()  # Utilise la méthode actuelle du SDK
        return {
            "balance": state['balance'],
            "equity": state['equity'],
            "account_id": ACCOUNT_ID
        }
    except Exception as e:
        return {"error": f"Impossible de récupérer les données : {str(e)}"}
