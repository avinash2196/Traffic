#!/bin/bash
# Startup script for Phase 1 - Run all 3 microservices (macOS/Linux)

set -e

echo "╔══════════════════════════════════════════════════════════════════════════╗"
echo "║           PHASE 1: STARTING ALL 3 ROADWATCH MICROSERVICES               ║"
echo "╚══════════════════════════════════════════════════════════════════════════╝"
echo ""

# Get script directory
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
cd "$SCRIPT_DIR"

# Setup virtual environment
if [ ! -d ".venv" ]; then
    echo "📦 Creating virtual environment..."
    python3 -m venv .venv
fi

# Activate virtual environment
source .venv/bin/activate

# Install dependencies
echo "📥 Installing dependencies..."
pip install -q -r requirements.txt

echo ""
echo "╔══════════════════════════════════════════════════════════════════════════╗"
echo "║                         STARTING SERVICES                               ║"
echo "╚══════════════════════════════════════════════════════════════════════════╝"
echo ""

# Function to run service in background
run_service() {
    local name=$1
    local port=$2
    local dir=$3
    
    echo "🚀 Starting $name (port $port)..."
    cd "$SCRIPT_DIR/$dir"
    python app.py > "../${dir}.log" 2>&1 &
    local pid=$!
    echo "   ✓ $name started (PID: $pid)"
    echo "   - Log: ./${dir}.log"
    sleep 2
}

# Start services
run_service "AUTH SERVICE" "8003" "auth-service"
run_service "CITIZEN API" "8001" "citizen-api"
run_service "OFFICER API" "8002" "officer-api"

echo ""
echo "╔══════════════════════════════════════════════════════════════════════════╗"
echo "║                    ALL SERVICES STARTING UP                             ║"
echo "╚══════════════════════════════════════════════════════════════════════════╝"
echo ""

cat << 'EOF'

📍 SERVICE ENDPOINTS:

  🔐 AUTH SERVICE (port 8003):
     - Health: http://127.0.0.1:8003/health
     - POST /api/auth/signup
     - POST /api/auth/login
     - POST /api/officer/register
     - POST /api/officer/login

  👤 CITIZEN API (port 8001):
     - Health: http://127.0.0.1:8001/health
     - POST /api/media/upload
     - POST /api/reports
     - GET /api/reports
     - GET /api/reports/{report_id}

  🚔 OFFICER API (port 8002):
     - Health: http://127.0.0.1:8002/health
     - GET /api/authority/reports
     - GET /api/authority/reports/{report_id}
     - POST /api/authority/reports/{report_id}/decision

📊 SHARED:
   - Database: ./roadwatch.db
   - Static: ./static/
   - Templates: ./templates/

🧪 QUICK TEST:
   Run in another terminal:
   
   # Test AUTH SERVICE
   curl http://127.0.0.1:8003/health
   
   # Test CITIZEN API
   curl http://127.0.0.1:8001/health
   
   # Test OFFICER API
   curl http://127.0.0.1:8002/health

💡 NOTES:
   - Services run in background with logs in *.log files
   - Check logs with: tail -f citizen-api.log
   - Stop all services: pkill -f "python app.py"
   - All services use the same ./roadwatch.db
   - Check your .env file for configuration

🔌 FRONTEND:
   Existing frontends automatically work with these services - no changes needed!

EOF

echo "✅ All services started!"
echo "📖 See PHASE-1-EXTRACTION-COMPLETE.md for more details"
echo ""
echo "To view logs:"
echo "  tail -f auth-service.log"
echo "  tail -f citizen-api.log"
echo "  tail -f officer-api.log"
echo ""
echo "To stop all services:"
echo "  pkill -f 'python app.py'"
