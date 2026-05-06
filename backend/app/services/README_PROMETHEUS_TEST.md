# Prometheus Service Test Guide

## Quick Start

### Prerequisites
1. Prometheus deployed to Kubernetes
2. Port-forward active to access Prometheus

### Step-by-Step

#### 1. Deploy Prometheus (if not already deployed)
```bash
cd monitoring/prometheus
./deploy.sh
```

Wait for pod to be ready:
```bash
kubectl wait --for=condition=ready pod -l app=prometheus -n monitoring --timeout=60s
```

#### 2. Port-Forward Prometheus Service
```bash
kubectl port-forward -n monitoring svc/prometheus-service 9090:9090
```

Keep this terminal open!

#### 3. Run Test Suite
Open a new terminal:
```bash
cd backend/app/services
python test_prometheus_service.py
```

---

## Expected Output

### Successful Test Run
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

  3. Namespace: monitoring
     Pod: prometheus-7d9f8c8b5d-x7k2m
     Container: prometheus
     CPU Usage: 0.0456 cores

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

  2. Namespace: kube-system
     Pod: coredns-5d78c9869d-abc12
     Container: coredns
     Memory Usage: 45.2 MB (47398912 bytes)

  3. Namespace: monitoring
     Pod: prometheus-7d9f8c8b5d-x7k2m
     Container: prometheus
     Memory Usage: 256.8 MB (269221888 bytes)

==============================================================
  Testing Pod Restart Count Metrics
==============================================================

📊 Fetching pod restart counts (all namespaces)...
[Prometheus] Executing query: kube_pod_container_status_restarts_total
[Prometheus] Query successful
[Prometheus] Retrieved 8 restart count metrics
✅ Retrieved 8 restart count metrics

Example metrics:

  1. Namespace: default
     Pod: my-app-7d8f9c5b6-x4k2p
     Container: app
     Restart Count: 0

  2. Namespace: default
     Pod: crash-test-pod
     Container: app
     Restart Count: 5

  3. Namespace: kube-system
     Pod: coredns-5d78c9869d-abc12
     Container: coredns
     Restart Count: 0

==============================================================
  Testing Pod Status Metrics
==============================================================

📊 Fetching pod status (all namespaces)...
[Prometheus] Executing query: kube_pod_status_phase
[Prometheus] Query successful
[Prometheus] Retrieved 10 pod status metrics
✅ Retrieved 10 pod status metrics

Example metrics:

  1. Namespace: default
     Pod: my-app-7d8f9c5b6-x4k2p
     Phase: Running
     Value: 1.0

  2. Namespace: default
     Pod: crash-test-pod
     Phase: Failed
     Value: 1.0

  3. Namespace: monitoring
     Pod: prometheus-7d9f8c8b5d-x7k2m
     Phase: Running
     Value: 1.0

==============================================================
  Testing Container Memory Limits
==============================================================

📊 Fetching memory limits (all namespaces)...
[Prometheus] Executing query: container_spec_memory_limit_bytes{container!=""}
[Prometheus] Query successful
[Prometheus] Retrieved 10 memory limit metrics
✅ Retrieved 10 memory limit metrics

Example metrics:

  1. Namespace: default
     Pod: my-app-7d8f9c5b6-x4k2p
     Container: app
     Memory Limit: 512.0 MB (536870912 bytes)

  2. Namespace: kube-system
     Pod: coredns-5d78c9869d-abc12
     Container: coredns
     Memory Limit: 170.0 MB (178257920 bytes)

  3. Namespace: monitoring
     Pod: prometheus-7d9f8c8b5d-x7k2m
     Container: prometheus
     Memory Limit: 512.0 MB (536870912 bytes)

==============================================================
  Testing Filtered Queries
==============================================================

📊 Testing namespace filter (namespace='default')...
   Found 3 CPU metrics in 'default' namespace

📊 Testing pod filter (pod='my-app-7d8f9c5b6-x4k2p')...
   Found 1 CPU metrics for pod 'my-app-7d8f9c5b6-x4k2p'

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

## Troubleshooting

### Error: Connection Failed

**Output**:
```
❌ Failed to connect to Prometheus

Troubleshooting:
1. Ensure Prometheus is running
2. Check if port-forward is active:
   kubectl port-forward -n monitoring svc/prometheus-service 9090:9090
3. Verify Prometheus URL is correct (default: http://localhost:9090)
```

**Solutions**:

1. **Check Prometheus pod is running**:
```bash
kubectl get pods -n monitoring
```

Expected:
```
NAME                          READY   STATUS    RESTARTS   AGE
prometheus-7d9f8c8b5d-x7k2m   1/1     Running   0          5m
```

2. **Verify port-forward is active**:
```bash
# Check if port 9090 is listening
netstat -an | grep 9090

# Or on Windows
netstat -an | findstr 9090
```

3. **Test Prometheus manually**:
```bash
curl http://localhost:9090/api/v1/status/config
```

4. **Restart port-forward**:
```bash
# Kill existing port-forward
pkill -f "port-forward.*prometheus"

# Start new port-forward
kubectl port-forward -n monitoring svc/prometheus-service 9090:9090
```

---

### Warning: No Metrics Found

**Output**:
```
⚠️  No CPU metrics found
   This may be normal if no containers are running or metrics aren't available yet
```

**Reasons**:
1. Prometheus just started (wait 15-30 seconds)
2. No containers running in cluster
3. Metrics not being scraped

**Solutions**:

1. **Wait for metrics to be scraped**:
```bash
# Wait 30 seconds
sleep 30

# Run test again
python test_prometheus_service.py
```

2. **Check Prometheus targets**:
Open http://localhost:9090/targets

All targets should show "UP" status.

3. **Verify metrics in Prometheus UI**:
Open http://localhost:9090/graph

Run query:
```promql
up
```

Should return results.

4. **Check if containers are running**:
```bash
kubectl get pods -A
```

---

### Warning: Missing kube-state-metrics

**Output**:
```
⚠️  No restart count metrics found
   Note: This requires kube-state-metrics to be installed
```

**Reason**: Some metrics require kube-state-metrics

**Solution**: Install kube-state-metrics (optional):
```bash
kubectl apply -f https://github.com/kubernetes/kube-state-metrics/releases/latest/download/kube-state-metrics.yaml
```

Wait for pod to be ready:
```bash
kubectl wait --for=condition=ready pod -l app.kubernetes.io/name=kube-state-metrics -n kube-system --timeout=60s
```

Run test again:
```bash
python test_prometheus_service.py
```

---

### Error: Import Error

**Output**:
```
ModuleNotFoundError: No module named 'prometheus_service'
```

**Solution**: Ensure you're in the correct directory:
```bash
cd backend/app/services
python test_prometheus_service.py
```

---

### Error: Missing requests module

**Output**:
```
ModuleNotFoundError: No module named 'requests'
```

**Solution**: Install dependencies:
```bash
pip install requests
```

Or install all project dependencies:
```bash
pip install -r requirements.txt
```

---

## Test Customization

### Change Prometheus URL

Edit `test_prometheus_service.py`:
```python
# Change this line
prometheus_url = "http://localhost:9090"

# To your custom URL
prometheus_url = "http://prometheus.monitoring.svc.cluster.local:9090"
```

### Test Specific Namespace

Modify the test to focus on a specific namespace:
```python
# In test_cpu_usage() function
cpu_metrics = service.get_cpu_usage(namespace="default")
```

### Test Specific Pod

Modify the test to focus on a specific pod:
```python
# In test_cpu_usage() function
cpu_metrics = service.get_cpu_usage(namespace="default", pod="my-app-123")
```

---

## Next Steps After Successful Test

1. ✅ Prometheus integration verified
2. 🔄 Integrate PrometheusService with MonitorService
3. 🔄 Enrich incidents with metrics
4. 🔄 Enhance AI diagnosis with metric context
5. 🔄 Add intelligent threshold detection

---

## Additional Resources

- **Main Documentation**: `PROMETHEUS_INTEGRATION.md`
- **Prometheus Setup**: `monitoring/prometheus/README.md`
- **Integration Guide**: `monitoring/prometheus/INTEGRATION_GUIDE.md`
- **PrometheusService Code**: `backend/app/services/prometheus_service.py`
