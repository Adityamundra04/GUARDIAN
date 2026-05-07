# 🌐 Guardian Demo Website

A simple Kubernetes-deployed website for testing Guardian's AI-powered monitoring and autonomous remediation capabilities.

## 📋 Overview

This demo website provides a **real-world Kubernetes deployment** that Guardian can monitor, detect failures in, and automatically remediate. It includes:

- ✅ **Working deployment** - Healthy nginx-based website
- ❌ **Failure scenarios** - Pre-configured pod failures for testing
- 🛡️ **Guardian integration** - Monitored by Prometheus and Guardian AI
- 🎨 **Modern UI** - Futuristic design showing Guardian branding

## 🏗️ Architecture

```
┌─────────────────────────────────────────┐
│         Kubernetes Cluster              │
│                                         │
│  ┌───────────────────────────────────┐ │
│  │  guardian-demo-website            │ │
│  │  (Deployment)                     │ │
│  │                                   │ │
│  │  ┌─────────────────────────────┐ │ │
│  │  │  nginx:1.25-alpine          │ │ │
│  │  │  Port: 80                   │ │ │
│  │  │  HTML from ConfigMap        │ │ │
│  │  └─────────────────────────────┘ │ │
│  └───────────────────────────────────┘ │
│                  │                      │
│                  ▼                      │
│  ┌───────────────────────────────────┐ │
│  │  Service (NodePort 30080)         │ │
│  └───────────────────────────────────┘ │
│                                         │
└─────────────────────────────────────────┘
                  │
                  ▼
        ┌─────────────────────┐
        │  Guardian Monitors  │
        │  - Prometheus       │
        │  - AI Engine        │
        │  - Remediation      │
        └─────────────────────┘
```

## 📁 Files

| File | Purpose |
|------|---------|
| `deployment.yaml` | Main website deployment with nginx |
| `service.yaml` | NodePort service exposing port 30080 |
| `configmap.yaml` | HTML content for the website |
| `failure-crashloop.yaml` | CrashLoopBackOff test scenario |
| `failure-imagepull.yaml` | ImagePullBackOff test scenario |
| `failure-oom.yaml` | Out of Memory (OOM) test scenario |

## 🚀 Quick Start

### 1. Deploy the Website

```bash
# Deploy all components
kubectl apply -f k8s/demo-website/deployment.yaml
kubectl apply -f k8s/demo-website/service.yaml
kubectl apply -f k8s/demo-website/configmap.yaml

# Or deploy everything at once
kubectl apply -f k8s/demo-website/
```

### 2. Verify Deployment

```bash
# Check pod status
kubectl get pods -l app=guardian-demo

# Check service
kubectl get svc guardian-demo-website

# Watch pod startup
kubectl get pods -l app=guardian-demo -w
```

Expected output:
```
NAME                                      READY   STATUS    RESTARTS   AGE
guardian-demo-website-xxxxxxxxxx-xxxxx    1/1     Running   0          30s
```

### 3. Access the Website

The website is exposed via NodePort on port **30080**.

**Option A: Direct Access (Docker Desktop / Minikube)**
```bash
# Open in browser
http://localhost:30080
```

**Option B: Port Forward**
```bash
# Forward to local port 8080
kubectl port-forward svc/guardian-demo-website 8080:80

# Open in browser
http://localhost:8080
```

### 4. View Logs

```bash
# View pod logs
kubectl logs -l app=guardian-demo --tail=50

# Follow logs in real-time
kubectl logs -l app=guardian-demo -f
```

## 🧪 Testing Guardian with Failure Scenarios

Guardian's AI monitoring and remediation can be tested using pre-configured failure scenarios.

### Scenario 1: CrashLoopBackOff

**What it tests:** Pod repeatedly crashes and restarts

```bash
# Deploy crashloop failure
kubectl apply -f k8s/demo-website/failure-crashloop.yaml

# Watch Guardian detect and remediate
kubectl get pods -w

# Check Guardian logs
kubectl logs -l app=guardian -n monitoring

# View incident in Guardian dashboard
# http://localhost:5173
```

**Expected Guardian behavior:**
1. ✅ Detects pod in CrashLoopBackOff state
2. ✅ Collects pod logs and metrics
3. ✅ AI analyzes crash reason
4. ✅ Suggests remediation (restart, rollback, or scale)
5. ✅ Executes remediation action
6. ✅ Displays incident in dashboard

**Cleanup:**
```bash
kubectl delete pod demo-crashloop-failure
```

### Scenario 2: ImagePullBackOff

**What it tests:** Pod fails to pull container image

```bash
# Deploy imagepull failure
kubectl apply -f k8s/demo-website/failure-imagepull.yaml

# Watch Guardian detect issue
kubectl get pods -w

# Check Guardian AI diagnosis
# Dashboard will show: "Image not found" or "Invalid image tag"
```

**Expected Guardian behavior:**
1. ✅ Detects ImagePullBackOff state
2. ✅ AI identifies invalid image tag
3. ✅ Suggests fix: update image or check registry
4. ✅ Logs incident with diagnosis

**Cleanup:**
```bash
kubectl delete pod demo-imagepull-failure
```

### Scenario 3: Out of Memory (OOM)

**What it tests:** Pod exceeds memory limits and gets killed

```bash
# Deploy OOM failure
kubectl apply -f k8s/demo-website/failure-oom.yaml

# Watch pod get OOMKilled
kubectl get pods -w

# Check Guardian remediation
# Dashboard will show memory limit issue
```

**Expected Guardian behavior:**
1. ✅ Detects OOMKilled status
2. ✅ Analyzes memory usage metrics
3. ✅ AI suggests: increase memory limits
4. ✅ May attempt pod restart
5. ✅ Logs resource constraint issue

**Cleanup:**
```bash
kubectl delete pod demo-oom-failure
```

## 🔍 End-to-End Testing Workflow

Complete workflow demonstrating Guardian's autonomous capabilities:

### Step 1: Ensure Guardian is Running

```bash
# Check Guardian backend
curl http://localhost:8000/health

# Check Prometheus
curl http://localhost:9090/-/healthy

# Check frontend
# Open http://localhost:5173
```

### Step 2: Deploy Healthy Website

```bash
kubectl apply -f k8s/demo-website/deployment.yaml
kubectl apply -f k8s/demo-website/service.yaml
kubectl apply -f k8s/demo-website/configmap.yaml

# Verify healthy state
kubectl get pods -l app=guardian-demo
```

### Step 3: Introduce Failure

```bash
# Choose a failure scenario
kubectl apply -f k8s/demo-website/failure-crashloop.yaml

# Watch in real-time
kubectl get pods -w
```

### Step 4: Observe Guardian Response

**In Terminal:**
```bash
# Watch Guardian logs
tail -f logs/guardian.log

# Watch AI analysis
tail -f logs/ai.log

# Watch remediation actions
tail -f logs/actions.log
```

**In Dashboard (http://localhost:5173):**
- ✅ New incident appears
- ✅ AI diagnosis displayed
- ✅ Remediation action shown
- ✅ Status updates in real-time

**In Grafana (http://localhost:3000):**
- ✅ Pod restart count increases
- ✅ Pod status changes visualized
- ✅ Metrics show anomaly

### Step 5: Verify Remediation

```bash
# Check if Guardian fixed the issue
kubectl get pods

# View incident history
curl http://localhost:8000/incidents | jq
```

### Step 6: Cleanup

```bash
# Remove failure pod
kubectl delete pod demo-crashloop-failure

# Or remove all demo resources
kubectl delete -f k8s/demo-website/
```

## 📊 Monitoring Integration

### Prometheus Metrics

The demo website exposes standard Kubernetes metrics:

```promql
# Pod CPU usage
container_cpu_usage_seconds_total{pod=~"guardian-demo.*"}

# Pod memory usage
container_memory_usage_bytes{pod=~"guardian-demo.*"}

# Pod restart count
kube_pod_container_status_restarts_total{pod=~"guardian-demo.*"}

# Pod status
kube_pod_status_phase{pod=~"guardian-demo.*"}
```

### Grafana Dashboards

View demo website metrics in Grafana:

1. Open Grafana: http://localhost:3000
2. Login: admin / admin
3. Navigate to: **Kubernetes Monitoring Dashboard**
4. Filter by: `app=guardian-demo`

## 🛠️ Troubleshooting

### Website Not Accessible

**Problem:** Cannot access http://localhost:30080

**Solutions:**
```bash
# Check if pod is running
kubectl get pods -l app=guardian-demo

# Check service
kubectl get svc guardian-demo-website

# Check NodePort
kubectl describe svc guardian-demo-website | grep NodePort

# Try port-forward instead
kubectl port-forward svc/guardian-demo-website 8080:80
# Then access: http://localhost:8080
```

### Pod Stuck in Pending

**Problem:** Pod shows `Pending` status

**Solutions:**
```bash
# Check pod events
kubectl describe pod -l app=guardian-demo

# Check node resources
kubectl top nodes

# Check if nodes are ready
kubectl get nodes
```

### ConfigMap Not Loading

**Problem:** Website shows nginx default page

**Solutions:**
```bash
# Verify ConfigMap exists
kubectl get configmap guardian-demo-html

# Check ConfigMap content
kubectl describe configmap guardian-demo-html

# Restart pod to reload ConfigMap
kubectl rollout restart deployment guardian-demo-website
```

### Guardian Not Detecting Failures

**Problem:** Failures not appearing in Guardian dashboard

**Solutions:**
```bash
# Check Guardian backend is running
curl http://localhost:8000/health

# Check Prometheus is scraping metrics
curl http://localhost:9090/api/v1/targets

# Check Guardian monitoring service
kubectl logs -l app=guardian -n monitoring

# Verify failure pod is actually failing
kubectl get pods
kubectl describe pod demo-crashloop-failure
```

## 🧹 Cleanup

### Remove Demo Website Only

```bash
kubectl delete -f k8s/demo-website/deployment.yaml
kubectl delete -f k8s/demo-website/service.yaml
kubectl delete -f k8s/demo-website/configmap.yaml
```

### Remove All Demo Resources

```bash
# Delete all demo website resources
kubectl delete -f k8s/demo-website/

# Verify cleanup
kubectl get all -l app=guardian-demo
```

### Remove Failure Test Pods

```bash
kubectl delete pod demo-crashloop-failure
kubectl delete pod demo-imagepull-failure
kubectl delete pod demo-oom-failure
```

## 📝 Configuration Details

### Resource Limits

The demo website uses minimal resources:

```yaml
resources:
  requests:
    memory: "64Mi"
    cpu: "100m"
  limits:
    memory: "128Mi"
    cpu: "200m"
```

### Health Checks

Liveness and readiness probes ensure pod health:

```yaml
livenessProbe:
  httpGet:
    path: /
    port: 80
  initialDelaySeconds: 10
  periodSeconds: 10

readinessProbe:
  httpGet:
    path: /
    port: 80
  initialDelaySeconds: 5
  periodSeconds: 5
```

### Labels

All resources use consistent labels:

```yaml
labels:
  app: guardian-demo
  component: website
```

## 🎯 Use Cases

### 1. Demo Guardian Capabilities
- Show AI-powered monitoring
- Demonstrate autonomous remediation
- Visualize incident response

### 2. Test Failure Scenarios
- Validate Guardian detection
- Test AI diagnosis accuracy
- Verify remediation actions

### 3. Training and Education
- Learn Kubernetes concepts
- Understand pod lifecycle
- Practice troubleshooting

### 4. Development Testing
- Test Guardian features
- Validate monitoring integration
- Debug remediation logic

## 🔗 Related Documentation

- [Main README](../../README.md) - Complete Guardian documentation
- [Prometheus Setup](../../monitoring/prometheus/README.md) - Metrics collection
- [Grafana Setup](../../monitoring/grafana/README.md) - Visualization dashboards
- [Demo Guide](../../DEMO_GUIDE.md) - Complete demo walkthrough

## 📄 License

Part of the Guardian project - MIT License

---

**Created by:** Aaditya  
**Project:** Guardian - AI-Powered Kubernetes Observability
