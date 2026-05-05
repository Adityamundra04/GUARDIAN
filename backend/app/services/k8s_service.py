"""
Kubernetes service module for Guardian.
Monitors Kubernetes cluster and detects problematic pods.
"""
from kubernetes import client, config
from typing import List, Dict, Optional


class K8sService:
    """
    Service for interacting with Kubernetes cluster.
    Provides methods to fetch pods and detect issues.
    """
    
    def __init__(self):
        """
        Initialize Kubernetes client.
        Loads kubeconfig and sets up CoreV1Api client.
        """
        # Load Kubernetes configuration from default location (~/.kube/config)
        config.load_kube_config()
        
        # Initialize Core V1 API client for pod operations
        self.v1 = client.CoreV1Api()
    
    def get_pods(self) -> List:
        """
        Fetch all pods from all namespaces in the cluster.
        
        Returns:
            List of pod objects from Kubernetes API
        """
        # Fetch pods across all namespaces
        pods = self.v1.list_pod_for_all_namespaces(watch=False)
        return pods.items
    
    def get_problematic_pods(self) -> List[Dict[str, str]]:
        """
        Detect and return pods with issues.
        
        Issues detected:
        - High restart count (> 2)
        - CrashLoopBackOff state
        - Error state
        
        Returns:
            List of dictionaries containing problematic pod information:
            [
                {
                    "name": "pod-name",
                    "namespace": "namespace",
                    "issue": "description of issue"
                }
            ]
        """
        problematic_pods = []
        
        # Get all pods
        pods = self.get_pods()
        
        for pod in pods:
            # Extract pod metadata
            pod_name = pod.metadata.name
            pod_namespace = pod.metadata.namespace
            
            # Check if pod has container statuses
            if not pod.status.container_statuses:
                continue
            
            # Iterate through each container in the pod
            for container_status in pod.status.container_statuses:
                # Check for high restart count
                restart_count = container_status.restart_count
                if restart_count is not None and restart_count > 2:
                    problematic_pods.append({
                        "name": pod_name,
                        "namespace": pod_namespace,
                        "issue": f"High restart count: {restart_count}"
                    })
                    continue  # Skip to next container to avoid duplicate entries
                
                # Check waiting state (CrashLoopBackOff, Error, etc.)
                if container_status.state and container_status.state.waiting:
                    waiting_reason = container_status.state.waiting.reason
                    
                    if waiting_reason:
                        # Detect CrashLoopBackOff
                        if "CrashLoopBackOff" in waiting_reason:
                            problematic_pods.append({
                                "name": pod_name,
                                "namespace": pod_namespace,
                                "issue": "CrashLoopBackOff"
                            })
                        # Detect Error states
                        elif "Error" in waiting_reason:
                            problematic_pods.append({
                                "name": pod_name,
                                "namespace": pod_namespace,
                                "issue": f"Error: {waiting_reason}"
                            })
                        # Other waiting states
                        else:
                            problematic_pods.append({
                                "name": pod_name,
                                "namespace": pod_namespace,
                                "issue": f"Waiting: {waiting_reason}"
                            })
                
                # Check terminated state with non-zero exit code
                if container_status.state and container_status.state.terminated:
                    terminated = container_status.state.terminated
                    if terminated.exit_code and terminated.exit_code != 0:
                        problematic_pods.append({
                            "name": pod_name,
                            "namespace": pod_namespace,
                            "issue": f"Terminated with exit code: {terminated.exit_code}"
                        })
        
        return problematic_pods
