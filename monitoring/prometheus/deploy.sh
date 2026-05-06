#!/bin/bash

# Prometheus Deployment Script for Guardian
# Deploys Prometheus monitoring to Kubernetes cluster

set -e

echo "========================================="
echo "  Deploying Prometheus for Guardian"
echo "========================================="
echo ""

# Check if kubectl is available
if ! command -v kubectl &> /dev/null; then
    echo "❌ kubectl not found. Please install kubectl first."
    exit 1
fi

# Check if cluster is accessible
if ! kubectl cluster-info &> /dev/null; then
    echo "❌ Cannot connect to Kubernetes cluster."
    echo "   Please ensure your cluster is running and kubeconfig is set."
    exit 1
fi

echo "✅ kubectl found"
echo "✅ Kubernetes cluster accessible"
echo ""

# Deploy Prometheus
echo "📦 Deploying Prometheus..."
echo ""

echo "1️⃣  Creating monitoring namespace..."
kubectl apply -f namespace.yaml

echo "2️⃣  Creating RBAC resources..."
kubectl apply -f prometheus-rbac.yaml

echo "3️⃣  Creating ConfigMap..."
kubectl apply -f prometheus-configmap.yaml

echo "4️⃣  Deploying Prometheus..."
kubectl apply -f prometheus-deployment.yaml

echo "5️⃣  Creating Service..."
kubectl apply -f prometheus-service.yaml

echo ""
echo "⏳ Waiting for Prometheus to be ready..."
kubectl wait --for=condition=available --timeout=120s deployment/prometheus -n monitoring

echo ""
echo "========================================="
echo "  ✅ Prometheus Deployed Successfully!"
echo "========================================="
echo ""

# Show status
echo "📊 Deployment Status:"
echo ""
kubectl get pods -n monitoring
echo ""
kubectl get svc -n monitoring
echo ""

# Show access instructions
echo "========================================="
echo "  🌐 Access Prometheus UI"
echo "========================================="
echo ""
echo "Run the following command:"
echo ""
echo "  kubectl port-forward svc/prometheus-service 9090:9090 -n monitoring"
echo ""
echo "Then open: http://localhost:9090"
echo ""

# Show verification commands
echo "========================================="
echo "  🔍 Verification Commands"
echo "========================================="
echo ""
echo "Check pods:"
echo "  kubectl get pods -n monitoring"
echo ""
echo "Check logs:"
echo "  kubectl logs -n monitoring deployment/prometheus"
echo ""
echo "Check targets (after port-forward):"
echo "  Open http://localhost:9090/targets"
echo ""

echo "🎉 Setup complete!"
