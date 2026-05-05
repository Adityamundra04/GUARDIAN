# Quick Start: AI-Powered Guardian

## Prerequisites

1. **Install Ollama**
   ```bash
   # Visit https://ollama.ai and download
   # Or use your package manager
   ```

2. **Pull llama3.1 Model**
   ```bash
   ollama pull llama3.1
   ```

3. **Start Ollama**
   ```bash
   ollama serve
   # Should run on http://localhost:11434
   ```

## Test Ollama Integration

```bash
# Test the Ollama client
cd ai-engine
python test_ollama.py
```

**Expected Output:**
```
🧪 Testing Ollama Client...
✅ Client initialized: http://localhost:11434
✅ Model: llama3.1
📤 Sending test prompt...
✅ Response received:
   Hello from Ollama!

🧪 Testing Kubernetes Diagnosis...
📤 Sending Kubernetes diagnosis prompt...
✅ Diagnosis received:
Cause: The container is crashing repeatedly...
Fix: 1. Check logs with kubectl logs...

🎉 All tests passed!
```

## Start Guardian with AI

```bash
# Start the backend
cd backend
uvicorn app.main:app --reload
```

**Expected Logs:**
```
🔧 Starting Guardian application...
🚀 Monitoring started...
✅ Background monitoring thread started
```

## Create a Test Incident

### Option 1: Deploy Failing Pod
```bash
# Deploy a pod that will crash
kubectl apply -f k8s/test-failures/crashloop.yaml

# Wait 5-10 seconds for detection
```

### Option 2: Manual API Call
```bash
# Create incident via API
curl -X POST http://localhost:8000/incidents/ \
  -H "Content-Type: application/json" \
  -d '{
    "issue": "[default] test-pod → CrashLoopBackOff"
  }'
```

## View AI-Enriched Incidents

```bash
# Get all incidents
curl http://localhost:8000/incidents/
```

**Expected Response:**
```json
[
  {
    "id": "abc-123-def-456",
    "issue": "[default] test-pod → CrashLoopBackOff",
    "status": "detected",
    "cause": "Container is failing to start, likely due to missing environment variables or incorrect configuration",
    "solution": "1. Check container logs with kubectl logs test-pod\n2. Verify environment variables in deployment\n3. Check resource limits and requests"
  }
]
```

## Monitor Logs

Watch the Guardian logs to see AI in action:

```
🔍 Found 1 issue(s) in cluster
⚠️  Issue detected: [default] test-pod - CrashLoopBackOff
🤖 Requesting AI diagnosis for: [default] test-pod → CrashLoopBackOff
✅ AI response received
📋 Cause: Container is failing to start, likely due to...
🔧 Solution: 1. Check container logs with kubectl logs...
✅ Incident created: abc-123 - [default] test-pod → CrashLoopBackOff
```

## Troubleshooting

### Ollama Not Running
```
❌ Cannot connect to Ollama at http://localhost:11434
```
**Fix:** Start Ollama with `ollama serve`

### Model Not Found
```
❌ Ollama API error: 404 - model not found
```
**Fix:** Pull the model with `ollama pull llama3.1`

### AI Timeout
```
❌ Ollama request timeout after 30 seconds
```
**Fix:** 
- Check Ollama is running
- Try a smaller/faster model
- Increase timeout in `ai_service.py`

### AI Fails But System Works
```
❌ AI diagnosis failed - using defaults
✅ Incident created: abc-123 - [default] test-pod → CrashLoopBackOff
```
**This is expected behavior!** The system continues to work even if AI fails.

## Architecture Summary

```
Kubernetes Issue
    ↓
Monitor Service
    ↓
AI Service (diagnose_issue)
    ↓
Ollama Client (generate)
    ↓
Ollama API (llama3.1)
    ↓
AI Response
    ↓
Parse Response
    ↓
Incident with Cause + Solution
```

## Files Created

```
ai-engine/
├── __init__.py
├── ollama_client.py      # HTTP client for Ollama API
└── test_ollama.py        # Test script

backend/app/services/
├── ai_service.py         # AI diagnosis service
└── monitor_service.py    # Updated with AI integration

backend/
├── AI_INTEGRATION.md     # Detailed documentation
└── MONITOR_SERVICE_IMPROVEMENTS.md
```

## Next Steps

1. ✅ Test Ollama connection
2. ✅ Start Guardian backend
3. ✅ Deploy failing pod or create manual incident
4. ✅ View AI-enriched incidents via API
5. 🎯 Integrate with frontend (future)
6. 🎯 Add incident resolution workflow (future)

## Success Criteria

✅ Ollama running on localhost:11434  
✅ llama3.1 model pulled  
✅ Guardian backend running  
✅ Incidents created with AI diagnosis  
✅ API returns cause and solution  
✅ System continues if AI fails  

## Quick Commands

```bash
# Start Ollama
ollama serve

# Test Ollama
cd ai-engine && python test_ollama.py

# Start Guardian
cd backend && uvicorn app.main:app --reload

# View incidents
curl http://localhost:8000/incidents/

# Check health
curl http://localhost:8000/health
```

🎉 **You're ready to use AI-powered Guardian!**
