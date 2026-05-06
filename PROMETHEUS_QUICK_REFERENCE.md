# ⚡ Prometheus Integration - Quick Reference

## 🚀 Quick Start Commands

### 1. Deploy Prometheus
```bash
cd monitoring/prometheus
./deploy.sh
```

### 2. Port-Forward
```bash
kubectl port-forward -n monitoring svc/prometheus-service 9090:9090
```

### 3. Run Tests
```bash
cd backend/app/services
python test_prometheus_service.py
```

---

## 💻 Code Snippets

### Initialize Service
```python
from backend.app.services.prometheus_service import PrometheusService

prom = PrometheusService(base_url="http://localhost:9090")
```

### Check Connection
```python
if prom.check_connection():
    print("✅ Connected")
```

### Get CPU Metrics
```python
cpu_metrics = prom.get_cpu_usage()
# or with filters:
cpu_metrics = prom.get_cpu_usage(namespace="default", pod="my-app")
```

### Get Memory Metrics
```python
memory_metrics = prom.get_memory_usage()
# or with filters:
memory_metrics = prom.get_memory_usage(namespace="default")
```

### Get Restart Counts
```python
restarts = prom.get_pod_restart_count()
```

---

## 🔧 Troubleshooting Commands

### Check Prometheus Pod
```bash
kubectl get pods -n monitoring
```

### Restart Port-Forward
```bash
pkill -f "port-forward.*prometheus"
kubectl port-forward -n monitoring svc/prometheus-service 9090:9090
```

### Test Prometheus API
```bash
curl http://localhost:9090/api/v1/status/config
```

### Check Prometheus Targets
```bash
open http://localhost:9090/targets
```

---

## 📊 Metric Data Structure

### CPU Metrics
```python
{
    'namespace': 'default',
    'pod': 'my-app-123',
    'container': 'app',
    'cpu_usage': 0.0234,  # cores
    'timestamp': 1234567890
}
```

### Memory Metrics
```python
{
    'namespace': 'default',
    'pod': 'my-app-123',
    'container': 'app',
    'memory_bytes': 134742016,
    'memory_mb': 128.5,
    'timestamp': 1234567890
}
```

### Restart Count
```python
{
    'namespace': 'default',
    'pod': 'my-app-123',
    'container': 'app',
    'restart_count': 5,
    'timestamp': 1234567890
}
```

---

## 📁 File Locations

| File | Location |
|------|----------|
| PrometheusService | `backend/app/services/prometheus_service.py` |
| Test Suite | `backend/app/services/test_prometheus_service.py` |
| Usage Guide | `PROMETHEUS_USAGE_GUIDE.md` |
| Integration Guide | `monitoring/prometheus/INTEGRATION_GUIDE.md` |
| Main Documentation | `PROMETHEUS_INTEGRATION.md` |

---

## ✅ Verification Checklist

- [ ] Prometheus pod is running
- [ ] Port-forward is active on 9090
- [ ] Test suite passes
- [ ] Metrics are being collected
- [ ] Connection check succeeds

---

## 🎯 Integration Example

```python
# In monitor_service.py
from backend.app.services.prometheus_service import PrometheusService

class MonitorService:
    def __init__(self):
        self.prometheus_service = PrometheusService()
    
    def check_system(self):
        issues = self.k8s_service.get_problematic_pods()
        
        for issue in issues:
            # Enrich with metrics
            cpu = self.prometheus_service.get_cpu_usage(
                namespace=issue['namespace'],
                pod=issue['name']
            )
            if cpu:
                issue['cpu_usage'] = cpu[0]['cpu_usage']
        
        return issues
```

---

## 📞 Support

- **Documentation**: `PROMETHEUS_USAGE_GUIDE.md`
- **Test Guide**: `backend/app/services/README_PROMETHEUS_TEST.md`
- **Prometheus Setup**: `monitoring/prometheus/README.md`
