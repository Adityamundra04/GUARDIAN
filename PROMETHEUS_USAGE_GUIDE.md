# 🎯 Prometheus Integration - Complete Usage Guide

## ✅ Status: FULLY IMPLEMENTED

The PrometheusService has been successfully implemented and is ready to use!

---

## 📦 What's Implemented

### 1. PrometheusService Class ✅
**Location**: `backend/app/services/prometheus_service.py`

**Features**:
- ✅ Configurable base URL (default: `http://localhost:9090`)
- ✅ Generic query method with error handling
- ✅ Timeout protection (10 seconds)
- ✅ Connection error handling
- ✅ Clean logging with `[Prometheus]` prefix
- ✅ Safe JSON parsing
- ✅ Returns empty results on failure (no crashes)

**Core Methods**:
| Method | PromQL Query | Returns |
|--------|--------------|---------|
| `check_connection()` | Status check | `bool` |
| `get_cpu_usage()` | `rate(container_cpu_usage_seconds_total[5m])` | `List[Dict]` |
| `get_memory_usage()` | `container_memory_usage_bytes` | `List[Dict]` |
| `get_pod_restart_count()` | `kube_pod_container_status_restarts_total` | `List[Dict]` |
| `get_pod_status()` | `kube_pod_status_phase` | `List[Dict]` |
| `get_container_memory_limit()` | `container_spec_memory_limit_bytes` | `List[Dict]` |

---

## 🚀 Quick Start

### Step 1: Ensure Prometheus is Running
```bash
# Check if Prometheus pod is running
kubectl get pods -n monitoring

# Expected output:
# NAME                          READY   STATUS    RESTARTS   AGE
# prometheus-7d9f8c8b5d-x7k2m   1/1     Running   0          5m
```

### Step 2: Port-Forward Prometheus
```bash
# Forward Prometheus to localhost:9090
kubectl port-forward -n monitoring svc/prometheus-service 9090:9090
```

**Keep this terminal open!**

### Step 3: Run the Test Suite
Open a new terminal:
```bash
cd backend/app/services
python test_prometheus_service.py
```

---

## 💻 Code Examples

### Example 1: Basic Connection Test
```python
from backend.app.services.prometheus_service import PrometheusService

# Initialize service
prom = PrometheusService(base_url="http://localhost:9090")

# Check connection
if prom.check_connection():
    print("✅ Prometheus is accessible")
else:
    print("❌ Cannot connect to Prometheus")
```

### Example 2: Fetch CPU Metrics
```python
from backend.app.services.prometheus_service import PrometheusService

prom = PrometheusService()

# Get CPU metrics for all pods
cpu_metrics = prom.get_cpu_usage()

for metric in cpu_metrics:
    print(f"Namespace: {metric['namespace']}")
    print(f"Pod: {metric['pod']}")
    print(f"Container: {metric['container']}")
    print(f"CPU Usage: {metric['cpu_usage']:.4f} cores")
    print("---")
```

### Example 3: Fetch Memory Metrics for Specific Namespace
```python
from backend.app.services.prometheus_service import PrometheusService

prom = PrometheusService()

# Get memory metrics for 'default' namespace only
memory_metrics = prom.get_memory_usage(namespace="default")

for metric in memory_metrics:
    print(f"Pod: {metric['pod']}")
    print(f"Memory: {metric['memory_mb']} MB")
    print("---")
```

### Example 4: Check Pod Restart Counts
```python
from backend.app.services.prometheus_service import PrometheusService

prom = PrometheusService()

# Get restart counts
restart_metrics = prom.get_pod_restart_count()

# Find pods with high restart counts
for metric in restart_metrics:
    if metric['restart_count'] > 5:
        print(f"⚠️  High restart count detected!")
        print(f"   Pod: {metric['pod']}")
        print(f"   Namespace: {metric['namespace']}")
        print(f"   Restarts: {metric['restart_count']}")
```

### Example 5: Custom Prometheus URL
```python
from backend.app.services.prometheus_service import PrometheusService

# Use custom Prometheus URL
prom = PrometheusService(
    base_url="http://prometheus.monitoring.svc.cluster.local:9090"
)

# Use as normal
cpu_metrics = prom.get_cpu_usage()
```

---

## 🔧 Integration with Guardian

### Integrate with MonitorService

**File**: `backend/app/services/monitor_service.py`

```python
from backend.app.services.prometheus_service import PrometheusService

class MonitorService:
    def __init__(self):
        self.k8s_service = K8sService()
        self.ai_service = AIService()
        self.action_executor = ActionExecutor()
        self.prometheus_service = PrometheusService()  # ADD THIS
        self.active_issues: Set[str] = set()
    
    def check_system(self) -> List[Dict[str, str]]:
        """Check system and enrich with Prometheus metrics."""
        try:
            # Get pod issues from Kubernetes
            issues = self.k8s_service.get_problematic_pods()
            
            # Enrich each issue with Prometheus metrics
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

### Enhance AI Diagnosis with Metrics

**File**: `backend/app/services/ai_service.py`

```python
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
    
    # Enhanced prompt with metrics
    prompt = f"""You are a Kubernetes expert debugging production systems.
Analyze the issue and give a SPECIFIC answer.

Issue details: {context}

Rules:
- Be specific, not generic
- If CrashLoopBackOff, explain WHY container crashes
- Consider CPU and memory metrics in your analysis
- Suggest a direct fix (not general advice)
- Keep answer short

Respond ONLY in this format:
Cause: <specific cause>
Fix: <specific fix>
"""
    
    # Rest of diagnosis logic...
```

---

## 📊 Test Output Example

When you run `python test_prometheus_service.py`, you should see:

```
==============================================================
  PROMETHEUS SERVICE TEST SUITE
==============================================================

This script tests the PrometheusService integration.
Ensure Prometheus is running and accessible before testing.

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

  2. Namespace: kube-system
     Pod: coredns-5d78c9869d-abc12
     Container: coredns
     CPU Usage: 0.0012 cores

==============================================================
  Testing Memory Usage Metrics
==============================================================

📊 Fetching memory usage (all namespaces)...
[Prometheus] Executing query: container_memory_usage_bytes{container!=""}
[Prometheus] Query successful
[Prometheus] Retrieved 12 memory metrics
✅ Retrieved 12 memory metrics

Example metrics:

  1. Namespace: default
     Pod: my-app-7d8f9c5b6-x4k2p
     Container: app
     Memory Usage: 128.5 MB (134742016 bytes)

==============================================================
  Test Summary
==============================================================

✅ All tests completed successfully!

Next Steps:
1. Integrate PrometheusService with MonitorService
2. Use metrics for intelligent incident detection
3. Enhance AI diagnosis with metric context
```

---

## 🛠️ Troubleshooting

### Issue 1: Connection Failed

**Error**:
```
[Prometheus] Failed to connect to http://localhost:9090
❌ Cannot proceed without Prometheus connection
```

**Solutions**:

1. **Check Prometheus is running**:
```bash
kubectl get pods -n monitoring
```

2. **Verify port-forward is active**:
```bash
# Kill existing port-forward
pkill -f "port-forward.*prometheus"

# Start new port-forward
kubectl port-forward -n monitoring svc/prometheus-service 9090:9090
```

3. **Test Prometheus manually**:
```bash
curl http://localhost:9090/api/v1/status/config
```

---

### Issue 2: No Metrics Found

**Warning**:
```
⚠️  No CPU metrics found
   This may be normal if no containers are running or metrics aren't available yet
```

**Solutions**:

1. **Wait for metrics to be scraped** (15-30 seconds):
```bash
sleep 30
python test_prometheus_service.py
```

2. **Check Prometheus targets**:
```bash
# Open Prometheus UI
open http://localhost:9090/targets

# All targets should show "UP" status
```

3. **Verify containers are running**:
```bash
kubectl get pods -A
```

---

### Issue 3: Missing kube-state-metrics

**Warning**:
```
⚠️  No restart count metrics found
   Note: This requires kube-state-metrics to be installed
```

**Solution**: Install kube-state-metrics (optional):
```bash
kubectl apply -f https://github.com/kubernetes/kube-state-metrics/releases/latest/download/kube-state-metrics.yaml
```

---

## 📚 API Reference

### PrometheusService Class

#### `__init__(base_url: str = "http://localhost:9090")`
Initialize Prometheus service.

**Parameters**:
- `base_url` (str): Prometheus server URL

**Example**:
```python
prom = PrometheusService(base_url="http://localhost:9090")
```

---

#### `check_connection() -> bool`
Check if Prometheus is accessible.

**Returns**: `True` if connected, `False` otherwise

**Example**:
```python
if prom.check_connection():
    print("Connected!")
```

---

#### `get_cpu_usage(namespace: Optional[str] = None, pod: Optional[str] = None) -> List[Dict[str, Any]]`
Get CPU usage metrics for containers.

**Parameters**:
- `namespace` (Optional[str]): Filter by namespace
- `pod` (Optional[str]): Filter by pod name

**Returns**: List of dictionaries with keys:
- `namespace` (str)
- `pod` (str)
- `container` (str)
- `cpu_usage` (float): CPU cores used
- `timestamp` (float)

**Example**:
```python
# All pods
cpu_metrics = prom.get_cpu_usage()

# Specific namespace
cpu_metrics = prom.get_cpu_usage(namespace="default")

# Specific pod
cpu_metrics = prom.get_cpu_usage(namespace="default", pod="my-app-123")
```

---

#### `get_memory_usage(namespace: Optional[str] = None, pod: Optional[str] = None) -> List[Dict[str, Any]]`
Get memory usage metrics for containers.

**Parameters**:
- `namespace` (Optional[str]): Filter by namespace
- `pod` (Optional[str]): Filter by pod name

**Returns**: List of dictionaries with keys:
- `namespace` (str)
- `pod` (str)
- `container` (str)
- `memory_bytes` (float): Memory in bytes
- `memory_mb` (float): Memory in MB
- `timestamp` (float)

**Example**:
```python
memory_metrics = prom.get_memory_usage(namespace="default")
```

---

#### `get_pod_restart_count(namespace: Optional[str] = None, pod: Optional[str] = None) -> List[Dict[str, Any]]`
Get pod restart count metrics.

**Parameters**:
- `namespace` (Optional[str]): Filter by namespace
- `pod` (Optional[str]): Filter by pod name

**Returns**: List of dictionaries with keys:
- `namespace` (str)
- `pod` (str)
- `container` (str)
- `restart_count` (int): Number of restarts
- `timestamp` (float)

**Example**:
```python
restarts = prom.get_pod_restart_count()
```

---

## 🎯 Next Steps

### Phase 11: Integrate with MonitorService
1. Add PrometheusService to MonitorService
2. Enrich incidents with CPU/memory metrics
3. Pass metric context to AI

### Phase 12: Enhance AI Diagnosis
1. Update AI prompts with metric context
2. Improve diagnosis accuracy
3. Add metric-based root cause analysis

### Phase 13: Intelligent Thresholds
1. Detect high CPU (>80%)
2. Detect memory pressure (>80% of limit)
3. Detect excessive restarts (>5)
4. Create metric-based incidents

---

## 📖 Additional Resources

- **Main Documentation**: `PROMETHEUS_INTEGRATION.md`
- **Prometheus Setup**: `monitoring/prometheus/README.md`
- **Integration Guide**: `monitoring/prometheus/INTEGRATION_GUIDE.md`
- **Test Guide**: `backend/app/services/README_PROMETHEUS_TEST.md`
- **Phase Summary**: `PHASE10_COMPLETION_SUMMARY.md`

---

## ✅ Success Criteria Met

| Requirement | Status | Implementation |
|-------------|:------:|----------------|
| PrometheusService class | ✅ | `prometheus_service.py` |
| Configurable base URL | ✅ | Constructor parameter |
| get_cpu_usage() | ✅ | Uses `container_cpu_usage_seconds_total` |
| get_memory_usage() | ✅ | Uses `container_memory_usage_bytes` |
| get_pod_restart_count() | ✅ | Uses `kube_pod_container_status_restarts_total` |
| Generic query method | ✅ | `_execute_query()` |
| Error handling | ✅ | Timeout, connection errors, invalid JSON |
| Clean logging | ✅ | `[Prometheus]` prefix |
| Test file | ✅ | `test_prometheus_service.py` |
| Safe failure handling | ✅ | Returns empty list on error |

---

🎉 **PrometheusService is fully implemented and ready to use!**
