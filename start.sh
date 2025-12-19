#!/bin/bash
# Start frontend and backend together
# - Ctrl+C stops both
# - If either crashes, everything stops

set -e

cd "$(dirname "$0")"

# Colors
GREEN='\033[0;32m'
BLUE='\033[0;34m'
RED='\033[0;31m'
NC='\033[0m'

echo -e "${GREEN}Starting FuelTracker...${NC}"

BACKEND_PID=""
FRONTEND_PID=""

cleanup() {
    echo -e "\n${RED}Stopping servers...${NC}"

    if [ -n "$BACKEND_PID" ] && kill -0 "$BACKEND_PID" 2>/dev/null; then
        echo -e "${BLUE}Stopping backend (PID $BACKEND_PID)${NC}"
        kill -TERM "$BACKEND_PID"
        wait "$BACKEND_PID" 2>/dev/null || true
    fi

    if [ -n "$FRONTEND_PID" ] && kill -0 "$FRONTEND_PID" 2>/dev/null; then
        echo -e "${BLUE}Stopping frontend (PID $FRONTEND_PID)${NC}"
        kill -TERM "$FRONTEND_PID"
        wait "$FRONTEND_PID" 2>/dev/null || true
    fi

    echo -e "${GREEN}All servers stopped.${NC}"
    exit 0
}

trap cleanup SIGINT SIGTERM EXIT

# ---------- Backend ----------
echo -e "${BLUE}Starting backend...${NC}"
cd backend

source venv/bin/activate
pip install -r requirements.txt

uvicorn app.main:app \
    --reload \
    --host 127.0.0.1 \
    --port 8000 &
BACKEND_PID=$!

cd ..

sleep 2

# ---------- Frontend ----------
echo -e "${BLUE}Starting frontend...${NC}"
cd frontend

npm run dev &
FRONTEND_PID=$!

cd ..

echo -e "${GREEN}Servers running${NC}"
echo -e "${BLUE}Backend:  http://localhost:8000${NC}"
echo -e "${BLUE}Frontend: http://localhost:5173${NC}"
echo -e "${GREEN}Press Ctrl+C to stop${NC}"

# ---------- Monitor ----------
while true; do
    if ! kill -0 "$BACKEND_PID" 2>/dev/null; then
        echo -e "${RED}Backend crashed. Shutting down.${NC}"
        break
    fi

    if ! kill -0 "$FRONTEND_PID" 2>/dev/null; then
        echo -e "${RED}Frontend crashed. Shutting down.${NC}"
        break
    fi

    sleep 1
done

cleanup

