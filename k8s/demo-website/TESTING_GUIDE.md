# 🧪 Guardian Demo Website - Complete Testing Guide

This guide walks you through testing Guardian's AI-powered monitoring and autonomous remediation using the demo website.

## 📋 Prerequisites

Before starting, ensure the following are running:

### 1. Kubernetes Cluster
```bash
kubectl cluster-info
kubectl get nodes
```

### 2. Guardian Backend
```bash
curl http://localhost:8000/health
```

Expected response:
```json
{
  "status": "healthy",
  "monitoring": "active"
}
```

### 3. Prometheus
```bash
curl http://localhost:9090/-/healthy
```

### 4. Guardian Frontend
Open browser: http://localhost:5173

### 5. Grafana (Optional)
Open browser: http://localhost:3000  
Login: admin / admin

---

## 🚀 Part 1: Deploy Healthy Website

### Step 1: Deploy the Demo Website

```bash
# Navigate to demo website directory
cd k8s/demo-website

# Deploy all resources
kubectl apply -f deployment.yaml
kubectl apply -f service.yaml
kubectl apply -f configmap.yaml

# Or use the deployment script
./deploy.sh
```

### Step 2: Verify Deployment

```bash
# Check pod status (should be Running)
kubectl get pods -l app=guardian-demo

# Expected output:
# NAME                                      READY   STATUS    RESTARTS   AGE
# guardian-demo-website-xxxxxxxxxx-xxxxx    1/1     Running   0          30s
```

### Step 3: Access the Website

Open browser: http://localhost:30080

You should see:
- 🛡️ Guardian Demo branding
- Futuristic purple gradient design
- "System Operational" status
- Pod information

### Step 4: Verify Monitoring

**Check Prometheus is scraping metrics:**
```bash
# Open Prometheus
http://localhost:9090

# Run query:
kube_pod_status_phase{pod=~"guardian-demo.*"}
```

**Check Grafana dashboard:**
```bash
# Open Grafana
http://localhost:3000

# Navigate to: Kubernetes Monitoring Dashboard
# Filter by: app=guardian-demo
```

---

## 🔴 Part 2: Test Failure Scenarios

### Test 1: CrashLoopBackOff

**What it tests:** Pod that repeatedly crashes and restarts

#### Deploy the Failure

```bash
kubectl apply -f failure-crashloop.yaml
```

#### Watch the Failure

```bash
# Watch pod status in real-time
kubectl get pods -w

# You should see:
# demo-crashloop-failure   0/1   CrashLoopBackOff   3   2m
```

#### Observe Guardian Response

**Terminal 1 - Watch Guardian logs:**
```bash
tail -f logs/guardian.log
```

**Terminal 2 - Watch AI analysis:**
```bash
tail -f logs/ai.log
```

**Terminal 3 - Watch remediation:**
```bash
tail -f logs/actions.log
```

**Browser - Guardian Dashboard:**
```
http://localhost:5173
```

Expected to see:
- ✅ New incident appears
- ✅ Status: "CrashLoopBackOff"
- ✅ AI Diagnosis: "Container exits with error code 1"
- ✅ AI Solution: "Check application logs, restart pod, or rollback"
- ✅ Action Taken: "restart_pod" or "rollback_release"
- ✅ Action Status: "pending" → "completed"

#### Check Pod Logs

```bash
# View crash logs
kubectl logs demo-crashloop-failure

# Expected output:
# Starting application...
# Application crashed!
```

#### Verify Guardian API

```bash
# Get all incidents
curl http://localhost:8000/incidents | jq

# Expected response includes:
# {
#   "id": "...",
#   "pod_name": "demo-crashloop-failure",
#   "namespace": "default",
#   "issue": "CrashLoopBackOff",
#   "status": "detected",
#   "ai_root_cause": "Container exits with error code 1",
#   "ai_solution": "...",
#   "action_taken": "restart_pod",
#   "action_status": "completed"
# }
```

#### Cleanup

```bash
kubectl delete pod demo-crashloop-failure
```

---

### Test 2: ImagePullBackOff

**What it tests:** Pod fails to pull non-existent container image

#### Deploy the Failure

```bash
kubectl apply -f failure-imagepull.yaml
```

#### Watch the Failure

```bash
kubectl get pods -w

# You should see:
# demo-imagepull-failure   0/1   ImagePullBackOff   0   1m
```

#### Observe Guardian Response

**Guardian Dashboard (http://localhost:5173):**

Expected to see:
- ✅ New incident: "demo-imagepull-failure"
- ✅ Status: "ImagePullBackOff"
- ✅ AI Diagnosis: "Image tag does not exist" or "Invalid image reference"
- ✅ AI Solution: "Update image tag to valid version" or "Check container registry"
- ✅ Action: May suggest manual intervention

#### Check Pod Events

```bash
kubectl describe pod demo-imagepull-failure

# Look for events:
# Failed to pull image "nginx:this-tag-does-not-exist-12345"
# Error: manifest unknown
```

#### Verify in Grafana

```bash
# Open Grafana: http://localhost:3000
# Navigate to: Kubernetes Monitoring Dashboard
# Check: Pod Status panel
# Should show: ImagePullBackOff state
```

#### Cleanup

```bash
kubectl delete pod demo-imagepull-failure
```

---

### Test 3: Out of Memory (OOM)

**What it tests:** Pod exceeds memory limits and gets killed

#### Deploy the Failure

```bash
kubectl apply -f failure-oom.yaml
```

#### Watch the Failure

```bash
kubectl get pods -w

# You should see:
# demo-oom-failure   0/1   OOMKilled   1   30s
# demo-oom-failure   0/1   CrashLoopBackOff   1   35s
```

#### Observe Guardian Response

**Guardian Dashboard:**

Expected to see:
- ✅ New incident: "demo-oom-failure"
- ✅ Status: "OOMKilled" or "CrashLoopBackOff"
- ✅ AI Diagnosis: "Container exceeded memory limit"
- ✅ AI Solution: "Increase memory limits" or "Optimize application memory usage"
- ✅ Action: May attempt restart or suggest configuration change

#### Check Memory Metrics

**Prometheus query:**
```promql
container_memory_usage_bytes{pod="demo-oom-failure"}
```

**Grafana:**
- Navigate to: Kubernetes Monitoring Dashboard
- Check: Memory Usage panel
- Should show: Memory spike before OOMKill

#### Check Pod Status

```bash
kubectl describe pod demo-oom-failure

# Look for:
# Last State: Terminated
# Reason: OOMKilled
# Exit Code: 137
```

#### Cleanup

```bash
kubectl delete pod demo-oom-failure
```

---

## 🎯 Part 3: End-to-End Workflow Test

Complete workflow demonstrating Guardian's full capabilities.

### Step 1: Clean Slate

```bash
# Remove any existing test pods
kubectl delete pod demo-crashloop-failure --ignore-not-found
kubectl delete pod demo-imagepull-failure --ignore-not-found
kubectl delete pod demo-oom-failure --ignore-not-found

# Verify clean state
kubectl get pods -l app=guardian-demo
```

### Step 2: Open Monitoring Interfaces

**Terminal 1 - Guardian logs:**
```bash
tail -f logs/guardian.log
```

**Terminal 2 - AI logs:**
```bash
tail -f logs/ai.log
```

**Terminal 3 - Action logs:**
```bash
tail -f logs/actions.log
```

**Browser Tab 1 - Guardian Dashboard:**
```
http://localhost:5173
```

**Browser Tab 2 - Grafana:**
```
http://localhost:3000
```

### Step 3: Introduce Failure

```bash
# Deploy crashloop failure
kubectl apply -f failure-crashloop.yaml

# Watch in real-time
kubectl get pods -w
```

### Step 4: Observe Complete Flow

**Expected Timeline:**

**T+0s:** Pod deployed
```
demo-crashloop-failure   0/1   Pending   0   0s
```

**T+5s:** Pod starts and crashes
```
demo-crashloop-failure   0/1   Error   0   5s
```

**T+10s:** Guardian detects issue
```
[Guardian Log] Detected pod failure: demo-crashloop-failure
[Guardian Log] Status: CrashLoopBackOff
```

**T+15s:** AI analyzes the issue
```
[AI Log] Analyzing pod: demo-crashloop-failure
[AI Log] Collecting logs and metrics...
[AI Log] Root cause: Container exits with error code 1
[AI Log] Solution: Restart pod or check application logs
```

**T+20s:** Remediation action executed
```
[Action Log] Executing action: restart_pod
[Action Log] Target: demo-crashloop-failure
[Action Log] Status: in_progress
```

**T+25s:** Dashboard updates
```
[Dashboard] New incident visible
[Dashboard] AI diagnosis displayed
[Dashboard] Remediation action shown
```

**T+30s:** Action completes
```
[Action Log] Action completed successfully
[Dashboard] Status updated to: resolved
```

### Step 5: Verify Results

**Check incident in API:**
```bash
curl http://localhost:8000/incidents | jq '.[0]'
```

**Check Grafana metrics:**
- Pod restart count increased
- Incident timeline visible

**Check Guardian dashboard:**
- Incident card shows complete flow
- AI diagnosis visible
- Remediation action logged

### Step 6: Cleanup

```bash
kubectl delete pod demo-crashloop-failure
```

---

## 📊 Part 4: Metrics Validation

### Prometheus Queries

Test these queries in Prometheus (http://localhost:9090):

**1. Pod Status:**
```promql
kube_pod_status_phase{pod=~"guardian-demo.*"}
```

**2. Pod Restarts:**
```promql
kube_pod_container_status_restarts_total{pod=~"guardian-demo.*"}
```

**3. CPU Usage:**
```promql
rate(container_cpu_usage_seconds_total{pod=~"guardian-demo.*"}[5m])
```

**4. Memory Usage:**
```promql
container_memory_usage_bytes{pod=~"guardian-demo.*"}
```

### Grafana Dashboards

**Kubernetes Monitoring Dashboard:**
- Pod count: Should show guardian-demo pods
- CPU usage: Should show resource consumption
- Memory usage: Should show memory trends
- Restart count: Should increase during failure tests

**Guardian AI Ops Dashboard:**
- Active incidents: Should show current failures
- Remediation events: Should show actions taken
- AI activity: Should show diagnosis events

---

## 🧪 Part 5: Automated Testing

Use the provided test script for automated testing:

```bash
# Run interactive test menu
./test-failures.sh

# Options:
# 1) CrashLoopBackOff test
# 2) ImagePullBackOff test
# 3) Out of Memory test
# 4) Run all scenarios
# 5) Cleanup all test pods
```

---

## ✅ Success Criteria Checklist

After completing all tests, verify:

### Detection
- [ ] Guardian detects pod failures within 30 seconds
- [ ] Failures appear in Guardian dashboard
- [ ] Prometheus metrics show anomalies
- [ ] Grafana dashboards update

### AI Analysis
- [ ] AI analyzes pod logs
- [ ] AI analyzes metrics
- [ ] AI provides root cause diagnosis
- [ ] AI suggests remediation actions

### Remediation
- [ ] Guardian executes remediation actions
- [ ] Actions are logged
- [ ] Action status updates (pending → completed)
- [ ] Incidents are tracked

### Visualization
- [ ] Dashboard shows incidents in real-time
- [ ] AI diagnosis is visible
- [ ] Remediation actions are displayed
- [ ] Status updates automatically

### API
- [ ] `/health` endpoint returns healthy status
- [ ] `/incidents` endpoint returns incident list
- [ ] Incident data includes AI analysis
- [ ] Incident data includes remediation info

---

## 🛠️ Troubleshooting

### Guardian Not Detecting Failures

**Problem:** Failures don't appear in dashboard

**Check:**
```bash
# 1. Guardian backend running?
curl http://localhost:8000/health

# 2. Prometheus scraping?
curl http://localhost:9090/api/v1/targets

# 3. Monitoring service running?
kubectl logs -l app=guardian -n monitoring

# 4. Pod actually failing?
kubectl get pods
kubectl describe pod demo-crashloop-failure
```

### AI Analysis Not Appearing

**Problem:** No AI diagnosis in dashboard

**Check:**
```bash
# 1. Ollama running?
curl http://localhost:11434/api/tags

# 2. AI service logs
tail -f logs/ai.log

# 3. Check for errors
tail -f logs/errors.log
```

### Dashboard Not Updating

**Problem:** Dashboard shows stale data

**Solutions:**
```bash
# 1. Check frontend is running
# Browser: http://localhost:5173

# 2. Check API connection
# Browser console: Check for API errors

# 3. Restart frontend
cd frontend
npm run dev
```

### Metrics Not Visible in Grafana

**Problem:** Grafana shows no data

**Check:**
```bash
# 1. Prometheus datasource configured?
# Grafana → Configuration → Data Sources

# 2. Prometheus accessible?
kubectl port-forward svc/prometheus-service 9090:9090 -n monitoring

# 3. Metrics exist?
# Prometheus: http://localhost:9090
# Query: kube_pod_status_phase
```

---

## 🧹 Complete Cleanup

After testing, clean up all resources:

```bash
# Remove demo website
kubectl delete -f deployment.yaml
kubectl delete -f service.yaml
kubectl delete -f configmap.yaml

# Remove test pods
kubectl delete pod demo-crashloop-failure --ignore-not-found
kubectl delete pod demo-imagepull-failure --ignore-not-found
kubectl delete pod demo-oom-failure --ignore-not-found

# Or use cleanup script
./cleanup.sh

# Verify cleanup
kubectl get all -l app=guardian-demo
```

---

## 📚 Additional Resources

- [Demo Website README](README.md) - Complete documentation
- [Main Guardian README](../../README.md) - Project overview
- [Demo Guide](../../DEMO_GUIDE.md) - Presentation guide
- [Prometheus Setup](../../monitoring/prometheus/README.md) - Metrics setup
- [Grafana Setup](../../monitoring/grafana/README.md) - Dashboard setup

---

**Happy Testing! 🎉**

If you encounter issues, check the troubleshooting section or review the Guardian logs.
