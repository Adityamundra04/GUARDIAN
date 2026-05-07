#!/bin/bash

# Guardian Demo Website - Failure Testing Script
# Tests Guardian's detection and remediation capabilities

set -e

echo "🧪 Guardian Failure Testing Suite"
echo "=================================="
echo ""

# Check if kubectl is available
if ! command -v kubectl &> /dev/null; then
    echo "❌ Error: kubectl not found"
    exit 1
fi

# Function to wait and observe
wait_and_observe() {
    local pod_name=$1
    local duration=$2
    
    echo "⏳ Observing for ${duration} seconds..."
    echo "   Watch Guardian dashboard: http://localhost:5173"
    echo "   Watch Grafana: http://localhost:3000"
    echo ""
    
    for i in $(seq 1 $duration); do
        echo -ne "   Time: ${i}/${duration}s\r"
        sleep 1
    done
    echo ""
}

# Function to show pod status
show_status() {
    echo "📊 Current Pod Status:"
    kubectl get pods -l app=guardian-demo -o wide 2>/dev/null || echo "   No guardian-demo pods found"
    kubectl get pod $1 -o wide 2>/dev/null || echo "   Pod $1 not found"
    echo ""
}

# Menu
echo "Select a failure scenario to test:"
echo ""
echo "1) CrashLoopBackOff - Pod repeatedly crashes"
echo "2) ImagePullBackOff - Invalid container image"
echo "3) Out of Memory (OOM) - Memory limit exceeded"
echo "4) Run all scenarios sequentially"
echo "5) Cleanup all test pods"
echo "0) Exit"
echo ""
read -p "Enter choice [0-5]: " choice

case $choice in
    1)
        echo ""
        echo "🔴 Testing: CrashLoopBackOff"
        echo "=============================="
        echo "This pod will repeatedly crash and restart"
        echo ""
        
        kubectl apply -f failure-crashloop.yaml
        echo "✅ Pod deployed: demo-crashloop-failure"
        echo ""
        
        wait_and_observe "demo-crashloop-failure" 30
        show_status "demo-crashloop-failure"
        
        echo "🔍 Check Guardian logs:"
        echo "   tail -f logs/guardian.log"
        echo "   tail -f logs/ai.log"
        echo ""
        echo "🧹 Cleanup: kubectl delete pod demo-crashloop-failure"
        ;;
        
    2)
        echo ""
        echo "🔴 Testing: ImagePullBackOff"
        echo "============================"
        echo "This pod will fail to pull a non-existent image"
        echo ""
        
        kubectl apply -f failure-imagepull.yaml
        echo "✅ Pod deployed: demo-imagepull-failure"
        echo ""
        
        wait_and_observe "demo-imagepull-failure" 30
        show_status "demo-imagepull-failure"
        
        echo "🔍 Check Guardian logs:"
        echo "   tail -f logs/guardian.log"
        echo "   tail -f logs/ai.log"
        echo ""
        echo "🧹 Cleanup: kubectl delete pod demo-imagepull-failure"
        ;;
        
    3)
        echo ""
        echo "🔴 Testing: Out of Memory (OOM)"
        echo "==============================="
        echo "This pod will exceed memory limits and get killed"
        echo ""
        
        kubectl apply -f failure-oom.yaml
        echo "✅ Pod deployed: demo-oom-failure"
        echo ""
        
        wait_and_observe "demo-oom-failure" 30
        show_status "demo-oom-failure"
        
        echo "🔍 Check Guardian logs:"
        echo "   tail -f logs/guardian.log"
        echo "   tail -f logs/ai.log"
        echo ""
        echo "🧹 Cleanup: kubectl delete pod demo-oom-failure"
        ;;
        
    4)
        echo ""
        echo "🔴 Testing: All Scenarios"
        echo "========================="
        echo "Running all failure scenarios sequentially"
        echo ""
        
        # Test 1: CrashLoop
        echo "--- Test 1/3: CrashLoopBackOff ---"
        kubectl apply -f failure-crashloop.yaml
        wait_and_observe "demo-crashloop-failure" 20
        show_status "demo-crashloop-failure"
        
        # Test 2: ImagePull
        echo "--- Test 2/3: ImagePullBackOff ---"
        kubectl apply -f failure-imagepull.yaml
        wait_and_observe "demo-imagepull-failure" 20
        show_status "demo-imagepull-failure"
        
        # Test 3: OOM
        echo "--- Test 3/3: Out of Memory ---"
        kubectl apply -f failure-oom.yaml
        wait_and_observe "demo-oom-failure" 20
        show_status "demo-oom-failure"
        
        echo "✅ All tests deployed!"
        echo ""
        echo "📊 View all incidents:"
        echo "   curl http://localhost:8000/incidents | jq"
        echo ""
        echo "🧹 Cleanup all: ./cleanup.sh"
        ;;
        
    5)
        echo ""
        echo "🧹 Cleaning up all test pods..."
        kubectl delete pod demo-crashloop-failure --ignore-not-found=true
        kubectl delete pod demo-imagepull-failure --ignore-not-found=true
        kubectl delete pod demo-oom-failure --ignore-not-found=true
        echo "✅ Cleanup complete!"
        ;;
        
    0)
        echo "Exiting..."
        exit 0
        ;;
        
    *)
        echo "❌ Invalid choice"
        exit 1
        ;;
esac

echo ""
echo "🎯 Next Steps:"
echo "   1. Check Guardian Dashboard: http://localhost:5173"
echo "   2. Check Grafana: http://localhost:3000"
echo "   3. View incidents: curl http://localhost:8000/incidents | jq"
echo "   4. Watch pods: kubectl get pods -w"
echo ""
