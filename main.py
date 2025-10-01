import os
from fastapi import FastAPI
from metaapi_cloud_sdk import MetaApi

app = FastAPI(title="MetaApi Service")

# Lecture des variables d'environnement
API_TOKEN = os.getenv("METAAPI_KEY")
ACCOUNT_ID = os.getenv("ACCOUNT_ID")

# Vérification des variables
if not API_TOKEN:
    print("⚠️ METAAPI_KEY non défini ! Vérifie tes variables Render")
if not ACCOUNT_ID:
    print("⚠️ ACCOUNT_ID non défini ! Vérifie tes variables Render")

# Initialisation du client MetaApi
client = MetaApi(API_TOKEN)

@app.get("/")
async def root():
    return {"status": "ok", "message": "Service en ligne"}

@app.get("/account-info")
async def account_info():
    # Vérifie que ACCOUNT_ID est défini
    if not ACCOUNT_ID:
        return {"error": "Pas de numéro de compte défini"}

    try:
        # Récupère l'objet compte
        account = await client.metatrader_account_api.get_account(ACCOUNT_ID)

        # Récupère l'état actuel du compte
        state = await account.get_state()

        # Retourne les informations importantes
        return {
            "account_id": ACCOUNT_ID,
            "balance": state.get("balance", None),
            "equity": state.get("equity", None),
            "margin_free": state.get("marginFree", None),
            "margin_level": state.get("marginLevel", None),
            "status": "success"
        }

    except Exception as e:
        return {"error": f"Impossible de récupérer les données : {str(e)}"}

# Commande pour tester le service localement
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=10000)
