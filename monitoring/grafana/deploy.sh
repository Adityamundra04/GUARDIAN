#!/bin/bash

# Grafana Deployment Script for Guardian AI Ops Platform
# This script deploys Grafana with auto-provisioned Prometheus datasource and dashboards

set -e

echo "=========================================="
echo "Guardian Grafana Deployment"
echo "=========================================="
echo ""

# Check if kubectl is available
if ! command -v kubectl &> /dev/null; then
    echo "ERROR: kubectl is not installed or not in PATH"
    exit 1
fi

# Check if monitoring namespace exists (should be created by Prometheus deployment)
echo "Checking monitoring namespace..."
if ! kubectl get namespace monitoring &> /dev/null; then
    echo "Creating monitoring namespace..."
    kubectl apply -f ../prometheus/namespace.yaml
fi

echo ""
echo "Step 1: Deploying Grafana datasource configuration..."
kubectl apply -f grafana-datasource-config.yaml

echo ""
echo "Step 2: Deploying Grafana dashboard provisioning configuration..."
kubectl apply -f grafana-dashboard-config.yaml

echo ""
echo "Step 3: Deploying Grafana..."
kubectl apply -f grafana-deployment.yaml

echo ""
echo "Step 4: Deploying Grafana service..."
kubectl apply -f grafana-service.yaml

echo ""
echo "=========================================="
echo "Deployment Complete!"
echo "=========================================="
echo ""
echo "Waiting for Grafana pod to be ready..."
kubectl wait --for=condition=ready pod -l app=grafana -n monitoring --timeout=120s

echo ""
echo "=========================================="
echo "Grafana Access Information"
echo "=========================================="
echo ""
echo "Grafana is now running!"
echo ""
echo "Access Methods:"
echo "  1. NodePort: http://localhost:30000"
echo "  2. Port Forward: kubectl port-forward svc/grafana-service 3000:3000 -n monitoring"
echo "     Then access: http://localhost:3000"
echo ""
echo "Default Credentials:"
echo "  Username: admin"
echo "  Password: admin"
echo ""
echo "Pre-configured Dashboards:"
echo "  - Kubernetes Monitoring Dashboard"
echo "  - Guardian AI Ops Dashboard"
echo ""
echo "Prometheus Datasource:"
echo "  - Auto-configured and connected to prometheus-service:9090"
echo ""
echo "=========================================="
echo "Verification Commands"
echo "=========================================="
echo ""
echo "Check Grafana pod status:"
echo "  kubectl get pods -n monitoring -l app=grafana"
echo ""
echo "Check Grafana service:"
echo "  kubectl get svc -n monitoring -l app=grafana"
echo ""
echo "View Grafana logs:"
echo "  kubectl logs -n monitoring -l app=grafana -f"
echo ""
echo "=========================================="
