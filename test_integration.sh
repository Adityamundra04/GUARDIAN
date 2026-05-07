#!/bin/bash

# Guardian Frontend-Backend Integration Test Script
# This script verifies that the frontend and backend are properly integrated

echo "=========================================="
echo "Guardian Integration Test"
echo "=========================================="
echo ""

# Colors for output
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Test 1: Check if backend is running
echo "Test 1: Checking backend status..."
BACKEND_RESPONSE=$(curl -s -o /dev/null -w "%{http_code}" http://127.0.0.1:8000/health 2>/dev/null)

if [ "$BACKEND_RESPONSE" = "200" ]; then
    echo -e "${GREEN}✓${NC} Backend is running (HTTP 200)"
else
    echo -e "${RED}✗${NC} Backend is not running (HTTP $BACKEND_RESPONSE)"
    echo -e "${YELLOW}→${NC} Start backend: uvicorn backend.app.main:app --reload"
    exit 1
fi

# Test 2: Check root endpoint
echo ""
echo "Test 2: Checking root endpoint..."
ROOT_RESPONSE=$(curl -s http://127.0.0.1:8000/)

if echo "$ROOT_RESPONSE" | grep -q "Guardian is running"; then
    echo -e "${GREEN}✓${NC} Root endpoint responding correctly"
else
    echo -e "${RED}✗${NC} Root endpoint not responding as expected"
fi

# Test 3: Check incidents endpoint
echo ""
echo "Test 3: Checking incidents endpoint..."
INCIDENTS_RESPONSE=$(curl -s -o /dev/null -w "%{http_code}" http://127.0.0.1:8000/incidents 2>/dev/null)

if [ "$INCIDENTS_RESPONSE" = "200" ]; then
    echo -e "${GREEN}✓${NC} Incidents endpoint responding (HTTP 200)"
    
    # Get incident count
    INCIDENT_COUNT=$(curl -s http://127.0.0.1:8000/incidents | python3 -c "import sys, json; print(len(json.load(sys.stdin)))" 2>/dev/null)
    echo -e "${GREEN}→${NC} Current incidents: $INCIDENT_COUNT"
else
    echo -e "${RED}✗${NC} Incidents endpoint not responding (HTTP $INCIDENTS_RESPONSE)"
fi

# Test 4: Check CORS headers
echo ""
echo "Test 4: Checking CORS configuration..."
CORS_HEADERS=$(curl -s -I -X OPTIONS http://127.0.0.1:8000/incidents \
    -H "Origin: http://localhost:5173" \
    -H "Access-Control-Request-Method: GET" 2>/dev/null | grep -i "access-control")

if [ ! -z "$CORS_HEADERS" ]; then
    echo -e "${GREEN}✓${NC} CORS headers present"
    echo "$CORS_HEADERS" | sed 's/^/  /'
else
    echo -e "${YELLOW}⚠${NC} CORS headers not found (may need backend restart)"
fi

# Test 5: Check frontend (if running)
echo ""
echo "Test 5: Checking frontend status..."
FRONTEND_RESPONSE=$(curl -s -o /dev/null -w "%{http_code}" http://localhost:5173/ 2>/dev/null)

if [ "$FRONTEND_RESPONSE" = "200" ]; then
    echo -e "${GREEN}✓${NC} Frontend is running (HTTP 200)"
else
    echo -e "${YELLOW}⚠${NC} Frontend is not running (HTTP $FRONTEND_RESPONSE)"
    echo -e "${YELLOW}→${NC} Start frontend: cd frontend && npm run dev"
fi

# Test 6: Check API service configuration
echo ""
echo "Test 6: Checking frontend API configuration..."
if [ -f "frontend/src/services/api.js" ]; then
    echo -e "${GREEN}✓${NC} API service file exists"
    
    # Check API URL
    API_URL=$(grep "API_BASE_URL" frontend/src/services/api.js | head -1)
    echo -e "${GREEN}→${NC} $API_URL"
else
    echo -e "${RED}✗${NC} API service file not found"
fi

# Test 7: Check environment configuration
echo ""
echo "Test 7: Checking environment configuration..."
if [ -f "frontend/.env" ]; then
    echo -e "${GREEN}✓${NC} .env file exists"
    cat frontend/.env | sed 's/^/  /'
else
    echo -e "${YELLOW}⚠${NC} .env file not found (using default URL)"
    if [ -f "frontend/.env.example" ]; then
        echo -e "${YELLOW}→${NC} Copy .env.example to .env if needed"
    fi
fi

# Summary
echo ""
echo "=========================================="
echo "Integration Test Summary"
echo "=========================================="
echo ""

if [ "$BACKEND_RESPONSE" = "200" ] && [ "$INCIDENTS_RESPONSE" = "200" ]; then
    echo -e "${GREEN}✓ Backend Integration: PASS${NC}"
else
    echo -e "${RED}✗ Backend Integration: FAIL${NC}"
fi

if [ "$FRONTEND_RESPONSE" = "200" ]; then
    echo -e "${GREEN}✓ Frontend Status: RUNNING${NC}"
else
    echo -e "${YELLOW}⚠ Frontend Status: NOT RUNNING${NC}"
fi

if [ ! -z "$CORS_HEADERS" ]; then
    echo -e "${GREEN}✓ CORS Configuration: OK${NC}"
else
    echo -e "${YELLOW}⚠ CORS Configuration: CHECK NEEDED${NC}"
fi

echo ""
echo "=========================================="
echo "Access Points"
echo "=========================================="
echo ""
echo "Backend API:  http://127.0.0.1:8000"
echo "API Docs:     http://127.0.0.1:8000/docs"
echo "Frontend:     http://localhost:5173"
echo ""
echo "=========================================="
