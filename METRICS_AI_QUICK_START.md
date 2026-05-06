# ⚡ Metrics-Aware AI - Quick Start Guide

## 🚀 Quick Test

### 1. Run Integration Test
```bash
python test_metrics_integration.py
```

### 2. Start Guardian with Metrics
```bash
# Terminal 1: Port-forward Prometheus
kubectl port-forward -n monitoring svc/prometheus-service 9090:9090

# Terminal 2: Deploy failing pod
kubectl apply -f k8s/test-failures/crashloop.yaml

# Terminal 3: Start Guardian
cd backend
python -m app.main
```

### 3. Watch for Metrics in Logs
```
[Prometheus] CPU usage: 0.0234 cores
[Prometheus] Memory usage: 128.5 MB
[Prometheus] Restart count: 5
[Prometheus] Metrics attached to AI context
[AI] Metrics-aware diagnosis completed
```

---

## 📊 What Changed

### MonitorService
- ✅ Imports PrometheusService
- ✅ Fetches metrics before AI diagnosis
- ✅ Enriches issue context with CPU, memory, restarts

### AIService
- ✅ Receives enriched context with metrics
- ✅ Includes metrics in AI prompt
- ✅ Enhanced rule-based detection with metrics

---

## 🔧 Key Methods

### `_enrich_issue_with_metrics()`
```python
# Fetches metrics from Prometheus
enriched_issue = monitor._enrich_issue_with_metrics(issue)

# Returns:
{
    "name": "my-app",
    "namespace": "default",
    "issue": "CrashLoopBackOff",
    "cpu_usage": "0.0234 cores",
    "memory_mb": "128.5 MB",
    "restart_count": 5
}
```

### `build_diagnosis_prompt()`
```python
# Includes metrics in AI prompt
prompt = ai_service.build_diagnosis_prompt(enriched_issue)

# Prompt includes:
# - CPU Usage
# - Memory Usage
# - Restart Count
# - Metric interpretation guidelines
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
🤖 Requesting metrics-aware AI diagnosis
📋 Cause: Container crashes with 5 restarts - persistent failure
🔧 Solution: Check logs, verify startup, dependencies
[AI] Metrics-aware diagnosis completed
```

### Safe Fallback (Prometheus Down)
```
[Monitor] Issue detected: [default] my-app → CrashLoopBackOff
[Prometheus] Failed to connect
[Prometheus] Continuing with default metrics
🤖 Requesting metrics-aware AI diagnosis
📋 Cause: Container crashes after startup
🔧 Solution: Check container logs
[AI] Metrics-aware diagnosis completed
```

---

## ✅ Verification Checklist

- [ ] PrometheusService initialized in MonitorService
- [ ] Metrics fetched before AI diagnosis
- [ ] CPU usage included in context
- [ ] Memory usage included in context
- [ ] Restart count included in context
- [ ] AI prompt includes metrics
- [ ] Safe fallback works (Prometheus down)
- [ ] No crashes on metric fetch failure
- [ ] Logs show `[Prometheus]` prefix
- [ ] Logs show `[AI] Metrics-aware diagnosis`

---

## 🧪 Test Commands

```bash
# Test integration
python test_metrics_integration.py

# Test with real pod
kubectl apply -f k8s/test-failures/crashloop.yaml
cd backend && python -m app.main

# Check Prometheus
kubectl get pods -n monitoring
kubectl port-forward -n monitoring svc/prometheus-service 9090:9090

# Clean up
kubectl delete -f k8s/test-failures/crashloop.yaml
```

---

## 📚 Documentation

- **Full Guide**: `METRICS_AWARE_AI_INTEGRATION.md`
- **Phase Summary**: `PHASE11_METRICS_AI_COMPLETE.md`
- **Prometheus Guide**: `PROMETHEUS_USAGE_GUIDE.md`

---

## 🎯 Success Criteria

✅ Metrics fetched from Prometheus  
✅ AI receives enriched context  
✅ Diagnosis includes metric analysis  
✅ Safe fallback on Prometheus failure  
✅ No system crashes  

🎉 **Metrics-aware AI is working!**
