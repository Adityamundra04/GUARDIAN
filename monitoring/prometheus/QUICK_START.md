# Prometheus Quick Start

## Deploy Prometheus

### Option 1: All-in-One Command
```bash
kubectl apply -f monitoring/prometheus/
```

### Option 2: Step-by-Step
```bash
kubectl apply -f monitoring/prometheus/namespace.yaml
kubectl apply -f monitoring/prometheus/prometheus-rbac.yaml
kubectl apply -f monitoring/prometheus/prometheus-configmap.yaml
kubectl apply -f monitoring/prometheus/prometheus-deployment.yaml
kubectl apply -f monitoring/prometheus/prometheus-service.yaml
```

### Option 3: Using Script
```bash
cd monitoring/prometheus
chmod +x deploy.sh
./deploy.sh
```

## Verify Deployment

### Check Pods
```bash
kubectl get pods -n monitoring
```

**Expected:**
```
NAME                          READY   STATUS    RESTARTS   AGE
prometheus-7d9f8c8b5d-x7k2m   1/1     Running   0          1m
```

### Check Service
```bash
kubectl get svc -n monitoring
```

**Expected:**
```
NAME                 TYPE       CLUSTER-IP      EXTERNAL-IP   PORT(S)          AGE
prometheus-service   NodePort   10.96.123.45    <none>        9090:30090/TCP   1m
```

## Access Prometheus UI

### Port Forward
```bash
kubectl port-forward svc/prometheus-service 9090:9090 -n monitoring
```

### Open Browser
```
http://localhost:9090
```

## Test Queries

### Query 1: Check Prometheus is Up
```promql
up
```

### Query 2: Check All Targets
```promql
up{job=~"kubernetes.*"}
```

### Query 3: Node Metrics
```promql
node_cpu_seconds_total
```

## Cleanup

```bash
kubectl delete -f monitoring/prometheus/
```

## Success Criteria

✅ Pod running  
✅ Service created  
✅ UI accessible  
✅ Queries working  

🎉 **Prometheus is ready!**
