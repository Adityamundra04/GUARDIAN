# Guardian Demo Guide

## Quick Start

### Prerequisites
```bash
# 1. Start Ollama
ollama serve

# 2. Ensure llama3.1 is installed
ollama pull llama3.1

# 3. Ensure Kubernetes cluster is running
kubectl cluster-info
```

### Start Guardian
```bash
cd backend
uvicorn app.main:app --reload
```

**Expected Output:**
```
🔧 Starting Guardian application...
🚀 Monitoring started...
✅ Background monitoring thread started
```

## Demo Scenario: CrashLoopBackOff

### Step 1: Deploy Failing Pod
```bash
kubectl apply -f k8s/test-failures/crashloop.yaml
```

### Step 2: Watch Guardian Logs

**Cycle 1 (First Detection):**
```
[Monitor] Found 1 issue(s) in cluster
[Monitor] Issue detected: [default] crash-test → CrashLoopBackOff
[AI] Diagnosis completed
[Monitor] Incident created: 550e8400-e29b-41d4-a716-446655440000
[Safety] Safe action decided: restart_pod for pod crash-test
[OpenClaw] Executing action: restart pod crash-test
[OpenClaw] Restart successful: crash-test
[OpenClaw] Action completed successfully
[Safety] Action recorded for default/crash-test (attempt 1/3)
```

**Cycle 2 (Still Failing):**
```
[Monitor] Found 1 issue(s) in cluster
[Monitor] Issue detected: [default] crash-test → CrashLoopBackOff
[Safety] Safe action decided: restart_pod for pod crash-test
[OpenClaw] Executing action: restart pod crash-test
[OpenClaw] Restart successful: crash-test
[Safety] Action recorded for default/crash-test (attempt 2/3)
```

**Cycle 3 (Last Attempt):**
```
[Monitor] Found 1 issue(s) in cluster
[Monitor] Issue detected: [default] crash-test → CrashLoopBackOff
[Safety] Safe action decided: restart_pod for pod crash-test
[OpenClaw] Executing action: restart pod crash-test
[OpenClaw] Restart successful: crash-test
[Safety] Action recorded for default/crash-test (attempt 3/3)
```

**Cycle 4 (Retry Limit Reached):**
```
[Monitor] Found 1 issue(s) in cluster
[Monitor] Issue detected: [default] crash-test → CrashLoopBackOff
[Safety] Retry limit reached for crash-test - skipping action
```

### Step 3: Check Incident via API
```bash
curl http://localhost:8000/incidents/ | jq
```

**Expected Response:**
```json
[
  {
    "id": "550e8400-e29b-41d4-a716-446655440000",
    "issue": "[default] crash-test → CrashLoopBackOff",
    "status": "detected",
    "cause": "Container exits immediately due to invalid command or missing entrypoint",
    "solution": "Check container entrypoint with kubectl describe pod and verify binary exists",
    "action_taken": "restart_pod",
    "action_status": "success"
  }
]
```

### Step 4: Cleanup
```bash
kubectl delete -f k8s/test-failures/crashloop.yaml
```

**Expected Log:**
```
[Monitor] Issue resolved: default/crash-test
```

## Demo Talking Points

### 1. Automatic Detection
"Guardian continuously monitors the Kubernetes cluster and automatically detects pod failures like CrashLoopBackOff."

### 2. AI-Powered Diagnosis
"When an issue is detected, Guardian uses AI (llama3.1 via Ollama) to analyze the problem and provide a specific root cause and actionable fix."

### 3. Safe Auto-Remediation
"Guardian's OpenClaw component automatically executes safe remediation actions. In this case, it restarts the failing pod."

### 4. Intelligent Retry Logic
"Guardian doesn't endlessly retry broken workloads. After 3 attempts, it stops and waits for manual intervention. This prevents resource waste and alert fatigue."

### 5. Complete Observability
"Every action is logged with clear prefixes ([Monitor], [AI], [Safety], [OpenClaw]) making it easy to understand what's happening."

### 6. Action Tracking
"Incidents include action_taken and action_status fields, providing full traceability of what Guardian did to remediate the issue."

## Key Features to Highlight

### ✅ Automatic Detection
- Monitors Kubernetes cluster continuously
- Detects CrashLoopBackOff, ImagePullBackOff, high restart counts

### ✅ AI-Powered Diagnosis
- Uses llama3.1 for root cause analysis
- Provides specific, actionable solutions
- Not generic troubleshooting lists

### ✅ Safe Auto-Remediation
- Only executes whitelisted actions
- Namespace restrictions (production disabled by default)
- Retry limits prevent endless loops
- Cooldown period between attempts

### ✅ Complete Observability
- Clean, prefixed logging
- Action results tracked in incidents
- Full audit trail

## Configuration

### Retry Limits
```python
# agent/safety_rules.py
MAX_RETRY_ATTEMPTS = 3  # Maximum retry attempts
COOLDOWN_SECONDS = 60   # Cooldown between retries
```

### Allowed Namespaces
```python
# agent/safety_rules.py
ALLOWED_NAMESPACES = [
    "default",
    "development",
    "staging",
    "testing",
    # "production",  # Disabled by default
]
```

### Safe Actions
```python
# agent/safety_rules.py
SAFE_ACTIONS = {
    "CrashLoopBackOff": "restart_pod",
    "ImagePullBackOff": "delete_pod",
    "High restart count": "restart_pod",
}
```

## API Endpoints

### Get All Incidents
```bash
curl http://localhost:8000/incidents/
```

### Get Specific Incident
```bash
curl http://localhost:8000/incidents/{incident_id}
```

### Health Check
```bash
curl http://localhost:8000/health
```

### Root
```bash
curl http://localhost:8000/
```

## Troubleshooting

### Issue: No AI diagnosis
**Check:**
- Is Ollama running? (`ollama serve`)
- Is llama3.1 installed? (`ollama pull llama3.1`)
- Can Guardian reach Ollama? (`curl http://localhost:11434`)

### Issue: No actions executed
**Check:**
- Is namespace in `ALLOWED_NAMESPACES`?
- Has retry limit been reached?
- Is cooldown active?
- Check Guardian logs for `[Safety]` messages

### Issue: Actions not working
**Check:**
- Kubernetes permissions (RBAC)
- Pod exists in correct namespace
- Check `[OpenClaw]` logs for errors

## Demo Script

### Introduction (30 seconds)
"Guardian is an AI-powered Kubernetes incident assistant that automatically detects, diagnoses, and fixes pod failures."

### Demo (2 minutes)
1. Show Guardian running
2. Deploy failing pod
3. Show logs (detection → diagnosis → remediation)
4. Show API response with action tracking
5. Show retry limit behavior

### Conclusion (30 seconds)
"Guardian provides complete self-healing for Kubernetes clusters with intelligent retry logic, AI-powered diagnosis, and safe auto-remediation."

## Success Metrics

✅ **Detection Time** - Issues detected within 5-10 seconds  
✅ **Diagnosis Quality** - Specific root causes, not generic advice  
✅ **Remediation Success** - Actions execute successfully  
✅ **Retry Behavior** - Stops after 3 attempts  
✅ **Log Clarity** - Clean, readable output  

🎉 **Guardian is demo-ready!**
