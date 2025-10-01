import React, { useState } from 'react';
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Label } from "@/components/ui/label";
import { Copy, CheckCircle } from "lucide-react";

export default function MainPy() {
  const [copied, setCopied] = useState(false);

  const mainPyCode = `# main.py
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import os
from metaapi_cloud_sdk import MetaApi

app = FastAPI(title="MetaApi Bridge pour MindTrader")

# CONFIGURATION CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Votre clé API MetaApi
API_TOKEN = os.getenv("METAAPI_KEY", "52c3348b-3e48-473e-88fd-d37734190a3b")
client = MetaApi(API_TOKEN)

@app.get("/")
async def root():
    return {
        "status": "ok",
        "service": "MetaApi Bridge pour MindTrader",
        "version": "1.0.0"
    }

@app.get("/account-info")
async def get_account_info():
    try:
        accounts = await client.metatrader_account_api.get_accounts()
        
        if not accounts or len(accounts) == 0:
            raise HTTPException(
                status_code=404, 
                detail="Aucun compte MetaTrader trouvé"
            )
        
        account = accounts[0]
        connection = account.get_rpc_connection()
        
        await connection.connect()
        await connection.wait_synchronized()
        
        account_info = await connection.get_account_information()
        
        return {
            "success": True,
            "account_login": getattr(account, 'login', 'N/A'),
            "broker": account_info.get("broker", "Unknown"),
            "currency": account_info.get("currency", "USD"),
            "server": account_info.get("server", "Unknown"),
            "balance": account_info.get("balance", 0),
            "equity": account_info.get("equity", 0),
            "margin": account_info.get("margin", 0),
            "freeMargin": account_info.get("freeMargin", 0),
            "leverage": account_info.get("leverage", 0),
            "profit": account_info.get("profit", 0)
        }
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erreur: {str(e)}")

@app.get("/positions")
async def get_positions():
    try:
        accounts = await client.metatrader_account_api.get_accounts()
        
        if not accounts or len(accounts) == 0:
            return {"success": False, "positions": [], "message": "Aucun compte"}
        
        account = accounts[0]
        connection = account.get_rpc_connection()
        
        await connection.connect()
        await connection.wait_synchronized()
        
        positions = await connection.get_positions()
        
        return {
            "success": True,
            "account_login": getattr(account, 'login', 'N/A'),
            "total_positions": len(positions),
            "positions": [
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
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erreur: {str(e)}")`;

  const copyToClipboard = () => {
    navigator.clipboard.writeText(mainPyCode);
    setCopied(true);
    setTimeout(() => setCopied(false), 2000);
  };

  return (
    <Card>
      <CardHeader>
        <CardTitle className="flex items-center gap-2">
          <div className="w-8 h-8 rounded-full bg-blue-600 text-white flex items-center justify-center font-bold">2</div>
          Fichier main.py
        </CardTitle>
      </CardHeader>
      <CardContent className="space-y-4">
        <div className="flex items-center justify-between mb-2">
          <Label className="font-semibold">📄 main.py</Label>
          <Button
            variant="outline"
            size="sm"
            onClick={copyToClipboard}
          >
            {copied ? (
              <><CheckCircle className="w-4 h-4 mr-2 text-green-600" /> Copié !</>
            ) : (
              <><Copy className="w-4 h-4 mr-2" /> Copier</>
            )}
          </Button>
        </div>
        <pre className="bg-slate-900 text-green-400 p-4 rounded-lg text-sm max-h-96 overflow-y-auto">
          {mainPyCode}
        </pre>
        <div className="bg-blue-50 border border-blue-200 rounded-lg p-3">
          <p className="text-sm text-blue-800">
            <strong>📝 Instructions :</strong><br />
            1. Créez un fichier nommé exactement <code className="bg-blue-100 px-1 rounded">main.py</code><br />
            2. Copiez le contenu ci-dessus<br />
            3. Sauvegardez le fichier
          </p>
        </div>
      </CardContent>
    </Card>
  );
}
