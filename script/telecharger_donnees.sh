#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")/.."

# Lance le programme principal : collecte des quatre sources puis conversion Parquet.
# "$@" transmet les options, par exemple --sources instacart ou --parquet-only.
exec python3 -m importation.collecter_donnees "$@"
