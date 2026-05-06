# Prometheus Monitoring Setup for Guardian

## Overview
This directory contains Kubernetes manifests to deploy Prometheus for monitoring the Guardian AI Ops system.

## Architecture

```
┌─────────────────────────────────────────┐
│         Kubernetes Cluster              │
│                                         │
│  ┌───────────────────────────────────┐ │
│  │  Monitoring Namespace             │ │
│  │                                   │ │
│  │  ┌─────────────────────────────┐ │ │
│  │  │  Prometheus                 │ │ │
│  │  │  - Scrapes metrics          │ │ │
│  │  │  - Stores time-series data  │ │ │
│  │  │  - Exposes UI on :9090      │ │ │
│  │  └─────────────────────────────┘ │ │
│  │                                   │ │
│  │  Scrapes:                         │ │
│  │  • Kubernetes API                 │ │
│  │  • Kubernetes Nodes               │ │
│  │  • Kubernetes Pods                │ │
│  │  • Kubernetes Services            │ │
│  └───────────────────────────────────┘ │
│                                         │
│  Guardian will later query Prometheus  │
│  for intelligent remediation decisions │
└─────────────────────────────────────────┘
```

## Files Explained

### 1. `namespace.yaml`
**Purpose:** Creates the `monitoring` namespace

**Content:**
- Namespace: `monitoring`

**Why:** Isolates monitoring components from application workloads

### 2. `prometheus-rbac.yaml`
**Purpose:** Sets up RBAC permissions for Prometheus

**Content:**
- ServiceAccount: `prometheus`
- ClusterRole: Permissions to read Kubernetes resources
- ClusterRoleBinding: Binds role to service account

**Why:** Prometheus needs permissions to discover and scrape Kubernetes resources

**Permissions:**
- Read nodes, services, endpoints, pods
- Read ingresses
- Access `/metrics` endpoints

### 3. `prometheus-configmap.yaml`
**Purpose:** Prometheus configuration

**Content:**
- Global settings (scrape interval: 15s)
- Scrape configs for:
  - Prometheus itself
  - Kubernetes API server
  - Kubernetes nodes
  - Kubernetes pods
  - Kubernetes services

**Why:** Defines what metrics to collect and how often

**Key Settings:**
- `scrape_interval: 15s` - Collect metrics every 15 seconds
- `evaluation_interval: 15s` - Evaluate rules every 15 seconds
- `retention: 7d` - Keep data for 7 days

### 4. `prometheus-deployment.yaml`
**Purpose:** Deploys Prometheus server

**Content:**
- Deployment with 1 replica
- Container: `prom/prometheus:v2.47.0`
- Volume mounts for config and storage
- Resource limits
- Health checks

**Why:** Runs the Prometheus server

**Key Settings:**
- Image: `prom/prometheus:v2.47.0` (stable version)
- Port: 9090
- Storage: emptyDir (ephemeral, for demo)
- Resources: 200m CPU, 512Mi memory (requests)
- Retention: 7 days

### 5. `prometheus-service.yaml`
**Purpose:** Exposes Prometheus UI

**Content:**
- Service type: NodePort
- Port: 9090
- NodePort: 30090

**Why:** Makes Prometheus accessible from outside the cluster

**Access:**
- Inside cluster: `http://prometheus-service.monitoring.svc.cluster.local:9090`
- Outside cluster: `http://<node-ip>:30090`
- Port-forward: `kubectl port-forward svc/prometheus-service 9090:9090 -n monitoring`

## Deployment Instructions

### Step 1: Create Namespace
```bash
kubectl apply -f monitoring/prometheus/namespace.yaml
```

**Expected Output:**
```
namespace/monitoring created
```

### Step 2: Create RBAC Resources
```bash
kubectl apply -f monitoring/prometheus/prometheus-rbac.yaml
```

**Expected Output:**
```
serviceaccount/prometheus created
clusterrole.rbac.authorization.k8s.io/prometheus created
clusterrolebinding.rbac.authorization.k8s.io/prometheus created
```

### Step 3: Create ConfigMap
```bash
kubectl apply -f monitoring/prometheus/prometheus-configmap.yaml
```

**Expected Output:**
```
configmap/prometheus-config created
```

### Step 4: Deploy Prometheus
```bash
kubectl apply -f monitoring/prometheus/prometheus-deployment.yaml
```

**Expected Output:**
```
deployment.apps/prometheus created
```

### Step 5: Create Service
```bash
kubectl apply -f monitoring/prometheus/prometheus-service.yaml
```

**Expected Output:**
```
service/prometheus-service created
```

### All-in-One Deployment
```bash
kubectl apply -f monitoring/prometheus/
```

## Verification

### Check Namespace
```bash
kubectl get namespace monitoring
```

**Expected Output:**
```
NAME         STATUS   AGE
monitoring   Active   1m
```

### Check Pods
```bash
kubectl get pods -n monitoring
```

**Expected Output:**
```
NAME                          READY   STATUS    RESTARTS   AGE
prometheus-7d9f8c8b5d-x7k2m   1/1     Running   0          1m
```

### Check Service
```bash
kubectl get svc -n monitoring
```

**Expected Output:**
```
NAME                 TYPE       CLUSTER-IP      EXTERNAL-IP   PORT(S)          AGE
prometheus-service   NodePort   10.96.123.45    <none>        9090:30090/TCP   1m
```

### Check Logs
```bash
kubectl logs -n monitoring deployment/prometheus
```

**Expected Output:**
```
level=info ts=... caller=main.go:... msg="Starting Prometheus"
level=info ts=... caller=main.go:... msg="Server is ready to receive web requests."
```

## Accessing Prometheus UI

### Method 1: Port Forward (Recommended for Development)
```bash
kubectl port-forward svc/prometheus-service 9090:9090 -n monitoring
```

Then open: http://localhost:9090

### Method 2: NodePort (If cluster has external access)
```bash
# Get node IP
kubectl get nodes -o wide

# Access Prometheus
# http://<node-ip>:30090
```

### Method 3: Inside Cluster
```bash
# From another pod
curl http://prometheus-service.monitoring.svc.cluster.local:9090/api/v1/query?query=up
```

## Testing Prometheus

### 1. Check Prometheus UI
Open http://localhost:9090 (after port-forward)

**Expected:** Prometheus web interface loads

### 2. Check Targets
Navigate to: Status → Targets

**Expected:** See scrape targets:
- prometheus (1/1 up)
- kubernetes-apiservers (1/1 up)
- kubernetes-nodes (X/X up)
- kubernetes-pods (X/X up)

### 3. Run Test Queries

#### Query 1: Check Prometheus is Up
```promql
up
```

**Expected:** Returns 1 for Prometheus itself

#### Query 2: Check Kubernetes Nodes
```promql
up{job="kubernetes-nodes"}
```

**Expected:** Returns 1 for each node

#### Query 3: Check All Targets
```promql
up{job=~"kubernetes.*"}
```

**Expected:** Returns metrics for all Kubernetes targets

#### Query 4: Node CPU Usage
```promql
node_cpu_seconds_total
```

**Expected:** Returns CPU metrics (if node-exporter is available)

#### Query 5: Pod Count
```promql
count(kube_pod_info)
```

**Expected:** Returns number of pods (if kube-state-metrics is available)

## Metrics Available

### Prometheus Self-Monitoring
- `prometheus_build_info` - Prometheus version
- `prometheus_tsdb_head_samples_appended_total` - Samples ingested
- `prometheus_http_requests_total` - HTTP requests

### Kubernetes API Server
- `apiserver_request_total` - API requests
- `apiserver_request_duration_seconds` - Request latency

### Kubernetes Nodes
- `node_cpu_seconds_total` - CPU usage
- `node_memory_MemTotal_bytes` - Total memory
- `node_memory_MemAvailable_bytes` - Available memory
- `node_filesystem_size_bytes` - Disk size
- `node_filesystem_avail_bytes` - Available disk

### Kubernetes Pods
- `container_cpu_usage_seconds_total` - Container CPU
- `container_memory_usage_bytes` - Container memory
- `container_network_receive_bytes_total` - Network RX
- `container_network_transmit_bytes_total` - Network TX

## Integration with Guardian

Guardian will later query Prometheus for:

### 1. CPU Monitoring
```promql
rate(container_cpu_usage_seconds_total[5m])
```

### 2. Memory Monitoring
```promql
container_memory_usage_bytes / container_spec_memory_limit_bytes
```

### 3. Pod Health Analysis
```promql
kube_pod_status_phase{phase="Running"}
```

### 4. Intelligent Remediation
- Detect high CPU → Scale up
- Detect high memory → Restart pod
- Detect pod failures → Auto-remediate

## Troubleshooting

### Issue: Pod not starting
**Check:**
```bash
kubectl describe pod -n monitoring -l app=prometheus
```

**Common causes:**
- Image pull error
- Insufficient resources
- ConfigMap not found

### Issue: No metrics showing
**Check:**
1. RBAC permissions
```bash
kubectl get clusterrolebinding prometheus
```

2. ConfigMap mounted
```bash
kubectl exec -n monitoring deployment/prometheus -- cat /etc/prometheus/prometheus.yml
```

3. Targets status in UI (Status → Targets)

### Issue: Can't access UI
**Check:**
1. Service exists
```bash
kubectl get svc -n monitoring
```

2. Port-forward working
```bash
kubectl port-forward svc/prometheus-service 9090:9090 -n monitoring
```

3. Pod is running
```bash
kubectl get pods -n monitoring
```

## Configuration Customization

### Change Scrape Interval
Edit `prometheus-configmap.yaml`:
```yaml
global:
  scrape_interval: 30s  # Change from 15s to 30s
```

### Change Retention Period
Edit `prometheus-deployment.yaml`:
```yaml
args:
  - '--storage.tsdb.retention.time=14d'  # Change from 7d to 14d
```

### Change Resource Limits
Edit `prometheus-deployment.yaml`:
```yaml
resources:
  requests:
    cpu: 500m      # Increase from 200m
    memory: 1Gi    # Increase from 512Mi
```

### Use Persistent Storage
Edit `prometheus-deployment.yaml`:
```yaml
volumes:
  - name: prometheus-storage
    persistentVolumeClaim:
      claimName: prometheus-pvc  # Replace emptyDir
```

## Cleanup

### Remove Prometheus
```bash
kubectl delete -f monitoring/prometheus/
```

### Remove Namespace
```bash
kubectl delete namespace monitoring
```

## Next Steps

1. ✅ Prometheus deployed and collecting metrics
2. 🔄 Add kube-state-metrics (optional, for pod-level metrics)
3. 🔄 Add node-exporter (optional, for node-level metrics)
4. 🔄 Integrate Guardian with Prometheus API
5. 🔄 Add Grafana for visualization (optional)

## Success Criteria

✅ **Prometheus UI accessible** - http://localhost:9090  
✅ **Targets showing up** - Status → Targets shows Kubernetes targets  
✅ **Queries working** - `up` query returns results  
✅ **Metrics collecting** - Time-series data visible in graphs  

🎉 **Prometheus is ready for Guardian integration!**
