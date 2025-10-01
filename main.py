import React from 'react';
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Alert, AlertDescription, AlertTitle } from "@/components/ui/alert";
import { Button } from "@/components/ui/button";
import { ExternalLink, Copy, CheckCircle, Rocket, Code, AlertCircle, Github } from "lucide-react";
import { useState } from "react";

export default function MT5BackendDocumentation() {
  const [copiedFile, setCopiedFile] = useState('');

  const copyToClipboard = (text, fileName) => {
    navigator.clipboard.writeText(text);
    setCopiedFile(fileName);
    setTimeout(() => setCopiedFile(''), 2000);
  };

  const mainPyCode = `# main.py
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import os
from metaapi_cloud_sdk import MetaApi

app = FastAPI(title="MetaApi Bridge pour MindTrader")

# ✅ CONFIGURATION CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 🔑 Votre clé API MetaApi
API_TOKEN = os.getenv("METAAPI_KEY", "52c3348b-3e48-473e-88fd-d37734190a3b")
client = MetaApi(API_TOKEN)

@app.get("/")
async def root():
    """Endpoint de vérification"""
    return {
        "status": "ok",
        "service": "MetaApi Bridge pour MindTrader",
        "version": "1.0.0"
    }

@app.get("/account-info")
async def get_account_info():
    """Récupère les informations de votre compte MT5"""
    try:
        # Récupérer tous les comptes
        accounts = await client.metatrader_account_api.get_accounts()
        
        if not accounts or len(accounts) == 0:
            raise HTTPException(
                status_code=404, 
                detail="Aucun compte MetaTrader trouvé sur MetaApi"
            )
        
        # Prendre le premier compte
        account = accounts[0]
        
        # Obtenir la connexion RPC
        connection = account.get_rpc_connection()
        
        # Connexion au compte MT5
        await connection.connect()
        await connection.wait_synchronized()
        
        # Récupération des informations du compte
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
        raise HTTPException(
            status_code=500, 
            detail=f"Erreur MetaApi: {str(e)}"
        )

@app.get("/positions")
async def get_positions():
    """Récupère toutes vos positions ouvertes"""
    try:
        accounts = await client.metatrader_account_api.get_accounts()
        
        if not accounts or len(accounts) == 0:
            return {
                "success": False, 
                "positions": [], 
                "message": "Aucun compte trouvé"
            }
        
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
        raise HTTPException(
            status_code=500, 
            detail=f"Erreur: {str(e)}"
        )

@app.get("/history")
async def get_history(days: int = 30):
    """Récupère l'historique des trades"""
    try:
        from datetime import datetime, timedelta
        
        accounts = await client.metatrader_account_api.get_accounts()
        
        if not accounts or len(accounts) == 0:
            return {
                "success": False, 
                "deals": [], 
                "message": "Aucun compte trouvé"
            }
        
        account = accounts[0]
        connection = account.get_rpc_connection()
        
        await connection.connect()
        await connection.wait_synchronized()
        
        start_time = datetime.now() - timedelta(days=days)
        deals = await connection.get_deals_by_time_range(start_time, datetime.now())
        
        return {
            "success": True,
            "account_login": getattr(account, 'login', 'N/A'),
            "total_deals": len(deals),
            "deals": [
                {
                    "id": deal.get("id"),
                    "symbol": deal.get("symbol"),
                    "type": deal.get("type"),
                    "volume": deal.get("volume"),
                    "price": deal.get("price"),
                    "profit": deal.get("profit"),
                    "commission": deal.get("commission"),
                    "swap": deal.get("swap"),
                    "time": deal.get("time")
                }
                for deal in deals
            ]
        }
        
    except Exception as e:
        raise HTTPException(
            status_code=500, 
            detail=f"Erreur: {str(e)}"
        )

if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)`;

  const requirementsTxtCode = `fastapi==0.104.1
uvicorn[standard]==0.24.0
metaapi-cloud-sdk==27.0.2
python-dateutil==2.8.2`;

  return (
    <div className="space-y-6">
      <Alert className="bg-red-50 border-red-300">
        <AlertCircle className="h-4 w-4 text-red-600" />
        <AlertTitle className="text-red-900">❌ Erreur 404 : Backend non à jour</AlertTitle>
        <AlertDescription className="text-red-700">
          Votre backend Render n'a pas le bon code. Suivez les étapes ci-dessous pour le mettre à jour.
        </AlertDescription>
      </Alert>

      {/* Guide de redéploiement étape par étape */}
      <Card className="shadow-lg border-0 bg-gradient-to-r from-blue-50 to-indigo-50">
        <CardHeader>
          <CardTitle className="flex items-center gap-2 text-blue-900">
            <Rocket className="w-5 h-5" />
            📝 Guide de Redéploiement (5 minutes)
          </CardTitle>
        </CardHeader>
        <CardContent className="space-y-4 text-sm text-blue-900">
          <div className="space-y-3">
            <h4 className="font-semibold text-lg">Étape 1 : Copier le nouveau code</h4>
            <p>Cliquez sur "Copier le code" ci-dessous pour copier le fichier <code className="bg-white px-2 py-1 rounded">main.py</code></p>
          </div>

          <div className="space-y-3">
            <h4 className="font-semibold text-lg">Étape 2 : Mettre à jour GitHub</h4>
            <ol className="list-decimal list-inside space-y-2 ml-2">
              <li>Allez sur votre repository GitHub du backend</li>
              <li>Ouvrez le fichier <code className="bg-white px-2 py-1 rounded">main.py</code></li>
              <li>Cliquez sur l'icône crayon ✏️ (Edit)</li>
              <li><strong>Supprimez TOUT le contenu actuel</strong></li>
              <li><strong>Collez le nouveau code</strong> que vous avez copié</li>
              <li>En bas de la page, ajoutez un message : "Fix CORS and add /account-info"</li>
              <li>Cliquez sur "Commit changes"</li>
            </ol>
          </div>

          <div className="space-y-3">
            <h4 className="font-semibold text-lg">Étape 3 : Render redéploie automatiquement</h4>
            <ol className="list-decimal list-inside space-y-2 ml-2">
              <li>Allez sur https://dashboard.render.com</li>
              <li>Cliquez sur votre service "theopmr-metaapi"</li>
              <li>Vous verrez "Deploying..." en haut</li>
              <li>Attendez 2-3 minutes (le statut passera à "Live")</li>
            </ol>
          </div>

          <div className="space-y-3">
            <h4 className="font-semibold text-lg">Étape 4 : Tester</h4>
            <ol className="list-decimal list-inside space-y-2 ml-2">
              <li>Ouvrez votre navigateur</li>
              <li>Allez sur : <code className="bg-white px-2 py-1 rounded">https://theopmr-metaapi.onrender.com/account-info</code></li>
              <li>✅ Si vous voyez du JSON avec "balance", "equity", etc. → C'est bon !</li>
              <li>❌ Si vous avez une erreur 404 → Attendez encore 1-2 minutes</li>
            </ol>
          </div>

          <div className="space-y-3">
            <h4 className="font-semibold text-lg">Étape 5 : Reconnecter dans MindTrader</h4>
            <p>Revenez sur cette page et testez à nouveau la connexion !</p>
          </div>
        </CardContent>
      </Card>

      {/* Fichier 1: main.py */}
      <Card className="shadow-lg border-0 bg-white">
        <CardHeader>
          <CardTitle className="flex items-center justify-between">
            <div className="flex items-center gap-2">
              <Code className="w-5 h-5 text-purple-500" />
              <span>1️⃣ main.py (Code Complet)</span>
            </div>
            <Button
              size="sm"
              variant="outline"
              onClick={() => copyToClipboard(mainPyCode, 'main.py')}
            >
              {copiedFile === 'main.py' ? (
                <>
                  <CheckCircle className="w-4 h-4 mr-2 text-green-600" />
                  Copié !
                </>
              ) : (
                <>
                  <Copy className="w-4 h-4 mr-2" />
                  Copier le code
                </>
              )}
            </Button>
          </CardTitle>
        </CardHeader>
        <CardContent>
          <pre className="bg-slate-900 text-slate-100 p-4 rounded-lg overflow-x-auto text-xs max-h-96">
            <code>{mainPyCode}</code>
          </pre>
        </CardContent>
      </Card>

      {/* Fichier 2: requirements.txt */}
      <Card className="shadow-lg border-0 bg-white">
        <CardHeader>
          <CardTitle className="flex items-center justify-between">
            <div className="flex items-center gap-2">
              <Code className="w-5 h-5 text-orange-500" />
              <span>2️⃣ requirements.txt</span>
            </div>
            <Button
              size="sm"
              variant="outline"
              onClick={() => copyToClipboard(requirementsTxtCode, 'requirements.txt')}
            >
              {copiedFile === 'requirements.txt' ? (
                <>
                  <CheckCircle className="w-4 h-4 mr-2 text-green-600" />
                  Copié !
                </>
              ) : (
                <>
                  <Copy className="w-4 h-4 mr-2" />
                  Copier le code
                </>
              )}
            </Button>
          </CardTitle>
        </CardHeader>
        <CardContent>
          <pre className="bg-slate-900 text-slate-100 p-4 rounded-lg overflow-x-auto text-xs">
            <code>{requirementsTxtCode}</code>
          </pre>
        </CardContent>
      </Card>

      {/* Vérification rapide */}
      <Alert className="bg-green-50 border-green-300">
        <CheckCircle className="h-4 w-4 text-green-600" />
        <AlertTitle className="text-green-900">✅ Vérification rapide</AlertTitle>
        <AlertDescription className="text-green-700">
          <p className="mb-2">Après le redéploiement, testez ces URLs dans votre navigateur :</p>
          <ul className="list-disc list-inside space-y-1">
            <li><code className="bg-white px-2 py-1 rounded text-xs">https://theopmr-metaapi.onrender.com/</code> → Doit afficher: {`{"status": "ok", ...}`}</li>
            <li><code className="bg-white px-2 py-1 rounded text-xs">https://theopmr-metaapi.onrender.com/account-info</code> → Doit afficher vos données MT5</li>
          </ul>
        </AlertDescription>
      </Alert>
    </div>
  );
}
