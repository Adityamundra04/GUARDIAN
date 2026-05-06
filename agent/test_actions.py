"""
Test script for action execution layer.
Demonstrates safety rules and action execution.
"""
from safety_rules import SafetyRules
from executor import ActionExecutor


def test_safety_rules():
    """Test safety rule decision making."""
    print("=" * 60)
    print("  Test 1: Safety Rules")
    print("=" * 60)
    print()
    
    # Test CrashLoopBackOff
    issue1 = {
        "name": "my-app-abc123",
        "namespace": "default",
        "issue": "CrashLoopBackOff"
    }
    
    print("📥 Issue 1: CrashLoopBackOff in default namespace")
    action1 = SafetyRules.decide_action(issue1)
    if action1:
        print(f"   Action: {action1['type']}")
        print(f"   Safe: {SafetyRules.is_action_safe(action1)}")
    print()
    
    # Test ImagePullBackOff
    issue2 = {
        "name": "frontend-xyz789",
        "namespace": "staging",
        "issue": "Error: ImagePullBackOff"
    }
    
    print("📥 Issue 2: ImagePullBackOff in staging namespace")
    action2 = SafetyRules.decide_action(issue2)
    if action2:
        print(f"   Action: {action2['type']}")
        print(f"   Safe: {SafetyRules.is_action_safe(action2)}")
    print()
    
    # Test production (blocked)
    issue3 = {
        "name": "prod-app-def456",
        "namespace": "production",
        "issue": "CrashLoopBackOff"
    }
    
    print("📥 Issue 3: CrashLoopBackOff in production namespace")
    action3 = SafetyRules.decide_action(issue3)
    if action3:
        print(f"   Action: {action3['type']}")
        print(f"   Safe: {SafetyRules.is_action_safe(action3)}")
    else:
        print("   ⚠️  No action (namespace blocked)")
    print()
    
    # Test unknown issue
    issue4 = {
        "name": "test-app-ghi012",
        "namespace": "default",
        "issue": "UnknownError"
    }
    
    print("📥 Issue 4: UnknownError in default namespace")
    action4 = SafetyRules.decide_action(issue4)
    if action4:
        print(f"   Action: {action4['type']}")
    else:
        print("   ℹ️  No action defined for this issue type")
    print()


def test_safety_config():
    """Test safety configuration summary."""
    print("=" * 60)
    print("  Test 2: Safety Configuration")
    print("=" * 60)
    print()
    
    config = SafetyRules.get_safe_actions_summary()
    
    print("📋 Safe Actions:")
    for issue, action in config["safe_actions"].items():
        print(f"   {issue} → {action}")
    print()
    
    print("⚠️  Manual Approval Required:")
    for action in config["manual_approval_required"]:
        print(f"   {action}")
    print()
    
    print("✅ Allowed Namespaces:")
    for namespace in config["allowed_namespaces"]:
        print(f"   {namespace}")
    print()


def test_action_mapping():
    """Test issue to action mapping."""
    print("=" * 60)
    print("  Test 3: Issue → Action Mapping")
    print("=" * 60)
    print()
    
    test_cases = [
        ("CrashLoopBackOff", "default"),
        ("ImagePullBackOff", "staging"),
        ("High restart count: 5", "default"),
        ("Terminated with exit code: 1", "testing"),
        ("Error: ImagePullBackOff", "development"),
    ]
    
    for issue_type, namespace in test_cases:
        issue = {
            "name": "test-pod",
            "namespace": namespace,
            "issue": issue_type
        }
        
        action = SafetyRules.decide_action(issue)
        if action:
            print(f"✅ {issue_type}")
            print(f"   Namespace: {namespace}")
            print(f"   Action: {action['type']}")
            print(f"   Safe: {SafetyRules.is_action_safe(action)}")
        else:
            print(f"❌ {issue_type}")
            print(f"   Namespace: {namespace}")
            print(f"   No action")
        print()


if __name__ == "__main__":
    print()
    print("🧪 Testing Action Execution Layer")
    print()
    
    try:
        # Test 1: Safety rules
        test_safety_rules()
        
        # Test 2: Safety configuration
        test_safety_config()
        
        # Test 3: Action mapping
        test_action_mapping()
        
        print("=" * 60)
        print("  ✅ All Tests Completed")
        print("=" * 60)
        print()
        print("💡 Key Takeaways:")
        print("   • CrashLoopBackOff → restart_pod")
        print("   • ImagePullBackOff → delete_pod")
        print("   • Production namespace blocked by default")
        print("   • Unknown issues have no action")
        print("   • All actions logged before execution")
        print()
        
    except Exception as e:
        print(f"❌ Test failed: {e}")
        print()
        print("Note: This test only checks safety rules logic.")
        print("Actual Kubernetes actions require cluster access.")
