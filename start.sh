#!/bin/bash

# RoadWatch Traffic MVP - macOS/Linux Startup Script
# Usage: chmod +x start.sh && ./start.sh

set -e  # Exit on error

echo "🚗 RoadWatch Traffic MVP - macOS/Linux Startup"

# Load environment variables from .env
if [ -f .env ]; then
    echo "📝 Loading configuration from .env..."
    export $(cat .env | grep -v '#' | xargs)
else
    echo "⚠️  .env file not found!"
    echo "Please copy .env.example to .env and fill in your API keys:"
    echo "  cp .env.example .env"
    echo "  nano .env  # Edit with your real API keys"
    exit 1
fi

# Verify required variables
if [ -z "$OPENAI_API_KEY" ]; then
    echo "❌ ERROR: OPENAI_API_KEY not set in .env"
    exit 1
fi

if [ -z "$GATEWAY_TOKEN" ]; then
    echo "❌ ERROR: GATEWAY_TOKEN not set in .env"
    exit 1
fi

# Check Python installation
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed"
    echo "Please install Python 3.11+ from https://www.python.org or via package manager"
    exit 1
fi

PYTHON_VERSION=$(python3 --version)
echo "✓ Python found: $PYTHON_VERSION"

# Create virtual environment if needed
VENV_PATH=".venv"
if [ ! -d "$VENV_PATH" ]; then
    echo "📦 Creating virtual environment..."
    python3 -m venv "$VENV_PATH"
    echo "✓ Virtual environment created"
fi

# Activate virtual environment
echo "🔌 Activating virtual environment..."
source "$VENV_PATH/bin/activate"

# Install dependencies
echo "📚 Installing dependencies..."
pip install -q -r requirements.txt
echo "✓ Dependencies installed"

# Create media directory
if [ ! -d "media_store" ]; then
    mkdir -p media_store
    echo "✓ Created media_store directory"
fi

# Handle signals for graceful shutdown
trap 'echo ""; echo "👋 RoadWatch stopped"; exit 0' SIGINT SIGTERM

# Run application
echo "🚀 Starting RoadWatch Traffic MVP..."
echo ""
echo "Configuration loaded:"
echo "  API: http://${FASTAPI_HOST:-127.0.0.1}:${FASTAPI_PORT:-8000}"
echo "  Gateway: http://${AI_GATEWAY_URL:-http://127.0.0.1:9999}"
echo ""
echo "📍 API available at: http://127.0.0.1:8000"
echo "📊 Documentation at: http://127.0.0.1:8000/api/docs"
echo "ℹ️  Press Ctrl+C to stop"
echo ""

# Start AI Gateway in background
echo "🤖 Starting AI Gateway..."
python ai_gateway_mvp.py > gateway.log 2>&1 &
GATEWAY_PID=$!

# Give gateway time to start
sleep 2

# Start FastAPI app
uvicorn app:app --host ${FASTAPI_HOST:-127.0.0.1} --port ${FASTAPI_PORT:-8000} --reload

# Cleanup on exit
kill $GATEWAY_PID 2>/dev/null || true

