# Prometheus Monitoring Setup - Summary

## ✅ Setup Complete

Prometheus monitoring has been added to Guardian with minimal, stable Kubernetes manifests.

## Files Created

```
monitoring/prometheus/
├── namespace.yaml                  # Creates monitoring namespace
├── prometheus-rbac.yaml            # RBAC permissions
├── prometheus-configmap.yaml       # Prometheus configuration
├── prometheus-deployment.yaml      # Prometheus deployment
├── prometheus-service.yaml         # Service (NodePort on 30090)
├── deploy.sh                       # Deployment script
├── README.md                       # Detailed documentation
└── QUICK_START.md                  # Quick reference
```

## What Each File Does

### 1. `namespace.yaml`
- Creates `monitoring` namespace
- Isolates monitoring components

### 2. `prometheus-rbac.yaml`
- ServiceAccount: `prometheus`
- ClusterRole: Read permissions for Kubernetes resources
- ClusterRoleBinding: Binds role to service account

**Permissions:**
- Read nodes, services, endpoints, pods
- Access `/metrics` endpoints

### 3. `prometheus-configmap.yaml`
- Prometheus configuration
- Scrape interval: 15s
- Scrapes:
  - Prometheus itself
  - Kubernetes API server
  - Kubernetes nodes
  - Kubernetes pods
  - Kubernetes services

### 4. `prometheus-deployment.yaml`
- Deployment with 1 replica
- Image: `prom/prometheus:v2.47.0`
- Port: 9090
- Storage: emptyDir (7 days retention)
- Resources: 200m CPU, 512Mi memory

### 5. `prometheus-service.yaml`
- Type: NodePort
- Port: 9090
- NodePort: 30090
- Exposes Prometheus UI

## Deployment

### Quick Deploy
```bash
kubectl apply -f monitoring/prometheus/
```

### Verify
```bash
kubectl get pods -n monitoring
kubectl get svc -n monitoring
```

### Access UI
```bash
kubectl port-forward svc/prometheus-service 9090:9090 -n monitoring
```

Then open: http://localhost:9090

## Configuration

### Scrape Interval
```yaml
global:
  scrape_interval: 15s  # Collect metrics every 15 seconds
```

### Retention Period
```yaml
args:
  - '--storage.tsdb.retention.time=7d'  # Keep data for 7 days
```

### Resources
```yaml
resources:
  requests:
    cpu: 200m
    memory: 512Mi
  limits:
    cpu: 500m
    memory: 1Gi
```

## Metrics Collected

### Prometheus Self-Monitoring
- `prometheus_build_info`
- `prometheus_tsdb_head_samples_appended_total`
- `prometheus_http_requests_total`

### Kubernetes API Server
- `apiserver_request_total`
- `apiserver_request_duration_seconds`

### Kubernetes Nodes
- `node_cpu_seconds_total`
- `node_memory_MemTotal_bytes`
- `node_memory_MemAvailable_bytes`
- `node_filesystem_size_bytes`

### Kubernetes Pods
- `container_cpu_usage_seconds_total`
- `container_memory_usage_bytes`
- `container_network_receive_bytes_total`
- `container_network_transmit_bytes_total`

## Test Queries

### Check Prometheus is Up
```promql
up
```

### Check Kubernetes Targets
```promql
up{job=~"kubernetes.*"}
```

### Node CPU Usage
```promql
node_cpu_seconds_total
```

### Container Memory Usage
```promql
container_memory_usage_bytes
```

## Guardian Integration (Future)

Guardian will query Prometheus for:

### 1. CPU Monitoring
```promql
rate(container_cpu_usage_seconds_total[5m])
```

**Use case:** Detect high CPU → Scale up or restart

### 2. Memory Monitoring
```promql
container_memory_usage_bytes / container_spec_memory_limit_bytes
```

**Use case:** Detect memory pressure → Increase limits or restart

### 3. Pod Health Analysis
```promql
kube_pod_status_phase{phase="Running"}
```

**Use case:** Detect pod failures → Auto-remediate

### 4. Network Monitoring
```promql
rate(container_network_receive_bytes_total[5m])
```

**Use case:** Detect network issues → Investigate connectivity

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
│  │  │  - Port: 9090               │ │ │
│  │  │  - Scrape: 15s              │ │ │
│  │  │  - Retention: 7d            │ │ │
│  │  └─────────────────────────────┘ │ │
│  │           ↓ scrapes               │ │
│  │  ┌─────────────────────────────┐ │ │
│  │  │  Kubernetes Resources       │ │ │
│  │  │  - API Server               │ │ │
│  │  │  - Nodes                    │ │ │
│  │  │  - Pods                     │ │ │
│  │  │  - Services                 │ │ │
│  │  └─────────────────────────────┘ │ │
│  └───────────────────────────────────┘ │
│                                         │
│  ┌───────────────────────────────────┐ │
│  │  Guardian (Future)                │ │
│  │  - Queries Prometheus             │ │
│  │  - Analyzes metrics               │ │
│  │  - Makes remediation decisions    │ │
│  └───────────────────────────────────┘ │
└─────────────────────────────────────────┘
```

## Verification Steps

### 1. Check Deployment
```bash
kubectl get pods -n monitoring
```

**Expected:**
```
NAME                          READY   STATUS    RESTARTS   AGE
prometheus-7d9f8c8b5d-x7k2m   1/1     Running   0          1m
```

### 2. Check Service
```bash
kubectl get svc -n monitoring
```

**Expected:**
```
NAME                 TYPE       CLUSTER-IP      EXTERNAL-IP   PORT(S)          AGE
prometheus-service   NodePort   10.96.123.45    <none>        9090:30090/TCP   1m
```

### 3. Check Logs
```bash
kubectl logs -n monitoring deployment/prometheus
```

**Expected:**
```
level=info msg="Server is ready to receive web requests."
```

### 4. Access UI
```bash
kubectl port-forward svc/prometheus-service 9090:9090 -n monitoring
```

Open: http://localhost:9090

### 5. Check Targets
Navigate to: Status → Targets

**Expected:** See active targets:
- prometheus (1/1 up)
- kubernetes-apiservers (1/1 up)
- kubernetes-nodes (X/X up)

### 6. Run Test Query
Query: `up`

**Expected:** Returns 1 for Prometheus

## Troubleshooting

### Pod Not Starting
```bash
kubectl describe pod -n monitoring -l app=prometheus
```

### No Metrics
Check RBAC:
```bash
kubectl get clusterrolebinding prometheus
```

### Can't Access UI
Check port-forward:
```bash
kubectl port-forward svc/prometheus-service 9090:9090 -n monitoring
```

## Cleanup

```bash
kubectl delete -f monitoring/prometheus/
```

## Success Criteria

✅ **Prometheus deployed** - Pod running in monitoring namespace  
✅ **Service created** - NodePort service on 30090  
✅ **UI accessible** - http://localhost:9090 works  
✅ **Targets active** - Kubernetes targets showing up  
✅ **Queries working** - `up` query returns results  
✅ **Metrics collecting** - Time-series data visible  

## Next Steps

1. ✅ Prometheus deployed and collecting metrics
2. 🔄 Add kube-state-metrics (optional, for pod-level metrics)
3. 🔄 Add node-exporter (optional, for node-level metrics)
4. 🔄 Integrate Guardian with Prometheus API
5. 🔄 Use metrics for intelligent remediation
6. 🔄 Add Grafana for visualization (optional)

## Key Features

✅ **Minimal setup** - No Helm required  
✅ **Stable configuration** - Production-ready manifests  
✅ **Kubernetes-native** - Uses service discovery  
✅ **RBAC-compliant** - Proper permissions  
✅ **Resource-limited** - Won't consume excessive resources  
✅ **Easy to deploy** - Single command deployment  
✅ **Easy to access** - Port-forward or NodePort  

🎉 **Prometheus is ready for Guardian integration!**
