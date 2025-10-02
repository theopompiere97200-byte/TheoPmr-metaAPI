# main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from backend_metaapi import get_account_info, get_open_positions

app = FastAPI(title="MetaApi Backend")

# Configuration CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def root():
    return {"message": "MetaApi backend is running 🚀"}


@app.get("/account-info")
async def account_info():
    try:
        return await get_account_info()
    except Exception as e:
        return {"error": str(e)}


@app.get("/positions")
async def positions():
    try:
        return {"positions": await get_open_positions()}
    except Exception as e:
        return {"error": str(e)}
