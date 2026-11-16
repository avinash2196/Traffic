#!/bin/bash
# CITIZEN API startup script (port 8001)

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
echo "Installing dependencies from citizen-api/requirements.txt..."
pip install -q -r citizen-api/requirements.txt

# Start citizen-api on port 8001
echo "🚀 Starting CITIZEN API on http://127.0.0.1:8001"
echo "   - POST /api/media/upload"
echo "   - POST /api/reports"
echo "   - GET /api/reports"
echo "   - GET /api/reports/{report_id}"
echo "   - GET /api/media/{media_id}/{filename}"
echo "   - POST /api/reports/{report_id}/clarification"

cd citizen-api
python app.py
