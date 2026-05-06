# Grafana Quick Reference - Guardian AI Ops

## 🚀 Quick Deploy

```bash
cd monitoring/grafana
chmod +x deploy.sh verify.sh
bash deploy.sh
```

## 🌐 Access Grafana

**NodePort:** http://localhost:30000  
**Port Forward:**
```bash
kubectl port-forward svc/grafana-service 3000:3000 -n monitoring
# Then: http://localhost:3000
```

**Credentials:** `admin` / `admin`

## 📊 Pre-configured Dashboards

1. **Kubernetes Monitoring Dashboard**
   - Pod CPU Usage
   - Pod Memory Usage
   - Pod Restart Count
   - Pod Status
   - Cluster Health

2. **Guardian AI Ops Dashboard**
   - Active Incidents
   - Remediation Events
   - Monitoring Activity
   - AI Diagnosis Activity
   - Incident Rate Over Time
   - Top Pods by Restart Count

## 🔧 Common Commands

### Check Status
```bash
kubectl get pods -n monitoring -l app=grafana
kubectl get svc -n monitoring grafana-service
```

### View Logs
```bash
kubectl logs -n monitoring -l app=grafana -f
```

### Restart Grafana
```bash
kubectl delete pod -n monitoring -l app=grafana
```

### Verify Setup
```bash
bash verify.sh
```

## 🧪 Test Prometheus Connection

```bash
GRAFANA_POD=$(kubectl get pods -n monitoring -l app=grafana -o jsonpath='{.items[0].metadata.name}')
kubectl exec -n monitoring $GRAFANA_POD -- wget -O- http://prometheus-service:9090/api/v1/query?query=up
```

## 🗑️ Cleanup

```bash
kubectl delete -f grafana-service.yaml
kubectl delete -f grafana-deployment.yaml
kubectl delete -f grafana-dashboard-config.yaml
kubectl delete -f grafana-datasource-config.yaml
```

## 🔍 Troubleshooting

**Pod not starting:**
```bash
kubectl describe pod -n monitoring -l app=grafana
kubectl logs -n monitoring -l app=grafana
```

**No data in dashboards:**
- Check Prometheus: http://localhost:30090
- Verify datasource in Grafana UI
- Wait a few minutes for metrics to populate

**Cannot access UI:**
- Verify service: `kubectl get svc -n monitoring grafana-service`
- Check pod status: `kubectl get pods -n monitoring -l app=grafana`
- Try port-forward instead of NodePort

## 📁 File Structure

```
monitoring/grafana/
├── grafana-deployment.yaml           # Main deployment
├── grafana-service.yaml              # NodePort service (30000)
├── grafana-datasource-config.yaml    # Prometheus datasource
├── grafana-dashboard-config.yaml     # Dashboard provisioning
├── dashboards/
│   ├── kubernetes-monitoring.json    # K8s dashboard
│   └── guardian-monitoring.json      # Guardian dashboard
├── deploy.sh                         # Deployment script
├── verify.sh                         # Verification script
├── README.md                         # Full documentation
├── SETUP_GUIDE.md                    # Step-by-step guide
└── QUICK_REFERENCE.md                # This file
```

## 🎯 Architecture

```
Kubernetes → Prometheus (scrape) → Grafana (visualize) → Guardian AI
```

## ✅ Success Checklist

- [ ] Grafana pod running
- [ ] UI accessible at http://localhost:30000
- [ ] Login successful (admin/admin)
- [ ] Prometheus datasource connected
- [ ] Both dashboards visible
- [ ] Dashboards showing live data
- [ ] Auto-refresh working (5s interval)

---

**For detailed instructions, see:** `SETUP_GUIDE.md`  
**For full documentation, see:** `README.md`
