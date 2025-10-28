#!/bin/bash
# start-bytebot-grimoire.sh

echo "🤖 Démarrage de ByteBot - Ton PC Personnel..."

cd ~/alexandria/operarius-puporum/bytebot

# Vérification de la clé API
if [ ! -f ".env" ]; then
    echo "❌ Fichier .env non trouvé! Configure ta clé API d'abord."
    echo "📝 Instructions:"
    echo "   1. Va sur https://makersuite.google.com/app/apikey (Gemini)"
    echo "   2. Ou https://platform.openai.com/api-keys (OpenAI)"
    echo "   3. Copie ta clé et configure le fichier .env"
    exit 1
fi

# Démarrage de ByteBot
echo "🚀 Démarrage de ByteBot..."
npm start &
BYTEBOT_PID=$!

# Attente de démarrage
sleep 3

# Vérification que ByteBot est actif
if curl -s http://localhost:3001/health > /dev/null; then
    echo "✅ ByteBot actif sur http://localhost:3001"
else
    echo "❌ Erreur de démarrage de ByteBot"
    exit 1
fi

# Démarrage de l'orchestrateur Relique
cd ../relique-integration
echo "🔮 Démarrage de l'orchestrateur Relique..."
npm start &
ORCHESTRATOR_PID=$!

# Attente de l'orchestrateur
sleep 3

echo "🎉 ByteBot + Grimoire actifs!"
echo ""
echo "📜 Grimoire: http://localhost:3010/grimoire"
echo "🤖 ByteBot: http://localhost:3001"
echo ""
echo "💬 Parle à ByteBot dans le Grimoire avec:"
echo "   'ByteBot, navigue vers github.com'"
echo "   'ByteBot, cherche des informations sur...'"
echo "   'ByteBot, ouvre un nouvel onglet avec...'"
echo ""
echo "🔑 Ton PC personnel est prêt!"

# Sauvegarde des PID
echo $BYTEBOT_PID > ../bytebot/.bytebot.pid
echo $ORCHESTRATOR_PID > .orchestrator.pid

# Ouverture automatique
if command -v xdg-open &> /dev/null; then
    xdg-open http://localhost:3010/grimoire
elif command -v open &> /dev/null; then
    open http://localhost:3010/grimoire
fi

wait $ORCHESTRATOR_PID