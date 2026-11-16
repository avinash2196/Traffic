#!/bin/bash

SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
cd "$SCRIPT_DIR"

echo "Starting Citizen App (port 3000)..." 
(cd citizen-app && bash start.sh) &
CITIZEN_PID=$!

sleep 2

echo "Starting Officer App (port 3001)..."
(cd officer-app && bash start.sh) &
OFFICER_PID=$!

echo ""
echo "Frontend apps starting:"
echo "  Citizen App:  http://127.0.0.1:3000"
echo "  Officer App:  http://127.0.0.1:3001"
echo ""
echo "PIDs: Citizen=$CITIZEN_PID, Officer=$OFFICER_PID"
echo "Press Ctrl+C to stop all services"

# Wait for signals
trap "kill $CITIZEN_PID $OFFICER_PID; exit" SIGINT SIGTERM
wait
