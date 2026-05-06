"""
Safety rules for Guardian action execution.
Defines which actions are safe to execute for different issue types.
"""
from typing import Optional, Dict


class SafetyRules:
    """
    Defines safe actions for different Kubernetes issues.
    Ensures only known, safe operations are executed automatically.
    """
    
    # Map of issue types to safe actions
    SAFE_ACTIONS = {
        "CrashLoopBackOff": "restart_pod",
        "ImagePullBackOff": "delete_pod",
        "Error: ImagePullBackOff": "delete_pod",
        "High restart count": "restart_pod",
        "Terminated with exit code": "restart_pod",
    }
    
    # Actions that require manual approval (not auto-executed)
    MANUAL_APPROVAL_REQUIRED = [
        "scale_deployment",
        "delete_deployment",
        "update_config",
    ]
    
    # Namespaces where auto-execution is allowed
    ALLOWED_NAMESPACES = [
        "default",
        "development",
        "staging",
        "testing",
        # "production",  # Uncomment to enable production auto-fix
    ]
    
    @staticmethod
    def decide_action(issue: Dict[str, str]) -> Optional[Dict[str, str]]:
        """
        Decide what action to take for a given issue.
        
        Args:
            issue: Dictionary with name, namespace, and issue description
        
        Returns:
            Action dictionary with type, namespace, pod_name, or None if no action
        """
        issue_type = issue.get("issue", "")
        namespace = issue.get("namespace", "")
        pod_name = issue.get("name", "")
        
        # Check if namespace is allowed for auto-execution
        if namespace not in SafetyRules.ALLOWED_NAMESPACES:
            print(f"⚠️  Auto-execution disabled for namespace: {namespace}")
            return None
        
        # Find matching action for issue type
        action_type = None
        for issue_pattern, action in SafetyRules.SAFE_ACTIONS.items():
            if issue_pattern in issue_type:
                action_type = action
                break
        
        if not action_type:
            print(f"ℹ️  No safe action defined for issue: {issue_type}")
            return None
        
        # Check if action requires manual approval
        if action_type in SafetyRules.MANUAL_APPROVAL_REQUIRED:
            print(f"⚠️  Action {action_type} requires manual approval")
            return None
        
        # Return action details
        action = {
            "type": action_type,
            "namespace": namespace,
            "pod_name": pod_name,
            "issue_type": issue_type
        }
        
        print(f"✅ Safe action decided: {action_type} for pod {pod_name}")
        
        return action
    
    @staticmethod
    def is_action_safe(action: Dict[str, str]) -> bool:
        """
        Verify if an action is safe to execute.
        
        Args:
            action: Action dictionary
        
        Returns:
            True if safe, False otherwise
        """
        action_type = action.get("type", "")
        namespace = action.get("namespace", "")
        
        # Check namespace
        if namespace not in SafetyRules.ALLOWED_NAMESPACES:
            print(f"❌ Action blocked: namespace {namespace} not in allowed list")
            return False
        
        # Check if action is in safe list
        if action_type not in SafetyRules.SAFE_ACTIONS.values():
            print(f"❌ Action blocked: {action_type} not in safe actions list")
            return False
        
        # Check if action requires manual approval
        if action_type in SafetyRules.MANUAL_APPROVAL_REQUIRED:
            print(f"❌ Action blocked: {action_type} requires manual approval")
            return False
        
        return True
    
    @staticmethod
    def get_safe_actions_summary() -> Dict[str, any]:
        """
        Get a summary of configured safety rules.
        
        Returns:
            Dictionary with safety configuration
        """
        return {
            "safe_actions": SafetyRules.SAFE_ACTIONS,
            "manual_approval_required": SafetyRules.MANUAL_APPROVAL_REQUIRED,
            "allowed_namespaces": SafetyRules.ALLOWED_NAMESPACES
        }
