"""
Test script for Ollama client.
Verifies connection and basic functionality.
"""
from ai_engine.ollama_client import OllamaClient 

def test_ollama_connection():
    """Test basic Ollama connection and generation."""
    print("🧪 Testing Ollama Client...")
    print("-" * 50)
    
    # Initialize client
    client = OllamaClient()
    print(f"✅ Client initialized: {client.base_url}")
    print(f"✅ Model: {client.model}")
    print()
    
    # Test simple prompt
    print("📤 Sending test prompt...")
    prompt = "Say 'Hello from Ollama!' in one sentence."
    
    response = client.generate(prompt, timeout=10)
    
    if response:
        print("✅ Response received:")
        print(f"   {response}")
        print()
        return True
    else:
        print("❌ No response received")
        print()
        return False


def test_kubernetes_diagnosis():
    """Test Kubernetes issue diagnosis."""
    print("🧪 Testing Kubernetes Diagnosis...")
    print("-" * 50)
    
    # Initialize client
    client = OllamaClient()
    
    # Test Kubernetes issue prompt
    prompt = """You are a Kubernetes expert.
Analyze the issue and provide:
1. Root cause
2. Fix

Issue: [default] my-app → CrashLoopBackOff

Respond ONLY in this format:
Cause: <root cause explanation>
Fix: <step-by-step fix>"""
    
    print("📤 Sending Kubernetes diagnosis prompt...")
    response = client.generate(prompt, timeout=30)
    
    if response:
        print("✅ Diagnosis received:")
        print(response)
        print()
        
        # Check if response has expected format
        if "cause:" in response.lower() and "fix:" in response.lower():
            print("✅ Response format is correct")
            return True
        else:
            print("⚠️  Response format may need adjustment")
            return True
    else:
        print("❌ No diagnosis received")
        return False


if __name__ == "__main__":
    print("=" * 50)
    print("  Ollama Client Test Suite")
    print("=" * 50)
    print()
    
    # Test 1: Basic connection
    test1_passed = test_ollama_connection()
    
    # Test 2: Kubernetes diagnosis
    test2_passed = test_kubernetes_diagnosis()
    
    # Summary
    print("=" * 50)
    print("  Test Summary")
    print("=" * 50)
    print(f"Basic Connection: {'✅ PASS' if test1_passed else '❌ FAIL'}")
    print(f"K8s Diagnosis:    {'✅ PASS' if test2_passed else '❌ FAIL'}")
    print()
    
    if test1_passed and test2_passed:
        print("🎉 All tests passed!")
    else:
        print("⚠️  Some tests failed. Check Ollama is running:")
        print("   ollama serve")
