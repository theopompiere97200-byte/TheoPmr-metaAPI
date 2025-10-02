from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from metaapi_cloud_sdk import MetaApi

import os
import asyncio

app = FastAPI()

# CORS config
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # ouvre à tout le monde
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

API_KEY = os.getenv("METAAPI_TOKEN", "")
metaapi = MetaApi(API_KEY)


@app.get("/")
async def root():
    return {"message": "MetaApi backend is running 🚀"}


@app.get("/account-info")
async def account_info():
    try:
        accounts = await metaapi.metatrader_account_api.get_accounts()
        if not accounts:
            return {"error": "Aucun compte MetaApi trouvé"}

        account = accounts[0]

        # Connexion au compte
        connection = account.get_rpc_connection()
        await connection.connect()

        # Attente de la connexion
        await connection.wait_synchronized()

        # Récupération des infos
        info = await connection.get_account_information()

        return {
            "login": info.get("login"),
            "currency": info.get("currency"),
            "server": info.get("server"),
            "balance": info.get("balance"),
            "equity": info.get("equity"),
        }

    except Exception as e:
        return {"error": str(e)}
