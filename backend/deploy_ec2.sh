#!/usr/bin/env bash
# deploy_ec2.sh

set -euo pipefail

# Load .env so variables are available to this script
if [ -f .env ]; then
  set -a
  # shellcheck disable=SC1091
  source .env
  set +a
fi

# --- Required variables checks ---
if [ -z "${TELEGRAM_BOT_TOKEN:-}" ]; then
  echo "ERROR: TELEGRAM_BOT_TOKEN is missing in .env"
  exit 1
fi

if [ -z "${TELEGRAM_WEBHOOK_SECRET:-}" ]; then
  echo "ERROR: TELEGRAM_WEBHOOK_SECRET is missing in .env"
  exit 1
fi

WEBHOOK_PATH="${TELEGRAM_WEBHOOK_PATH:-/api/v1/telegram/webhook}"

echo "Starting services using docker-compose.ec2.yml..."
docker compose -f docker-compose.ec2.yml up -d --build

echo "Waiting for ngrok tunnel to be ready..."
PUBLIC_URL=""
for i in {1..30}; do
  PUBLIC_URL="$(curl -s http://127.0.0.1:4040/api/tunnels \
    | python -c "import sys, json; d=json.load(sys.stdin); print(d['tunnels'][0]['public_url'] if d.get('tunnels') else '')" \
    2>/dev/null || true)"
  if [ -n "${PUBLIC_URL:-}" ]; then
    break
  fi
  sleep 1
done

if [ -z "${PUBLIC_URL:-}" ]; then
  echo "ERROR: Could not obtain ngrok public URL"
  echo "Check ngrok logs:"
  echo "docker compose -f docker-compose.ec2.yml logs ngrok"
  exit 1
fi

WEBHOOK_URL="${PUBLIC_URL}${WEBHOOK_PATH}"

echo "Setting Telegram webhook to: ${WEBHOOK_URL}"
curl -s "https://api.telegram.org/bot${TELEGRAM_BOT_TOKEN}/setWebhook" \
  -d "url=${WEBHOOK_URL}" \
  -d "secret_token=${TELEGRAM_WEBHOOK_SECRET}" \
  -d "drop_pending_updates=true" \
  | python -m json.tool

echo "Deployment completed successfully."
echo "API Docs: http://<EC2_PUBLIC_IP>/docs"
echo "Ngrok public URL: ${PUBLIC_URL}"
