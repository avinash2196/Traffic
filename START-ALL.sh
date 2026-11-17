#!/bin/bash

# RoadWatch Traffic MVP - All-In-One Startup Script
# For macOS and Linux
#
# Usage:
#   ./START-ALL.sh              (Normal startup, keeps existing data)
#   ./START-ALL.sh --clean      (Clean startup, deletes database and cache)

set -e

SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
cd "$SCRIPT_DIR"

CLEAN_MODE=false
if [ "$1" = "--clean" ]; then
    CLEAN_MODE=true
fi

echo "================================================================================"
echo "                 ROADWATCH TRAFFIC MVP - STARTING ALL SERVICES"
if [ "$CLEAN_MODE" = true ]; then
    echo "                         [CLEAN MODE - DATABASE WILL BE RESET]"
fi
echo "================================================================================"

# Step 0: Clean database if requested
if [ "$CLEAN_MODE" = true ]; then
    echo ""
    echo "[0/7] Cleaning database and cache..."
    
    if [ -f "roadwatch.db" ]; then
        rm -f roadwatch.db
        echo "      Deleted: roadwatch.db"
    fi
    
    if [ -d "media_store" ]; then
        rm -rf media_store
        mkdir -p media_store
        echo "      Cleared: media_store/"
    fi
    
    echo "      Done"
fi

# Step 1: Setup virtual environment
echo ""
echo "[1/7] Setting up Python virtual environment..."
if [ ! -d ".venv" ]; then
    python3 -m venv .venv
fi
source .venv/bin/activate
echo "      Done"

# Step 2: Install dependencies
echo ""
echo "[2/7] Installing dependencies..."
pip install -q -r requirements.txt
echo "      Done"

# Step 3: Start microservices
echo ""
echo "[3/7] Starting microservices (ports 9001, 9002, 9003, 9004)..."

echo "      - Auth Service (9003)..."
cd auth && python app.py > ../logs-auth.txt 2>&1 &
AUTH_PID=$!
cd ..
sleep 1

echo "      - Citizen API (9001)..."
cd citizen && python app.py > ../logs-citizen-api.txt 2>&1 &
CITIZEN_PID=$!
cd ..
sleep 1

echo "      - Officer API (9002)..."
cd officer && python app.py > ../logs-officer-api.txt 2>&1 &
OFFICER_PID=$!
cd ..
sleep 1

echo "      - AI Gateway (9004)..."
cd ai-gateway && python app.py > ../logs-ai-gateway.txt 2>&1 &
GATEWAY_PID=$!
cd ..
sleep 1

echo "      - AI Worker (Background)..."
cd ai-worker && python app.py > ../logs-ai-worker.txt 2>&1 &
WORKER_PID=$!
cd ..
sleep 1

echo "      Done"

# Step 4: Start frontends
echo ""
echo "[4/7] Starting frontend applications..."

echo "      - Citizen Frontend (3001)..."
cd citizen-app && python app.py > ../logs-citizen-app.txt 2>&1 &
CITIZEN_APP_PID=$!
cd ..
sleep 1

echo "      - Officer Frontend (3002)..."
cd officer-app && python app.py > ../logs-officer-app.txt 2>&1 &
OFFICER_APP_PID=$!
cd ..
sleep 1

echo "      Done"

# Step 5: Wait for services to stabilize
echo ""
echo "[5/7] Waiting for services to stabilize..."
sleep 15
echo "      Done"

# Step 6: Verify services
echo ""
echo "[6/7] Verifying all services..."

check_service() {
    local name=$1
    local url=$2
    if curl -s "$url" > /dev/null 2>&1; then
        echo "      [OK] $name"
        return 0
    else
        echo "      [FAIL] $name"
        return 1
    fi
}

all_healthy=true
check_service "Auth Service" "http://127.0.0.1:9003/health" || all_healthy=false
check_service "Citizen API" "http://127.0.0.1:9001/health" || all_healthy=false
check_service "Officer API" "http://127.0.0.1:9002/health" || all_healthy=false
check_service "AI Gateway" "http://127.0.0.1:9004/health" || all_healthy=false
check_service "Citizen Frontend" "http://127.0.0.1:3001/" || all_healthy=false
check_service "Officer Frontend" "http://127.0.0.1:3002/" || all_healthy=false

# Step 7: Display dashboard
cat << "EOF"

================================================================================
                        ROADWATCH IS RUNNING!
================================================================================

MICROSERVICES:
  Auth Service          http://127.0.0.1:9003/
  Citizen API           http://127.0.0.1:9001/
  Officer API           http://127.0.0.1:9002/
  AI Gateway            http://127.0.0.1:9004/
  AI Worker             (Background Service)

FRONTENDS:
  Citizen Portal        http://127.0.0.1:3001/     <- Click here to start
  Officer Portal        http://127.0.0.1:3002/     <- Click here to review

TESTING:
  Citizen test flow:
    1. Visit http://127.0.0.1:3001/
    2. Sign up with email/password
    3. Create report with media upload
    4. View report in My Reports

  Officer test flow:
    1. Visit http://127.0.0.1:3002/
    2. Sign up as officer
    3. Review reports in queue
    4. Make decisions (approve/reject)

DATABASE:
  SQLite DB: ./roadwatch.db
EOF

if [ "$CLEAN_MODE" = true ]; then
    echo "  STATUS: Database was reset for clean start"
fi

cat << "EOF"

LOGS:
  Auth Service:         logs-auth.txt
  Citizen API:          logs-citizen-api.txt
  Officer API:          logs-officer-api.txt
  AI Gateway:           logs-ai-gateway.txt
  AI Worker:            logs-ai-worker.txt
  Citizen App:          logs-citizen-app.txt
  Officer App:          logs-officer-app.txt

STOPPING SERVICES:
  Run: kill $AUTH_PID $CITIZEN_PID $OFFICER_PID $GATEWAY_PID $WORKER_PID $CITIZEN_APP_PID $OFFICER_APP_PID
  Or: Ctrl+C in this terminal

================================================================================
EOF

if [ "$all_healthy" = true ]; then
    echo "All services are healthy! You can now use RoadWatch."
else
    echo "WARNING: Some services failed to start. Check the logs above."
fi

echo ""
echo "Press Ctrl+C to stop all services"
echo ""

# Wait for user interrupt
trap "echo 'Stopping all services...'; kill $AUTH_PID $CITIZEN_PID $OFFICER_PID $GATEWAY_PID $WORKER_PID $CITIZEN_APP_PID $OFFICER_APP_PID 2>/dev/null; exit 0" INT TERM

wait
