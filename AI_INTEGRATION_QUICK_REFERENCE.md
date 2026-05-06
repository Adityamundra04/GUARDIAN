# AI Integration Quick Reference

## ✅ Status: COMPLETE

AI diagnosis is **fully integrated** with the monitoring system.

## What Was Done

### 1. Import AIService ✅
```python
from backend.app.services.ai_service import AIService
```

### 2. Initialize AIService ✅
```python
def __init__(self):
    self.k8s_service = K8sService()
    self.ai_service = AIService()  # ✅ Added
```

### 3. Call AI on Incident Creation ✅
```python
def create_incident_from_issue(self, issue: Dict[str, str]):
    # ... duplicate check ...
    
    # Get AI diagnosis
    diagnosis = {"cause": "Unknown", "solution": "Manual investigation required"}
    try:
        diagnosis = self.ai_service.diagnose_issue(issue)  # ✅ AI called
        print(f"🤖 AI diagnosis added to incident")
    except Exception as e:
        print(f"❌ AI diagnosis failed: {e}")
```

### 4. Add AI Output to Incident ✅
```python
incident = Incident(
    issue=incident_message,
    status="detected",
    cause=diagnosis.get("cause", "Unknown"),        # ✅ AI cause
    solution=diagnosis.get("solution", "Manual investigation required")  # ✅ AI solution
)
```

## Result

### Before ❌
```json
{
  "issue": "[production] my-app → CrashLoopBackOff",
  "cause": null,
  "solution": null
}
```

### After ✅
```json
{
  "issue": "[production] my-app → CrashLoopBackOff",
  "cause": "Container exits immediately due to invalid command or missing entrypoint",
  "solution": "Check container entrypoint with kubectl describe pod and verify binary exists"
}
```

## Test It

```bash
# 1. Start Ollama
ollama serve

# 2. Start Guardian
cd backend && uvicorn app.main:app --reload

# 3. Deploy failing pod
kubectl apply -f k8s/test-failures/crashloop.yaml

# 4. Check incidents (wait 5-10 seconds)
curl http://localhost:8000/incidents/
```

## Expected Logs

```
🔍 Found 1 issue(s) in cluster
⚠️  Issue detected: [default] crashloop-test - CrashLoopBackOff
🤖 Requesting AI diagnosis for: [default] crashloop-test - CrashLoopBackOff
✅ AI response received (245 chars)
📋 Cause: Container exits immediately due to invalid command...
🔧 Solution: Check container entrypoint with kubectl describe...
🤖 AI diagnosis added to incident
✅ Incident created: abc-123 - [default] crashloop-test → CrashLoopBackOff
```

## Files Modified

- `backend/app/services/monitor_service.py` - Added AI integration (~10 lines)

## Success Criteria

✅ AIService imported  
✅ AIService initialized  
✅ AI called on incident creation  
✅ AI output added to incident  
✅ Error handling in place  
✅ Logging added  
✅ Existing logic preserved  

🎉 **Integration Complete!**
