#!/usr/bin/env python3
"""
Simple verification script for metrics-aware AI integration.
Checks that the code changes are in place without running the full system.
"""
import os


def check_file_contains(filepath, search_strings, description):
    """Check if file contains all search strings."""
    print(f"\n📄 Checking {description}...")
    print(f"   File: {filepath}")
    
    if not os.path.exists(filepath):
        print(f"   ❌ File not found!")
        return False
    
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    all_found = True
    for search_str in search_strings:
        if search_str in content:
            print(f"   ✅ Found: {search_str[:50]}...")
        else:
            print(f"   ❌ Missing: {search_str[:50]}...")
            all_found = False
    
    return all_found


def main():
    """Verify metrics-aware AI integration."""
    print("=" * 60)
    print("  METRICS-AWARE AI INTEGRATION VERIFICATION")
    print("=" * 60)
    print("\nThis script verifies that code changes are in place.")
    
    results = []
    
    # Check 1: MonitorService imports PrometheusService
    results.append(check_file_contains(
        'backend/app/services/monitor_service.py',
        [
            'from backend.app.services.prometheus_service import PrometheusService',
            'self.prometheus_service = PrometheusService()',
            'def _enrich_issue_with_metrics',
            'enriched_issue = self._enrich_issue_with_metrics(issue)'
        ],
        'MonitorService Integration'
    ))
    
    # Check 2: AIService includes metrics in prompt
    results.append(check_file_contains(
        'backend/app/services/ai_service.py',
        [
            'cpu_usage = issue_context.get',
            'memory_mb = issue_context.get',
            'restart_count = issue_context.get',
            'CPU Usage:',
            'Memory Usage:',
            'Restart Count:',
            'metrics-aware'
        ],
        'AIService Metrics Integration'
    ))
    
    # Check 3: PrometheusService exists
    results.append(check_file_contains(
        'backend/app/services/prometheus_service.py',
        [
            'class PrometheusService',
            'def get_cpu_usage',
            'def get_memory_usage',
            'def get_pod_restart_count'
        ],
        'PrometheusService Implementation'
    ))
    
    # Summary
    print("\n" + "=" * 60)
    print("  VERIFICATION SUMMARY")
    print("=" * 60)
    
    passed = sum(results)
    total = len(results)
    
    print(f"\n📊 Results: {passed}/{total} checks passed")
    
    if passed == total:
        print("\n🎉 All verifications passed!")
        print("\n✅ Metrics-aware AI integration is correctly implemented!")
        print("\nNext Steps:")
        print("1. Ensure Prometheus is running:")
        print("   kubectl port-forward -n monitoring svc/prometheus-service 9090:9090")
        print("\n2. Deploy a failing pod:")
        print("   kubectl apply -f k8s/test-failures/crashloop.yaml")
        print("\n3. Start Guardian:")
        print("   cd backend && python -m app.main")
        print("\n4. Watch logs for metrics:")
        print("   [Prometheus] CPU usage: ...")
        print("   [Prometheus] Memory usage: ...")
        print("   [Prometheus] Restart count: ...")
        print("   [AI] Metrics-aware diagnosis completed")
        return 0
    else:
        print("\n⚠️  Some verifications failed")
        print("\nPlease review the failed checks above.")
        return 1


if __name__ == "__main__":
    exit(main())
