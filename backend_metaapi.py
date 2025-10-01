# backend_metaapi.py
from metaapi_cloud_sdk import MetaApi
import os

API_TOKEN = os.getenv("METAAPI_KEY", "52c3348b-3e48-473e-88fd-d37734190a3b")
client = MetaApi(API_TOKEN)

def get_first_account():
    accounts = client.metatrader_account_api.get_accounts()
    if not accounts:
        return None
    return accounts[0]

def get_account_balance(account):
    try:
        connection = account.get_rpc_connection()
        connection.connect()
        connection.wait_synchronized()
        info = connection.get_account_information()
        return info.get("balance", 0)
    except Exception:
        return 0
