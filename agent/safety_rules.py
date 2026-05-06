"""
Safety rules for Guardian action execution.
Defines which actions are safe to execute for different issue types.
"""
from typing import Optional, Dict
import time


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
    
    # Retry limits and cooldown
    MAX_RETRY_ATTEMPTS = 3  # Maximum retry attempts per pod
    COOLDOWN_SECONDS = 60  # Cooldown period between retries
    
    # Track retry attempts and last action time
    # Format: {"namespace/pod-name": {"attempts": count, "last_action": timestamp}}
    _retry_tracker: Dict[str, Dict] = {}
    
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
        pod_identifier = f"{namespace}/{pod_name}"
        
        # Check if namespace is allowed for auto-execution
        if namespace not in SafetyRules.ALLOWED_NAMESPACES:
            print(f"[Safety] Auto-execution disabled for namespace: {namespace}")
            return None
        
        # Check retry limit
        if not SafetyRules._check_retry_limit(pod_identifier):
            print(f"[Safety] Retry limit reached for {pod_name} - skipping action")
            return None
        
        # Check cooldown
        if not SafetyRules._check_cooldown(pod_identifier):
            print(f"[Safety] Cooldown active for {pod_name} - skipping action")
            return None
        
        # Find matching action for issue type
        action_type = None
        for issue_pattern, action in SafetyRules.SAFE_ACTIONS.items():
            if issue_pattern in issue_type:
                action_type = action
                break
        
        if not action_type:
            print(f"[Safety] No safe action defined for issue: {issue_type}")
            return None
        
        # Check if action requires manual approval
        if action_type in SafetyRules.MANUAL_APPROVAL_REQUIRED:
            print(f"[Safety] Action {action_type} requires manual approval")
            return None
        
        # Return action details
        action = {
            "type": action_type,
            "namespace": namespace,
            "pod_name": pod_name,
            "issue_type": issue_type
        }
        
        print(f"[Safety] Safe action decided: {action_type} for pod {pod_name}")
        
        return action
    
    @staticmethod
    def _check_retry_limit(pod_identifier: str) -> bool:
        """
        Check if retry limit has been reached for a pod.
        
        Args:
            pod_identifier: Format "namespace/pod-name"
        
        Returns:
            True if retry is allowed, False if limit reached
        """
        if pod_identifier not in SafetyRules._retry_tracker:
            return True
        
        attempts = SafetyRules._retry_tracker[pod_identifier].get("attempts", 0)
        return attempts < SafetyRules.MAX_RETRY_ATTEMPTS
    
    @staticmethod
    def _check_cooldown(pod_identifier: str) -> bool:
        """
        Check if cooldown period has passed since last action.
        
        Args:
            pod_identifier: Format "namespace/pod-name"
        
        Returns:
            True if cooldown passed, False if still in cooldown
        """
        if pod_identifier not in SafetyRules._retry_tracker:
            return True
        
        last_action = SafetyRules._retry_tracker[pod_identifier].get("last_action", 0)
        time_since_last = time.time() - last_action
        return time_since_last >= SafetyRules.COOLDOWN_SECONDS
    
    @staticmethod
    def record_action(pod_identifier: str) -> None:
        """
        Record an action execution for retry tracking.
        
        Args:
            pod_identifier: Format "namespace/pod-name"
        """
        if pod_identifier not in SafetyRules._retry_tracker:
            SafetyRules._retry_tracker[pod_identifier] = {"attempts": 0, "last_action": 0}
        
        SafetyRules._retry_tracker[pod_identifier]["attempts"] += 1
        SafetyRules._retry_tracker[pod_identifier]["last_action"] = time.time()
        
        attempts = SafetyRules._retry_tracker[pod_identifier]["attempts"]
        print(f"[Safety] Action recorded for {pod_identifier} (attempt {attempts}/{SafetyRules.MAX_RETRY_ATTEMPTS})")
    
    @staticmethod
    def reset_tracker(pod_identifier: str) -> None:
        """
        Reset retry tracker for a pod (when issue is resolved).
        
        Args:
            pod_identifier: Format "namespace/pod-name"
        """
        if pod_identifier in SafetyRules._retry_tracker:
            del SafetyRules._retry_tracker[pod_identifier]
            print(f"[Safety] Retry tracker reset for {pod_identifier}")
    
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
            print(f"[Safety] Action blocked: namespace {namespace} not in allowed list")
            return False
        
        # Check if action is in safe list
        if action_type not in SafetyRules.SAFE_ACTIONS.values():
            print(f"[Safety] Action blocked: {action_type} not in safe actions list")
            return False
        
        # Check if action requires manual approval
        if action_type in SafetyRules.MANUAL_APPROVAL_REQUIRED:
            print(f"[Safety] Action blocked: {action_type} requires manual approval")
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
            "allowed_namespaces": SafetyRules.ALLOWED_NAMESPACES,
            "max_retry_attempts": SafetyRules.MAX_RETRY_ATTEMPTS,
            "cooldown_seconds": SafetyRules.COOLDOWN_SECONDS
        }
