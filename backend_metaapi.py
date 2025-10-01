import React from 'react';
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Alert, AlertDescription, AlertTitle } from "@/components/ui/alert";
import { Button } from "@/components/ui/button";
import { ExternalLink, Rocket, Github } from "lucide-react";

import RequirementsTxt from './RequirementsTxt';
import MainPy from './MainPy';

export default function MT5BackendDocumentation() {
  return (
    <div className="space-y-6">
      <Alert className="bg-blue-50 border-blue-200">
        <Rocket className="h-5 w-5 text-blue-600" />
        <AlertTitle className="text-blue-900 text-lg">🚀 Déploiement Backend sur Render.com</AlertTitle>
        <AlertDescription className="text-blue-800">
          Suivez ce guide pour déployer votre backend MetaApi en <strong>5 minutes chrono</strong> !
        </AlertDescription>
      </Alert>

      {/* Fichier 1: requirements.txt */}
      <RequirementsTxt />

      {/* Fichier 2: main.py */}
      <MainPy />

      {/* Étape 3: Upload sur GitHub */}
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
              Créer le dépôt GitHub
            </a>
          </Button>
        </CardContent>
      </Card>

      {/* Étape 4: Déployer sur Render */}
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
            <li>Connectez votre dépôt GitHub "metaapi-backend"</li>
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
            <li>Attendez 3-5 minutes le déploiement ⏳</li>
            <li>Copiez l'URL générée (ex: https://votre-app.onrender.com)</li>
          </ol>
          <Button variant="outline" asChild className="w-full">
            <a href="https://dashboard.render.com" target="_blank">
              <ExternalLink className="w-4 h-4 mr-2" />
              Aller sur Render
            </a>
          </Button>
        </CardContent>
      </Card>

      <Alert className="bg-green-50 border-green-200">
        <AlertTitle className="text-green-900">✅ Après le déploiement</AlertTitle>
        <AlertDescription className="text-green-800">
          Une fois déployé, revenez sur MindTrader et testez la connexion avec l'URL de votre backend !
        </AlertDescription>
      </Alert>
    </div>
  );
}
