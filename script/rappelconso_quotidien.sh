#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")/.."
mkdir -p data/logs
# Éviter deux collectes simultanées (flock fourni par util-linux).
exec flock -n data/rappelconso.lock bash script/telecharger_donnees.sh --sources rappelconso >> data/logs/rappelconso.log 2>&1
