from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import os
import asyncio
from metaapi_cloud_sdk import MetaApi

app = FastAPI()

# 🔹 Activer CORS pour toutes les requêtes (nécessaire pour Base44)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # autoriser toutes les origines
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 🔹 Récupérer la clé MetaApi depuis les variables d'environnement
API_TOKEN = os.getenv("METAAPI_KEY")
if not API_TOKEN:
    raise RuntimeError("Veuillez définir la variable d'environnement METAAPI_KEY avec votre clé MetaApi")

client = MetaApi(API_TOKEN)

# 🔹 Endpoint racine pour tester le backend
@app.get("/")
async def root():
    return {"message": "Backend MetaApi OK"}

# 🔹 Endpoint exact pour Base44
@app.get("/account-info")
async def account_info():
    try:
        # Récupérer la liste des comptes associés à la clé MetaApi
        accounts_list = await client.metatrader_account_api.get_accounts_list()
        info = []
        for summary in accounts_list:
            # Récupérer les infos détaillées de chaque compte
            account = await client.metatrader_account_api.get_account(summary.id)
            info.append({
                "login": account.login,
                "type": account.type,
                "server": account.server,
                "balance": getattr(account, "balance", None),
                "equity": getattr(account, "equity", None),
                "status": "connected" if getattr(account, "connection_status", "disconnected") == "connected" else "disconnected"
            })
        return info
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# 🔹 Pour exécuter en local si besoin
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "backend_metaapi:app",
        host="0.0.0.0",
        port=int(os.environ.get("PORT", 8000)),
        reload=True
    )
