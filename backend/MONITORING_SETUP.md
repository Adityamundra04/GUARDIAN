# Guardian Real-Time Monitoring System

## Overview
Guardian now includes automatic Kubernetes monitoring that detects issues and creates incidents in real-time.

## How It Works

### 1. Monitor Service (`backend/app/services/monitor_service.py`)
- **MonitorService class** manages the monitoring logic
- **check_system()**: Checks Kubernetes for problematic pods
- **create_incident_from_issue()**: Creates incidents automatically
- **Duplicate Prevention**: Uses a set to track active issues (format: `namespace/pod-name`)

### 2. Background Monitoring (`backend/app/main.py`)
- **Background thread** runs continuously (daemon mode)
- **Monitoring interval**: Every 5 seconds
- **Auto-start**: Launches on application startup
- **Error handling**: Catches exceptions to prevent crashes

### 3. Incident Flow
```
Kubernetes Issue Detected
    ↓
MonitorService.check_system()
    ↓
Issue Found?
    ↓ (yes)
Check if duplicate
    ↓ (not duplicate)
Create Incident
    ↓
Add to incidents_db
    ↓
Track in active_issues set
```

## Features

✅ **Automatic Detection**
- High restart counts (> 2)
- CrashLoopBackOff states
- Error states
- Terminated containers

✅ **Duplicate Prevention**
- Tracks active issues by `namespace/pod-name`
- Skips creating duplicate incidents

✅ **Continuous Monitoring**
- Runs in background thread
- 5-second check interval
- Daemon thread (stops with app)

✅ **Error Safety**
- Try-catch blocks prevent crashes
- Kubernetes connection errors handled
- Monitoring continues on errors

✅ **Logging**
- "🚀 Monitoring started..."
- "Issue detected: Pod X - Y"
- "Incident created: ID - Description"
- "Skipping duplicate incident for X"

## Running the System

```bash
# Start the server
cd backend
uvicorn app.main:app --reload

# Expected output:
# 🔧 Starting Guardian application...
# 🚀 Monitoring started...
# ✅ Background monitoring thread started
```

## Testing

### 1. Check if monitoring is running
```bash
curl http://localhost:8000/health
# Response: {"status": "ok"}
```

### 2. View auto-created incidents
```bash
curl http://localhost:8000/incidents/
# Returns list of incidents (empty if no K8s issues)
```

### 3. Simulate a pod crash in Kubernetes
- The system will detect it within 5 seconds
- An incident will be created automatically
- Check logs for: "Issue detected: Pod..."

## Architecture

```
┌─────────────────────────────────────┐
│   FastAPI Application (main.py)    │
│                                     │
│  ┌──────────────────────────────┐  │
│  │  Background Thread (daemon)  │  │
│  │                              │  │
│  │  Every 5 seconds:            │  │
│  │  1. Check K8s cluster        │  │
│  │  2. Detect issues            │  │
│  │  3. Create incidents         │  │
│  └──────────────────────────────┘  │
│                                     │
│  ┌──────────────────────────────┐  │
│  │   MonitorService             │  │
│  │   - check_system()           │  │
│  │   - create_incident()        │  │
│  │   - active_issues tracking   │  │
│  └──────────────────────────────┘  │
│                                     │
│  ┌──────────────────────────────┐  │
│  │   K8sService                 │  │
│  │   - get_problematic_pods()   │  │
│  └──────────────────────────────┘  │
│                                     │
│  ┌──────────────────────────────┐  │
│  │   Incidents API              │  │
│  │   - incidents_db (in-memory) │  │
│  └──────────────────────────────┘  │
└─────────────────────────────────────┘
```

## Next Steps

### Optional Enhancements:
1. **Configurable interval**: Add environment variable for check frequency
2. **Issue resolution**: Auto-clear resolved issues from tracking
3. **Webhooks**: Send notifications when incidents are created
4. **Metrics**: Track detection rate, incident count
5. **AI Integration**: Use Ollama to suggest solutions

## Notes

- Monitoring runs as a **daemon thread** (stops when app stops)
- **No database** required (in-memory storage)
- **Thread-safe**: Uses simple list append (safe for single writer)
- **Production-ready**: Error handling prevents crashes
