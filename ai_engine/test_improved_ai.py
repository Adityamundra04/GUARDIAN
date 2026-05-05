"""
Test script for improved AI diagnosis.
Demonstrates better context and specific answers.
"""
import sys
import os

# Add paths for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../backend/app/services'))
sys.path.insert(0, os.path.dirname(__file__))

from ai_service import AIService


def test_crashloop_diagnosis():
    """Test CrashLoopBackOff diagnosis with full context."""
    print("=" * 60)
    print("  Test 1: CrashLoopBackOff with Full Context")
    print("=" * 60)
    print()
    
    ai_service = AIService()
    
    # Simulate issue from Kubernetes
    issue = {
        "name": "my-app-deployment-abc123",
        "namespace": "production",
        "issue": "CrashLoopBackOff"
    }
    
    print("📥 Input Issue:")
    print(f"   Pod: {issue['name']}")
    print(f"   Namespace: {issue['namespace']}")
    print(f"   Error: {issue['issue']}")
    print()
    
    # Get diagnosis
    diagnosis = ai_service.diagnose_issue(issue)
    
    print()
    print("📤 AI Diagnosis:")
    print(f"   Cause: {diagnosis['cause']}")
    print(f"   Fix: {diagnosis['solution']}")
    print()


def test_high_restart_diagnosis():
    """Test high restart count diagnosis."""
    print("=" * 60)
    print("  Test 2: High Restart Count")
    print("=" * 60)
    print()
    
    ai_service = AIService()
    
    issue = {
        "name": "backend-service-xyz789",
        "namespace": "default",
        "issue": "High restart count: 5"
    }
    
    print("📥 Input Issue:")
    print(f"   Pod: {issue['name']}")
    print(f"   Namespace: {issue['namespace']}")
    print(f"   Error: {issue['issue']}")
    print()
    
    diagnosis = ai_service.diagnose_issue(issue)
    
    print()
    print("📤 AI Diagnosis:")
    print(f"   Cause: {diagnosis['cause']}")
    print(f"   Fix: {diagnosis['solution']}")
    print()


def test_image_pull_error():
    """Test ImagePullBackOff diagnosis."""
    print("=" * 60)
    print("  Test 3: ImagePullBackOff")
    print("=" * 60)
    print()
    
    ai_service = AIService()
    
    issue = {
        "name": "frontend-app-def456",
        "namespace": "staging",
        "issue": "Error: ImagePullBackOff"
    }
    
    print("📥 Input Issue:")
    print(f"   Pod: {issue['name']}")
    print(f"   Namespace: {issue['namespace']}")
    print(f"   Error: {issue['issue']}")
    print()
    
    diagnosis = ai_service.diagnose_issue(issue)
    
    print()
    print("📤 AI Diagnosis:")
    print(f"   Cause: {diagnosis['cause']}")
    print(f"   Fix: {diagnosis['solution']}")
    print()


def test_string_fallback():
    """Test backward compatibility with string input."""
    print("=" * 60)
    print("  Test 4: String Input (Backward Compatibility)")
    print("=" * 60)
    print()
    
    ai_service = AIService()
    
    issue_string = "[default] test-pod → CrashLoopBackOff"
    
    print("📥 Input Issue (string):")
    print(f"   {issue_string}")
    print()
    
    diagnosis = ai_service.diagnose_issue(issue_string)
    
    print()
    print("📤 AI Diagnosis:")
    print(f"   Cause: {diagnosis['cause']}")
    print(f"   Fix: {diagnosis['solution']}")
    print()


def compare_prompts():
    """Show the difference between old and new prompts."""
    print("=" * 60)
    print("  Prompt Comparison")
    print("=" * 60)
    print()
    
    ai_service = AIService()
    
    issue = {
        "name": "my-app",
        "namespace": "production",
        "issue": "CrashLoopBackOff"
    }
    
    print("🆕 NEW PROMPT (with context):")
    print("-" * 60)
    new_prompt = ai_service.build_diagnosis_prompt(issue)
    print(new_prompt)
    print()
    
    print("📊 Key Improvements:")
    print("   ✅ Includes pod name, namespace, and error separately")
    print("   ✅ Explicit rules for specific answers")
    print("   ✅ Instructs to explain WHY (not just what)")
    print("   ✅ Requests direct fixes (not generic advice)")
    print("   ✅ Emphasizes short, actionable responses")
    print()


if __name__ == "__main__":
    print()
    print("🧪 Testing Improved AI Diagnosis")
    print()
    
    # Show prompt improvements
    compare_prompts()
    
    print("\n" + "=" * 60)
    print("  Running Diagnosis Tests")
    print("=" * 60)
    print()
    print("⚠️  Note: These tests require Ollama to be running")
    print("   Start with: ollama serve")
    print()
    
    try:
        # Test 1: CrashLoopBackOff
        test_crashloop_diagnosis()
        
        # Test 2: High restart count
        test_high_restart_diagnosis()
        
        # Test 3: ImagePullBackOff
        test_image_pull_error()
        
        # Test 4: String fallback
        test_string_fallback()
        
        print("=" * 60)
        print("  ✅ All Tests Completed")
        print("=" * 60)
        print()
        print("💡 Expected Improvements:")
        print("   • More specific root causes (not generic)")
        print("   • Actionable fixes (not general advice)")
        print("   • Shorter, focused responses")
        print("   • Better understanding of WHY issues occur")
        print()
        
    except Exception as e:
        print(f"❌ Test failed: {e}")
        print()
        print("Troubleshooting:")
        print("   1. Ensure Ollama is running: ollama serve")
        print("   2. Ensure llama3.1 is installed: ollama pull llama3.1")
        print("   3. Check Ollama is accessible: curl http://localhost:11434")
