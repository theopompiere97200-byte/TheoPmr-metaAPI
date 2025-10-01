from fastapi import FastAPI
import os
import asyncio
from metaapi_cloud_sdk import MetaApi

app = FastAPI()

API_TOKEN = os.getenv("METAAPI_KEY")
client = MetaApi(API_TOKEN)

@app.get("/")
async def root():
    return {"message": "Backend MetaApi OK"}

@app.get("/accounts")
async def get_accounts():
    accounts = await client.metatrader_account_api.get_accounts()
    return [{"login": a.login, "type": a.type, "server": a.server} for a in accounts]
