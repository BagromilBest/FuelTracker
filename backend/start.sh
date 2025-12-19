#!/bin/bash
# Start the backend server

cd "$(dirname "$0")"

echo "Starting backend server..."
source venv/bin/activate
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
