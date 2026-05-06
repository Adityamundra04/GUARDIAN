"""
Action executor for Guardian.
Executes safe Kubernetes actions to fix detected issues.
"""
from kubernetes import client, config
from typing import Optional, Dict
import time


class ActionExecutor:
    """
    Executes safe Kubernetes actions to remediate issues.
    Provides methods for common fix operations like restarting pods.
    """
    
    def __init__(self):
        """
        Initialize action executor with Kubernetes client.
        """
        # Load Kubernetes configuration
        config.load_kube_config()
        
        # Initialize API clients
        self.core_v1 = client.CoreV1Api()
        self.apps_v1 = client.AppsV1Api()
    
    def restart_pod(self, namespace: str, pod_name: str) -> Dict[str, str]:
        """
        Restart a pod by deleting it (Kubernetes will recreate it).
        
        Args:
            namespace: Kubernetes namespace
            pod_name: Name of the pod to restart
        
        Returns:
            Dictionary with status and message
        """
        try:
            print(f"[OpenClaw] Executing action: restart pod {pod_name}")
            
            # Delete the pod (it will be recreated by the controller)
            self.core_v1.delete_namespaced_pod(
                name=pod_name,
                namespace=namespace,
                body=client.V1DeleteOptions()
            )
            
            print(f"[OpenClaw] Restart successful: {pod_name}")
            
            return {
                "status": "success",
                "message": f"Pod {pod_name} restarted successfully",
                "action": "restart_pod"
            }
        
        except client.exceptions.ApiException as e:
            error_msg = f"Failed to restart pod: {e.reason}"
            print(f"[OpenClaw] Restart failed: {error_msg}")
            return {
                "status": "error",
                "message": error_msg,
                "action": "restart_pod"
            }
        except Exception as e:
            error_msg = f"Unexpected error: {str(e)}"
            print(f"[OpenClaw] Restart failed: {error_msg}")
            return {
                "status": "error",
                "message": error_msg,
                "action": "restart_pod"
            }
    
    def delete_pod(self, namespace: str, pod_name: str) -> Dict[str, str]:
        """
        Delete a pod (useful for ImagePullBackOff to retry image pull).
        
        Args:
            namespace: Kubernetes namespace
            pod_name: Name of the pod to delete
        
        Returns:
            Dictionary with status and message
        """
        try:
            print(f"[OpenClaw] Executing action: delete pod {pod_name}")
            
            # Delete the pod
            self.core_v1.delete_namespaced_pod(
                name=pod_name,
                namespace=namespace,
                body=client.V1DeleteOptions()
            )
            
            print(f"[OpenClaw] Delete successful: {pod_name}")
            
            return {
                "status": "success",
                "message": f"Pod {pod_name} deleted successfully",
                "action": "delete_pod"
            }
        
        except client.exceptions.ApiException as e:
            error_msg = f"Failed to delete pod: {e.reason}"
            print(f"[OpenClaw] Delete failed: {error_msg}")
            return {
                "status": "error",
                "message": error_msg,
                "action": "delete_pod"
            }
        except Exception as e:
            error_msg = f"Unexpected error: {str(e)}"
            print(f"[OpenClaw] Delete failed: {error_msg}")
            return {
                "status": "error",
                "message": error_msg,
                "action": "delete_pod"
            }
    
    def scale_deployment(self, namespace: str, deployment_name: str, replicas: int) -> Dict[str, str]:
        """
        Scale a deployment to a specific number of replicas.
        
        Args:
            namespace: Kubernetes namespace
            deployment_name: Name of the deployment
            replicas: Target number of replicas
        
        Returns:
            Dictionary with status and message
        """
        try:
            print(f"📊 Executing action: scale deployment {deployment_name} to {replicas} replicas in namespace {namespace}")
            
            # Get current deployment
            deployment = self.apps_v1.read_namespaced_deployment(
                name=deployment_name,
                namespace=namespace
            )
            
            # Update replicas
            deployment.spec.replicas = replicas
            
            # Apply the change
            self.apps_v1.patch_namespaced_deployment(
                name=deployment_name,
                namespace=namespace,
                body=deployment
            )
            
            print(f"✅ Deployment {deployment_name} scaled to {replicas} replicas")
            
            return {
                "status": "success",
                "message": f"Deployment {deployment_name} scaled to {replicas} replicas"
            }
        
        except client.exceptions.ApiException as e:
            error_msg = f"Failed to scale deployment {deployment_name}: {e.reason}"
            print(f"❌ {error_msg}")
            return {
                "status": "error",
                "message": error_msg
            }
        except Exception as e:
            error_msg = f"Unexpected error scaling deployment {deployment_name}: {str(e)}"
            print(f"❌ {error_msg}")
            return {
                "status": "error",
                "message": error_msg
            }
    
    def get_pod_owner(self, namespace: str, pod_name: str) -> Optional[str]:
        """
        Get the owner (deployment/replicaset) of a pod.
        
        Args:
            namespace: Kubernetes namespace
            pod_name: Name of the pod
        
        Returns:
            Owner name or None
        """
        try:
            pod = self.core_v1.read_namespaced_pod(name=pod_name, namespace=namespace)
            
            if pod.metadata.owner_references:
                for owner in pod.metadata.owner_references:
                    if owner.kind == "ReplicaSet":
                        # Get deployment from replicaset
                        rs = self.apps_v1.read_namespaced_replica_set(
                            name=owner.name,
                            namespace=namespace
                        )
                        if rs.metadata.owner_references:
                            for rs_owner in rs.metadata.owner_references:
                                if rs_owner.kind == "Deployment":
                                    return rs_owner.name
                    elif owner.kind == "Deployment":
                        return owner.name
            
            return None
        
        except Exception as e:
            print(f"⚠️  Could not determine pod owner: {e}")
            return None
