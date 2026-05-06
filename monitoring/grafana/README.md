# Grafana Integration for Guardian AI Ops Platform

This directory contains Kubernetes manifests for deploying Grafana with automatic Prometheus integration and pre-configured dashboards for the Guardian AI Ops platform.

## 🎯 Overview

Grafana provides live visualization of:
- **Kubernetes Infrastructure Metrics** (CPU, memory, pod status, restarts)
- **Guardian AI Ops Activity** (incidents, remediations, monitoring status)

## 📁 Files

```
monitoring/grafana/
├── grafana-deployment.yaml           # Grafana deployment manifest
├── grafana-service.yaml              # Grafana NodePort service (port 30000)
├── grafana-datasource-config.yaml    # Auto-provisioned Prometheus datasource
├── grafana-dashboard-config.yaml     # Dashboard provisioning configuration
├── dashboards/
│   ├── kubernetes-monitoring.json    # Kubernetes infrastructure dashboard
│   └── guardian-monitoring.json      # Guardian AI Ops dashboard
├── deploy.sh                         # Automated deployment script
└── README.md                         # This file
```

## 🚀 Quick Start

### Prerequisites

1. **Kubernetes cluster** running (Minikube, Kind, or any K8s cluster)
2. **kubectl** configured and connected to your cluster
3. **Prometheus** already deployed in the `monitoring` namespace
   - If not deployed, run: `cd ../prometheus && bash deploy.sh`

### Deployment

```bash
# Navigate to the grafana directory
cd monitoring/grafana

# Make the deployment script executable
chmod +x deploy.sh

# Run the deployment script
bash deploy.sh
```

The script will:
1. ✅ Create/verify the monitoring namespace
2. ✅ Deploy Grafana datasource configuration (auto-connects to Prometheus)
3. ✅ Deploy dashboard provisioning configuration
4. ✅ Deploy Grafana pod
5. ✅ Expose Grafana service on NodePort 30000
6. ✅ Wait for Grafana to be ready

## 🌐 Accessing Grafana

### Method 1: NodePort (Recommended for local clusters)

```bash
# Access Grafana directly via NodePort
http://localhost:30000
```

### Method 2: Port Forward

```bash
# Forward Grafana service to local port 3000
kubectl port-forward svc/grafana-service 3000:3000 -n monitoring

# Access Grafana
http://localhost:3000
```

### Default Credentials

```
Username: admin
Password: admin
```

**Note:** Grafana will prompt you to change the password on first login (optional for demo purposes).

## 📊 Pre-configured Dashboards

Grafana comes with two auto-provisioned dashboards:

### 1. Kubernetes Monitoring Dashboard

**Visualizes:**
- Pod CPU Usage (%)
- Pod Memory Usage (bytes)
- Pod Restart Count (gauge with thresholds)
- Pod Status (Running/Down)
- Cluster Health Overview (Ready Nodes, Running Pods)

**Refresh Rate:** 5 seconds  
**Time Range:** Last 15 minutes

### 2. Guardian AI Ops Dashboard

**Visualizes:**
- Active Incidents (gauge)
- Remediation Events (total count)
- Monitoring Activity Status (Active/Inactive)
- AI Diagnosis Activity Status (Online/Offline)
- Incident Rate Over Time (time series)
- Remediation Events Over Time (time series)
- Top Pods by Restart Count (bar chart)

**Refresh Rate:** 5 seconds  
**Time Range:** Last 15 minutes

## 🔧 Configuration Details

### Prometheus Datasource

The Prometheus datasource is **automatically configured** on Grafana startup:

```yaml
Name: Prometheus
Type: prometheus
URL: http://prometheus-service:9090
Access: proxy
Default: true
```

No manual configuration required!

### Dashboard Provisioning

Dashboards are automatically loaded from the `dashboards/` directory on startup. You can:
- Edit existing dashboards in the Grafana UI
- Create new dashboards
- Export dashboards as JSON

## 🧪 Verification Commands

### Check Grafana Pod Status

```bash
kubectl get pods -n monitoring -l app=grafana
```

Expected output:
```
NAME                       READY   STATUS    RESTARTS   AGE
grafana-xxxxxxxxxx-xxxxx   1/1     Running   0          2m
```

### Check Grafana Service

```bash
kubectl get svc -n monitoring -l app=grafana
```

Expected output:
```
NAME              TYPE       CLUSTER-IP      EXTERNAL-IP   PORT(S)          AGE
grafana-service   NodePort   10.96.xxx.xxx   <none>        3000:30000/TCP   2m
```

### View Grafana Logs

```bash
kubectl logs -n monitoring -l app=grafana -f
```

### Check All Monitoring Resources

```bash
kubectl get all -n monitoring
```

## 🔍 Troubleshooting

### Grafana Pod Not Starting

```bash
# Check pod status
kubectl describe pod -n monitoring -l app=grafana

# Check logs
kubectl logs -n monitoring -l app=grafana
```

### Prometheus Datasource Not Connected

1. Check if Prometheus is running:
   ```bash
   kubectl get pods -n monitoring -l app=prometheus
   ```

2. Verify Prometheus service:
   ```bash
   kubectl get svc -n monitoring prometheus-service
   ```

3. Test Prometheus connectivity from Grafana pod:
   ```bash
   kubectl exec -n monitoring -it $(kubectl get pod -n monitoring -l app=grafana -o jsonpath='{.items[0].metadata.name}') -- wget -O- http://prometheus-service:9090/api/v1/status/config
   ```

### Dashboards Not Appearing

1. Check dashboard provisioning configuration:
   ```bash
   kubectl get configmap -n monitoring grafana-dashboards-config -o yaml
   ```

2. Restart Grafana pod:
   ```bash
   kubectl delete pod -n monitoring -l app=grafana
   ```

### Cannot Access Grafana UI

1. **For NodePort access:**
   - Ensure you're using the correct NodePort: `30000`
   - Check if your cluster supports NodePort (Minikube/Kind do)

2. **For Port Forward:**
   - Ensure the port-forward command is running
   - Check if port 3000 is already in use locally

## 🗑️ Cleanup

To remove Grafana from your cluster:

```bash
# Delete Grafana resources
kubectl delete -f grafana-service.yaml
kubectl delete -f grafana-deployment.yaml
kubectl delete -f grafana-dashboard-config.yaml
kubectl delete -f grafana-datasource-config.yaml

# Optionally delete the monitoring namespace (removes Prometheus too)
kubectl delete namespace monitoring
```

## 📈 Architecture Flow

```
Kubernetes Cluster
       ↓
   Prometheus (scrapes metrics every 15s)
       ↓
   Grafana (queries Prometheus)
       ↓
   Dashboards (visualize metrics)
       ↓
   Guardian AI (uses same observability stack)
```

## 🎨 Customization

### Adding New Dashboards

1. Create a new dashboard in Grafana UI
2. Export the dashboard as JSON
3. Save the JSON file in `dashboards/` directory
4. The dashboard will auto-load on next Grafana restart

### Modifying Existing Dashboards

1. Edit dashboards directly in Grafana UI
2. Changes are persisted in Grafana's storage
3. To make changes permanent, export and save to `dashboards/` directory

### Changing Grafana Configuration

Edit `grafana-deployment.yaml` to modify:
- Resource limits (memory/CPU)
- Environment variables
- Admin credentials
- Storage configuration

## 📚 Additional Resources

- [Grafana Documentation](https://grafana.com/docs/)
- [Prometheus Documentation](https://prometheus.io/docs/)
- [Kubernetes Monitoring Guide](https://kubernetes.io/docs/tasks/debug-application-cluster/resource-metrics-pipeline/)

## ✅ Success Criteria

After deployment, you should have:
- ✅ Grafana UI accessible at http://localhost:30000
- ✅ Prometheus datasource connected and working
- ✅ Two dashboards visible: "Kubernetes Monitoring Dashboard" and "Guardian AI Ops Dashboard"
- ✅ Live metrics visualized with 5-second refresh rate
- ✅ No errors in Grafana logs

## 🎯 Next Steps

1. Access Grafana UI
2. Explore the pre-configured dashboards
3. Monitor your Kubernetes cluster and Guardian AI Ops activity
4. Create custom dashboards for specific use cases
5. Set up alerts (optional, for production use)

---

**Guardian AI Ops Platform** - Autonomous Kubernetes Monitoring & Remediation
