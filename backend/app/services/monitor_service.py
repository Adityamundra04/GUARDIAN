"""
Monitoring service for Guardian.
Continuously monitors Kubernetes cluster and creates incidents automatically.
"""
from typing import Optional, Dict, Set, List
from backend.app.services.k8s_service import K8sService
from backend.app.services.ai_service import AIService
from backend.app.models.incident import Incident
from backend.app.api.incidents import incidents_db


class MonitorService:
    """
    Service for monitoring Kubernetes cluster and managing incidents.
    Detects issues and automatically creates incidents with AI-powered diagnosis.
    """
    
    def __init__(self):
        """
        Initialize monitoring service.
        Sets up Kubernetes service, AI service, and tracking for active issues.
        """
        self.k8s_service = K8sService()
        self.ai_service = AIService()
        
        # Track active issues to avoid duplicates
        # Format: "namespace/pod-name"
        self.active_issues: Set[str] = set()
    
    def check_system(self) -> List[Dict[str, str]]:
        """
        Check Kubernetes cluster for problematic pods.
        
        Returns:
            List of all detected issues (empty list if none or error)
        """
        try:
            # Get all problematic pods from Kubernetes
            problematic_pods = self.k8s_service.get_problematic_pods()
            return problematic_pods if problematic_pods else []
        except Exception as e:
            print(f"❌ Error checking system: {e}")
            return []
    
    def create_incident_from_issue(self, issue: Dict[str, str]) -> Optional[Incident]:
        """
        Create an incident from a detected Kubernetes issue.
        Avoids creating duplicate incidents for the same pod.
        Uses AI to diagnose root cause and suggest fixes.
        
        Args:
            issue: Dictionary with name, namespace, and issue description
        
        Returns:
            Created Incident object, or None if duplicate
        """
        # Create unique identifier for this pod issue
        pod_identifier = f"{issue['namespace']}/{issue['name']}"
        
        # Check if we already have an active incident for this pod
        if pod_identifier in self.active_issues:
            print(f"⏭️  Skipping duplicate incident for {pod_identifier}")
            return None
        
        # Create cleaner incident message format: [namespace] pod-name → issue
        incident_message = f"[{issue['namespace']}] {issue['name']} → {issue['issue']}"
        
        # Get AI diagnosis for the issue
        diagnosis = {"cause": "Unknown", "solution": "Manual investigation required"}
        try:
            diagnosis = self.ai_service.diagnose_issue(incident_message)
        except Exception as e:
            print(f"❌ AI diagnosis failed: {e}")
        
        # Create incident with AI-enriched data
        incident = Incident(
            issue=incident_message,
            status="detected",
            cause=diagnosis.get("cause", "Unknown"),
            solution=diagnosis.get("solution", "Manual investigation required")
        )
        
        # Add to in-memory database
        incidents_db.append(incident)
        
        # Track this issue as active
        self.active_issues.add(pod_identifier)
        
        print(f"✅ Incident created: {incident.id} - {incident.issue}")
        
        return incident
    
    def remove_resolved_issues(self, current_issues: List[Dict[str, str]]) -> None:
        """
        Remove resolved issues from active tracking.
        Compares current problematic pods with tracked issues and removes resolved ones.
        
        Args:
            current_issues: List of currently detected issues
        """
        # Build set of currently problematic pods
        current_pods = set()
        for issue in current_issues:
            pod_identifier = f"{issue['namespace']}/{issue['name']}"
            current_pods.add(pod_identifier)
        
        # Find resolved issues (in active_issues but not in current_pods)
        resolved_issues = self.active_issues - current_pods
        
        # Remove resolved issues from tracking
        if resolved_issues:
            for resolved in resolved_issues:
                self.active_issues.discard(resolved)
                print(f"🔄 Resolved issue removed from tracking: {resolved}")
    
    def monitor_and_create_incidents(self) -> None:
        """
        Check system and automatically create incidents for detected issues.
        This is the main monitoring loop function.
        
        Handles:
        - Multiple issues simultaneously
        - Duplicate prevention
        - Automatic cleanup of resolved issues
        - Error safety
        """
        try:
            # Check for all issues in the cluster
            issues = self.check_system()
            
            # Remove resolved issues from tracking
            self.remove_resolved_issues(issues)
            
            # Handle each detected issue
            if issues:
                print(f"🔍 Found {len(issues)} issue(s) in cluster")
                
                for issue in issues:
                    try:
                        # Log detection
                        print(f"⚠️  Issue detected: [{issue['namespace']}] {issue['name']} - {issue['issue']}")
                        
                        # Create incident (will skip if duplicate)
                        self.create_incident_from_issue(issue)
                        
                    except Exception as e:
                        # Log error but continue processing other issues
                        print(f"❌ Error creating incident for {issue.get('name', 'unknown')}: {e}")
            else:
                # No issues detected - system healthy
                pass
                
        except Exception as e:
            # Catch all errors to prevent monitoring loop from crashing
            print(f"❌ Error in monitoring loop: {e}")
    
    def clear_resolved_issues(self) -> None:
        """
        Manually clear all tracked issues.
        Useful for testing or manual reset.
        """
        cleared_count = len(self.active_issues)
        self.active_issues.clear()
        print(f"🧹 Cleared {cleared_count} tracked issue(s)")
