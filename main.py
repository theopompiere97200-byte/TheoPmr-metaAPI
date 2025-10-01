import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from metaapi_cloud_sdk import MetaApi

app = FastAPI()

# CORS pour Base44
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # tu peux remplacer "*" par ton domaine Base44 si tu veux
    allow_credentials=False,
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
    return {"status": "ok"}

@app.get("/account-info")
async def account_info():
    if not ACCOUNT_ID:
        return {"error": "Pas de numéro de compte défini"}
    try:
        account = await client.metatrader_account_api.get_account(ACCOUNT_ID)
        # Utilisation de getattr pour éviter les erreurs si certaines propriétés n'existent pas
        return {
            "balance": getattr(account, "balance", None),
            "equity": getattr(account, "equity", None),
            "margin": getattr(account, "margin", None),
            "margin_free": getattr(account, "marginFree", None),
            "account_id": ACCOUNT_ID
        }
    except Exception as e:
        return {"error": f"Impossible de récupérer les données : {str(e)}"}
