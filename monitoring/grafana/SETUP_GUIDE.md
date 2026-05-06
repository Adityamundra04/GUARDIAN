# Grafana Setup Guide for Guardian AI Ops Platform

Complete step-by-step guide to deploy and configure Grafana for the Guardian AI Ops platform.

## 📋 Prerequisites Checklist

Before starting, ensure you have:

- [ ] Kubernetes cluster running (Minikube, Kind, K3s, or cloud K8s)
- [ ] `kubectl` installed and configured
- [ ] Prometheus deployed in the `monitoring` namespace
- [ ] Terminal access with bash support

## 🚀 Installation Steps

### Step 1: Verify Prometheus is Running

```bash
# Check if Prometheus is deployed
kubectl get pods -n monitoring -l app=prometheus

# Expected output:
# NAME                          READY   STATUS    RESTARTS   AGE
# prometheus-xxxxxxxxxx-xxxxx   1/1     Running   0          5m
```

If Prometheus is not running, deploy it first:

```bash
cd monitoring/prometheus
bash deploy.sh
cd ../grafana
```

### Step 2: Deploy Grafana

```bash
# Navigate to the grafana directory
cd monitoring/grafana

# Make scripts executable
chmod +x deploy.sh verify.sh

# Run the deployment script
bash deploy.sh
```

The deployment script will:
1. Create/verify the monitoring namespace
2. Deploy Grafana datasource configuration
3. Deploy dashboard provisioning configuration
4. Deploy Grafana pod
5. Expose Grafana service
6. Wait for Grafana to be ready

**Expected output:**
```
==========================================
Guardian Grafana Deployment
==========================================

Step 1: Deploying Grafana datasource configuration...
configmap/grafana-datasources created

Step 2: Deploying Grafana dashboard provisioning configuration...
configmap/grafana-dashboards-config created

Step 3: Deploying Grafana...
deployment.apps/grafana created

Step 4: Deploying Grafana service...
service/grafana-service created

==========================================
Deployment Complete!
==========================================

Grafana is now running!

Access Methods:
  1. NodePort: http://localhost:30000
  2. Port Forward: kubectl port-forward svc/grafana-service 3000:3000 -n monitoring
     Then access: http://localhost:3000

Default Credentials:
  Username: admin
  Password: admin
```

### Step 3: Verify Deployment

```bash
# Run the verification script
bash verify.sh
```

**Expected output:**
```
==========================================
Guardian Grafana Verification
==========================================

✅ kubectl is available
✅ Monitoring namespace exists
✅ Grafana pod found: grafana-xxxxxxxxxx-xxxxx
✅ Grafana pod is Running
✅ Grafana pod is Ready
✅ Grafana service exists
   Type: NodePort
   NodePort: 30000
✅ Prometheus service exists (datasource available)
✅ Grafana datasources ConfigMap exists
✅ Grafana dashboards config ConfigMap exists
✅ Grafana HTTP endpoint is responding
```

### Step 4: Access Grafana UI

#### Option A: NodePort (Recommended for local clusters)

```bash
# Open browser to:
http://localhost:30000
```

#### Option B: Port Forward

```bash
# Start port forwarding
kubectl port-forward svc/grafana-service 3000:3000 -n monitoring

# Open browser to:
http://localhost:3000
```

### Step 5: Login to Grafana

1. Open Grafana in your browser
2. Enter credentials:
   - **Username:** `admin`
   - **Password:** `admin`
3. (Optional) Change password when prompted
4. Click "Skip" if you want to keep the default password for demo purposes

### Step 6: Verify Dashboards

1. Click on the **Dashboards** icon (four squares) in the left sidebar
2. You should see two pre-configured dashboards:
   - **Kubernetes Monitoring Dashboard**
   - **Guardian AI Ops Dashboard**
3. Click on each dashboard to view live metrics

### Step 7: Verify Prometheus Datasource

1. Click on **Configuration** (gear icon) in the left sidebar
2. Click on **Data Sources**
3. You should see **Prometheus** listed as the default datasource
4. Click on **Prometheus** to view configuration
5. Scroll down and click **Save & Test**
6. You should see: "Data source is working"

## 📊 Using the Dashboards

### Kubernetes Monitoring Dashboard

This dashboard shows:

- **Pod CPU Usage (%)** - Time series graph showing CPU usage per pod
- **Pod Memory Usage** - Time series graph showing memory consumption per pod
- **Pod Restart Count** - Gauge showing restart counts with color thresholds
- **Pod Status** - Gauge showing running vs down pods
- **Cluster Health Overview** - Time series showing ready nodes and running pods

**Use cases:**
- Monitor resource utilization across pods
- Identify pods with high CPU/memory usage
- Track pod restarts (potential issues)
- Overall cluster health monitoring

### Guardian AI Ops Dashboard

This dashboard shows:

- **Active Incidents** - Gauge showing current number of incidents
- **Remediation Events** - Total count of remediation actions taken
- **Monitoring Activity** - Status of monitoring system (Active/Inactive)
- **AI Diagnosis Activity** - Status of AI diagnosis engine (Online/Offline)
- **Incident Rate Over Time** - Time series showing incident frequency
- **Remediation Events Over Time** - Time series showing remediation actions
- **Top Pods by Restart Count** - Bar chart showing pods with most incidents

**Use cases:**
- Track Guardian AI Ops activity
- Monitor incident detection and remediation
- Identify problematic pods requiring attention
- Measure system effectiveness

## 🔧 Configuration

### Changing Refresh Rate

Both dashboards are set to refresh every **5 seconds** by default.

To change:
1. Open a dashboard
2. Click the refresh dropdown (top right)
3. Select a different interval (10s, 30s, 1m, etc.)

### Changing Time Range

Default time range is **Last 15 minutes**.

To change:
1. Open a dashboard
2. Click the time range selector (top right)
3. Select a different range or set custom range

### Customizing Dashboards

1. Open a dashboard
2. Click the **Settings** icon (gear) at the top
3. Make your changes
4. Click **Save dashboard**

To make changes permanent:
1. Click **Share** icon (top right)
2. Click **Export** tab
3. Click **Save to file**
4. Replace the JSON file in `monitoring/grafana/dashboards/`

## 🧪 Testing the Integration

### Test 1: Verify Prometheus Connection

```bash
# Get Grafana pod name
GRAFANA_POD=$(kubectl get pods -n monitoring -l app=grafana -o jsonpath='{.items[0].metadata.name}')

# Test Prometheus connectivity from Grafana
kubectl exec -n monitoring $GRAFANA_POD -- wget -O- http://prometheus-service:9090/api/v1/query?query=up
```

Expected: JSON response with Prometheus metrics

### Test 2: Create a Test Incident

```bash
# Deploy a crashloop pod to generate incidents
kubectl apply -f ../../k8s/test-failures/crashloop.yaml

# Wait 30 seconds, then check Guardian AI Ops Dashboard
# You should see:
# - Active Incidents increase
# - Incident Rate spike
# - Pod appear in "Top Pods by Restart Count"
```

### Test 3: Verify Dashboard Auto-Refresh

1. Open the Guardian AI Ops Dashboard
2. Note the current incident count
3. Wait 5 seconds (auto-refresh interval)
4. Dashboard should update automatically with new data

## 🔍 Troubleshooting

### Issue: Grafana Pod Not Starting

**Symptoms:**
- Pod status is `Pending`, `CrashLoopBackOff`, or `Error`

**Solution:**
```bash
# Check pod details
kubectl describe pod -n monitoring -l app=grafana

# Check logs
kubectl logs -n monitoring -l app=grafana

# Common fixes:
# 1. Insufficient resources - check node capacity
# 2. Image pull issues - check internet connectivity
# 3. ConfigMap issues - verify ConfigMaps exist
```

### Issue: Cannot Access Grafana UI

**Symptoms:**
- Browser shows "Connection refused" or "Unable to connect"

**Solution:**

For NodePort access:
```bash
# Verify service is exposed
kubectl get svc -n monitoring grafana-service

# Check NodePort value (should be 30000)
# Try accessing: http://localhost:30000
```

For Port Forward:
```bash
# Kill any existing port-forward
pkill -f "port-forward.*grafana"

# Start fresh port-forward
kubectl port-forward svc/grafana-service 3000:3000 -n monitoring

# Access: http://localhost:3000
```

### Issue: Prometheus Datasource Not Working

**Symptoms:**
- Dashboards show "No data" or "Datasource error"
- Datasource test fails

**Solution:**
```bash
# Verify Prometheus is running
kubectl get pods -n monitoring -l app=prometheus

# Verify Prometheus service exists
kubectl get svc -n monitoring prometheus-service

# Test connectivity from Grafana pod
GRAFANA_POD=$(kubectl get pods -n monitoring -l app=grafana -o jsonpath='{.items[0].metadata.name}')
kubectl exec -n monitoring $GRAFANA_POD -- wget -O- http://prometheus-service:9090/api/v1/status/config

# If this fails, Prometheus may not be running correctly
```

### Issue: Dashboards Not Appearing

**Symptoms:**
- No dashboards visible in Grafana UI
- Only "Create your first dashboard" message

**Solution:**
```bash
# Check dashboard provisioning ConfigMap
kubectl get configmap -n monitoring grafana-dashboards-config -o yaml

# Restart Grafana pod to reload dashboards
kubectl delete pod -n monitoring -l app=grafana

# Wait for pod to restart
kubectl wait --for=condition=ready pod -l app=grafana -n monitoring --timeout=120s

# Refresh Grafana UI in browser
```

### Issue: Dashboards Show "No Data"

**Symptoms:**
- Dashboards load but panels show "No data"

**Possible causes and solutions:**

1. **Prometheus has no metrics yet:**
   - Wait a few minutes for Prometheus to scrape metrics
   - Check Prometheus UI: http://localhost:30090

2. **Prometheus queries are incorrect:**
   - Open Prometheus UI: http://localhost:30090
   - Go to Graph tab
   - Try running queries manually (e.g., `up`, `kube_pod_info`)

3. **Kubernetes metrics not available:**
   - Some metrics require kube-state-metrics or node-exporter
   - Check if these are deployed in your cluster

## 🗑️ Cleanup

To remove Grafana:

```bash
# Delete all Grafana resources
kubectl delete -f grafana-service.yaml
kubectl delete -f grafana-deployment.yaml
kubectl delete -f grafana-dashboard-config.yaml
kubectl delete -f grafana-datasource-config.yaml

# Verify deletion
kubectl get all -n monitoring -l app=grafana
```

To remove entire monitoring stack (Prometheus + Grafana):

```bash
# Delete monitoring namespace (removes everything)
kubectl delete namespace monitoring
```

## 📚 Next Steps

After successful setup:

1. **Explore Dashboards** - Familiarize yourself with the pre-configured dashboards
2. **Create Custom Dashboards** - Build dashboards for specific use cases
3. **Set Up Alerts** (Optional) - Configure Grafana alerts for critical metrics
4. **Integrate with Guardian** - Ensure Guardian AI is using the same observability stack
5. **Monitor Production** - Use Grafana for live production monitoring

## 🎯 Success Checklist

- [ ] Grafana pod is running and ready
- [ ] Grafana UI is accessible (http://localhost:30000)
- [ ] Can login with admin/admin credentials
- [ ] Prometheus datasource is connected and working
- [ ] "Kubernetes Monitoring Dashboard" is visible and showing data
- [ ] "Guardian AI Ops Dashboard" is visible and showing data
- [ ] Dashboards auto-refresh every 5 seconds
- [ ] No errors in Grafana logs

## 📞 Support

If you encounter issues not covered in this guide:

1. Check Grafana logs: `kubectl logs -n monitoring -l app=grafana -f`
2. Check Prometheus logs: `kubectl logs -n monitoring -l app=prometheus -f`
3. Verify all resources: `kubectl get all -n monitoring`
4. Review Grafana documentation: https://grafana.com/docs/

---

**Guardian AI Ops Platform** - Autonomous Kubernetes Monitoring & Remediation
