# Grafana Deployment Checklist

Use this checklist to ensure successful Grafana deployment for Guardian AI Ops.

## Pre-Deployment Checklist

- [ ] Kubernetes cluster is running
- [ ] `kubectl` is installed and configured
- [ ] Can run: `kubectl get nodes` successfully
- [ ] Prometheus is deployed in `monitoring` namespace
- [ ] Can access Prometheus UI at http://localhost:30090
- [ ] Terminal has bash support (Linux/Mac/WSL/Git Bash)

## Deployment Steps

- [ ] Navigate to grafana directory: `cd monitoring/grafana`
- [ ] Make scripts executable: `chmod +x deploy.sh verify.sh` (Linux/Mac only)
- [ ] Run deployment: `bash deploy.sh`
- [ ] Wait for "Deployment Complete!" message
- [ ] Note the access URL and credentials

## Post-Deployment Verification

- [ ] Run verification script: `bash verify.sh`
- [ ] All checks show ✅ (green checkmarks)
- [ ] Grafana pod status is "Running"
- [ ] Grafana pod is "Ready"
- [ ] Grafana service exists with NodePort 30000
- [ ] Prometheus service exists (datasource)
- [ ] ConfigMaps exist (datasources and dashboards)
- [ ] HTTP endpoint responds

## Access Verification

- [ ] Open browser to http://localhost:30000
- [ ] Grafana login page loads
- [ ] Can login with admin/admin
- [ ] (Optional) Change password or skip
- [ ] Grafana home page loads successfully

## Dashboard Verification

- [ ] Click Dashboards icon (four squares) in left sidebar
- [ ] See "Kubernetes Monitoring Dashboard" in list
- [ ] See "Guardian AI Ops Dashboard" in list
- [ ] Click "Kubernetes Monitoring Dashboard"
- [ ] Dashboard loads without errors
- [ ] Panels show data (not "No data")
- [ ] Click "Guardian AI Ops Dashboard"
- [ ] Dashboard loads without errors
- [ ] Panels show data or placeholders

## Datasource Verification

- [ ] Click Configuration (gear icon) in left sidebar
- [ ] Click "Data Sources"
- [ ] See "Prometheus" listed as default
- [ ] Click "Prometheus"
- [ ] URL shows: http://prometheus-service:9090
- [ ] Scroll down and click "Save & Test"
- [ ] See green message: "Data source is working"

## Functionality Testing

- [ ] Dashboard auto-refreshes every 5 seconds
- [ ] Time range selector works (top right)
- [ ] Refresh interval selector works (top right)
- [ ] Can zoom in/out on time series graphs
- [ ] Hover over graphs shows tooltips
- [ ] Gauges display current values
- [ ] No error messages in browser console

## Optional: Create Test Incident

- [ ] Deploy crashloop pod: `kubectl apply -f ../../k8s/test-failures/crashloop.yaml`
- [ ] Wait 30 seconds
- [ ] Refresh Guardian AI Ops Dashboard
- [ ] See incident count increase
- [ ] See pod appear in "Top Pods by Restart Count"
- [ ] Clean up: `kubectl delete -f ../../k8s/test-failures/crashloop.yaml`

## Troubleshooting (If Issues)

If any checks fail, try these steps:

### Grafana Pod Not Running
- [ ] Check pod status: `kubectl describe pod -n monitoring -l app=grafana`
- [ ] Check logs: `kubectl logs -n monitoring -l app=grafana`
- [ ] Verify resources: `kubectl top nodes` (ensure sufficient CPU/memory)
- [ ] Delete and redeploy: `kubectl delete pod -n monitoring -l app=grafana`

### Cannot Access UI
- [ ] Verify service: `kubectl get svc -n monitoring grafana-service`
- [ ] Check NodePort is 30000
- [ ] Try port-forward: `kubectl port-forward svc/grafana-service 3000:3000 -n monitoring`
- [ ] Access via port-forward: http://localhost:3000

### Prometheus Datasource Not Working
- [ ] Verify Prometheus is running: `kubectl get pods -n monitoring -l app=prometheus`
- [ ] Check Prometheus service: `kubectl get svc -n monitoring prometheus-service`
- [ ] Test connectivity from Grafana pod:
  ```bash
  GRAFANA_POD=$(kubectl get pods -n monitoring -l app=grafana -o jsonpath='{.items[0].metadata.name}')
  kubectl exec -n monitoring $GRAFANA_POD -- wget -O- http://prometheus-service:9090/api/v1/status/config
  ```

### Dashboards Not Appearing
- [ ] Check ConfigMap: `kubectl get configmap -n monitoring grafana-dashboards-config`
- [ ] Restart Grafana: `kubectl delete pod -n monitoring -l app=grafana`
- [ ] Wait for pod to restart: `kubectl wait --for=condition=ready pod -l app=grafana -n monitoring --timeout=120s`
- [ ] Refresh browser

### Dashboards Show "No Data"
- [ ] Wait 2-3 minutes for Prometheus to scrape metrics
- [ ] Check Prometheus has data: http://localhost:30090 → Graph → Query: `up`
- [ ] Verify time range is appropriate (last 15 minutes)
- [ ] Check if kube-state-metrics is deployed (some queries need it)

## Success Criteria

All of the following should be true:

- [ ] ✅ Grafana pod is running and ready
- [ ] ✅ Grafana UI is accessible at http://localhost:30000
- [ ] ✅ Can login with admin/admin
- [ ] ✅ Prometheus datasource is connected and working
- [ ] ✅ "Kubernetes Monitoring Dashboard" is visible
- [ ] ✅ "Guardian AI Ops Dashboard" is visible
- [ ] ✅ Dashboards show live data (or appropriate placeholders)
- [ ] ✅ Dashboards auto-refresh every 5 seconds
- [ ] ✅ No errors in Grafana logs
- [ ] ✅ No errors in browser console

## Cleanup (If Needed)

To remove Grafana:

- [ ] Delete service: `kubectl delete -f grafana-service.yaml`
- [ ] Delete deployment: `kubectl delete -f grafana-deployment.yaml`
- [ ] Delete dashboard config: `kubectl delete -f grafana-dashboard-config.yaml`
- [ ] Delete datasource config: `kubectl delete -f grafana-datasource-config.yaml`
- [ ] Verify deletion: `kubectl get all -n monitoring -l app=grafana`

## Documentation Reference

- **Quick Start:** `QUICK_REFERENCE.md`
- **Detailed Guide:** `SETUP_GUIDE.md`
- **Full Documentation:** `README.md`
- **Integration Summary:** `../GRAFANA_INTEGRATION_COMPLETE.md`

## Support Commands

```bash
# Check all monitoring resources
kubectl get all -n monitoring

# View Grafana logs
kubectl logs -n monitoring -l app=grafana -f

# Restart Grafana
kubectl delete pod -n monitoring -l app=grafana

# Run verification
bash verify.sh

# Port forward (alternative access)
kubectl port-forward svc/grafana-service 3000:3000 -n monitoring
```

---

**Status:** [ ] Not Started | [ ] In Progress | [ ] Complete ✅

**Date:** _______________

**Notes:**
_____________________________________________________________________________
_____________________________________________________________________________
_____________________________________________________________________________
