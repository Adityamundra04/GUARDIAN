#!/bin/bash

# Guardian Demo Website Cleanup Script
# Removes all demo website resources from Kubernetes

set -e

echo "🧹 Guardian Demo Website Cleanup"
echo "================================="
echo ""

# Check if kubectl is available
if ! command -v kubectl &> /dev/null; then
    echo "❌ Error: kubectl not found"
    exit 1
fi

echo "🗑️  Removing demo website resources..."
echo ""

# Delete deployment
echo "Deleting deployment..."
kubectl delete -f deployment.yaml --ignore-not-found=true

# Delete service
echo "Deleting service..."
kubectl delete -f service.yaml --ignore-not-found=true

# Delete configmap
echo "Deleting configmap..."
kubectl delete -f configmap.yaml --ignore-not-found=true

# Delete failure test pods
echo "Deleting failure test pods..."
kubectl delete pod demo-crashloop-failure --ignore-not-found=true
kubectl delete pod demo-imagepull-failure --ignore-not-found=true
kubectl delete pod demo-oom-failure --ignore-not-found=true

echo ""
echo "✅ Cleanup complete!"
echo ""
echo "📊 Remaining resources (should be empty):"
kubectl get all -l app=guardian-demo
echo ""
