#!/usr/bin/env python3
"""
Test script to verify metrics-aware AI integration.
Tests that MonitorService enriches issues with Prometheus metrics before AI diagnosis.
"""
import sys
import os

# Add backend to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'backend'))

from backend.app.services.monitor_service import MonitorService


def print_section(title):
    """Print formatted section header."""
    print("\n" + "=" * 60)
    print(f"  {title}")
    print("=" * 60)


def test_metric_enrichment():
    """Test that issues are enriched with Prometheus metrics."""
    print_section("Testing Metrics-Aware AI Integration")
    
    # Initialize MonitorService
    print("\n📦 Initializing MonitorService...")
    monitor = MonitorService()
    
    # Verify PrometheusService is initialized
    if hasattr(monitor, 'prometheus_service'):
        print("✅ PrometheusService initialized")
    else:
        print("❌ PrometheusService NOT initialized")
        return False
    
    # Create a test issue
    print("\n🧪 Creating test issue...")
    test_issue = {
        'name': 'test-pod-123',
        'namespace': 'default',
        'issue': 'CrashLoopBackOff'
    }
    
    print(f"   Pod: {test_issue['name']}")
    print(f"   Namespace: {test_issue['namespace']}")
    print(f"   Issue: {test_issue['issue']}")
    
    # Test metric enrichment
    print("\n📊 Testing metric enrichment...")
    try:
        enriched_issue = monitor._enrich_issue_with_metrics(test_issue)
        
        print("\n✅ Metric enrichment completed!")
        print("\nEnriched Issue Context:")
        print(f"   Pod: {enriched_issue.get('name')}")
        print(f"   Namespace: {enriched_issue.get('namespace')}")
        print(f"   Issue: {enriched_issue.get('issue')}")
        print(f"   CPU Usage: {enriched_issue.get('cpu_usage', 'N/A')}")
        print(f"   Memory Usage: {enriched_issue.get('memory_mb', 'N/A')}")
        print(f"   Restart Count: {enriched_issue.get('restart_count', 'N/A')}")
        
        # Verify metrics are present (even if N/A)
        has_cpu = 'cpu_usage' in enriched_issue
        has_memory = 'memory_mb' in enriched_issue
        has_restarts = 'restart_count' in enriched_issue
        
        print("\n📋 Verification:")
        print(f"   CPU metric present: {'✅' if has_cpu else '❌'}")
        print(f"   Memory metric present: {'✅' if has_memory else '❌'}")
        print(f"   Restart count present: {'✅' if has_restarts else '❌'}")
        
        if has_cpu and has_memory and has_restarts:
            print("\n🎉 All metrics are present in enriched context!")
            return True
        else:
            print("\n⚠️  Some metrics are missing")
            return False
    
    except Exception as e:
        print(f"\n❌ Error during metric enrichment: {str(e)}")
        return False


def test_ai_service_integration():
    """Test that AIService receives enriched context."""
    print_section("Testing AIService Integration")
    
    from backend.app.services.ai_service import AIService
    
    print("\n📦 Initializing AIService...")
    ai_service = AIService()
    
    # Create enriched issue context
    enriched_issue = {
        'name': 'test-pod-123',
        'namespace': 'default',
        'issue': 'CrashLoopBackOff',
        'cpu_usage': '0.0234 cores',
        'memory_mb': '128.5 MB',
        'restart_count': 5
    }
    
    print("\n🧪 Testing AI prompt generation with metrics...")
    try:
        prompt = ai_service.build_diagnosis_prompt(enriched_issue)
        
        # Verify metrics are in prompt
        has_cpu_in_prompt = 'CPU Usage' in prompt or 'cpu_usage' in prompt.lower()
        has_memory_in_prompt = 'Memory Usage' in prompt or 'memory' in prompt.lower()
        has_restarts_in_prompt = 'Restart Count' in prompt or 'restart' in prompt.lower()
        
        print("\n📋 Prompt Verification:")
        print(f"   CPU in prompt: {'✅' if has_cpu_in_prompt else '❌'}")
        print(f"   Memory in prompt: {'✅' if has_memory_in_prompt else '❌'}")
        print(f"   Restarts in prompt: {'✅' if has_restarts_in_prompt else '❌'}")
        
        if has_cpu_in_prompt and has_memory_in_prompt and has_restarts_in_prompt:
            print("\n🎉 AI prompt includes all metrics!")
            print("\n📄 Sample Prompt (first 500 chars):")
            print(prompt[:500] + "...")
            return True
        else:
            print("\n⚠️  Some metrics missing from prompt")
            return False
    
    except Exception as e:
        print(f"\n❌ Error testing AI integration: {str(e)}")
        return False


def main():
    """Run all tests."""
    print("\n" + "=" * 60)
    print("  METRICS-AWARE AI INTEGRATION TEST SUITE")
    print("=" * 60)
    print("\nThis script verifies that Guardian enriches AI context with Prometheus metrics.")
    
    # Test 1: Metric Enrichment
    test1_passed = test_metric_enrichment()
    
    # Test 2: AI Service Integration
    test2_passed = test_ai_service_integration()
    
    # Summary
    print_section("Test Summary")
    
    print("\n📊 Results:")
    print(f"   Metric Enrichment: {'✅ PASS' if test1_passed else '❌ FAIL'}")
    print(f"   AI Service Integration: {'✅ PASS' if test2_passed else '❌ FAIL'}")
    
    if test1_passed and test2_passed:
        print("\n🎉 All tests passed!")
        print("\n✅ Metrics-aware AI integration is working correctly!")
        print("\nNext Steps:")
        print("1. Ensure Prometheus is running and port-forwarded")
        print("2. Deploy a failing pod to test end-to-end")
        print("3. Watch Guardian logs for metrics-aware diagnosis")
        return 0
    else:
        print("\n⚠️  Some tests failed")
        print("\nTroubleshooting:")
        print("1. Verify MonitorService imports PrometheusService")
        print("2. Verify AIService prompt includes metrics")
        print("3. Check for any import errors")
        return 1


if __name__ == "__main__":
    sys.exit(main())
