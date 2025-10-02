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
import asyncio
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
        "message": "MetaApi backend is running 🚀",
        "version": "1.0.0"
    }

@app.get("/account-info")
async def get_account_info():
    try:
        print("📡 Récupération des comptes MetaApi...")
        accounts = await client.metatrader_account_api.get_accounts()
        
        if not accounts or len(accounts) == 0:
            raise HTTPException(
                status_code=404, 
                detail="Aucun compte MetaTrader trouvé sur votre compte MetaApi"
            )
        
        print(f"✅ {len(accounts)} compte(s) trouvé(s)")
        account = accounts[0]
        
        # Vérifier si le compte est déployé
        if account.state != "DEPLOYED":
            raise HTTPException(
                status_code=400,
                detail=f"Le compte n'est pas déployé. Statut actuel: {account.state}"
            )
        
        print(f"🔌 Connexion au compte {account.login}...")
        connection = account.get_rpc_connection()
        
        # Connexion au compte
        await connection.connect()
        print("⏳ Attente de la synchronisation...")
        
        # Attendre la synchronisation avec timeout
        try:
            await asyncio.wait_for(connection.wait_synchronized(), timeout=30.0)
            print("✅ Synchronisation complète !")
        except asyncio.TimeoutError:
            print("⚠️ Timeout synchronisation, tentative de récupération quand même...")
        
        # Récupération des informations du compte
        print("📊 Récupération des données du compte...")
        account_info = await connection.get_account_information()
        
        print(f"💰 Balance: {account_info.get('balance', 'N/A')}")
        print(f"💵 Equity: {account_info.get('equity', 'N/A')}")
        
        return {
            "success": True,
            "account_login": str(account.login),
            "account_id": account.id,
            "broker": account_info.get("broker", "Unknown"),
            "currency": account_info.get("currency", "USD"),
            "server": account_info.get("server", "Unknown"),
            "balance": account_info.get("balance", 0),
            "equity": account_info.get("equity", 0),
            "margin": account_info.get("margin", 0),
            "freeMargin": account_info.get("freeMargin", 0),
            "leverage": account_info.get("leverage", 0),
            "profit": account_info.get("profit", 0),
            "state": account.state
        }
        
    except HTTPException:
        raise
    except Exception as e:
        print(f"❌ Erreur: {str(e)}")
        raise HTTPException(
            status_code=500, 
            detail=f"Erreur MetaApi: {str(e)}"
        )

@app.get("/positions")
async def get_positions():
    try:
        print("📡 Récupération des comptes...")
        accounts = await client.metatrader_account_api.get_accounts()
        
        if not accounts or len(accounts) == 0:
            return {
                "success": False, 
                "positions": [], 
                "message": "Aucun compte trouvé"
            }
        
        account = accounts[0]
        print(f"🔌 Connexion au compte {account.login}...")
        connection = account.get_rpc_connection()
        
        await connection.connect()
        
        try:
            await asyncio.wait_for(connection.wait_synchronized(), timeout=30.0)
        except asyncio.TimeoutError:
            print("⚠️ Timeout synchronisation positions")
        
        print("📊 Récupération des positions...")
        positions = await connection.get_positions()
        print(f"✅ {len(positions)} position(s) trouvée(s)")
        
        return {
            "success": True,
            "account_login": str(account.login),
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
        print(f"❌ Erreur positions: {str(e)}")
        raise HTTPException(
            status_code=500, 
            detail=f"Erreur positions: {str(e)}"
        )`;

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
          Fichier main.py (Version Améliorée)
        </CardTitle>
      </CardHeader>
      <CardContent className="space-y-4">
        <div className="flex items-center justify-between mb-2">
          <Label className="font-semibold">🐍 main.py</Label>
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
        <div className="bg-orange-50 border border-orange-200 rounded-lg p-3">
          <p className="text-sm text-orange-800">
            <strong>⚠️ IMPORTANT - Vérifiez votre clé API :</strong><br />
            1. Allez sur <a href="https://app.metaapi.cloud" target="_blank" className="text-blue-600 underline">https://app.metaapi.cloud</a><br />
            2. Menu → <strong>API</strong> (en haut à droite)<br />
            3. Copiez votre <strong>API Token</strong> (pas le compte ID !)<br />
            4. Mettez à jour la variable <code className="bg-orange-100 px-1 rounded">METAAPI_KEY</code> dans Render avec ce token<br />
            5. Redémarrez votre service Render
          </p>
        </div>
        <div className="bg-blue-50 border border-blue-200 rounded-lg p-3">
          <p className="text-sm text-blue-800">
            <strong>📝 Après avoir copié :</strong><br />
            1. Remplacez TOUT le contenu de <code className="bg-blue-100 px-1 rounded">main.py</code><br />
            2. Commitez et push sur GitHub<br />
            3. Render va redéployer automatiquement<br />
            4. Attendez 2-3 minutes<br />
            5. Revenez tester la connexion
          </p>
        </div>
      </CardContent>
    </Card>
  );
}
