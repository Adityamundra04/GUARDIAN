#!/bin/bash

# Guardian Demo Website Deployment Script
# Deploys the demo website to Kubernetes cluster

set -e

echo "🛡️  Guardian Demo Website Deployment"
echo "===================================="
echo ""

# Check if kubectl is available
if ! command -v kubectl &> /dev/null; then
    echo "❌ Error: kubectl not found"
    echo "Please install kubectl first"
    exit 1
fi

# Check if cluster is accessible
if ! kubectl cluster-info &> /dev/null; then
    echo "❌ Error: Cannot connect to Kubernetes cluster"
    echo "Please ensure your cluster is running"
    exit 1
fi

echo "✅ Kubernetes cluster is accessible"
echo ""

# Deploy ConfigMap
echo "📦 Deploying ConfigMap..."
kubectl apply -f configmap.yaml

# Deploy Deployment
echo "🚀 Deploying website..."
kubectl apply -f deployment.yaml

# Deploy Service
echo "🌐 Deploying service..."
kubectl apply -f service.yaml

echo ""
echo "⏳ Waiting for deployment to be ready..."
kubectl wait --for=condition=available --timeout=60s deployment/guardian-demo-website

echo ""
echo "✅ Deployment complete!"
echo ""
echo "📊 Deployment Status:"
kubectl get pods -l app=guardian-demo
echo ""
kubectl get svc guardian-demo-website
echo ""

echo "🌐 Access the website:"
echo "   URL: http://localhost:30080"
echo ""
echo "🔍 Useful commands:"
echo "   View pods:  kubectl get pods -l app=guardian-demo"
echo "   View logs:  kubectl logs -l app=guardian-demo"
echo "   Port forward: kubectl port-forward svc/guardian-demo-website 8080:80"
echo ""
echo "🧪 Test failure scenarios:"
echo "   kubectl apply -f failure-crashloop.yaml"
echo "   kubectl apply -f failure-imagepull.yaml"
echo "   kubectl apply -f failure-oom.yaml"
echo ""
