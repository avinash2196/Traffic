#!/bin/bash
# API GATEWAY startup script (port 8000)

set -e

# Determine script directory
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"

# Change to project directory
cd "$PROJECT_DIR"

# Create virtual environment if it doesn't exist
if [ ! -d ".venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv .venv
fi

# Activate virtual environment
source .venv/bin/activate

# Install dependencies
echo "Installing dependencies from api-gateway/requirements.txt..."
pip install -q -r api-gateway/requirements.txt

# Start api-gateway on port 8000
echo "API GATEWAY STARTUP: Starting api-gateway on http://127.0.0.1:8000"
echo "   Routes to:"
echo "   - auth-service on port 8003"
echo "   - citizen-api on port 8001"
echo "   - officer-api on port 8002"

cd api-gateway
python app.py
