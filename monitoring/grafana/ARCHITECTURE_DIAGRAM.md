# Grafana Architecture Diagram

## Complete Guardian AI Ops Observability Stack

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                         KUBERNETES CLUSTER                                   │
│                                                                              │
│  ┌────────────────────────────────────────────────────────────────────────┐ │
│  │                        APPLICATION LAYER                                │ │
│  │                                                                          │ │
│  │  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐              │ │
│  │  │   Pod    │  │   Pod    │  │   Pod    │  │   Pod    │              │ │
│  │  │ (nginx)  │  │ (redis)  │  │ (mysql)  │  │ (app)    │              │ │
│  │  └────┬─────┘  └────┬─────┘  └────┬─────┘  └────┬─────┘              │ │
│  │       │             │             │             │                       │ │
│  │       └─────────────┴─────────────┴─────────────┘                       │ │
│  │                           │                                              │ │
│  │                           │ Metrics (CPU, Memory, Restarts, Status)     │ │
│  │                           ▼                                              │ │
│  └────────────────────────────────────────────────────────────────────────┘ │
│                                                                              │
│  ┌────────────────────────────────────────────────────────────────────────┐ │
│  │                      MONITORING NAMESPACE                               │ │
│  │                                                                          │ │
│  │  ┌──────────────────────────────────────────────────────────────────┐  │ │
│  │  │                    PROMETHEUS                                     │  │ │
│  │  │  ┌────────────────────────────────────────────────────────────┐  │  │ │
│  │  │  │  Metrics Collection & Storage                              │  │  │ │
│  │  │  │  - Scrapes Kubernetes API every 15s                        │  │  │ │
│  │  │  │  - Scrapes node metrics                                    │  │  │ │
│  │  │  │  - Scrapes pod metrics                                     │  │  │ │
│  │  │  │  - Stores time-series data                                 │  │  │ │
│  │  │  │  - Exposes HTTP API on port 9090                           │  │  │ │
│  │  │  └────────────────────────────────────────────────────────────┘  │  │ │
│  │  │                                                                    │  │ │
│  │  │  Service: prometheus-service                                      │  │ │
│  │  │  Type: NodePort                                                    │  │ │
│  │  │  Port: 9090 → NodePort: 30090                                     │  │ │
│  │  └──────────────────────────┬─────────────────────────────────────────┘  │ │
│  │                             │                                            │ │
│  │                             │ HTTP Queries (PromQL)                      │ │
│  │                             ▼                                            │ │
│  │  ┌──────────────────────────────────────────────────────────────────┐  │ │
│  │  │                      GRAFANA                                      │  │ │
│  │  │  ┌────────────────────────────────────────────────────────────┐  │  │ │
│  │  │  │  Visualization & Dashboards                                │  │  │ │
│  │  │  │                                                             │  │  │ │
│  │  │  │  ┌──────────────────────────────────────────────────────┐ │  │  │ │
│  │  │  │  │  Auto-Provisioned Datasource                         │ │  │  │ │
│  │  │  │  │  - Name: Prometheus                                  │ │  │  │ │
│  │  │  │  │  - URL: http://prometheus-service:9090               │ │  │  │ │
│  │  │  │  │  - Type: prometheus                                  │ │  │  │ │
│  │  │  │  │  - Default: true                                     │ │  │  │ │
│  │  │  │  └──────────────────────────────────────────────────────┘ │  │  │ │
│  │  │  │                                                             │  │  │ │
│  │  │  │  ┌──────────────────────────────────────────────────────┐ │  │  │ │
│  │  │  │  │  Pre-Configured Dashboards                           │ │  │  │ │
│  │  │  │  │                                                       │ │  │  │ │
│  │  │  │  │  1. Kubernetes Monitoring Dashboard                  │ │  │  │ │
│  │  │  │  │     - Pod CPU Usage (%)                              │ │  │  │ │
│  │  │  │  │     - Pod Memory Usage                               │ │  │  │ │
│  │  │  │  │     - Pod Restart Count                              │ │  │  │ │
│  │  │  │  │     - Pod Status (Running/Down)                      │ │  │  │ │
│  │  │  │  │     - Cluster Health Overview                        │ │  │  │ │
│  │  │  │  │                                                       │ │  │  │ │
│  │  │  │  │  2. Guardian AI Ops Dashboard                        │ │  │  │ │
│  │  │  │  │     - Active Incidents                               │ │  │  │ │
│  │  │  │  │     - Remediation Events                             │ │  │  │ │
│  │  │  │  │     - Monitoring Activity                            │ │  │  │ │
│  │  │  │  │     - AI Diagnosis Activity                          │ │  │  │ │
│  │  │  │  │     - Incident Rate Over Time                        │ │  │  │ │
│  │  │  │  │     - Top Pods by Restart Count                      │ │  │  │ │
│  │  │  │  │                                                       │ │  │  │ │
│  │  │  │  │  Refresh: 5 seconds                                  │ │  │  │ │
│  │  │  │  │  Time Range: Last 15 minutes                         │ │  │  │ │
│  │  │  │  └──────────────────────────────────────────────────────┘ │  │  │ │
│  │  │  └────────────────────────────────────────────────────────────┘  │  │ │
│  │  │                                                                    │  │ │
│  │  │  Service: grafana-service                                         │  │ │
│  │  │  Type: NodePort                                                    │  │ │
│  │  │  Port: 3000 → NodePort: 30000                                     │  │ │
│  │  │  Credentials: admin / admin                                       │  │ │
│  │  └──────────────────────────────────────────────────────────────────┘  │ │
│  │                                                                          │ │
│  └────────────────────────────────────────────────────────────────────────┘ │
│                                                                              │
└──────────────────────────────────────┬───────────────────────────────────────┘
                                       │
                                       │ Observability Data
                                       ▼
                        ┌──────────────────────────────┐
                        │     GUARDIAN AI ENGINE       │
                        │                              │
                        │  ┌────────────────────────┐  │
                        │  │  AI Diagnosis Service  │  │
                        │  │  - Analyzes metrics    │  │
                        │  │  - Detects anomalies   │  │
                        │  │  - Suggests fixes      │  │
                        │  └────────────────────────┘  │
                        │                              │
                        │  ┌────────────────────────┐  │
                        │  │  Action Executor       │  │
                        │  │  - Restarts pods       │  │
                        │  │  - Scales deployments  │  │
                        │  │  - Applies fixes       │  │
                        │  └────────────────────────┘  │
                        │                              │
                        │  ┌────────────────────────┐  │
                        │  │  Monitor Service       │  │
                        │  │  - Continuous watch    │  │
                        │  │  - Incident creation   │  │
                        │  │  - Status tracking     │  │
                        │  └────────────────────────┘  │
                        └──────────────────────────────┘
                                       │
                                       │ Remediation Actions
                                       ▼
                        ┌──────────────────────────────┐
                        │    KUBERNETES API SERVER     │
                        │  - Apply fixes               │
                        │  - Update resources          │
                        │  - Restart pods              │
                        └──────────────────────────────┘
```

## Data Flow

```
1. APPLICATION METRICS
   Pods → Kubernetes API → Prometheus
   
2. METRICS STORAGE
   Prometheus stores time-series data
   
3. VISUALIZATION
   Grafana queries Prometheus → Displays dashboards
   
4. AI MONITORING
   Guardian AI queries Prometheus → Analyzes metrics
   
5. INCIDENT DETECTION
   Guardian AI detects issues → Creates incidents
   
6. REMEDIATION
   Guardian AI executes fixes → Updates Kubernetes
   
7. FEEDBACK LOOP
   Updated metrics → Prometheus → Grafana/Guardian AI
```

## Access Points

```
┌─────────────────────────────────────────────────────────────┐
│                      USER ACCESS                             │
│                                                              │
│  ┌────────────────────────────────────────────────────────┐ │
│  │  Web Browser                                            │ │
│  │                                                          │ │
│  │  http://localhost:30090  ──────▶  Prometheus UI         │ │
│  │  http://localhost:30000  ──────▶  Grafana UI            │ │
│  │  http://localhost:8000   ──────▶  Guardian API          │ │
│  │  http://localhost:3001   ──────▶  Guardian Frontend     │ │
│  │                                                          │ │
│  └────────────────────────────────────────────────────────┘ │
│                                                              │
│  ┌────────────────────────────────────────────────────────┐ │
│  │  kubectl CLI                                            │ │
│  │                                                          │ │
│  │  kubectl get pods -n monitoring                         │ │
│  │  kubectl logs -n monitoring -l app=grafana              │ │
│  │  kubectl port-forward svc/grafana-service 3000:3000     │ │
│  │                                                          │ │
│  └────────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────┘
```

## Component Relationships

```
┌──────────────┐
│ Kubernetes   │
│ Resources    │
└──────┬───────┘
       │ exposes metrics
       ▼
┌──────────────┐
│ Prometheus   │◀────────────┐
│ (Collector)  │             │
└──────┬───────┘             │
       │ stores              │ queries
       │ time-series         │
       ▼                     │
┌──────────────┐             │
│ Prometheus   │             │
│ (Storage)    │             │
└──────┬───────┘             │
       │                     │
       ├─────────────────────┤
       │                     │
       ▼                     ▼
┌──────────────┐      ┌──────────────┐
│   Grafana    │      │  Guardian AI │
│ (Visualize)  │      │  (Analyze)   │
└──────────────┘      └──────┬───────┘
                             │ remediates
                             ▼
                      ┌──────────────┐
                      │ Kubernetes   │
                      │ API Server   │
                      └──────────────┘
```

## Deployment Architecture

```
monitoring/grafana/
│
├── Kubernetes Manifests
│   ├── grafana-deployment.yaml
│   │   └── Creates: Grafana pod with auto-provisioning
│   ├── grafana-service.yaml
│   │   └── Exposes: NodePort 30000
│   ├── grafana-datasource-config.yaml
│   │   └── Configures: Prometheus datasource
│   └── grafana-dashboard-config.yaml
│       └── Provisions: Dashboard loading
│
├── Dashboard Definitions
│   ├── kubernetes-monitoring.json
│   │   └── Visualizes: K8s infrastructure metrics
│   └── guardian-monitoring.json
│       └── Visualizes: Guardian AI Ops activity
│
├── Automation Scripts
│   ├── deploy.sh
│   │   └── Deploys: All resources automatically
│   └── verify.sh
│       └── Verifies: Deployment success
│
└── Documentation
    ├── README.md
    ├── SETUP_GUIDE.md
    ├── QUICK_REFERENCE.md
    ├── DEPLOYMENT_CHECKLIST.md
    ├── IMPLEMENTATION_SUMMARY.md
    └── ARCHITECTURE_DIAGRAM.md (this file)
```

## Network Topology

```
┌─────────────────────────────────────────────────────────────┐
│                    Kubernetes Network                        │
│                                                              │
│  Namespace: monitoring                                       │
│                                                              │
│  ┌────────────────────────────────────────────────────────┐ │
│  │  Service: prometheus-service                            │ │
│  │  ClusterIP: 10.96.x.x                                   │ │
│  │  Port: 9090                                             │ │
│  │  NodePort: 30090                                        │ │
│  │  Selector: app=prometheus                               │ │
│  └────────────────────────────────────────────────────────┘ │
│                          │                                   │
│                          │ Internal DNS                      │
│                          │ prometheus-service:9090           │
│                          ▼                                   │
│  ┌────────────────────────────────────────────────────────┐ │
│  │  Service: grafana-service                               │ │
│  │  ClusterIP: 10.96.x.x                                   │ │
│  │  Port: 3000                                             │ │
│  │  NodePort: 30000                                        │ │
│  │  Selector: app=grafana                                  │ │
│  └────────────────────────────────────────────────────────┘ │
│                                                              │
└─────────────────────────────────────────────────────────────┘
                          │
                          │ External Access
                          ▼
                   ┌──────────────┐
                   │   Browser    │
                   │ localhost:   │
                   │   30000      │
                   └──────────────┘
```

## Security Model

```
┌─────────────────────────────────────────────────────────────┐
│                    Security Layers                           │
│                                                              │
│  Layer 1: Kubernetes RBAC                                    │
│  ├── Prometheus ServiceAccount                               │
│  ├── ClusterRole (read metrics)                              │
│  └── ClusterRoleBinding                                      │
│                                                              │
│  Layer 2: Network Policies (optional)                        │
│  ├── Allow Grafana → Prometheus                              │
│  ├── Allow Guardian → Prometheus                             │
│  └── Deny all other traffic                                  │
│                                                              │
│  Layer 3: Authentication                                     │
│  ├── Grafana: admin/admin (default)                          │
│  ├── Prometheus: No auth (internal only)                     │
│  └── Guardian API: No auth (demo)                            │
│                                                              │
│  Layer 4: Service Exposure                                   │
│  ├── NodePort: Limited to cluster nodes                      │
│  ├── ClusterIP: Internal only                                │
│  └── LoadBalancer: Not used (demo)                           │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

## Scaling Considerations

```
Current Setup (Demo):
├── Grafana: 1 replica
├── Prometheus: 1 replica
└── Storage: emptyDir (ephemeral)

Production Setup (Future):
├── Grafana: 2-3 replicas (HA)
├── Prometheus: 2 replicas (HA)
├── Storage: PersistentVolume
├── Backup: Automated snapshots
└── Monitoring: Grafana monitors Prometheus
```

---

**Architecture Status:** ✅ Complete and Deployed  
**Components:** Kubernetes + Prometheus + Grafana + Guardian AI  
**Access:** http://localhost:30000 (Grafana)  
**Documentation:** Complete with diagrams
