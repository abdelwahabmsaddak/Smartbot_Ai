#!/usr/bin/env bash
set -e
cd "$(dirname "$0")/api"
python3 -m venv venv || true
source venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
export PYTHONPATH=$(pwd)
export PORT=${PORT:-8000}
uvicorn main:app --host 0.0.0.0 --port "$PORT"
