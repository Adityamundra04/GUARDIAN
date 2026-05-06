# Prometheus Integration Quick Guide

## Quick Start

### 1. Deploy Prometheus
```bash
cd monitoring/prometheus
./deploy.sh
```

### 2. Verify Deployment
```bash
kubectl get pods -n monitoring
# Expected: prometheus-xxx Running
```

### 3. Port-Forward for Local Access
```bash
kubectl port-forward -n monitoring svc/prometheus-service 9090:9090
```

### 4. Test Integration
```bash
cd backend/app/services
python test_prometheus_service.py
```

---

## Using PrometheusService in Code

### Basic Usage

```python
from backend.app.services.prometheus_service import PrometheusService

# Initialize
prom = PrometheusService(base_url="http://localhost:9090")

# Check connection
if not prom.check_connection():
    print("Prometheus not available")
    exit(1)

# Get metrics
cpu_metrics = prom.get_cpu_usage()
memory_metrics = prom.get_memory_usage()
restart_counts = prom.get_pod_restart_count()
```

### Filtered Queries

```python
# Get metrics for specific namespace
cpu = prom.get_cpu_usage(namespace="default")

# Get metrics for specific pod
memory = prom.get_memory_usage(namespace="default", pod="my-app-123")

# Get restart count for specific pod
restarts = prom.get_pod_restart_count(namespace="default", pod="my-app-123")
```

### Example: Detect High CPU

```python
def detect_high_cpu_pods(threshold=0.8):
    """Find pods with CPU usage above threshold."""
    prom = PrometheusService()
    cpu_metrics = prom.get_cpu_usage()
    
    high_cpu_pods = []
    for metric in cpu_metrics:
        if metric['cpu_usage'] > threshold:
            high_cpu_pods.append({
                'pod': metric['pod'],
                'namespace': metric['namespace'],
                'cpu_usage': metric['cpu_usage']
            })
    
    return high_cpu_pods
```

### Example: Detect Memory Issues

```python
def detect_memory_pressure():
    """Find pods approaching memory limits."""
    prom = PrometheusService()
    
    usage = prom.get_memory_usage()
    limits = prom.get_container_memory_limit()
    
    # Create lookup for limits
    limit_map = {}
    for limit in limits:
        key = f"{limit['namespace']}/{limit['pod']}/{limit['container']}"
        limit_map[key] = limit['limit_mb']
    
    # Check usage vs limits
    pressure_pods = []
    for metric in usage:
        key = f"{metric['namespace']}/{metric['pod']}/{metric['container']}"
        limit = limit_map.get(key, 0)
        
        if limit > 0:
            usage_percent = (metric['memory_mb'] / limit) * 100
            if usage_percent > 80:  # 80% threshold
                pressure_pods.append({
                    'pod': metric['pod'],
                    'namespace': metric['namespace'],
                    'usage_mb': metric['memory_mb'],
                    'limit_mb': limit,
                    'usage_percent': round(usage_percent, 2)
                })
    
    return pressure_pods
```

---

## Integration with MonitorService

### Step 1: Add PrometheusService

```python
# In backend/app/services/monitor_service.py

from backend.app.services.prometheus_service import PrometheusService

class MonitorService:
    def __init__(self):
        self.k8s_service = K8sService()
        self.ai_service = AIService()
        self.action_executor = ActionExecutor()
        self.prometheus_service = PrometheusService()  # ADD THIS
        self.active_issues: Set[str] = set()
```

### Step 2: Enrich Issues with Metrics

```python
def check_system(self) -> List[Dict[str, str]]:
    """Check system and enrich with Prometheus metrics."""
    try:
        # Get pod issues from K8s
        issues = self.k8s_service.get_problematic_pods()
        
        # Enrich each issue with metrics
        for issue in issues:
            namespace = issue['namespace']
            pod = issue['name']
            
            # Add CPU metrics
            cpu_metrics = self.prometheus_service.get_cpu_usage(
                namespace=namespace, 
                pod=pod
            )
            if cpu_metrics:
                issue['cpu_usage'] = cpu_metrics[0]['cpu_usage']
            
            # Add memory metrics
            memory_metrics = self.prometheus_service.get_memory_usage(
                namespace=namespace,
                pod=pod
            )
            if memory_metrics:
                issue['memory_mb'] = memory_metrics[0]['memory_mb']
            
            # Add restart count
            restart_metrics = self.prometheus_service.get_pod_restart_count(
                namespace=namespace,
                pod=pod
            )
            if restart_metrics:
                issue['restart_count'] = restart_metrics[0]['restart_count']
        
        return issues
    
    except Exception as e:
        print(f"❌ Error checking system: {e}")
        return []
```

### Step 3: Update AI Diagnosis

```python
# In backend/app/services/ai_service.py

def diagnose_issue(self, issue: Dict[str, str]) -> Dict[str, str]:
    """Diagnose issue with metric context."""
    
    # Build context with metrics
    context = f"""
Pod: {issue['name']}
Namespace: {issue['namespace']}
Error: {issue['issue']}
CPU Usage: {issue.get('cpu_usage', 'N/A')} cores
Memory Usage: {issue.get('memory_mb', 'N/A')} MB
Restart Count: {issue.get('restart_count', 'N/A')}
"""
    
    # Rest of diagnosis logic...
```

---

## Available Metrics

### CPU Metrics
```python
cpu_metrics = prom.get_cpu_usage()
# Returns: [
#   {
#     'namespace': 'default',
#     'pod': 'my-app-123',
#     'container': 'app',
#     'cpu_usage': 0.0234,  # cores
#     'timestamp': 1234567890
#   }
# ]
```

### Memory Metrics
```python
memory_metrics = prom.get_memory_usage()
# Returns: [
#   {
#     'namespace': 'default',
#     'pod': 'my-app-123',
#     'container': 'app',
#     'memory_bytes': 104857600,
#     'memory_mb': 100.0,
#     'timestamp': 1234567890
#   }
# ]
```

### Restart Count
```python
restart_metrics = prom.get_pod_restart_count()
# Returns: [
#   {
#     'namespace': 'default',
#     'pod': 'my-app-123',
#     'container': 'app',
#     'restart_count': 5,
#     'timestamp': 1234567890
#   }
# ]
```

### Pod Status
```python
status_metrics = prom.get_pod_status()
# Returns: [
#   {
#     'namespace': 'default',
#     'pod': 'my-app-123',
#     'phase': 'Running',
#     'value': 1.0,
#     'timestamp': 1234567890
#   }
# ]
```

---

## Troubleshooting

### Connection Issues

**Problem**: `[Prometheus] Failed to connect`

**Solution**:
```bash
# Check Prometheus is running
kubectl get pods -n monitoring

# Restart port-forward
kubectl port-forward -n monitoring svc/prometheus-service 9090:9090

# Test connection
curl http://localhost:9090/api/v1/status/config
```

### No Metrics

**Problem**: `⚠️ No CPU metrics found`

**Solutions**:
1. Wait 15-30 seconds for metrics to be scraped
2. Check Prometheus targets: http://localhost:9090/targets
3. Verify containers are running: `kubectl get pods -A`

### Missing kube-state-metrics

**Problem**: `⚠️ No restart count metrics found`

**Solution**: Install kube-state-metrics:
```bash
kubectl apply -f https://github.com/kubernetes/kube-state-metrics/releases/latest/download/kube-state-metrics.yaml
```

---

## Next Steps

1. ✅ Deploy Prometheus
2. ✅ Test PrometheusService
3. 🔄 Integrate with MonitorService
4. 🔄 Enhance AI diagnosis with metrics
5. 🔄 Add intelligent threshold detection
6. 🔄 Create metric-based alerts

---

## References

- Main documentation: `PROMETHEUS_INTEGRATION.md`
- Prometheus setup: `monitoring/prometheus/README.md`
- Test suite: `backend/app/services/test_prometheus_service.py`
