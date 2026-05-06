"""
Test script for PrometheusService.
Verifies Prometheus connection and tests all query methods.

Usage:
    cd backend/app/services
    python test_prometheus_service.py

Prerequisites:
    1. Prometheus deployed to Kubernetes
    2. Port-forward active: kubectl port-forward -n monitoring svc/prometheus-service 9090:9090
"""
import sys
import os

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from prometheus_service import PrometheusService


def print_section(title: str):
    """Print a formatted section header."""
    print("\n" + "=" * 60)
    print(f"  {title}")
    print("=" * 60)


def test_connection(service: PrometheusService) -> bool:
    """
    Test Prometheus connection.
    
    Returns:
        True if connected, False otherwise
    """
    print_section("Testing Prometheus Connection")
    
    connected = service.check_connection()
    
    if connected:
        print("✅ Successfully connected to Prometheus")
        return True
    else:
        print("❌ Failed to connect to Prometheus")
        print("\nTroubleshooting:")
        print("1. Ensure Prometheus is running")
        print("2. Check if port-forward is active:")
        print("   kubectl port-forward -n monitoring svc/prometheus-service 9090:9090")
        print("3. Verify Prometheus URL is correct (default: http://localhost:9090)")
        return False


def test_cpu_usage(service: PrometheusService):
    """Test CPU usage metrics query."""
    print_section("Testing CPU Usage Metrics")
    
    # Test without filters
    print("\n📊 Fetching CPU usage (all namespaces)...")
    cpu_metrics = service.get_cpu_usage()
    
    if cpu_metrics:
        print(f"✅ Retrieved {len(cpu_metrics)} CPU metrics")
        
        # Show first 3 examples
        print("\nExample metrics:")
        for i, metric in enumerate(cpu_metrics[:3]):
            print(f"\n  {i+1}. Namespace: {metric['namespace']}")
            print(f"     Pod: {metric['pod']}")
            print(f"     Container: {metric['container']}")
            print(f"     CPU Usage: {metric['cpu_usage']:.4f} cores")
    else:
        print("⚠️  No CPU metrics found")
        print("   This may be normal if no containers are running or metrics aren't available yet")


def test_memory_usage(service: PrometheusService):
    """Test memory usage metrics query."""
    print_section("Testing Memory Usage Metrics")
    
    # Test without filters
    print("\n📊 Fetching memory usage (all namespaces)...")
    memory_metrics = service.get_memory_usage()
    
    if memory_metrics:
        print(f"✅ Retrieved {len(memory_metrics)} memory metrics")
        
        # Show first 3 examples
        print("\nExample metrics:")
        for i, metric in enumerate(memory_metrics[:3]):
            print(f"\n  {i+1}. Namespace: {metric['namespace']}")
            print(f"     Pod: {metric['pod']}")
            print(f"     Container: {metric['container']}")
            print(f"     Memory Usage: {metric['memory_mb']} MB ({metric['memory_bytes']} bytes)")
    else:
        print("⚠️  No memory metrics found")
        print("   This may be normal if no containers are running or metrics aren't available yet")


def test_restart_count(service: PrometheusService):
    """Test pod restart count metrics query."""
    print_section("Testing Pod Restart Count Metrics")
    
    # Test without filters
    print("\n📊 Fetching pod restart counts (all namespaces)...")
    restart_metrics = service.get_pod_restart_count()
    
    if restart_metrics:
        print(f"✅ Retrieved {len(restart_metrics)} restart count metrics")
        
        # Show first 3 examples
        print("\nExample metrics:")
        for i, metric in enumerate(restart_metrics[:3]):
            print(f"\n  {i+1}. Namespace: {metric['namespace']}")
            print(f"     Pod: {metric['pod']}")
            print(f"     Container: {metric['container']}")
            print(f"     Restart Count: {metric['restart_count']}")
    else:
        print("⚠️  No restart count metrics found")
        print("   Note: This requires kube-state-metrics to be installed")


def test_pod_status(service: PrometheusService):
    """Test pod status metrics query."""
    print_section("Testing Pod Status Metrics")
    
    # Test without filters
    print("\n📊 Fetching pod status (all namespaces)...")
    status_metrics = service.get_pod_status()
    
    if status_metrics:
        print(f"✅ Retrieved {len(status_metrics)} pod status metrics")
        
        # Show first 3 examples
        print("\nExample metrics:")
        for i, metric in enumerate(status_metrics[:3]):
            print(f"\n  {i+1}. Namespace: {metric['namespace']}")
            print(f"     Pod: {metric['pod']}")
            print(f"     Phase: {metric['phase']}")
            print(f"     Value: {metric['value']}")
    else:
        print("⚠️  No pod status metrics found")
        print("   Note: This requires kube-state-metrics to be installed")


def test_memory_limits(service: PrometheusService):
    """Test container memory limits query."""
    print_section("Testing Container Memory Limits")
    
    # Test without filters
    print("\n📊 Fetching memory limits (all namespaces)...")
    limit_metrics = service.get_container_memory_limit()
    
    if limit_metrics:
        print(f"✅ Retrieved {len(limit_metrics)} memory limit metrics")
        
        # Show first 3 examples
        print("\nExample metrics:")
        for i, metric in enumerate(limit_metrics[:3]):
            print(f"\n  {i+1}. Namespace: {metric['namespace']}")
            print(f"     Pod: {metric['pod']}")
            print(f"     Container: {metric['container']}")
            print(f"     Memory Limit: {metric['limit_mb']} MB ({metric['limit_bytes']} bytes)")
    else:
        print("⚠️  No memory limit metrics found")
        print("   This may be normal if containers don't have memory limits set")


def test_filtered_queries(service: PrometheusService):
    """Test queries with namespace and pod filters."""
    print_section("Testing Filtered Queries")
    
    # Test with namespace filter
    print("\n📊 Testing namespace filter (namespace='default')...")
    cpu_metrics = service.get_cpu_usage(namespace="default")
    print(f"   Found {len(cpu_metrics)} CPU metrics in 'default' namespace")
    
    # Test with pod filter (if we have any pods)
    if cpu_metrics:
        test_pod = cpu_metrics[0]['pod']
        print(f"\n📊 Testing pod filter (pod='{test_pod}')...")
        pod_metrics = service.get_cpu_usage(pod=test_pod)
        print(f"   Found {len(pod_metrics)} CPU metrics for pod '{test_pod}'")


def main():
    """Main test execution."""
    print("\n" + "=" * 60)
    print("  PROMETHEUS SERVICE TEST SUITE")
    print("=" * 60)
    print("\nThis script tests the PrometheusService integration.")
    print("Ensure Prometheus is running and accessible before testing.")
    
    # Initialize service
    prometheus_url = "http://localhost:9090"
    print(f"\nInitializing PrometheusService with URL: {prometheus_url}")
    service = PrometheusService(base_url=prometheus_url)
    
    # Test connection first
    if not test_connection(service):
        print("\n❌ Cannot proceed without Prometheus connection")
        print("\nSetup Instructions:")
        print("1. Deploy Prometheus to Kubernetes:")
        print("   cd monitoring/prometheus")
        print("   ./deploy.sh")
        print("\n2. Port-forward Prometheus service:")
        print("   kubectl port-forward -n monitoring svc/prometheus-service 9090:9090")
        print("\n3. Run this test again")
        sys.exit(1)
    
    # Run all tests
    try:
        test_cpu_usage(service)
        test_memory_usage(service)
        test_restart_count(service)
        test_pod_status(service)
        test_memory_limits(service)
        test_filtered_queries(service)
        
        # Summary
        print_section("Test Summary")
        print("\n✅ All tests completed successfully!")
        print("\nNext Steps:")
        print("1. Integrate PrometheusService with MonitorService")
        print("2. Use metrics for intelligent incident detection")
        print("3. Enhance AI diagnosis with metric context")
        
    except Exception as e:
        print(f"\n❌ Test failed with error: {str(e)}")
        sys.exit(1)


if __name__ == "__main__":
    main()
