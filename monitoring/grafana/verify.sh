#!/bin/bash

# Grafana Verification Script for Guardian AI Ops Platform
# This script verifies that Grafana is properly deployed and accessible

echo "=========================================="
echo "Guardian Grafana Verification"
echo "=========================================="
echo ""

# Check if kubectl is available
if ! command -v kubectl &> /dev/null; then
    echo "❌ ERROR: kubectl is not installed or not in PATH"
    exit 1
fi
echo "✅ kubectl is available"

# Check monitoring namespace
echo ""
echo "Checking monitoring namespace..."
if kubectl get namespace monitoring &> /dev/null; then
    echo "✅ Monitoring namespace exists"
else
    echo "❌ Monitoring namespace does not exist"
    exit 1
fi

# Check Grafana pod
echo ""
echo "Checking Grafana pod..."
GRAFANA_POD=$(kubectl get pods -n monitoring -l app=grafana -o jsonpath='{.items[0].metadata.name}' 2>/dev/null)
if [ -z "$GRAFANA_POD" ]; then
    echo "❌ Grafana pod not found"
    exit 1
fi
echo "✅ Grafana pod found: $GRAFANA_POD"

# Check pod status
POD_STATUS=$(kubectl get pod -n monitoring $GRAFANA_POD -o jsonpath='{.status.phase}')
if [ "$POD_STATUS" == "Running" ]; then
    echo "✅ Grafana pod is Running"
else
    echo "⚠️  Grafana pod status: $POD_STATUS"
fi

# Check pod readiness
POD_READY=$(kubectl get pod -n monitoring $GRAFANA_POD -o jsonpath='{.status.conditions[?(@.type=="Ready")].status}')
if [ "$POD_READY" == "True" ]; then
    echo "✅ Grafana pod is Ready"
else
    echo "⚠️  Grafana pod is not ready yet"
fi

# Check Grafana service
echo ""
echo "Checking Grafana service..."
if kubectl get svc -n monitoring grafana-service &> /dev/null; then
    echo "✅ Grafana service exists"
    SERVICE_TYPE=$(kubectl get svc -n monitoring grafana-service -o jsonpath='{.spec.type}')
    NODE_PORT=$(kubectl get svc -n monitoring grafana-service -o jsonpath='{.spec.ports[0].nodePort}')
    echo "   Type: $SERVICE_TYPE"
    echo "   NodePort: $NODE_PORT"
else
    echo "❌ Grafana service not found"
    exit 1
fi

# Check Prometheus service (datasource)
echo ""
echo "Checking Prometheus service (datasource)..."
if kubectl get svc -n monitoring prometheus-service &> /dev/null; then
    echo "✅ Prometheus service exists (datasource available)"
else
    echo "⚠️  Prometheus service not found - datasource may not work"
fi

# Check ConfigMaps
echo ""
echo "Checking Grafana configuration..."
if kubectl get configmap -n monitoring grafana-datasources &> /dev/null; then
    echo "✅ Grafana datasources ConfigMap exists"
else
    echo "❌ Grafana datasources ConfigMap not found"
fi

if kubectl get configmap -n monitoring grafana-dashboards-config &> /dev/null; then
    echo "✅ Grafana dashboards config ConfigMap exists"
else
    echo "❌ Grafana dashboards config ConfigMap not found"
fi

# Test Grafana HTTP endpoint
echo ""
echo "Testing Grafana HTTP endpoint..."
if kubectl exec -n monitoring $GRAFANA_POD -- wget -q -O- http://localhost:3000/api/health &> /dev/null; then
    echo "✅ Grafana HTTP endpoint is responding"
else
    echo "⚠️  Grafana HTTP endpoint not responding yet (may still be starting)"
fi

# Summary
echo ""
echo "=========================================="
echo "Verification Summary"
echo "=========================================="
echo ""
echo "Access Grafana:"
echo "  NodePort: http://localhost:$NODE_PORT"
echo "  Port Forward: kubectl port-forward svc/grafana-service 3000:3000 -n monitoring"
echo ""
echo "Default Credentials:"
echo "  Username: admin"
echo "  Password: admin"
echo ""
echo "View Logs:"
echo "  kubectl logs -n monitoring $GRAFANA_POD -f"
echo ""
echo "=========================================="
