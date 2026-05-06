"""
Prometheus service for Guardian.
Fetches Kubernetes metrics from Prometheus for AI-powered analysis.
"""
import requests
from typing import Dict, List, Optional, Any
from datetime import datetime


class PrometheusService:
    """
    Service for querying Prometheus metrics.
    Provides methods to fetch CPU, memory, and pod health metrics.
    """
    
    def __init__(self, base_url: str = "http://localhost:9090"):
        """
        Initialize Prometheus service.
        
        Args:
            base_url: Prometheus server URL (default: http://localhost:9090)
        """
        self.base_url = base_url.rstrip('/')
        self.query_url = f"{self.base_url}/api/v1/query"
        self.timeout = 10  # seconds
    
    def _execute_query(self, query: str) -> Optional[Dict[str, Any]]:
        """
        Execute a PromQL query against Prometheus.
        
        Args:
            query: PromQL query string
        
        Returns:
            Query result as dictionary, or None if error
        """
        try:
            print(f"[Prometheus] Executing query: {query}")
            
            response = requests.get(
                self.query_url,
                params={'query': query},
                timeout=self.timeout
            )
            
            if response.status_code == 200:
                data = response.json()
                
                if data.get('status') == 'success':
                    print(f"[Prometheus] Query successful")
                    return data.get('data', {})
                else:
                    print(f"[Prometheus] Query failed: {data.get('error', 'Unknown error')}")
                    return None
            else:
                print(f"[Prometheus] HTTP error: {response.status_code}")
                return None
        
        except requests.exceptions.Timeout:
            print(f"[Prometheus] Query timeout after {self.timeout} seconds")
            return None
        except requests.exceptions.ConnectionError:
            print(f"[Prometheus] Failed to connect to {self.base_url}")
            return None
        except Exception as e:
            print(f"[Prometheus] Error executing query: {str(e)}")
            return None
    
    def get_cpu_usage(self, namespace: Optional[str] = None, pod: Optional[str] = None) -> List[Dict[str, Any]]:
        """
        Get CPU usage metrics for containers.
        
        Args:
            namespace: Filter by namespace (optional)
            pod: Filter by pod name (optional)
        
        Returns:
            List of CPU usage metrics
        """
        print(f"[Prometheus] Fetching CPU metrics")
        
        # Build query with optional filters
        query = 'rate(container_cpu_usage_seconds_total{container!=""}[5m])'
        
        if namespace:
            query = f'rate(container_cpu_usage_seconds_total{{namespace="{namespace}",container!=""}}[5m])'
        if pod:
            query = f'rate(container_cpu_usage_seconds_total{{pod="{pod}",container!=""}}[5m])'
        
        result = self._execute_query(query)
        
        if not result:
            return []
        
        # Parse results
        metrics = []
        for item in result.get('result', []):
            metric = item.get('metric', {})
            value = item.get('value', [None, None])
            
            metrics.append({
                'namespace': metric.get('namespace', 'unknown'),
                'pod': metric.get('pod', 'unknown'),
                'container': metric.get('container', 'unknown'),
                'cpu_usage': float(value[1]) if len(value) > 1 else 0.0,
                'timestamp': value[0] if len(value) > 0 else None
            })
        
        print(f"[Prometheus] Retrieved {len(metrics)} CPU metrics")
        return metrics
    
    def get_memory_usage(self, namespace: Optional[str] = None, pod: Optional[str] = None) -> List[Dict[str, Any]]:
        """
        Get memory usage metrics for containers.
        
        Args:
            namespace: Filter by namespace (optional)
            pod: Filter by pod name (optional)
        
        Returns:
            List of memory usage metrics
        """
        print(f"[Prometheus] Fetching memory metrics")
        
        # Build query with optional filters
        query = 'container_memory_usage_bytes{container!=""}'
        
        if namespace:
            query = f'container_memory_usage_bytes{{namespace="{namespace}",container!=""}}'
        if pod:
            query = f'container_memory_usage_bytes{{pod="{pod}",container!=""}}'
        
        result = self._execute_query(query)
        
        if not result:
            return []
        
        # Parse results
        metrics = []
        for item in result.get('result', []):
            metric = item.get('metric', {})
            value = item.get('value', [None, None])
            
            memory_bytes = float(value[1]) if len(value) > 1 else 0.0
            memory_mb = memory_bytes / (1024 * 1024)  # Convert to MB
            
            metrics.append({
                'namespace': metric.get('namespace', 'unknown'),
                'pod': metric.get('pod', 'unknown'),
                'container': metric.get('container', 'unknown'),
                'memory_bytes': memory_bytes,
                'memory_mb': round(memory_mb, 2),
                'timestamp': value[0] if len(value) > 0 else None
            })
        
        print(f"[Prometheus] Retrieved {len(metrics)} memory metrics")
        return metrics
    
    def get_pod_restart_count(self, namespace: Optional[str] = None, pod: Optional[str] = None) -> List[Dict[str, Any]]:
        """
        Get pod restart count metrics.
        
        Args:
            namespace: Filter by namespace (optional)
            pod: Filter by pod name (optional)
        
        Returns:
            List of restart count metrics
        """
        print(f"[Prometheus] Fetching pod restart counts")
        
        # Build query with optional filters
        query = 'kube_pod_container_status_restarts_total'
        
        if namespace:
            query = f'kube_pod_container_status_restarts_total{{namespace="{namespace}"}}'
        if pod:
            query = f'kube_pod_container_status_restarts_total{{pod="{pod}"}}'
        
        result = self._execute_query(query)
        
        if not result:
            return []
        
        # Parse results
        metrics = []
        for item in result.get('result', []):
            metric = item.get('metric', {})
            value = item.get('value', [None, None])
            
            restart_count = int(float(value[1])) if len(value) > 1 else 0
            
            metrics.append({
                'namespace': metric.get('namespace', 'unknown'),
                'pod': metric.get('pod', 'unknown'),
                'container': metric.get('container', 'unknown'),
                'restart_count': restart_count,
                'timestamp': value[0] if len(value) > 0 else None
            })
        
        print(f"[Prometheus] Retrieved {len(metrics)} restart count metrics")
        return metrics
    
    def get_pod_status(self, namespace: Optional[str] = None) -> List[Dict[str, Any]]:
        """
        Get pod status metrics.
        
        Args:
            namespace: Filter by namespace (optional)
        
        Returns:
            List of pod status metrics
        """
        print(f"[Prometheus] Fetching pod status")
        
        # Build query with optional filters
        query = 'kube_pod_status_phase'
        
        if namespace:
            query = f'kube_pod_status_phase{{namespace="{namespace}"}}'
        
        result = self._execute_query(query)
        
        if not result:
            return []
        
        # Parse results
        metrics = []
        for item in result.get('result', []):
            metric = item.get('metric', {})
            value = item.get('value', [None, None])
            
            phase_value = float(value[1]) if len(value) > 1 else 0
            
            metrics.append({
                'namespace': metric.get('namespace', 'unknown'),
                'pod': metric.get('pod', 'unknown'),
                'phase': metric.get('phase', 'unknown'),
                'value': phase_value,
                'timestamp': value[0] if len(value) > 0 else None
            })
        
        print(f"[Prometheus] Retrieved {len(metrics)} pod status metrics")
        return metrics
    
    def get_container_memory_limit(self, namespace: Optional[str] = None, pod: Optional[str] = None) -> List[Dict[str, Any]]:
        """
        Get container memory limits.
        
        Args:
            namespace: Filter by namespace (optional)
            pod: Filter by pod name (optional)
        
        Returns:
            List of memory limit metrics
        """
        print(f"[Prometheus] Fetching memory limits")
        
        # Build query with optional filters
        query = 'container_spec_memory_limit_bytes{container!=""}'
        
        if namespace:
            query = f'container_spec_memory_limit_bytes{{namespace="{namespace}",container!=""}}'
        if pod:
            query = f'container_spec_memory_limit_bytes{{pod="{pod}",container!=""}}'
        
        result = self._execute_query(query)
        
        if not result:
            return []
        
        # Parse results
        metrics = []
        for item in result.get('result', []):
            metric = item.get('metric', {})
            value = item.get('value', [None, None])
            
            limit_bytes = float(value[1]) if len(value) > 1 else 0.0
            limit_mb = limit_bytes / (1024 * 1024)  # Convert to MB
            
            metrics.append({
                'namespace': metric.get('namespace', 'unknown'),
                'pod': metric.get('pod', 'unknown'),
                'container': metric.get('container', 'unknown'),
                'limit_bytes': limit_bytes,
                'limit_mb': round(limit_mb, 2),
                'timestamp': value[0] if len(value) > 0 else None
            })
        
        print(f"[Prometheus] Retrieved {len(metrics)} memory limit metrics")
        return metrics
    
    def check_connection(self) -> bool:
        """
        Check if Prometheus is accessible.
        
        Returns:
            True if connected, False otherwise
        """
        try:
            print(f"[Prometheus] Checking connection to {self.base_url}")
            
            response = requests.get(
                f"{self.base_url}/api/v1/status/config",
                timeout=5
            )
            
            if response.status_code == 200:
                print(f"[Prometheus] Connection successful")
                return True
            else:
                print(f"[Prometheus] Connection failed: HTTP {response.status_code}")
                return False
        
        except Exception as e:
            print(f"[Prometheus] Connection failed: {str(e)}")
            return False
