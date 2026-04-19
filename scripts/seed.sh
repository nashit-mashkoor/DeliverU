#!/usr/bin/env bash

set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
ENV_FILE_PATH="${ENV_FILE:-$ROOT_DIR/.env}"

if [[ ! -f "$ENV_FILE_PATH" ]]; then
  echo "Env file not found: $ENV_FILE_PATH" >&2
  exit 1
fi

set -a
. "$ENV_FILE_PATH"
set +a

cd "$ROOT_DIR/backend"
PYTHONPATH="${PYTHONPATH:-..}" uv run python -m backend.database.seed
