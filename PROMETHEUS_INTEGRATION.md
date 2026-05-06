# Prometheus Integration for Guardian

## Overview

Guardian now includes **Prometheus integration** for advanced Kubernetes metrics monitoring. This enables intelligent incident detection based on real-time CPU, memory, and pod health metrics.

---

## Architecture

```
Kubernetes Cluster
    ↓
Prometheus (scrapes metrics every 15s)
    ↓
PrometheusService (queries metrics via HTTP API)
    ↓
MonitorService (detects issues + creates incidents)
    ↓
AIService (diagnoses with metric context)
    ↓
ActionExecutor (executes remediation)
```

---

## Components

### 1. Prometheus Deployment

**Location**: `monitoring/prometheus/`

**Files**:
- `namespace.yaml` - Creates `monitoring` namespace
- `prometheus-rbac.yaml` - ServiceAccount, ClusterRole, ClusterRoleBinding
- `prometheus-configmap.yaml` - Prometheus configuration
- `prometheus-deployment.yaml` - Prometheus deployment (v2.47.0)
- `prometheus-service.yaml` - NodePort service (port 30090)
- `deploy.sh` - Deployment script

**Deployment**:
```bash
cd monitoring/prometheus
./deploy.sh
```

**Verification**:
```bash
# Check deployment
kubectl get pods -n monitoring

# Port-forward for local access
kubectl port-forward -n monitoring svc/prometheus-service 9090:9090

# Access UI
open http://localhost:9090
```

---

### 2. PrometheusService

**Location**: `backend/app/services/prometheus_service.py`

**Purpose**: Query Prometheus metrics via HTTP API

**Methods**:

| Method | Description | Parameters |
|--------|-------------|------------|
| `check_connection()` | Verify Prometheus is accessible | None |
| `get_cpu_usage()` | Fetch CPU usage metrics | `namespace`, `pod` (optional) |
| `get_memory_usage()` | Fetch memory usage metrics | `namespace`, `pod` (optional) |
| `get_pod_restart_count()` | Fetch pod restart counts | `namespace`, `pod` (optional) |
| `get_pod_status()` | Fetch pod status/phase | `namespace` (optional) |
| `get_container_memory_limit()` | Fetch memory limits | `namespace`, `pod` (optional) |

**Example Usage**:
```python
from backend.app.services.prometheus_service import PrometheusService

# Initialize service
prom = PrometheusService(base_url="http://localhost:9090")

# Check connection
if prom.check_connection():
    # Get CPU metrics for all pods
    cpu_metrics = prom.get_cpu_usage()
    
    # Get memory metrics for specific namespace
    memory_metrics = prom.get_memory_usage(namespace="default")
    
    # Get restart counts for specific pod
    restarts = prom.get_pod_restart_count(namespace="default", pod="my-pod")
```

---

### 3. Testing

**Location**: `backend/app/services/test_prometheus_service.py`

**Purpose**: Verify Prometheus integration and test all query methods

**Run Tests**:
```bash
# Ensure Prometheus is running and port-forwarded
kubectl port-forward -n monitoring svc/prometheus-service 9090:9090

# Run test suite
cd backend/app/services
python test_prometheus_service.py
```

**Test Coverage**:
- ✅ Connection verification
- ✅ CPU usage queries
- ✅ Memory usage queries
- ✅ Pod restart count queries
- ✅ Pod status queries
- ✅ Memory limit queries
- ✅ Filtered queries (namespace, pod)

---

## Metrics Available

### Container Metrics
- `container_cpu_usage_seconds_total` - CPU usage over time
- `container_memory_usage_bytes` - Current memory usage
- `container_spec_memory_limit_bytes` - Memory limits

### Pod Metrics (requires kube-state-metrics)
- `kube_pod_container_status_restarts_total` - Restart counts
- `kube_pod_status_phase` - Pod phase (Running, Pending, Failed, etc.)

### Kubernetes API Metrics
- `up` - Target health status
- Node metrics
- Service metrics

---

## Integration with Guardian

### Current State (Phase 10)
✅ Prometheus deployed to Kubernetes  
✅ PrometheusService created with query methods  
✅ Test suite created and verified  

### Next Steps (Future Phases)

#### Phase 11: Integrate with MonitorService
```python
# Add PrometheusService to MonitorService
class MonitorService:
    def __init__(self):
        self.k8s_service = K8sService()
        self.ai_service = AIService()
        self.prometheus_service = PrometheusService()  # NEW
        
    def check_system(self):
        # Get pod issues from K8s
        issues = self.k8s_service.get_problematic_pods()
        
        # Enrich with Prometheus metrics
        for issue in issues:
            namespace = issue['namespace']
            pod = issue['name']
            
            # Add CPU metrics
            cpu = self.prometheus_service.get_cpu_usage(namespace, pod)
            issue['cpu_usage'] = cpu[0]['cpu_usage'] if cpu else None
            
            # Add memory metrics
            memory = self.prometheus_service.get_memory_usage(namespace, pod)
            issue['memory_mb'] = memory[0]['memory_mb'] if memory else None
            
            # Add restart count
            restarts = self.prometheus_service.get_pod_restart_count(namespace, pod)
            issue['restart_count'] = restarts[0]['restart_count'] if restarts else 0
        
        return issues
```

#### Phase 12: Enhance AI Diagnosis
```python
# Pass metric context to AI
def diagnose_issue(self, issue: Dict[str, str]) -> Dict[str, str]:
    context = f"""
    Pod: {issue['name']}
    Namespace: {issue['namespace']}
    Error: {issue['issue']}
    CPU Usage: {issue.get('cpu_usage', 'N/A')} cores
    Memory Usage: {issue.get('memory_mb', 'N/A')} MB
    Restart Count: {issue.get('restart_count', 'N/A')}
    """
    # AI gets richer context for better diagnosis
```

#### Phase 13: Intelligent Thresholds
```python
# Detect issues based on metrics
def detect_high_cpu(self):
    cpu_metrics = self.prometheus_service.get_cpu_usage()
    
    for metric in cpu_metrics:
        if metric['cpu_usage'] > 0.8:  # 80% CPU
            self.create_incident_from_issue({
                'name': metric['pod'],
                'namespace': metric['namespace'],
                'issue': f"High CPU usage: {metric['cpu_usage']:.2f} cores"
            })
```

---

## Configuration

### Prometheus URL
Default: `http://localhost:9090`

**Change URL**:
```python
# In code
service = PrometheusService(base_url="http://prometheus.monitoring.svc.cluster.local:9090")

# Or via environment variable (future enhancement)
PROMETHEUS_URL = os.getenv("PROMETHEUS_URL", "http://localhost:9090")
```

### Scrape Interval
Default: `15s`

**Change interval** in `monitoring/prometheus/prometheus-configmap.yaml`:
```yaml
global:
  scrape_interval: 30s  # Change to 30 seconds
```

---

## Troubleshooting

### Connection Failed
**Error**: `[Prometheus] Failed to connect to http://localhost:9090`

**Solutions**:
1. Verify Prometheus is running:
   ```bash
   kubectl get pods -n monitoring
   ```

2. Check port-forward is active:
   ```bash
   kubectl port-forward -n monitoring svc/prometheus-service 9090:9090
   ```

3. Test Prometheus UI manually:
   ```bash
   curl http://localhost:9090/api/v1/status/config
   ```

### No Metrics Found
**Error**: `⚠️ No CPU metrics found`

**Solutions**:
1. Wait for metrics to be scraped (15-30 seconds after deployment)

2. Verify Prometheus is scraping targets:
   - Open http://localhost:9090/targets
   - Check all targets are "UP"

3. Run a test query in Prometheus UI:
   ```promql
   up
   ```

### Missing kube-state-metrics
**Error**: `⚠️ No restart count metrics found`

**Solution**: Some metrics require kube-state-metrics to be installed:
```bash
kubectl apply -f https://github.com/kubernetes/kube-state-metrics/releases/latest/download/kube-state-metrics.yaml
```

---

## Demo Flow

### Setup
```bash
# 1. Deploy Prometheus
cd monitoring/prometheus
./deploy.sh

# 2. Port-forward
kubectl port-forward -n monitoring svc/prometheus-service 9090:9090

# 3. Test integration
cd backend/app/services
python test_prometheus_service.py
```

### Expected Output
```
==============================================================
  PROMETHEUS SERVICE TEST SUITE
==============================================================

Initializing PrometheusService with URL: http://localhost:9090

==============================================================
  Testing Prometheus Connection
==============================================================
[Prometheus] Checking connection to http://localhost:9090
[Prometheus] Connection successful
✅ Successfully connected to Prometheus

==============================================================
  Testing CPU Usage Metrics
==============================================================

📊 Fetching CPU usage (all namespaces)...
[Prometheus] Executing query: rate(container_cpu_usage_seconds_total{container!=""}[5m])
[Prometheus] Query successful
[Prometheus] Retrieved 12 CPU metrics
✅ Retrieved 12 CPU metrics

Example metrics:

  1. Namespace: default
     Pod: my-app-7d8f9c5b6-x4k2p
     Container: app
     CPU Usage: 0.0234 cores

...
```

---

## Success Criteria

✅ **Phase 10 Complete**:
- Prometheus deployed to Kubernetes
- PrometheusService created with all query methods
- Test suite passes successfully
- Documentation complete

🎯 **Ready for Phase 11**:
- Integrate PrometheusService with MonitorService
- Enrich incidents with metric context
- Enhance AI diagnosis with metrics

---

## References

- **Prometheus Documentation**: https://prometheus.io/docs/
- **PromQL Queries**: https://prometheus.io/docs/prometheus/latest/querying/basics/
- **Kubernetes Metrics**: https://kubernetes.io/docs/tasks/debug/debug-cluster/resource-metrics-pipeline/
- **kube-state-metrics**: https://github.com/kubernetes/kube-state-metrics
