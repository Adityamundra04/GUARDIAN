# ✅ Guardian Demo Website - Verification Checklist

Use this checklist to verify the demo website is working correctly.

## 📋 Pre-Deployment Verification

### Prerequisites
- [ ] Kubernetes cluster is running
  ```bash
  kubectl cluster-info
  ```
- [ ] kubectl is installed and configured
  ```bash
  kubectl version --client
  ```
- [ ] Guardian backend is running
  ```bash
  curl http://localhost:8000/health
  ```
- [ ] Prometheus is running
  ```bash
  curl http://localhost:9090/-/healthy
  ```
- [ ] Frontend is accessible
  ```bash
  curl http://localhost:5173
  ```

## 🚀 Deployment Verification

### Step 1: Deploy Resources
- [ ] ConfigMap deployed successfully
  ```bash
  kubectl apply -f k8s/demo-website/configmap.yaml
  kubectl get configmap guardian-demo-html
  ```
- [ ] Deployment created successfully
  ```bash
  kubectl apply -f k8s/demo-website/deployment.yaml
  kubectl get deployment guardian-demo-website
  ```
- [ ] Service created successfully
  ```bash
  kubectl apply -f k8s/demo-website/service.yaml
  kubectl get svc guardian-demo-website
  ```

### Step 2: Pod Status
- [ ] Pod is running
  ```bash
  kubectl get pods -l app=guardian-demo
  # Expected: STATUS = Running
  ```
- [ ] Pod has correct labels
  ```bash
  kubectl get pods -l app=guardian-demo -o jsonpath='{.items[0].metadata.labels}'
  # Expected: app=guardian-demo, component=website
  ```
- [ ] Pod is ready (1/1)
  ```bash
  kubectl get pods -l app=guardian-demo -o jsonpath='{.items[0].status.containerStatuses[0].ready}'
  # Expected: true
  ```

### Step 3: Service Configuration
- [ ] Service type is NodePort
  ```bash
  kubectl get svc guardian-demo-website -o jsonpath='{.spec.type}'
  # Expected: NodePort
  ```
- [ ] NodePort is 30080
  ```bash
  kubectl get svc guardian-demo-website -o jsonpath='{.spec.ports[0].nodePort}'
  # Expected: 30080
  ```
- [ ] Service selector matches pod labels
  ```bash
  kubectl get svc guardian-demo-website -o jsonpath='{.spec.selector}'
  # Expected: app=guardian-demo, component=website
  ```

### Step 4: ConfigMap Content
- [ ] ConfigMap contains index.html
  ```bash
  kubectl get configmap guardian-demo-html -o jsonpath='{.data.index\.html}' | head -n 5
  # Expected: <!DOCTYPE html>
  ```
- [ ] ConfigMap is mounted in pod
  ```bash
  kubectl describe pod -l app=guardian-demo | grep -A 5 "Mounts:"
  # Expected: /usr/share/nginx/html from html-content
  ```

## 🌐 Access Verification

### Step 1: Website Accessibility
- [ ] Website loads via NodePort
  ```bash
  curl -s http://localhost:30080 | grep "Guardian Demo"
  # Expected: <h1>Guardian Demo</h1>
  ```
- [ ] Website returns HTTP 200
  ```bash
  curl -s -o /dev/null -w "%{http_code}" http://localhost:30080
  # Expected: 200
  ```
- [ ] Website displays in browser
  - Open: http://localhost:30080
  - [ ] Purple gradient background visible
  - [ ] Shield icon (🛡️) visible
  - [ ] "Guardian Demo" title visible
  - [ ] "System Operational" status visible

### Step 2: Port Forward (Alternative)
- [ ] Port forward works
  ```bash
  kubectl port-forward svc/guardian-demo-website 8080:80 &
  curl -s http://localhost:8080 | grep "Guardian Demo"
  # Expected: <h1>Guardian Demo</h1>
  ```

## 📊 Monitoring Verification

### Step 1: Prometheus Metrics
- [ ] Pod metrics are scraped
  ```bash
  curl -s 'http://localhost:9090/api/v1/query?query=kube_pod_status_phase{pod=~"guardian-demo.*"}' | jq '.data.result'
  # Expected: Non-empty result
  ```
- [ ] Container metrics available
  ```bash
  curl -s 'http://localhost:9090/api/v1/query?query=container_memory_usage_bytes{pod=~"guardian-demo.*"}' | jq '.data.result'
  # Expected: Non-empty result
  ```

### Step 2: Grafana Dashboard
- [ ] Grafana is accessible
  ```bash
  curl -s http://localhost:3000/api/health
  # Expected: {"database":"ok"}
  ```
- [ ] Kubernetes dashboard exists
  - Open: http://localhost:3000
  - Login: admin / admin
  - [ ] "Kubernetes Monitoring" dashboard visible
  - [ ] Can filter by app=guardian-demo

### Step 3: Guardian Backend
- [ ] Backend detects demo pod
  ```bash
  # Wait 30 seconds for monitoring cycle
  curl -s http://localhost:8000/incidents | jq '.[] | select(.pod_name | contains("guardian-demo"))'
  # Expected: May be empty if no issues (healthy pod)
  ```

## 🧪 Failure Scenario Verification

### Test 1: CrashLoopBackOff
- [ ] Failure manifest deploys
  ```bash
  kubectl apply -f k8s/demo-website/failure-crashloop.yaml
  kubectl get pod demo-crashloop-failure
  ```
- [ ] Pod enters CrashLoopBackOff
  ```bash
  # Wait 30 seconds
  kubectl get pod demo-crashloop-failure -o jsonpath='{.status.containerStatuses[0].state.waiting.reason}'
  # Expected: CrashLoopBackOff
  ```
- [ ] Guardian detects failure
  ```bash
  # Wait 60 seconds
  curl -s http://localhost:8000/incidents | jq '.[] | select(.pod_name == "demo-crashloop-failure")'
  # Expected: Incident object with AI diagnosis
  ```
- [ ] Dashboard shows incident
  - Open: http://localhost:5173
  - [ ] Incident card visible
  - [ ] Pod name: demo-crashloop-failure
  - [ ] Status: CrashLoopBackOff
  - [ ] AI diagnosis present
- [ ] Cleanup successful
  ```bash
  kubectl delete pod demo-crashloop-failure
  kubectl get pod demo-crashloop-failure
  # Expected: Error (not found)
  ```

### Test 2: ImagePullBackOff
- [ ] Failure manifest deploys
  ```bash
  kubectl apply -f k8s/demo-website/failure-imagepull.yaml
  kubectl get pod demo-imagepull-failure
  ```
- [ ] Pod enters ImagePullBackOff
  ```bash
  # Wait 30 seconds
  kubectl get pod demo-imagepull-failure -o jsonpath='{.status.containerStatuses[0].state.waiting.reason}'
  # Expected: ImagePullBackOff or ErrImagePull
  ```
- [ ] Guardian detects failure
  ```bash
  # Wait 60 seconds
  curl -s http://localhost:8000/incidents | jq '.[] | select(.pod_name == "demo-imagepull-failure")'
  # Expected: Incident object
  ```
- [ ] Dashboard shows incident
  - Open: http://localhost:5173
  - [ ] Incident visible
  - [ ] AI diagnosis mentions image issue
- [ ] Cleanup successful
  ```bash
  kubectl delete pod demo-imagepull-failure
  ```

### Test 3: Out of Memory
- [ ] Failure manifest deploys
  ```bash
  kubectl apply -f k8s/demo-website/failure-oom.yaml
  kubectl get pod demo-oom-failure
  ```
- [ ] Pod gets OOMKilled
  ```bash
  # Wait 30 seconds
  kubectl get pod demo-oom-failure -o jsonpath='{.status.containerStatuses[0].lastState.terminated.reason}'
  # Expected: OOMKilled
  ```
- [ ] Guardian detects failure
  ```bash
  # Wait 60 seconds
  curl -s http://localhost:8000/incidents | jq '.[] | select(.pod_name == "demo-oom-failure")'
  # Expected: Incident object
  ```
- [ ] Dashboard shows incident
  - Open: http://localhost:5173
  - [ ] Incident visible
  - [ ] AI diagnosis mentions memory
- [ ] Cleanup successful
  ```bash
  kubectl delete pod demo-oom-failure
  ```

## 🔧 Script Verification

### Deployment Script
- [ ] deploy.sh is executable
  ```bash
  ls -l k8s/demo-website/deploy.sh
  # Expected: -rwxr-xr-x (or similar with x permission)
  ```
- [ ] deploy.sh runs successfully
  ```bash
  cd k8s/demo-website
  ./deploy.sh
  # Expected: "✅ Deployment complete!"
  ```
- [ ] All resources created
  ```bash
  kubectl get all -l app=guardian-demo
  # Expected: deployment, pod, service
  ```

### Cleanup Script
- [ ] cleanup.sh is executable
  ```bash
  ls -l k8s/demo-website/cleanup.sh
  ```
- [ ] cleanup.sh runs successfully
  ```bash
  cd k8s/demo-website
  ./cleanup.sh
  # Expected: "✅ Cleanup complete!"
  ```
- [ ] All resources removed
  ```bash
  kubectl get all -l app=guardian-demo
  # Expected: No resources found
  ```

### Test Script
- [ ] test-failures.sh is executable
  ```bash
  ls -l k8s/demo-website/test-failures.sh
  ```
- [ ] test-failures.sh menu works
  ```bash
  cd k8s/demo-website
  echo "0" | ./test-failures.sh
  # Expected: Menu displays and exits
  ```

## 📚 Documentation Verification

### File Existence
- [ ] README.md exists and is complete
  ```bash
  wc -l k8s/demo-website/README.md
  # Expected: 500+ lines
  ```
- [ ] TESTING_GUIDE.md exists
  ```bash
  wc -l k8s/demo-website/TESTING_GUIDE.md
  # Expected: 700+ lines
  ```
- [ ] QUICK_REFERENCE.md exists
  ```bash
  wc -l k8s/demo-website/QUICK_REFERENCE.md
  # Expected: 200+ lines
  ```
- [ ] IMPLEMENTATION_SUMMARY.md exists
  ```bash
  wc -l k8s/demo-website/IMPLEMENTATION_SUMMARY.md
  # Expected: 400+ lines
  ```

### Content Quality
- [ ] README has architecture diagram
  ```bash
  grep -q "Architecture" k8s/demo-website/README.md
  ```
- [ ] README has quick start section
  ```bash
  grep -q "Quick Start" k8s/demo-website/README.md
  ```
- [ ] TESTING_GUIDE has step-by-step instructions
  ```bash
  grep -q "Step 1:" k8s/demo-website/TESTING_GUIDE.md
  ```
- [ ] QUICK_REFERENCE has command examples
  ```bash
  grep -q "kubectl" k8s/demo-website/QUICK_REFERENCE.md
  ```

### Main README Integration
- [ ] Main README mentions demo website
  ```bash
  grep -q "Demo Website" README.md
  ```
- [ ] Main README links to demo docs
  ```bash
  grep -q "k8s/demo-website/README.md" README.md
  ```

## 🎯 End-to-End Workflow

### Complete Test Flow
- [ ] Start with clean cluster
  ```bash
  kubectl delete -f k8s/demo-website/ --ignore-not-found
  ```
- [ ] Deploy demo website
  ```bash
  cd k8s/demo-website && ./deploy.sh
  ```
- [ ] Verify website is accessible
  ```bash
  curl -s http://localhost:30080 | grep "Guardian Demo"
  ```
- [ ] Deploy failure scenario
  ```bash
  kubectl apply -f failure-crashloop.yaml
  ```
- [ ] Wait for Guardian detection (60s)
  ```bash
  sleep 60
  ```
- [ ] Verify incident in API
  ```bash
  curl -s http://localhost:8000/incidents | jq '.[0].pod_name'
  ```
- [ ] Verify incident in dashboard
  - Open: http://localhost:5173
  - [ ] Incident visible
- [ ] Verify metrics in Grafana
  - Open: http://localhost:3000
  - [ ] Pod restart count increased
- [ ] Cleanup everything
  ```bash
  ./cleanup.sh
  ```
- [ ] Verify cleanup
  ```bash
  kubectl get all -l app=guardian-demo
  # Expected: No resources found
  ```

## ✅ Final Verification

### All Systems Go
- [ ] Demo website deploys successfully
- [ ] Website is accessible via browser
- [ ] All three failure scenarios work
- [ ] Guardian detects all failures
- [ ] AI provides diagnosis for all failures
- [ ] Dashboard displays incidents correctly
- [ ] Prometheus collects metrics
- [ ] Grafana visualizes data
- [ ] Scripts work correctly
- [ ] Documentation is complete
- [ ] Cleanup works properly

## 🎉 Success Criteria

If all items above are checked, the Guardian demo website is:
- ✅ **Fully functional**
- ✅ **Properly integrated**
- ✅ **Well documented**
- ✅ **Ready for use**

---

## 📝 Notes

Use this space to record any issues or observations:

```
Date: ___________
Tester: ___________

Issues Found:
- 

Observations:
- 

Recommendations:
- 
```

---

**Verification Date:** ___________  
**Verified By:** ___________  
**Status:** ⬜ PASS / ⬜ FAIL  
**Notes:** ___________
