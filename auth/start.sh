#!/bin/bash
# AUTH SERVICE startup script (port 8003)

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
echo "Installing dependencies from auth-service/requirements.txt..."
pip install -q -r auth-service/requirements.txt

# Start auth-service on port 8003
echo "🚀 Starting AUTH SERVICE on http://127.0.0.1:8003"
echo "   - POST /api/auth/signup"
echo "   - POST /api/auth/login"
echo "   - POST /api/auth/logout"
echo "   - GET /api/auth/me"
echo "   - POST /api/officer/register"
echo "   - POST /api/officer/login"

cd auth-service
python app.py
