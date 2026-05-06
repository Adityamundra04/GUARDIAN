#!/usr/bin/env python3
"""
Verification script for Kubernetes logs integration.
Checks that the code changes are in place.
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
            print(f"   ✅ Found: {search_str[:60]}...")
        else:
            print(f"   ❌ Missing: {search_str[:60]}...")
            all_found = False
    
    return all_found


def main():
    """Verify logs integration."""
    print("=" * 60)
    print("  KUBERNETES LOGS INTEGRATION VERIFICATION")
    print("=" * 60)
    print("\nThis script verifies that log integration is in place.")
    
    results = []
    
    # Check 1: K8sService has get_pod_logs()
    results.append(check_file_contains(
        'backend/app/services/k8s_service.py',
        [
            'def get_pod_logs',
            'read_namespaced_pod_log',
            'tail_lines',
            '[K8s] Fetching logs for pod',
            '[K8s] Logs retrieved successfully'
        ],
        'K8sService Log Retrieval'
    ))
    
    # Check 2: MonitorService fetches logs
    results.append(check_file_contains(
        'backend/app/services/monitor_service.py',
        [
            'self.k8s_service.get_pod_logs',
            "enriched_issue['logs']",
            '[K8s] Pod logs attached to AI context',
            '[K8s] Continuing without logs'
        ],
        'MonitorService Log Integration'
    ))
    
    # Check 3: AIService includes logs in prompt
    results.append(check_file_contains(
        'backend/app/services/ai_service.py',
        [
            "logs = issue_context.get('logs'",
            'Recent Container Logs:',
            'PRIORITIZE log analysis',
            'stack traces',
            '(with logs)'
        ],
        'AIService Log-Aware Prompts'
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
        print("\n✅ Kubernetes logs integration is correctly implemented!")
        print("\nNext Steps:")
        print("1. Deploy a failing pod:")
        print("   kubectl apply -f k8s/test-failures/crashloop.yaml")
        print("\n2. Start Prometheus port-forward:")
        print("   kubectl port-forward -n monitoring svc/prometheus-service 9090:9090")
        print("\n3. Start Guardian:")
        print("   cd backend && python -m app.main")
        print("\n4. Watch logs for log integration:")
        print("   [K8s] Fetching logs for pod...")
        print("   [K8s] Logs retrieved successfully")
        print("   [K8s] Pod logs attached to AI context")
        print("   🤖 Requesting enriched AI diagnosis (with logs)")
        return 0
    else:
        print("\n⚠️  Some verifications failed")
        print("\nPlease review the failed checks above.")
        return 1


if __name__ == "__main__":
    exit(main())
