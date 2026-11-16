#!/bin/bash

SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
cd "$SCRIPT_DIR"

echo ""
echo "╔════════════════════════════════════════════════════════════════╗"
echo "║          STARTING ALL ROADWATCH SERVICES (9000 range)         ║"
echo "╚════════════════════════════════════════════════════════════════╝"
echo ""

# Function to start a service
start_service() {
    local dir=$1
    local name=$2
    local port=$3
    
    if [ -z "$port" ]; then
        port_info="background"
    else
        port_info="port $port"
    fi
    
    echo "Starting $name ($port_info)..."
    (
        cd "$dir"
        if [ ! -d ".venv" ]; then
            python3 -m venv .venv
        fi
        source .venv/bin/activate
        pip install -r requirements.txt > /dev/null 2>&1
        python app.py
    ) &
}

# Start all services in background
start_service "auth" "Auth Service" "9003"
sleep 1
start_service "citizen" "Citizen API" "9001"
sleep 1
start_service "officer" "Officer API" "9002"
sleep 1
start_service "ai-gateway" "AI Gateway" "9004"
sleep 1
start_service "ai-worker" "AI Worker (Background)" ""
sleep 1
start_service "citizen-app" "Citizen App (Frontend)" "9000"
sleep 1
start_service "officer-app" "Officer App (Frontend)" "9010"

echo ""
echo "╔════════════════════════════════════════════════════════════════╗"
echo "║                    ALL SERVICES STARTED                        ║"
echo "╚════════════════════════════════════════════════════════════════╝"
echo ""

echo "BACKEND SERVICES (APIs):"
echo "  • Auth Service          → http://127.0.0.1:9003"
echo "  • Citizen API           → http://127.0.0.1:9001"
echo "  • Officer API           → http://127.0.0.1:9002"
echo "  • AI Gateway            → http://127.0.0.1:9004"
echo "  • AI Worker             → Processing background jobs"
echo ""

echo "FRONTEND APPS (Open in browser):"
echo "  • Citizen App           → http://127.0.0.1:9000"
echo "  • Officer App           → http://127.0.0.1:9010"
echo ""

echo "SHARED DATABASE:"
echo "  • SQLite                → ./shared/roadwatch.db"
echo ""

echo "════════════════════════════════════════════════════════════════"
echo ""

echo "HEALTH CHECKS (test in new terminal):"
echo "  curl http://127.0.0.1:9003/health  # Auth"
echo "  curl http://127.0.0.1:9001/health  # Citizen"
echo "  curl http://127.0.0.1:9002/health  # Officer"
echo "  curl http://127.0.0.1:9004/health  # AI Gateway"
echo ""

echo "TESTING:"
echo "  1. Open http://127.0.0.1:9000 in browser → Citizen App"
echo "  2. Open http://127.0.0.1:9010 in browser → Officer App"
echo "  3. Test citizen flow: signup → login → submit report"
echo "  4. Test officer flow: register → login → view queue"
echo ""

echo "STOPPING SERVICES:"
echo "  Press Ctrl+C to stop all services"
echo ""

echo "════════════════════════════════════════════════════════════════"
echo ""

# Wait for signals
trap "pkill -P $$; exit" SIGINT SIGTERM
wait
