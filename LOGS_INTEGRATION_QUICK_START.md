# ⚡ Kubernetes Logs Integration - Quick Start

## 🚀 Quick Test

### 1. Verify Integration
```bash
python verify_logs_integration.py
```

### 2. Test End-to-End
```bash
# Terminal 1: Port-forward Prometheus
kubectl port-forward -n monitoring svc/prometheus-service 9090:9090

# Terminal 2: Deploy failing pod
kubectl apply -f k8s/test-failures/crashloop.yaml

# Terminal 3: Start Guardian
cd backend
python -m app.main
```

### 3. Watch for Logs in Output
```
[K8s] Fetching logs for pod crash-test
[K8s] Logs retrieved successfully (1245 chars)
[K8s] Pod logs attached to AI context
🤖 Requesting enriched AI diagnosis (with logs)
📋 Cause: Container fails due to [specific error from logs]
🔧 Solution: [specific fix based on logs]
```

---

## 📊 What Changed

### K8sService
- ✅ Added `get_pod_logs()` method
- ✅ Fetches last 50 lines of logs
- ✅ Truncates to 2000 characters
- ✅ Safe error handling

### MonitorService
- ✅ Fetches logs after metrics
- ✅ Attaches logs to enriched context
- ✅ Safe fallback if logs unavailable

### AIService
- ✅ Includes logs in AI prompt
- ✅ Prioritizes log analysis
- ✅ Enhanced diagnosis with log context

---

## 🔧 Key Methods

### `get_pod_logs()`
```python
# Fetch pod logs
logs = k8s_service.get_pod_logs(
    namespace="default",
    pod_name="my-app",
    tail_lines=50
)

# Returns:
# - Last 50 lines of logs
# - Truncated to 2000 chars
# - Empty string if unavailable
```

### Enriched Context
```python
{
    "name": "my-app",
    "namespace": "default",
    "issue": "CrashLoopBackOff",
    "cpu_usage": "0.0234 cores",
    "memory_mb": "128.5 MB",
    "restart_count": 5,
    "logs": "Error: Connection refused..."  # NEW
}
```

---

## 📝 Example Logs

### Success
```
[Monitor] Issue detected: [default] my-app → CrashLoopBackOff
[Prometheus] CPU usage: 0.0234 cores
[Prometheus] Memory usage: 128.5 MB
[Prometheus] Restart count: 5
[Prometheus] Metrics attached to AI context
[K8s] Fetching logs for pod my-app in namespace default
[K8s] Logs retrieved successfully (1245 chars)
[K8s] Pod logs attached to AI context
🤖 Requesting enriched AI diagnosis (with logs)
📋 Cause: Container fails to connect to database at localhost:5432
🔧 Solution: Verify database service and update connection string
```

### Safe Fallback (No Logs)
```
[Monitor] Issue detected: [default] my-app → CrashLoopBackOff
[Prometheus] Metrics attached to AI context
[K8s] Fetching logs for pod my-app in namespace default
[K8s] Failed to fetch logs for my-app: API error 404
[K8s] Continuing without logs
🤖 Requesting enriched AI diagnosis
📋 Cause: Container crashes with 5 restarts
🔧 Solution: Check logs and verify startup
```

---

## ✅ Verification Checklist

- [ ] `get_pod_logs()` method exists in K8sService
- [ ] Logs fetched in `_enrich_issue_with_metrics()`
- [ ] Logs attached to `enriched_issue['logs']`
- [ ] AI prompt includes "Recent Container Logs:"
- [ ] AI guidelines prioritize log analysis
- [ ] Safe fallback works (no logs available)
- [ ] No crashes on log fetch failure
- [ ] Logs show `[K8s]` prefix
- [ ] Logs show "(with logs)" indicator
- [ ] Diagnosis references specific log errors

---

## 🧪 Test Commands

```bash
# Verify integration
python verify_logs_integration.py

# Deploy failing pod
kubectl apply -f k8s/test-failures/crashloop.yaml

# Check pod logs manually
kubectl logs crash-test -n default

# Start Guardian
cd backend && python -m app.main

# Clean up
kubectl delete -f k8s/test-failures/crashloop.yaml
```

---

## 📊 Before vs After

### Before (Phase 11)
```
AI Context:
- Issue: CrashLoopBackOff
- CPU: 0.02 cores
- Memory: 128 MB
- Restarts: 5

Diagnosis: "Container crashes - check logs"
```

### After (Phase 12)
```
AI Context:
- Issue: CrashLoopBackOff
- CPU: 0.02 cores
- Memory: 128 MB
- Restarts: 5
- Logs: "Error: Connection refused at localhost:5432"

Diagnosis: "Container fails to connect to database at localhost:5432 - verify database service"
```

**Improvement**: Diagnosis is now specific to actual log errors!

---

## 🎯 Success Criteria

✅ Logs fetched from Kubernetes  
✅ Logs attached to AI context  
✅ AI prompt includes logs  
✅ Diagnosis references log errors  
✅ Safe fallback on log failure  
✅ No system crashes  

🎉 **Log-aware AI is working!**

---

## 📚 Documentation

- **Full Guide**: `LOGS_INTEGRATION_COMPLETE.md`
- **Metrics Integration**: `METRICS_AWARE_AI_INTEGRATION.md`
- **Prometheus Guide**: `PROMETHEUS_USAGE_GUIDE.md`

---

## 🔄 Integration Timeline

- ✅ Phase 10: Prometheus metrics
- ✅ Phase 11: Metrics-aware AI
- ✅ Phase 12: Logs integration (Current)
- 🔄 Phase 13: Intelligent thresholds

Guardian now has the most comprehensive AI diagnosis system!
