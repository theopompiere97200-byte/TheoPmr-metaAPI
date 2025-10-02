# backend_metaapi.py
import os
from metaapi_cloud_sdk import MetaApi


# Récupère la clé MetaApi depuis les variables d'environnement
API_KEY = os.getenv("METAAPI_KEY", "")
metaapi = MetaApi(API_KEY)


async def get_first_account():
    """Récupère le premier compte MetaApi configuré"""
    accounts = await metaapi.metatrader_account_api.get_accounts()
    if not accounts or len(accounts) == 0:
        raise Exception("Aucun compte MetaApi trouvé")
    return accounts[0]


async def get_account_info():
    """Retourne les infos du compte (login, balance, equity, etc.)"""
    account = await get_first_account()
    connection = account.get_rpc_connection()

    await connection.connect()
    await connection.wait_synchronized()

    info = await connection.get_account_information()
    return {
        "login": info.get("login"),
        "currency": info.get("currency"),
        "server": info.get("server"),
        "balance": info.get("balance"),
        "equity": info.get("equity"),
        "margin": info.get("margin"),
        "freeMargin": info.get("freeMargin"),
        "leverage": info.get("leverage"),
        "profit": info.get("profit")
    }


async def get_open_positions():
    """Retourne toutes les positions ouvertes sur le compte"""
    account = await get_first_account()
    connection = account.get_rpc_connection()

    await connection.connect()
    await connection.wait_synchronized()

    positions = await connection.get_positions()
    return [
        {
            "id": pos.get("id"),
            "symbol": pos.get("symbol"),
            "type": pos.get("type"),
            "volume": pos.get("volume"),
            "openPrice": pos.get("openPrice"),
            "currentPrice": pos.get("currentPrice"),
            "profit": pos.get("profit"),
            "swap": pos.get("swap"),
            "commission": pos.get("commission"),
            "stopLoss": pos.get("stopLoss"),
            "takeProfit": pos.get("takeProfit"),
            "openTime": pos.get("time")
        }
        for pos in positions
    ]

