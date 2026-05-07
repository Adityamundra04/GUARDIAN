# 🛡️ Guardian

**AI-Powered Kubernetes Observability & Autonomous Remediation Platform**

Guardian is an intelligent Kubernetes operations platform that automatically detects, diagnoses, and remediates pod failures using AI-powered analysis. It combines real-time monitoring, Prometheus metrics, AI reasoning (Ollama + llama3.1), and autonomous remediation to keep your Kubernetes clusters healthy.

---

## 🌟 Features

- **🔍 Intelligent Monitoring** - Continuous Kubernetes cluster monitoring with automatic issue detection
- **🤖 AI-Powered Diagnosis** - Uses Ollama (llama3.1) to analyze failures with metrics and log context
- **⚡ Autonomous Remediation** - OpenClaw engine safely executes fixes (pod restarts, scaling, etc.)
- **📊 Prometheus Integration** - Collects CPU, memory, and restart metrics for context-aware diagnosis
- **📈 Grafana Dashboards** - Pre-configured dashboards for infrastructure and Guardian activity
- **💾 Persistent Storage** - SQLite database for incident history and tracking
- **🎨 Futuristic Dashboard** - React-based UI with real-time incident visualization
- **📝 Comprehensive Logging** - Structured logs with rotation for all system components
- **🔒 Safety-First** - Retry limits, namespace restrictions, and cooldown periods
- **📦 Pod Log Analysis** - Analyzes container logs for root cause identification

---

## 🎯 Why Guardian?

Kubernetes failures are inevitable. Manual intervention is slow and error-prone. Guardian automates the entire incident response workflow:

1. **Detects** failures instantly (CrashLoopBackOff, ImagePullBackOff, high restarts)
2. **Collects** metrics and logs for comprehensive context
3. **Diagnoses** root cause using AI reasoning
4. **Remediates** issues automatically with safety guardrails
5. **Tracks** everything in a persistent database
6. **Visualizes** incidents in real-time on a modern dashboard

---

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    Kubernetes Cluster                        │
│                                                              │
│  ┌────────────┐  ┌────────────┐  ┌────────────┐           │
│  │   Pods     │  │  Services  │  │ Deployments│           │
│  └─────┬──────┘  └─────┬──────┘  └─────┬──────┘           │
│        │                │                │                   │
│        └────────────────┴────────────────┘                   │
│                         │                                    │
└─────────────────────────┼────────────────────────────────────┘
                          │
                          ▼
         ┌────────────────────────────────┐
         │   Guardian Monitoring Service   │
         │   (FastAPI + Python)            │
         │   - Detects pod failures        │
         │   - Tracks active incidents     │
         └────────┬───────────────┬────────┘
                  │               │
        ┌─────────▼──────┐   ┌───▼──────────────┐
        │  Prometheus     │   │  Kubernetes API  │
        │  Metrics        │   │  Pod Logs        │
        │  - CPU usage    │   │  - Error traces  │
        │  - Memory       │   │  - Stack traces  │
        │  - Restarts     │   │  - Exceptions    │
        └────────┬────────┘   └───┬──────────────┘
                 │                │
                 └────────┬───────┘
                          │
                          ▼
              ┌───────────────────────┐
              │   AI Diagnosis Engine  │
              │   (Ollama + llama3.1)  │
              │   - Analyzes context   │
              │   - Identifies cause   │
              │   - Suggests solution  │
              └───────────┬───────────┘
                          │
                          ▼
              ┌───────────────────────┐
              │  OpenClaw Remediation  │
              │  - Safety validation   │
              │  - Execute actions     │
              │  - Track results       │
              └───────────┬───────────┘
                          │
                          ▼
              ┌───────────────────────┐
              │   SQLite Database      │
              │   - Incident history   │
              │   - Remediation logs   │
              └───────────┬───────────┘
                          │
                          ▼
              ┌───────────────────────┐
              │  Frontend Dashboard    │
              │  (React + Tailwind)    │
              │  - Live incidents      │
              │  - AI diagnosis        │
              │  - System status       │
              └───────────────────────┘
```

---

## 🛠️ Tech Stack

### Backend
- **FastAPI** - Modern Python web framework
- **Python 3.9+** - Core language
- **SQLAlchemy** - ORM for database operations
- **SQLite** - Lightweight persistent storage
- **Kubernetes Python Client** - Cluster interaction

### AI Engine
- **Ollama** - Local LLM inference server
- **llama3.1** - AI model for diagnosis

### Monitoring
- **Prometheus** - Metrics collection and storage
- **Grafana** - Visualization dashboards

### Frontend
- **React 18** - UI framework
- **Vite** - Build tool
- **Tailwind CSS** - Utility-first styling
- **Framer Motion** - Animations

### Infrastructure
- **Kubernetes** - Container orchestration
- **kubectl** - Kubernetes CLI

---

## 📁 Project Structure

```
guardian/
├── backend/                    # FastAPI backend application
│   └── app/
│       ├── api/               # API endpoints
│       │   └── incidents.py   # Incident CRUD operations
│       ├── core/              # Core utilities
│       │   ├── database.py    # SQLite configuration
│       │   └── logger.py      # Logging setup
│       ├── models/            # Data models
│       │   ├── incident.py    # Pydantic models
│       │   └── incident_db.py # SQLAlchemy ORM models
│       ├── services/          # Business logic
│       │   ├── monitor_service.py    # Main monitoring loop
│       │   ├── ai_service.py         # AI diagnosis
│       │   ├── k8s_service.py        # Kubernetes interaction
│       │   └── prometheus_service.py # Metrics fetching
│       └── main.py            # FastAPI app entry point
│
├── agent/                     # OpenClaw remediation engine
│   ├── executor.py            # Action execution (restart, scale, etc.)
│   └── safety_rules.py        # Safety validation and retry logic
│
├── ai_engine/                 # AI diagnosis engine
│   └── ollama_client.py       # Ollama API client
│
├── frontend/                  # React dashboard
│   ├── src/
│   │   ├── components/        # React components
│   │   ├── pages/             # Page components
│   │   ├── services/          # API client
│   │   └── App.jsx            # Main app component
│   └── package.json           # Node dependencies
│
├── monitoring/                # Observability stack
│   ├── prometheus/            # Prometheus manifests
│   │   ├── namespace.yaml
│   │   ├── prometheus-deployment.yaml
│   │   └── prometheus-service.yaml
│   └── grafana/               # Grafana manifests and dashboards
│       ├── grafana-deployment.yaml
│       ├── grafana-service.yaml
│       └── dashboards/        # Pre-configured dashboards
│
├── k8s/                       # Kubernetes resources
│   └── test-failures/         # Test failure scenarios
│       ├── crashloop.yaml     # CrashLoopBackOff test
│       └── oom.yaml           # Out of memory test
│
├── logs/                      # Application logs (auto-created)
│   ├── guardian.log           # Main application log
│   ├── errors.log             # Error-level logs
│   ├── monitoring.log         # Monitoring service logs
│   ├── ai.log                 # AI diagnosis logs
│   └── actions.log            # Remediation action logs
│
├── data/                      # Database storage (auto-created)
│   └── guardian.db            # SQLite database
│
├── requirements.txt           # Python dependencies
└── README.md                  # This file
```

---

## 📋 Prerequisites

Before starting, ensure you have the following installed:

### Required Software

| Software | Version | Purpose |
|----------|---------|---------|
| **Python** | 3.9+ | Backend application |
| **Node.js** | 18+ | Frontend application |
| **npm** | 9+ | Package manager |
| **Kubernetes** | 1.24+ | Container orchestration |
| **kubectl** | 1.24+ | Kubernetes CLI |
| **Ollama** | Latest | AI inference server |
| **Docker Desktop** | Latest | Local Kubernetes (or Minikube) |

### Verify Installations

```bash
# Check Python version
python --version  # Should be 3.9 or higher

# Check Node.js version
node --version    # Should be 18 or higher

# Check kubectl
kubectl version --client

# Check Kubernetes cluster
kubectl get nodes

# Check Ollama
ollama --version
```

---

## 🚀 Quick Start Guide

### Step 1: Install Ollama

Ollama provides local AI inference for Guardian's diagnosis engine.

#### macOS / Linux
```bash
# Install Ollama
curl -fsSL https://ollama.com/install.sh | sh

# Pull llama3.1 model
ollama pull llama3.1

# Verify installation
ollama run llama3.1
# Type "Hello" and press Enter to test
# Press Ctrl+D to exit
```

#### Windows
1. Download Ollama from https://ollama.com/download
2. Run the installer
3. Open PowerShell and run:
```powershell
ollama pull llama3.1
ollama run llama3.1
```

**Important**: Keep Ollama running in the background. Guardian needs it for AI diagnosis.

---

### Step 2: Setup Kubernetes

Guardian requires a running Kubernetes cluster.

#### Using Docker Desktop (Recommended for local development)

1. Install Docker Desktop from https://www.docker.com/products/docker-desktop
2. Open Docker Desktop settings
3. Go to **Kubernetes** tab
4. Check **Enable Kubernetes**
5. Click **Apply & Restart**
6. Wait for Kubernetes to start (green indicator)

#### Verify Kubernetes

```bash
# Check cluster status
kubectl cluster-info

# Check nodes
kubectl get nodes

# Expected output:
# NAME             STATUS   ROLES           AGE   VERSION
# docker-desktop   Ready    control-plane   1d    v1.27.2
```

---

### Step 3: Deploy Prometheus

Prometheus collects metrics from Kubernetes for AI-powered diagnosis.

```bash
# Navigate to project root
cd guardian

# Deploy Prometheus to monitoring namespace
kubectl apply -f monitoring/prometheus/namespace.yaml
kubectl apply -f monitoring/prometheus/

# Verify Prometheus is running
kubectl get pods -n monitoring

# Expected output:
# NAME                          READY   STATUS    RESTARTS   AGE
# prometheus-xxxxxxxxxx-xxxxx   1/1     Running   0          30s

# Access Prometheus UI (optional)
kubectl port-forward svc/prometheus-service 9090:9090 -n monitoring
# Open browser: http://localhost:9090
```

---

### Step 4: Deploy Grafana (Optional but Recommended)

Grafana provides beautiful dashboards for infrastructure visualization.

```bash
# Deploy Grafana
cd monitoring/grafana
bash deploy.sh

# Or manually:
kubectl apply -f monitoring/grafana/

# Verify Grafana is running
kubectl get pods -n monitoring -l app=grafana

# Access Grafana UI
kubectl port-forward svc/grafana-service 3000:3000 -n monitoring
# Open browser: http://localhost:3000
# Login: admin / admin
```

**Pre-configured Dashboards:**
- Kubernetes Monitoring Dashboard (CPU, memory, restarts, pod status)
- Guardian AI Ops Dashboard (incidents, remediations, activity)

---

### Step 5: Setup Backend

```bash
# Navigate to project root
cd guardian

# Create virtual environment
python -m venv venv

# Activate virtual environment
# On macOS/Linux:
source venv/bin/activate
# On Windows:
venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Start FastAPI backend
uvicorn backend.app.main:app --reload --host 0.0.0.0 --port 8000

# Backend will start on http://127.0.0.1:8000
# API docs available at http://127.0.0.1:8000/docs
```

**Expected Output:**
```
INFO:     Uvicorn running on http://0.0.0.0:8000 (Press CTRL+C to quit)
INFO:     Started reloader process
INFO:     Started server process
INFO:     Waiting for application startup.
[2026-05-06 10:00:00] [INFO] [Guardian] Guardian Application Started
[2026-05-06 10:00:00] [INFO] [Guardian] Background monitoring thread started successfully
```

---

### Step 6: Setup Frontend

Open a **new terminal** (keep backend running).

```bash
# Navigate to frontend directory
cd guardian/frontend

# Install dependencies
npm install

# Start development server
npm run dev

# Frontend will start on http://localhost:5173
```

**Expected Output:**
```
  VITE v5.0.0  ready in 500 ms

  ➜  Local:   http://localhost:5173/
  ➜  Network: use --host to expose
  ➜  press h to show help
```

Open your browser to **http://localhost:5173** to see the Guardian dashboard.

---

## 🌐 Demo Website

Guardian includes a **demo website deployment** for easy testing and demonstration of monitoring capabilities.

### Quick Start

```bash
# Deploy the demo website
cd k8s/demo-website
./deploy.sh

# Access the website
http://localhost:30080
```

### Features

- ✅ **Healthy deployment** - Working nginx-based website with Guardian branding
- ✅ **Failure scenarios** - Pre-configured CrashLoop, ImagePull, and OOM tests
- ✅ **Automated scripts** - Easy deployment, testing, and cleanup
- ✅ **Complete documentation** - Comprehensive guides and quick reference

### Test Failure Scenarios

```bash
# Interactive testing menu
cd k8s/demo-website
./test-failures.sh

# Or manually deploy failures:
kubectl apply -f failure-crashloop.yaml    # CrashLoopBackOff test
kubectl apply -f failure-imagepull.yaml    # ImagePullBackOff test
kubectl apply -f failure-oom.yaml          # Out of Memory test
```

### Documentation

- **[Demo Website README](k8s/demo-website/README.md)** - Complete documentation
- **[Testing Guide](k8s/demo-website/TESTING_GUIDE.md)** - Step-by-step testing procedures
- **[Quick Reference](k8s/demo-website/QUICK_REFERENCE.md)** - Command cheat sheet

### Cleanup

```bash
cd k8s/demo-website
./cleanup.sh
```

---

## 🧪 Testing Guardian

### Test 1: Create a Failing Pod

Let's create a pod that crashes to test Guardian's detection and remediation.

```bash
# Deploy a crashloop pod
kubectl apply -f k8s/test-failures/crashloop.yaml

# Watch the pod status
kubectl get pods -w

# Expected output:
# NAME                        READY   STATUS             RESTARTS   AGE
# crashloop-test-pod          0/1     CrashLoopBackOff   3          2m
```

### Test 2: Observe Guardian in Action

1. **Check Backend Logs** (in backend terminal):
```
[2026-05-06 10:05:00] [INFO] [MonitorService] Found 1 issue(s) in cluster
[2026-05-06 10:05:00] [INFO] [MonitorService] Issue detected: [default] crashloop-test-pod → CrashLoopBackOff
[2026-05-06 10:05:00] [INFO] [AIService] Requesting AI diagnosis for: [default] crashloop-test-pod - CrashLoopBackOff (with logs)
[2026-05-06 10:05:05] [INFO] [AIService] AI response received (245 chars)
[2026-05-06 10:05:05] [INFO] [MonitorService] Incident created: abc-123-def-456
[2026-05-06 10:05:05] [INFO] [OpenClaw] Executing action: restart pod crashloop-test-pod
[2026-05-06 10:05:06] [INFO] [OpenClaw] Restart successful: crashloop-test-pod
```

2. **Check Frontend Dashboard** (http://localhost:5173):
   - New incident appears in real-time
   - AI diagnosis shows root cause
   - Remediation action is displayed
   - Status updates automatically

3. **Check Database**:
```bash
# View incidents in database
sqlite3 data/guardian.db "SELECT * FROM incidents;"
```

4. **Check Grafana** (http://localhost:3000):
   - Open "Guardian AI Ops Dashboard"
   - See incident count increase
   - View remediation events
   - Monitor pod restart count

### Test 3: Cleanup

```bash
# Delete the test pod
kubectl delete -f k8s/test-failures/crashloop.yaml

# Verify cleanup
kubectl get pods
```

---

## 📡 API Endpoints

Guardian exposes a RESTful API for incident management.

### Base URL
```
http://127.0.0.1:8000
```

### Endpoints

#### 1. Health Check
```http
GET /health
```

**Response:**
```json
{
  "status": "ok"
}
```

#### 2. Get All Incidents
```http
GET /incidents
```

**Response:**
```json
[
  {
    "id": "abc-123-def-456",
    "issue": "[default] crashloop-test-pod → CrashLoopBackOff",
    "status": "detected",
    "cause": "Container repeatedly crashes after startup with 5 restarts - indicates persistent failure",
    "solution": "Check container logs using kubectl logs and verify application startup, entrypoint, and dependencies",
    "action_taken": "restart_pod",
    "action_status": "success"
  }
]
```

#### 3. Get Single Incident
```http
GET /incidents/{incident_id}
```

**Response:**
```json
{
  "id": "abc-123-def-456",
  "issue": "[default] crashloop-test-pod → CrashLoopBackOff",
  "status": "detected",
  "cause": "Container repeatedly crashes after startup",
  "solution": "Check container logs and verify application startup",
  "action_taken": "restart_pod",
  "action_status": "success"
}
```

#### 4. Create Incident (Manual)
```http
POST /incidents
Content-Type: application/json

{
  "issue": "Test incident",
  "status": "detected",
  "cause": "Manual test",
  "solution": "No action needed"
}
```

### Interactive API Documentation

FastAPI provides automatic interactive API documentation:

- **Swagger UI**: http://127.0.0.1:8000/docs
- **ReDoc**: http://127.0.0.1:8000/redoc

---

## 📝 Logging System

Guardian uses structured logging with automatic rotation.

### Log Files

All logs are stored in the `logs/` directory (auto-created on startup):

| Log File | Purpose | Content |
|----------|---------|---------|
| `guardian.log` | Main application log | All system events |
| `errors.log` | Error-level logs only | Exceptions and errors |
| `monitoring.log` | Monitoring service | Pod detection, metrics fetching |
| `ai.log` | AI diagnosis | AI requests and responses |
| `actions.log` | Remediation actions | OpenClaw execution logs |

### Log Format

```
[2026-05-06 10:00:00] [INFO] [ServiceName] Log message
```

### Viewing Logs

```bash
# Tail main log
tail -f logs/guardian.log

# Tail error log
tail -f logs/errors.log

# Tail monitoring log
tail -f logs/monitoring.log

# View AI diagnosis logs
tail -f logs/ai.log

# View remediation actions
tail -f logs/actions.log
```

### Log Rotation

Logs automatically rotate when they reach 5MB. Up to 5 backup files are kept per log.

---

## 💾 Database

Guardian uses SQLite for persistent incident storage.

### Database Location
```
data/guardian.db
```

### Schema

**incidents** table:
```sql
CREATE TABLE incidents (
    id TEXT PRIMARY KEY,
    issue TEXT NOT NULL,
    status TEXT DEFAULT 'detected',
    cause TEXT,
    solution TEXT,
    action_taken TEXT,
    action_status TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

### Querying the Database

```bash
# Open SQLite shell
sqlite3 data/guardian.db

# View all incidents
SELECT * FROM incidents;

# View recent incidents
SELECT * FROM incidents ORDER BY created_at DESC LIMIT 10;

# Count incidents by status
SELECT status, COUNT(*) FROM incidents GROUP BY status;

# Exit SQLite
.exit
```

---

## 🎨 Frontend Dashboard

The Guardian dashboard provides real-time visualization of incidents and system status.

### Features

1. **Live Incident Feed**
   - Real-time incident updates (5-second refresh)
   - Expandable incident cards
   - AI diagnosis display
   - Remediation action tracking

2. **System Status Panel**
   - Kubernetes connection status
   - Prometheus connection status
   - AI engine status
   - Remediation engine status

3. **Statistics Cards**
   - Active incidents count
   - Resolved incidents count
   - Auto-remediated count
   - System uptime

4. **Futuristic UI**
   - Glassmorphism effects
   - 3D hover animations
   - Animated gradients
   - Smooth transitions
   - Responsive design

### Accessing the Dashboard

```
http://localhost:5173
```

### Dashboard Components

- **Navbar** - System status and live indicator
- **Hero Section** - Statistics and system overview
- **Incident List** - Live incident feed with AI diagnosis
- **Monitoring Panel** - Service health indicators

---

## 🔄 Complete Workflow Example

Here's what happens when a pod fails:

### 1. Failure Occurs
```bash
# Pod enters CrashLoopBackOff state
kubectl get pods
# NAME                READY   STATUS             RESTARTS   AGE
# my-app-pod          0/1     CrashLoopBackOff   5          3m
```

### 2. Guardian Detects Issue
```
[MonitorService] Found 1 issue(s) in cluster
[MonitorService] Issue detected: [default] my-app-pod → CrashLoopBackOff
```

### 3. Metrics Collection
```
[PrometheusService] Fetching CPU metrics
[PrometheusService] Fetching memory metrics
[PrometheusService] Fetching restart count
[K8sService] Fetching logs for pod my-app-pod
```

### 4. AI Diagnosis
```
[AIService] Requesting AI diagnosis with metrics and logs
[AIService] AI response received
[AIService] Cause: Container repeatedly crashes with 5 restarts
[AIService] Solution: Check logs and verify application startup
```

### 5. Incident Creation
```
[MonitorService] Incident created: abc-123-def-456
[Database] Incident saved to database
```

### 6. Remediation Decision
```
[Safety] Safe action decided: restart_pod for pod my-app-pod
[Safety] Action recorded (attempt 1/3)
```

### 7. Action Execution
```
[OpenClaw] Executing action: restart pod my-app-pod
[OpenClaw] Restart successful: my-app-pod
```

### 8. Frontend Update
```
Dashboard automatically refreshes and displays:
- New incident card
- AI diagnosis
- Remediation action: "restart_pod"
- Action status: "success"
```

### 9. Grafana Visualization
```
Guardian AI Ops Dashboard shows:
- Active incidents: 1
- Remediation events: +1
- Pod restart count increased
```

---

## 🔧 Troubleshooting

### Issue: Backend won't start

**Symptoms:**
```
ModuleNotFoundError: No module named 'fastapi'
```

**Solution:**
```bash
# Ensure virtual environment is activated
source venv/bin/activate  # macOS/Linux
venv\Scripts\activate     # Windows

# Reinstall dependencies
pip install -r requirements.txt
```

---

### Issue: Ollama connection failed

**Symptoms:**
```
[AIService] Error in AI diagnosis: Cannot connect to Ollama at http://localhost:11434
```

**Solution:**
```bash
# Check if Ollama is running
ollama list

# If not running, start Ollama
ollama serve

# In another terminal, verify model is available
ollama pull llama3.1
```

---

### Issue: Prometheus connection failed

**Symptoms:**
```
[PrometheusService] Failed to connect to http://localhost:9090
```

**Solution:**
```bash
# Check if Prometheus pod is running
kubectl get pods -n monitoring

# If not running, redeploy
kubectl apply -f monitoring/prometheus/

# Port-forward to access locally
kubectl port-forward svc/prometheus-service 9090:9090 -n monitoring
```

---

### Issue: Kubernetes connection failed

**Symptoms:**
```
kubernetes.config.config_exception.ConfigException: Invalid kube-config file
```

**Solution:**
```bash
# Verify kubectl works
kubectl get nodes

# Check kubeconfig
kubectl config view

# If using Docker Desktop, ensure Kubernetes is enabled
# Docker Desktop → Settings → Kubernetes → Enable Kubernetes
```

---

### Issue: Frontend shows "Backend Connection Lost"

**Symptoms:**
- Red banner in dashboard
- No incidents loading

**Solution:**
```bash
# 1. Check if backend is running
curl http://127.0.0.1:8000/health

# 2. Check backend logs for errors
# Look in backend terminal for error messages

# 3. Verify CORS settings in backend/app/main.py
# Ensure frontend URL is in allowed origins

# 4. Restart backend
# Press Ctrl+C in backend terminal
uvicorn backend.app.main:app --reload --host 0.0.0.0 --port 8000
```

---

### Issue: No incidents appearing

**Symptoms:**
- Dashboard shows "No Active Incidents"
- Monitoring log shows no issues detected

**Solution:**
```bash
# 1. Create a test failure
kubectl apply -f k8s/test-failures/crashloop.yaml

# 2. Wait 5-10 seconds for detection

# 3. Check monitoring logs
tail -f logs/monitoring.log

# 4. Verify namespace is allowed in agent/safety_rules.py
# Default allowed namespaces: default, development, staging, testing
```

---

### Issue: Grafana dashboards show "No Data"

**Symptoms:**
- Grafana panels display "No data"

**Solution:**
```bash
# 1. Verify Prometheus is collecting metrics
# Open http://localhost:9090
# Go to Status → Targets
# Ensure targets are "UP"

# 2. Wait 2-3 minutes for metrics to populate

# 3. Check Prometheus datasource in Grafana
# Configuration → Data Sources → Prometheus
# Click "Save & Test" - should show "Data source is working"

# 4. Verify time range in dashboard (top right)
# Set to "Last 15 minutes"
```

---

### Issue: Database locked error

**Symptoms:**
```
sqlite3.OperationalError: database is locked
```

**Solution:**
```bash
# Close any open SQLite connections
# Restart the backend

# If issue persists, delete and recreate database
rm data/guardian.db
# Backend will recreate it on next startup
```

---

## 🚀 Running the Complete System

### Full Startup Sequence

```bash
# Terminal 1: Start Ollama (if not running)
ollama serve

# Terminal 2: Start Prometheus port-forward (optional, for local access)
kubectl port-forward svc/prometheus-service 9090:9090 -n monitoring

# Terminal 3: Start Grafana port-forward (optional)
kubectl port-forward svc/grafana-service 3000:3000 -n monitoring

# Terminal 4: Start Backend
cd guardian
source venv/bin/activate  # or venv\Scripts\activate on Windows
uvicorn backend.app.main:app --reload --host 0.0.0.0 --port 8000

# Terminal 5: Start Frontend
cd guardian/frontend
npm run dev
```

### Access Points

| Service | URL | Credentials |
|---------|-----|-------------|
| **Frontend Dashboard** | http://localhost:5173 | None |
| **Backend API** | http://127.0.0.1:8000 | None |
| **API Docs** | http://127.0.0.1:8000/docs | None |
| **Prometheus** | http://localhost:9090 | None |
| **Grafana** | http://localhost:3000 | admin / admin |

---

## 🎯 Future Improvements

Guardian is actively being improved. Planned enhancements include:

- **Predictive Remediation** - ML-based failure prediction before they occur
- **Advanced AI Reasoning** - Multi-stage reasoning with confidence scoring
- **RBAC & Authentication** - Role-based access control for production use
- **Webhook Notifications** - Slack, PagerDuty, email alerts
- **Custom Remediation Actions** - User-defined remediation workflows
- **Distributed Architecture** - Multi-cluster support
- **Historical Analysis** - Trend analysis and pattern detection
- **Cost Optimization** - Resource usage recommendations
- **Compliance Reporting** - Audit logs and compliance dashboards

---

## 📸 Screenshots

### Frontend Dashboard
![Guardian Dashboard](docs/screenshots/dashboard.png)
*Real-time incident monitoring with AI diagnosis*

### Grafana - Kubernetes Monitoring
![Kubernetes Dashboard](docs/screenshots/grafana-k8s.png)
*Infrastructure metrics visualization*

### Grafana - Guardian AI Ops
![Guardian Dashboard](docs/screenshots/grafana-guardian.png)
*AI Ops activity and remediation tracking*

### Incident Detail
![Incident Detail](docs/screenshots/incident-detail.png)
*Detailed incident view with AI analysis*

---

## 📄 License

This project is licensed under the MIT License.

```
MIT License

Copyright (c) 2026 Aaditya

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```

---

## 👨‍💻 Author

**Aaditya**

Guardian - AI-Powered Kubernetes Observability & Autonomous Remediation Platform

---

## 🙏 Acknowledgments

- **Ollama** - For providing local LLM inference
- **Kubernetes** - For container orchestration
- **Prometheus** - For metrics collection
- **Grafana** - For beautiful dashboards
- **FastAPI** - For the excellent Python web framework
- **React** - For the powerful UI library

---

## 📞 Support

If you encounter issues or have questions:

1. Check the [Troubleshooting](#-troubleshooting) section
2. Review the logs in `logs/` directory
3. Check GitHub Issues (if applicable)
4. Consult the API documentation at http://127.0.0.1:8000/docs

---

## ⭐ Star This Project

If you find Guardian useful, please consider giving it a star on GitHub!

---

**Guardian** - Autonomous AI-Powered Kubernetes Operations Platform  
*Making Kubernetes operations intelligent, automated, and observable.*
