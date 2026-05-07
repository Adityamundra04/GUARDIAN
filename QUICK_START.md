# 🚀 Guardian Quick Start Guide

Get Guardian up and running in **5 minutes**!

---

## ⚡ Prerequisites Check

Before starting, verify you have:

```bash
# Check Python
python --version  # Should be 3.9+

# Check Node.js
node --version    # Should be 18+

# Check kubectl
kubectl version --client

# Check Kubernetes cluster
kubectl get nodes

# Check Ollama
ollama --version
```

---

## 🎯 5-Minute Setup

### Step 1: Install Ollama & Pull Model (2 minutes)

```bash
# Install Ollama (if not installed)
curl -fsSL https://ollama.com/install.sh | sh

# Pull llama3.1 model
ollama pull llama3.1

# Keep Ollama running in background
ollama serve &
```

---

### Step 2: Deploy Prometheus (1 minute)

```bash
# Deploy Prometheus
kubectl apply -f monitoring/prometheus/

# Verify deployment
kubectl get pods -n monitoring

# Expected output:
# NAME                          READY   STATUS    RESTARTS   AGE
# prometheus-xxxxxxxxxx-xxxxx   1/1     Running   0          30s
```

---

### Step 3: Start Backend (1 minute)

```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
source venv/bin/activate  # macOS/Linux
# OR
venv\Scripts\activate     # Windows

# Install dependencies
pip install -r requirements.txt

# Start backend
uvicorn backend.app.main:app --reload --host 0.0.0.0 --port 8000
```

**Expected Output**:
```
INFO:     Uvicorn running on http://0.0.0.0:8000
[2026-05-06 10:00:00] [INFO] [Guardian] Guardian Application Started
[2026-05-06 10:00:00] [INFO] [Guardian] Background monitoring thread started
```

---

### Step 4: Start Frontend (1 minute)

**Open a new terminal** (keep backend running):

```bash
# Navigate to frontend
cd frontend

# Install dependencies (first time only)
npm install

# Start frontend
npm run dev
```

**Expected Output**:
```
VITE v5.0.0  ready in 500 ms
➜  Local:   http://localhost:5173/
```

---

## 🎉 You're Ready!

Open your browser to: **http://localhost:5173**

You should see:
- ✅ Guardian dashboard with futuristic UI
- ✅ "LIVE" indicator (green)
- ✅ System status showing "ONLINE"
- ✅ "All Systems Operational" message

---

## 🧪 Test It Out

### Create a Test Incident

```bash
# Deploy a crashloop pod
kubectl apply -f k8s/test-failures/crashloop.yaml

# Watch the pod fail
kubectl get pods -w
```

**What happens**:
1. Pod enters CrashLoopBackOff (10-15 seconds)
2. Guardian detects the failure
3. AI analyzes the issue
4. Remediation action executes
5. Incident appears in dashboard

**Check the dashboard**: New incident card should appear with AI diagnosis!

---

## 🔍 Verify Integration

Run the integration test script:

```bash
# Make script executable
chmod +x test_integration.sh

# Run tests
./test_integration.sh
```

**Expected Output**:
```
==========================================
Guardian Integration Test
==========================================

Test 1: Checking backend status...
✓ Backend is running (HTTP 200)

Test 2: Checking root endpoint...
✓ Root endpoint responding correctly

Test 3: Checking incidents endpoint...
✓ Incidents endpoint responding (HTTP 200)
→ Current incidents: 1

Test 4: Checking CORS configuration...
✓ CORS headers present

Test 5: Checking frontend status...
✓ Frontend is running (HTTP 200)

==========================================
Integration Test Summary
==========================================

✓ Backend Integration: PASS
✓ Frontend Status: RUNNING
✓ CORS Configuration: OK
```

---

## 📊 Access Points

| Service | URL | Purpose |
|---------|-----|---------|
| **Frontend Dashboard** | http://localhost:5173 | Main UI |
| **Backend API** | http://127.0.0.1:8000 | REST API |
| **API Docs** | http://127.0.0.1:8000/docs | Swagger UI |
| **Prometheus** | http://localhost:9090 | Metrics (port-forward) |

---

## 🐛 Quick Troubleshooting

### Backend won't start

```bash
# Ensure virtual environment is activated
source venv/bin/activate

# Reinstall dependencies
pip install -r requirements.txt
```

### Frontend shows "Backend Connection Lost"

```bash
# Check if backend is running
curl http://127.0.0.1:8000/health

# Should return: {"status":"ok"}
```

### Ollama connection failed

```bash
# Check if Ollama is running
ollama list

# If not running, start it
ollama serve
```

### No incidents appearing

```bash
# Check monitoring logs
tail -f logs/monitoring.log

# Verify namespace is allowed in agent/safety_rules.py
# Default: default, development, staging, testing
```

---

## 🎯 Next Steps

1. **Deploy Grafana** (optional):
   ```bash
   cd monitoring/grafana
   bash deploy.sh
   # Access: http://localhost:3000 (admin/admin)
   ```

2. **Explore API Documentation**:
   - Open http://127.0.0.1:8000/docs
   - Try the interactive API endpoints

3. **Check Logs**:
   ```bash
   # Main log
   tail -f logs/guardian.log
   
   # AI diagnosis log
   tail -f logs/ai.log
   
   # Remediation actions
   tail -f logs/actions.log
   ```

4. **Create More Test Failures**:
   ```bash
   # Out of memory test
   kubectl apply -f k8s/test-failures/oom.yaml
   
   # Bad config test
   kubectl apply -f k8s/test-failures/bad-config.yaml
   ```

---

## 📚 Documentation

- **Full README**: `README.md`
- **Integration Guide**: `FRONTEND_BACKEND_INTEGRATION.md`
- **Engineering Review**: `ENGINEERING_REVIEW.md`

---

## ✅ Success Checklist

- [ ] Ollama installed and running
- [ ] llama3.1 model pulled
- [ ] Kubernetes cluster running
- [ ] Prometheus deployed
- [ ] Backend started (port 8000)
- [ ] Frontend started (port 5173)
- [ ] Dashboard accessible
- [ ] "LIVE" indicator green
- [ ] Test incident created
- [ ] Incident appears in dashboard
- [ ] AI diagnosis visible
- [ ] Remediation action shown

---

## 🎉 Congratulations!

Guardian is now running! You have:

- ✅ AI-powered Kubernetes monitoring
- ✅ Automatic incident detection
- ✅ AI diagnosis with metrics and logs
- ✅ Autonomous remediation
- ✅ Real-time dashboard
- ✅ Persistent incident tracking

**Enjoy your autonomous AI Ops platform!** 🚀

---

**Need Help?** Check the troubleshooting section in `README.md`
