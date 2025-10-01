from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import os
import asyncio
from metaapi_cloud_sdk import MetaApi

app = FastAPI()

# Activer CORS pour toutes les requêtes (nécessaire pour Base44)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # autoriser toutes les origines
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Récupérer la clé MetaApi depuis les variables d'environnement
API_TOKEN = os.getenv("METAAPI_KEY")
client = MetaApi(API_TOKEN)

@app.get("/")
async def root():
    return {"message": "Backend MetaApi OK"}

@app.get("/accounts")
async def get_accounts():
    accounts = await client.metatrader_account_api.get_accounts()
    return [{"login": a.login, "type": a.type, "server": a.server} for a in accounts]

@app.get("/account-info")
async def account_info():
    # endpoint pour Base44
    accounts = await client.metatrader_account_api.get_accounts()
    info = []
    for a in accounts:
        info.append({
            "login": a.login,
            "type": a.type,
            "server": a.server,
            "balance": getattr(a, "balance", None),
            "equity": getattr(a, "equity", None)
        })
    return info

# Pour exécuter en local si besoin
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("backend_metaapi:app", host="0.0.0.0", port=int(os.environ.get("PORT", 8000)), reload=True)
