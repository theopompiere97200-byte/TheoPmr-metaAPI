import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from metaapi_cloud_sdk import MetaApi

# --- Vérification des variables d'environnement ---
API_TOKEN = os.getenv("METAAPI_KEY")
ACCOUNT_ID = os.getenv("ACCOUNT_ID")

if not API_TOKEN or not ACCOUNT_ID:
    raise Exception("⚠️ METAAPI_KEY ou ACCOUNT_ID non définis ! Vérifie tes variables Render")

# --- Création du client MetaApi ---
client = MetaApi(API_TOKEN)

# --- Création de l'application FastAPI ---
app = FastAPI(title="MetaApi Backend")

# --- Activation CORS pour tous les domaines ---
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # ou ["https://ton-saas.com"] pour plus de sécurité
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    return {"status": "online"}

@app.get("/account-info")
async def account_info():
    try:
        # Récupération de l'état historique (balance, equity) pour MT5 G2
        account = await client.metatrader_account_api.get_account(ACCOUNT_ID)
        state = await account.get_historical_state()  # méthode correcte
        return {
            "balance": state.balance,
            "equity": state.equity,
            "account_id": ACCOUNT_ID
        }
    except Exception as e:
        return {"error": f"Impossible de récupérer les données : {str(e)}"}
