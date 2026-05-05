# AI Integration with Ollama

## Overview
Guardian now includes AI-powered diagnosis using Ollama with the llama3.1 model. When incidents are detected, the AI automatically analyzes the issue and provides root cause analysis and fix suggestions.

## Architecture

```
┌─────────────────────────────────────────────────┐
│         Kubernetes Issue Detected               │
└────────────────┬────────────────────────────────┘
                 │
                 ▼
┌─────────────────────────────────────────────────┐
│      MonitorService.create_incident()           │
│                                                 │
│  1. Format issue message                        │
│  2. Call AIService.diagnose_issue()             │
│  3. Create incident with AI results             │
└────────────────┬────────────────────────────────┘
                 │
                 ▼
┌─────────────────────────────────────────────────┐
│           AIService.diagnose_issue()            │
│                                                 │
│  1. Build diagnosis prompt                      │
│  2. Call OllamaClient.generate()                │
│  3. Parse AI response                           │
│  4. Return {cause, solution}                    │
└────────────────┬────────────────────────────────┘
                 │
                 ▼
┌─────────────────────────────────────────────────┐
│        OllamaClient.generate()                  │
│                                                 │
│  POST http://localhost:11434/api/generate       │
│  {                                              │
│    "model": "llama3.1",                         │
│    "prompt": "...",                             │
│    "stream": false                              │
│  }                                              │
└─────────────────────────────────────────────────┘
```

## Components

### 1. Ollama Client (`ai-engine/ollama_client.py`)

**Purpose:** Low-level HTTP client for Ollama API

**Key Methods:**
- `generate(prompt, timeout=30)` - Send prompt and get response

**Features:**
- Non-streaming API calls
- Configurable timeout (default: 30 seconds)
- Error handling for connection issues
- Uses llama3.1 model

**Example Usage:**
```python
client = OllamaClient()
response = client.generate("Analyze this Kubernetes issue...")
```

### 2. AI Service (`backend/app/services/ai_service.py`)

**Purpose:** High-level service for incident diagnosis

**Key Methods:**
- `diagnose_issue(issue)` - Get AI diagnosis for an issue
- `build_diagnosis_prompt(issue)` - Create structured prompt
- `parse_ai_response(response)` - Extract cause and solution

**Prompt Format:**
```
You are a Kubernetes expert.
Analyze the issue and provide:
1. Root cause
2. Fix

Issue: [namespace] pod-name → CrashLoopBackOff

Respond ONLY in this format:
Cause: <root cause explanation>
Fix: <step-by-step fix>
```

**Response Parsing:**
- Extracts text after "Cause:"
- Extracts text after "Fix:"
- Handles multi-line responses
- Returns defaults if parsing fails

**Error Handling:**
- If AI fails: `cause = "Unknown - AI service unavailable"`
- If AI fails: `solution = "Manual investigation required"`

### 3. Updated Monitor Service (`backend/app/services/monitor_service.py`)

**Changes:**
- Added `AIService` initialization
- Updated `create_incident_from_issue()` to call AI diagnosis
- Enriches incidents with AI-generated cause and solution

**Flow:**
```python
def create_incident_from_issue(self, issue):
    # 1. Check for duplicates
    if pod_identifier in self.active_issues:
        return None
    
    # 2. Format incident message
    incident_message = f"[{namespace}] {pod} → {issue}"
    
    # 3. Get AI diagnosis
    diagnosis = self.ai_service.diagnose_issue(incident_message)
    
    # 4. Create incident with AI data
    incident = Incident(
        issue=incident_message,
        cause=diagnosis["cause"],
        solution=diagnosis["solution"]
    )
    
    # 5. Store and track
    incidents_db.append(incident)
    self.active_issues.add(pod_identifier)
```

## Setup Requirements

### 1. Install Ollama
```bash
# Download from https://ollama.ai
# Or use package manager
```

### 2. Pull llama3.1 Model
```bash
ollama pull llama3.1
```

### 3. Start Ollama Server
```bash
ollama serve
# Runs on http://localhost:11434
```

### 4. Verify Ollama is Running
```bash
curl http://localhost:11434/api/generate -d '{
  "model": "llama3.1",
  "prompt": "Hello",
  "stream": false
}'
```

## Example Flow

### Scenario: CrashLoopBackOff Detected

**1. Kubernetes Issue Detected:**
```
Pod: my-app
Namespace: default
Issue: CrashLoopBackOff
```

**2. Monitor Service Creates Incident:**
```
🔍 Found 1 issue(s) in cluster
⚠️  Issue detected: [default] my-app - CrashLoopBackOff
```

**3. AI Service Called:**
```
🤖 Requesting AI diagnosis for: [default] my-app → CrashLoopBackOff
```

**4. Ollama Prompt Sent:**
```
You are a Kubernetes expert.
Analyze the issue and provide:
1. Root cause
2. Fix

Issue: [default] my-app → CrashLoopBackOff

Respond ONLY in this format:
Cause: <root cause explanation>
Fix: <step-by-step fix>
```

**5. AI Response Received:**
```
✅ AI response received
📋 Cause: Container is failing to start, likely due to...
🔧 Solution: 1. Check container logs with kubectl logs...
```

**6. Incident Created:**
```json
{
  "id": "abc-123-def-456",
  "issue": "[default] my-app → CrashLoopBackOff",
  "status": "detected",
  "cause": "Container is failing to start, likely due to missing environment variables or incorrect configuration",
  "solution": "1. Check container logs with kubectl logs my-app\n2. Verify environment variables\n3. Check resource limits"
}
```

**7. API Response:**
```bash
curl http://localhost:8000/incidents/

[
  {
    "id": "abc-123-def-456",
    "issue": "[default] my-app → CrashLoopBackOff",
    "status": "detected",
    "cause": "Container is failing to start...",
    "solution": "1. Check container logs..."
  }
]
```

## Error Handling

### AI Service Unavailable
```
❌ Cannot connect to Ollama at http://localhost:11434
❌ AI diagnosis failed - using defaults

Incident created with:
- cause: "Unknown - AI service unavailable"
- solution: "Manual investigation required"
```

### AI Timeout
```
❌ Ollama request timeout after 30 seconds
❌ AI diagnosis failed - using defaults
```

### Parsing Error
```
❌ Error parsing AI response: invalid format

Incident created with:
- cause: "Unknown"
- solution: "Manual investigation required"
```

### System Continues
**IMPORTANT:** If AI fails, the system continues to work:
- Incident is still created
- Monitoring continues
- No system crash

## Performance Considerations

### Non-Blocking Design
- AI calls happen during incident creation
- Each incident gets its own AI call
- Errors don't block other incidents

### Timeout Protection
- 30-second timeout on AI requests
- Prevents hanging on slow responses
- System continues if timeout occurs

### Fallback Values
- Always provides default cause/solution
- Never leaves fields empty
- Graceful degradation

## Testing

### Test AI Integration
```bash
# 1. Start Ollama
ollama serve

# 2. Start Guardian
cd backend
uvicorn app.main:app --reload

# 3. Create a failing pod
kubectl apply -f k8s/test-failures/crashloop.yaml

# 4. Check incidents
curl http://localhost:8000/incidents/

# Expected: Incident with AI-generated cause and solution
```

### Test AI Failure Handling
```bash
# 1. Stop Ollama
# (kill the ollama process)

# 2. Create a failing pod
kubectl apply -f k8s/test-failures/crashloop.yaml

# 3. Check incidents
curl http://localhost:8000/incidents/

# Expected: Incident with default cause/solution
```

## Logs

### Successful AI Diagnosis
```
🔍 Found 1 issue(s) in cluster
⚠️  Issue detected: [default] my-app - CrashLoopBackOff
🤖 Requesting AI diagnosis for: [default] my-app → CrashLoopBackOff
✅ AI response received
📋 Cause: Container is failing to start, likely due to...
🔧 Solution: 1. Check container logs with kubectl logs...
✅ Incident created: abc-123 - [default] my-app → CrashLoopBackOff
```

### AI Failure
```
🔍 Found 1 issue(s) in cluster
⚠️  Issue detected: [default] my-app - CrashLoopBackOff
🤖 Requesting AI diagnosis for: [default] my-app → CrashLoopBackOff
❌ Cannot connect to Ollama at http://localhost:11434
❌ AI diagnosis failed - using defaults
✅ Incident created: abc-123 - [default] my-app → CrashLoopBackOff
```

## Configuration

### Change Ollama URL
```python
# In ai_service.py
self.ollama_client = OllamaClient(
    base_url="http://your-ollama-server:11434",
    model="llama3.1"
)
```

### Change Model
```python
# In ai_service.py
self.ollama_client = OllamaClient(
    base_url="http://localhost:11434",
    model="llama3.2"  # or any other model
)
```

### Change Timeout
```python
# In ai_service.py, diagnose_issue method
response = self.ollama_client.generate(prompt, timeout=60)  # 60 seconds
```

## API Response Format

### GET /incidents/
```json
[
  {
    "id": "550e8400-e29b-41d4-a716-446655440000",
    "issue": "[default] my-app → CrashLoopBackOff",
    "status": "detected",
    "cause": "Container is failing to start, likely due to missing environment variables or incorrect entrypoint configuration",
    "solution": "1. Check container logs: kubectl logs my-app\n2. Verify environment variables in deployment\n3. Check resource limits and requests\n4. Verify image exists and is accessible"
  }
]
```

### GET /incidents/{id}
```json
{
  "id": "550e8400-e29b-41d4-a716-446655440000",
  "issue": "[default] my-app → CrashLoopBackOff",
  "status": "detected",
  "cause": "Container is failing to start...",
  "solution": "1. Check container logs..."
}
```

## Success Criteria Met

✅ **AI called on incident creation** - Integrated in `create_incident_from_issue()`  
✅ **Cause and solution added** - Stored in Incident model  
✅ **API returns enriched data** - Full incident with AI diagnosis  
✅ **Works with llama3.1** - Configured in OllamaClient  
✅ **Non-blocking** - Errors don't crash system  
✅ **Simple implementation** - No async, no database  
✅ **Error handling** - Fallback values on failure  

## Next Steps

### Optional Enhancements:
1. **Async AI calls** - Don't block incident creation
2. **Caching** - Cache AI responses for similar issues
3. **Multiple models** - Try different models for comparison
4. **Streaming** - Use streaming API for faster responses
5. **Feedback loop** - Learn from resolved incidents
