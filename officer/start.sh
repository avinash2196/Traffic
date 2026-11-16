#!/bin/bash
# OFFICER API startup script (port 8002)

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
echo "Installing dependencies from officer-api/requirements.txt..."
pip install -q -r officer-api/requirements.txt

# Start officer-api on port 8002
echo "🚀 Starting OFFICER API on http://127.0.0.1:8002"
echo "   - GET /api/authority/reports"
echo "   - GET /api/authority/reports/{report_id}"
echo "   - GET /api/authority/reports/{report_id}/media/{filename}"
echo "   - POST /api/authority/reports/{report_id}/decision"
echo "   - GET /api/authority/reports/{report_id}/evidence.zip"

cd officer-api
python app.py
