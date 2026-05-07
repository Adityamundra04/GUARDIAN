# 🚀 Guardian Demo Website - Quick Reference

One-page reference for common commands and workflows.

## 📦 Deployment

```bash
# Deploy everything
kubectl apply -f k8s/demo-website/

# Or individually
kubectl apply -f k8s/demo-website/deployment.yaml
kubectl apply -f k8s/demo-website/service.yaml
kubectl apply -f k8s/demo-website/configmap.yaml

# Using script
cd k8s/demo-website && ./deploy.sh
```

## 🔍 Verification

```bash
# Check pods
kubectl get pods -l app=guardian-demo

# Check service
kubectl get svc guardian-demo-website

# Check logs
kubectl logs -l app=guardian-demo

# Watch pods
kubectl get pods -w
```

## 🌐 Access

```bash
# Direct access (NodePort)
http://localhost:30080

# Port forward
kubectl port-forward svc/guardian-demo-website 8080:80
# Then: http://localhost:8080
```

## 🧪 Test Failures

```bash
# CrashLoopBackOff
kubectl apply -f k8s/demo-website/failure-crashloop.yaml

# ImagePullBackOff
kubectl apply -f k8s/demo-website/failure-imagepull.yaml

# Out of Memory
kubectl apply -f k8s/demo-website/failure-oom.yaml

# Interactive testing
cd k8s/demo-website && ./test-failures.sh
```

## 📊 Monitoring

```bash
# Guardian Dashboard
http://localhost:5173

# Guardian API
curl http://localhost:8000/health
curl http://localhost:8000/incidents | jq

# Prometheus
http://localhost:9090

# Grafana
http://localhost:3000
# Login: admin / admin
```

## 📝 Logs

```bash
# Guardian logs
tail -f logs/guardian.log

# AI analysis logs
tail -f logs/ai.log

# Remediation logs
tail -f logs/actions.log

# All logs
tail -f logs/*.log
```

## 🔍 Debugging

```bash
# Describe pod
kubectl describe pod -l app=guardian-demo

# Get pod events
kubectl get events --sort-by='.lastTimestamp'

# Check pod status
kubectl get pods -o wide

# Check resource usage
kubectl top pods
```

## 🧹 Cleanup

```bash
# Remove demo website
kubectl delete -f k8s/demo-website/

# Remove test pods
kubectl delete pod demo-crashloop-failure
kubectl delete pod demo-imagepull-failure
kubectl delete pod demo-oom-failure

# Using script
cd k8s/demo-website && ./cleanup.sh
```

## 📊 Prometheus Queries

```promql
# Pod status
kube_pod_status_phase{pod=~"guardian-demo.*"}

# Pod restarts
kube_pod_container_status_restarts_total{pod=~"guardian-demo.*"}

# CPU usage
rate(container_cpu_usage_seconds_total{pod=~"guardian-demo.*"}[5m])

# Memory usage
container_memory_usage_bytes{pod=~"guardian-demo.*"}
```

## 🎯 Common Workflows

### Deploy and Test CrashLoop

```bash
# 1. Deploy website
kubectl apply -f k8s/demo-website/

# 2. Verify healthy
kubectl get pods -l app=guardian-demo

# 3. Deploy failure
kubectl apply -f k8s/demo-website/failure-crashloop.yaml

# 4. Watch Guardian respond
kubectl get pods -w

# 5. Check dashboard
# http://localhost:5173

# 6. Cleanup
kubectl delete pod demo-crashloop-failure
```

### View Incident in API

```bash
# Get all incidents
curl http://localhost:8000/incidents | jq

# Get latest incident
curl http://localhost:8000/incidents | jq '.[0]'

# Get specific fields
curl http://localhost:8000/incidents | jq '.[0] | {pod: .pod_name, issue: .issue, ai_cause: .ai_root_cause}'
```

### Monitor in Real-Time

```bash
# Terminal 1: Watch pods
kubectl get pods -w

# Terminal 2: Guardian logs
tail -f logs/guardian.log

# Terminal 3: AI logs
tail -f logs/ai.log

# Browser: Dashboard
http://localhost:5173
```

## 🛠️ Troubleshooting

### Website Not Accessible

```bash
# Check pod status
kubectl get pods -l app=guardian-demo

# Check service
kubectl get svc guardian-demo-website

# Try port-forward
kubectl port-forward svc/guardian-demo-website 8080:80
```

### Guardian Not Detecting

```bash
# Check Guardian backend
curl http://localhost:8000/health

# Check Prometheus
curl http://localhost:9090/-/healthy

# Check monitoring logs
tail -f logs/monitoring.log
```

### Pod Stuck in Pending

```bash
# Check events
kubectl describe pod -l app=guardian-demo

# Check node resources
kubectl top nodes

# Check nodes
kubectl get nodes
```

## 📋 Resource Labels

All demo resources use these labels:

```yaml
labels:
  app: guardian-demo
  component: website
```

Filter commands:
```bash
kubectl get all -l app=guardian-demo
kubectl get pods -l app=guardian-demo
kubectl logs -l app=guardian-demo
```

## 🔗 URLs

| Service | URL | Credentials |
|---------|-----|-------------|
| Demo Website | http://localhost:30080 | - |
| Guardian Dashboard | http://localhost:5173 | - |
| Guardian API | http://localhost:8000 | - |
| Prometheus | http://localhost:9090 | - |
| Grafana | http://localhost:3000 | admin / admin |

## 📁 Files

| File | Purpose |
|------|---------|
| `deployment.yaml` | Main website deployment |
| `service.yaml` | NodePort service (30080) |
| `configmap.yaml` | HTML content |
| `failure-crashloop.yaml` | CrashLoop test |
| `failure-imagepull.yaml` | ImagePull test |
| `failure-oom.yaml` | OOM test |
| `deploy.sh` | Deployment script |
| `cleanup.sh` | Cleanup script |
| `test-failures.sh` | Interactive testing |

## 💡 Tips

- Use `-w` flag to watch resources in real-time
- Use `jq` to format JSON output
- Use `--tail=50` to limit log output
- Use `-f` to follow logs continuously
- Use `--ignore-not-found=true` for safe cleanup
- Check Guardian dashboard for visual feedback
- Monitor Grafana for metrics visualization

---

**Quick Start:**
```bash
cd k8s/demo-website
./deploy.sh
./test-failures.sh
```

**Quick Cleanup:**
```bash
cd k8s/demo-website
./cleanup.sh
```
