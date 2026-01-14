#!/bin/bash

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo -e "${GREEN}🚀 Starting Gmail Schedule Watcher Backend${NC}"

# Check if Redis is running
if ! command -v redis-cli &> /dev/null; then
    echo -e "${RED}❌ redis-cli not found. Please install Redis.${NC}"
    exit 1
fi

if ! redis-cli ping &> /dev/null; then
    echo -e "${YELLOW}⚠️  Redis is not running. Attempting to start...${NC}"
    redis-server --daemonize yes
    sleep 1
    if redis-cli ping &> /dev/null; then
        echo -e "${GREEN}✅ Redis started successfully${NC}"
    else
        echo -e "${RED}❌ Failed to start Redis. Please start it manually.${NC}"
        exit 1
    fi
else
    echo -e "${GREEN}✅ Redis is running${NC}"
fi

# Function to cleanup on exit
cleanup() {
    echo -e "\n${YELLOW}🛑 Shutting down...${NC}"
    # Kill Celery worker
    if [ ! -z "$CELERY_PID" ]; then
        kill $CELERY_PID 2>/dev/null
        echo -e "${GREEN}✅ Celery worker stopped${NC}"
    fi
    exit 0
}

trap cleanup SIGINT SIGTERM

# Start Celery worker in background
echo -e "${GREEN}🔧 Starting Celery worker...${NC}"
celery -A app.celery_app worker --loglevel=info &
CELERY_PID=$!
sleep 2

if ps -p $CELERY_PID > /dev/null; then
    echo -e "${GREEN}✅ Celery worker started (PID: $CELERY_PID)${NC}"
else
    echo -e "${RED}❌ Failed to start Celery worker${NC}"
    exit 1
fi

# Start FastAPI server (foreground)
echo -e "${GREEN}🌐 Starting FastAPI server...${NC}"
echo -e "${GREEN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
uvicorn main:app --reload --host 0.0.0.0 --port 8000

