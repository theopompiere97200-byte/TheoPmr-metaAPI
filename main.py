import React from 'react';
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Alert, AlertDescription, AlertTitle } from "@/components/ui/alert";
import { Button } from "@/components/ui/button";
import { Label } from "@/components/ui/label";
import { ExternalLink, Copy, CheckCircle, Rocket, Code, AlertCircle, Github } from "lucide-react";
import { useState } from "react";

export default function MT5BackendDocumentation() {
  const [copiedFile, setCopiedFile] = useState('');

  const copyToClipboard = (text, fileName) => {
    navigator.clipboard.writeText(text);
    setCopiedFile(fileName);
    setTimeout(() => setCopiedFile(''), 2000);
  };

  const requirementsTxtCode = `fastapi==0.104.1
uvicorn[standard]==0.24.0
metaapi-cloud-sdk==27.0.1`;

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

  return (
    <div className="space-y-6">
      <Alert className="bg-blue-50 border-blue-200">
        <Rocket className="h-5 w-5 text-blue-600" />
        <AlertTitle className="text-blue-900 text-lg">🚀 Déploiement Backend</AlertTitle>
        <AlertDescription className="text-blue-800">
          Guide complet pour déployer votre backend MetaApi sur Render.com
        </AlertDescription>
      </Alert>

      <Card>
        <CardHeader>
          <CardTitle className="flex items-center gap-2">
            <div className="w-8 h-8 rounded-full bg-blue-600 text-white flex items-center justify-center font-bold">1</div>
            Fichier requirements.txt
          </CardTitle>
        </CardHeader>
        <CardContent className="space-y-4">
          <div className="flex items-center justify-between mb-2">
            <Label className="font-semibold">📄 requirements.txt</Label>
            <Button
              variant="outline"
              size="sm"
              onClick={() => copyToClipboard(requirementsTxtCode, 'requirements.txt')}
            >
              {copiedFile === 'requirements.txt' ? (
                <><CheckCircle className="w-4 h-4 mr-2 text-green-600" /> Copié !</>
              ) : (
                <><Copy className="w-4 h-4 mr-2" /> Copier</>
              )}
            </Button>
          </div>
          <pre className="bg-slate-900 text-green-400 p-4 rounded-lg text-sm">
            {requirementsTxtCode}
          </pre>
        </CardContent>
      </Card>

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
              onClick={() => copyToClipboard(mainPyCode, 'main.py')}
            >
              {copiedFile === 'main.py' ? (
                <><CheckCircle className="w-4 h-4 mr-2 text-green-600" /> Copié !</>
              ) : (
                <><Copy className="w-4 h-4 mr-2" /> Copier</>
              )}
            </Button>
          </div>
          <pre className="bg-slate-900 text-green-400 p-4 rounded-lg text-sm max-h-96 overflow-y-auto">
            {mainPyCode}
          </pre>
        </CardContent>
      </Card>

      <Card>
        <CardHeader>
          <CardTitle className="flex items-center gap-2">
            <div className="w-8 h-8 rounded-full bg-blue-600 text-white flex items-center justify-center font-bold">3</div>
            Upload sur GitHub
          </CardTitle>
        </CardHeader>
        <CardContent className="space-y-3">
          <ol className="list-decimal list-inside space-y-2 text-sm">
            <li>Créez un dossier sur votre PC : <code className="bg-slate-100 px-2 py-1 rounded">metaapi-backend</code></li>
            <li>Créez les 2 fichiers dedans avec le contenu copié ci-dessus</li>
            <li>Allez sur <a href="https://github.com/new" target="_blank" className="text-blue-600 hover:underline">github.com/new</a></li>
            <li>Créez un dépôt "metaapi-backend" (Public)</li>
            <li>Uploadez les 2 fichiers via "Add file" → "Upload files"</li>
          </ol>
          <Button variant="outline" asChild className="w-full">
            <a href="https://github.com/new" target="_blank">
              <Github className="w-4 h-4 mr-2" />
              Créer le dépôt
            </a>
          </Button>
        </CardContent>
      </Card>

      <Card>
        <CardHeader>
          <CardTitle className="flex items-center gap-2">
            <div className="w-8 h-8 rounded-full bg-blue-600 text-white flex items-center justify-center font-bold">4</div>
            Déployer sur Render
          </CardTitle>
        </CardHeader>
        <CardContent className="space-y-3">
          <ol className="list-decimal list-inside space-y-2 text-sm">
            <li>Allez sur <a href="https://dashboard.render.com" target="_blank" className="text-blue-600 hover:underline">dashboard.render.com</a></li>
            <li>Cliquez sur "New +" → "Web Service"</li>
            <li>Connectez votre dépôt GitHub</li>
            <li>Configurez :
              <ul className="ml-6 mt-2 space-y-1">
                <li>• Name: <code className="bg-slate-100 px-2 py-1 rounded">metaapi-backend</code></li>
                <li>• Runtime: <code className="bg-slate-100 px-2 py-1 rounded">Python 3</code></li>
                <li>• Build Command: <code className="bg-slate-100 px-2 py-1 rounded">pip install -r requirements.txt</code></li>
                <li>• Start Command: <code className="bg-slate-100 px-2 py-1 rounded">uvicorn main:app --host 0.0.0.0 --port $PORT</code></li>
              </ul>
            </li>
            <li>Ajoutez la variable d'environnement :
              <ul className="ml-6 mt-2">
                <li>• Key: <code className="bg-slate-100 px-2 py-1 rounded">METAAPI_KEY</code></li>
                <li>• Value: <code className="bg-slate-100 px-2 py-1 rounded">52c3348b-3e48-473e-88fd-d37734190a3b</code></li>
              </ul>
            </li>
            <li>Cliquez sur "Create Web Service"</li>
            <li>Attendez 3-5 minutes le déploiement</li>
          </ol>
          <Button variant="outline" asChild className="w-full">
            <a href="https://dashboard.render.com" target="_blank">
              <ExternalLink className="w-4 h-4 mr-2" />
              Aller sur Render
            </a>
          </Button>
        </CardContent>
      </Card>
    </div>
  );
}
