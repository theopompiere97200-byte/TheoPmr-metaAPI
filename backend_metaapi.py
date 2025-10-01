from metaapi_cloud_sdk import MetaApi

class MetaApiHelper:
    def __init__(self, api_token):
        self.client = MetaApi(api_token)

    async def get_account_info(self, account_id):
        account = await self.client.metatrader_account_api.get_account(account_id)
        return {
            "balance": getattr(account, "balance", None),
            "equity": getattr(account, "equity", None),
            "margin": getattr(account, "margin", None),
            "margin_free": getattr(account, "marginFree", None),
            "account_id": account_id
        }
