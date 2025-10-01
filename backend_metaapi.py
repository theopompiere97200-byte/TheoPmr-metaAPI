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

# 🔹 Endpoint pour lister tous les comptes MT5
@app.get("/accounts")
async def get_accounts():
    try:
        accounts = await client.metatrader_account_api.get_accounts()
        return [{"login": a.login, "type": a.type, "server": a.server} for a in accounts]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# 🔹 Endpoint exact pour Base44
@app.get("/account-info")
async def account_info():
    try:
        accounts = await client.metatrader_account_api.get_accounts()
        info = []
        for a in accounts:
            info.append({
                "login": a.login,
                "type": a.type,
                "server": a.server,
                "balance": getattr(a, "balance", None),
                "equity": getattr(a, "equity", None),
                "status": "connected" if getattr(a, "connection_status", "disconnected") == "connected" else "disconnected"
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
