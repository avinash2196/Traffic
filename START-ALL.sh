#!/bin/bash

# RoadWatch Traffic MVP - All-In-One Startup Script
# For macOS and Linux

set -e

SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
cd "$SCRIPT_DIR"

echo "================================================================================"
echo "                 ROADWATCH TRAFFIC MVP - STARTING ALL SERVICES"
echo "================================================================================"

# Step 1: Setup virtual environment
echo ""
echo "[1/6] Setting up Python virtual environment..."
if [ ! -d ".venv" ]; then
    python3 -m venv .venv
fi
source .venv/bin/activate
echo "      Done"

# Step 2: Install dependencies
echo ""
echo "[2/6] Installing dependencies..."
pip install -q -r requirements.txt
echo "      Done"

# Step 3: Start microservices
echo ""
echo "[3/6] Starting microservices (ports 9001, 9002, 9003)..."
echo "      - Auth Service (9001)..."
cd auth && python app.py > ../logs-auth.txt 2>&1 &
AUTH_PID=$!
cd ..
sleep 1

echo "      - Citizen API (9002)..."
cd citizen && python app.py > ../logs-citizen-api.txt 2>&1 &
CITIZEN_PID=$!
cd ..
sleep 1

echo "      - Officer API (9003)..."
cd officer && python app.py > ../logs-officer-api.txt 2>&1 &
OFFICER_PID=$!
cd ..
sleep 1

echo "      Done"

# Step 4: Start frontends
echo ""
echo "[4/6] Starting frontend applications..."
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
echo "[5/6] Waiting for services to stabilize..."
sleep 15
echo "      Done"

# Step 6: Verify services
echo ""
echo "[6/6] Verifying all services..."

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
check_service "Auth Service" "http://127.0.0.1:9001/health" || all_healthy=false
check_service "Citizen API" "http://127.0.0.1:9002/health" || all_healthy=false
check_service "Officer API" "http://127.0.0.1:9003/health" || all_healthy=false
check_service "Citizen Frontend" "http://127.0.0.1:3001/" || all_healthy=false
check_service "Officer Frontend" "http://127.0.0.1:3002/" || all_healthy=false

# Display dashboard
cat << "EOF"

================================================================================
                        ROADWATCH IS RUNNING!
================================================================================

MICROSERVICES:
  Auth Service          http://127.0.0.1:9001/
  Citizen API           http://127.0.0.1:9002/
  Officer API           http://127.0.0.1:9003/

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

LOGS:
  Auth Service:         logs-auth.txt
  Citizen API:          logs-citizen-api.txt
  Officer API:          logs-officer-api.txt
  Citizen App:          logs-citizen-app.txt
  Officer App:          logs-officer-app.txt

STOPPING SERVICES:
  Run: kill $AUTH_PID $CITIZEN_PID $OFFICER_PID $CITIZEN_APP_PID $OFFICER_APP_PID
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
trap "echo 'Stopping all services...'; kill $AUTH_PID $CITIZEN_PID $OFFICER_PID $CITIZEN_APP_PID $OFFICER_APP_PID 2>/dev/null; exit 0" INT TERM

wait
