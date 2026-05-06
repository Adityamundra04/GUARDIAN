# Action Execution Layer (OpenClaw Integration)

## Overview
Guardian now includes an automatic action execution layer that safely fixes Kubernetes issues without human intervention.

## Architecture

```
┌─────────────────────────────────────────────────┐
│         Kubernetes Issue Detected               │
│         (CrashLoopBackOff, ImagePullBackOff)   │
└────────────────┬────────────────────────────────┘
                 │
                 ▼
┌─────────────────────────────────────────────────┐
│      MonitorService.create_incident()           │
│                                                 │
│  1. Create incident                             │
│  2. Get AI diagnosis                            │
│  3. Execute remediation action ← NEW            │
└────────────────┬────────────────────────────────┘
                 │
                 ▼
┌─────────────────────────────────────────────────┐
│   SafetyRules.decide_action()                   │
│                                                 │
│  • Map issue type → action                      │
│  • Check namespace allowed                      │
│  • Verify action is safe                        │
└────────────────┬────────────────────────────────┘
                 │
                 ▼
┌─────────────────────────────────────────────────┐
│   ActionExecutor.execute()                      │
│                                                 │
│  • restart_pod()                                │
│  • delete_pod()                                 │
│  • scale_deployment()                           │
└─────────────────────────────────────────────────┘
```

## Components

### 1. ActionExecutor (`agent/executor.py`)

**Purpose:** Executes Kubernetes actions safely

**Methods:**
- `restart_pod(namespace, pod_name)` - Restart a pod by deleting it
- `delete_pod(namespace, pod_name)` - Delete a pod (for ImagePullBackOff)
- `scale_deployment(namespace, deployment, replicas)` - Scale a deployment
- `get_pod_owner(namespace, pod_name)` - Get deployment owning a pod

**Example:**
```python
executor = ActionExecutor()
result = executor.restart_pod("default", "my-app-abc123")
# Returns: {"status": "success", "message": "Pod restarted successfully"}
```

### 2. SafetyRules (`agent/safety_rules.py`)

**Purpose:** Define safe actions and enforce safety policies

**Safe Actions Mapping:**
```python
SAFE_ACTIONS = {
    "CrashLoopBackOff": "restart_pod",
    "ImagePullBackOff": "delete_pod",
    "Error: ImagePullBackOff": "delete_pod",
    "High restart count": "restart_pod",
    "Terminated with exit code": "restart_pod",
}
```

**Allowed Namespaces:**
```python
ALLOWED_NAMESPACES = [
    "default",
    "development",
    "staging",
    "testing",
    # "production",  # Disabled by default for safety
]
```

**Methods:**
- `decide_action(issue)` - Decide what action to take
- `is_action_safe(action)` - Verify action is safe
- `get_safe_actions_summary()` - Get safety configuration

### 3. MonitorService Integration

**Updated Methods:**
- `__init__()` - Initialize ActionExecutor
- `create_incident_from_issue()` - Call remediation after incident creation
- `execute_remediation_action()` - NEW - Execute safe actions

## Safety Features

### 1. Namespace Restrictions
- Only executes in allowed namespaces
- Production disabled by default
- Configurable in `safety_rules.py`

### 2. Action Whitelist
- Only predefined safe actions allowed
- No arbitrary commands
- No dangerous operations (delete deployment, etc.)

### 3. Manual Approval Required
```python
MANUAL_APPROVAL_REQUIRED = [
    "scale_deployment",
    "delete_deployment",
    "update_config",
]
```

### 4. Logging
- Every action logged before execution
- Success/failure logged
- Blocked actions logged

## Flow Example: CrashLoopBackOff

### Step-by-Step

1. **Issue Detected**
```
🔍 Found 1 issue(s) in cluster
⚠️  Issue detected: [default] my-app - CrashLoopBackOff
```

2. **Incident Created**
```
🤖 Requesting AI diagnosis for: [default] my-app - CrashLoopBackOff
✅ AI response received
📋 Cause: Container exits immediately due to invalid command
🔧 Solution: Check container entrypoint with kubectl describe
🤖 AI diagnosis added to incident
✅ Incident created: abc-123 - [default] my-app → CrashLoopBackOff
```

3. **Action Decided**
```
✅ Safe action decided: restart_pod for pod my-app
```

4. **Action Executed**
```
🔄 Executing action: restart pod my-app in namespace default
✅ Pod my-app deleted successfully (will be recreated)
✅ Remediation action completed: Pod my-app restarted successfully
```

### Complete Log Output
```
🔍 Found 1 issue(s) in cluster
⚠️  Issue detected: [default] my-app - CrashLoopBackOff
🤖 Requesting AI diagnosis for: [default] my-app - CrashLoopBackOff
✅ AI response received (245 chars)
📋 Cause: Container exits immediately due to invalid command...
🔧 Solution: Check container entrypoint with kubectl describe...
🤖 AI diagnosis added to incident
✅ Incident created: abc-123 - [default] my-app → CrashLoopBackOff
✅ Safe action decided: restart_pod for pod my-app
🔄 Executing action: restart pod my-app in namespace default
✅ Pod my-app deleted successfully (will be recreated)
✅ Remediation action completed: Pod my-app restarted successfully
```

## Supported Actions

### 1. Restart Pod (CrashLoopBackOff)
**Trigger:** CrashLoopBackOff, High restart count, Terminated with exit code
**Action:** Delete pod (Kubernetes recreates it)
**Use case:** Temporary failures, transient errors

### 2. Delete Pod (ImagePullBackOff)
**Trigger:** ImagePullBackOff, Error: ImagePullBackOff
**Action:** Delete pod to retry image pull
**Use case:** Temporary registry issues, image pull failures

### 3. Scale Deployment (Future)
**Trigger:** Manual approval required
**Action:** Scale deployment up/down
**Use case:** Resource issues (currently disabled)

## Configuration

### Enable Production Auto-Fix
```python
# In agent/safety_rules.py
ALLOWED_NAMESPACES = [
    "default",
    "development",
    "staging",
    "testing",
    "production",  # ← Uncomment to enable
]
```

### Add New Safe Action
```python
# In agent/safety_rules.py
SAFE_ACTIONS = {
    "CrashLoopBackOff": "restart_pod",
    "ImagePullBackOff": "delete_pod",
    "MyNewIssue": "my_new_action",  # ← Add new mapping
}
```

### Implement New Action
```python
# In agent/executor.py
def my_new_action(self, namespace: str, pod_name: str) -> Dict[str, str]:
    """Execute my new action."""
    try:
        print(f"🔧 Executing action: my_new_action for {pod_name}")
        # Implementation here
        return {"status": "success", "message": "Action completed"}
    except Exception as e:
        return {"status": "error", "message": str(e)}
```

## Testing

### Test CrashLoopBackOff Auto-Fix
```bash
# 1. Start Guardian
cd backend && uvicorn app.main:app --reload

# 2. Deploy failing pod
kubectl apply -f k8s/test-failures/crashloop.yaml

# 3. Watch logs (Guardian will auto-restart the pod)
# Expected: Pod deleted and recreated automatically

# 4. Verify incident
curl http://localhost:8000/incidents/
```

### Test ImagePullBackOff Auto-Fix
```bash
# 1. Create pod with invalid image
kubectl run test-image --image=invalid/image:tag

# 2. Watch Guardian logs
# Expected: Pod deleted automatically

# 3. Verify action executed
kubectl get pods
```

### Test Safety Blocks

#### Test 1: Production Namespace (Blocked)
```bash
# 1. Create failing pod in production
kubectl create namespace production
kubectl run test-prod --image=busybox --namespace=production -- /bin/sh -c "exit 1"

# 2. Watch Guardian logs
# Expected: ⚠️  Auto-execution disabled for namespace: production
```

#### Test 2: Unknown Issue (No Action)
```bash
# 1. Create pod with unknown issue
# Expected: ℹ️  No safe action defined for issue: <issue_type>
```

## API Response

### Before Action Execution
```json
{
  "id": "abc-123",
  "issue": "[default] my-app → CrashLoopBackOff",
  "status": "detected",
  "cause": "Container exits immediately due to invalid command",
  "solution": "Check container entrypoint with kubectl describe"
}
```

### After Action Execution
The incident remains the same, but the pod is automatically restarted in Kubernetes.

## Safety Guarantees

✅ **Only whitelisted actions** - No arbitrary commands  
✅ **Namespace restrictions** - Only allowed namespaces  
✅ **No dangerous operations** - No delete deployment, no scale down to 0  
✅ **Logging before execution** - Every action logged  
✅ **Error handling** - Failures don't crash system  
✅ **Manual approval for risky actions** - Scale, delete deployment require approval  

## Files Created

```
agent/
├── __init__.py
├── executor.py          # Action execution
└── safety_rules.py      # Safety policies

backend/app/services/
└── monitor_service.py   # Updated with action execution
```

## Monitoring

### Check Safety Configuration
```python
from agent.safety_rules import SafetyRules

config = SafetyRules.get_safe_actions_summary()
print(config)
# Output:
# {
#   "safe_actions": {...},
#   "manual_approval_required": [...],
#   "allowed_namespaces": [...]
# }
```

### Disable Auto-Execution
```python
# In agent/safety_rules.py
ALLOWED_NAMESPACES = []  # Disable all auto-execution
```

## Troubleshooting

### Issue: Actions not executing
**Check:**
1. Is namespace in `ALLOWED_NAMESPACES`?
2. Is issue type in `SAFE_ACTIONS`?
3. Check Guardian logs for safety blocks

### Issue: Action fails
**Check:**
1. Kubernetes permissions (RBAC)
2. Pod exists and is in correct namespace
3. Check error message in logs

### Issue: Wrong action executed
**Check:**
1. Issue type mapping in `SAFE_ACTIONS`
2. Verify issue detection is correct
3. Review safety rules logic

## Future Enhancements

1. **Action history** - Track all executed actions
2. **Rollback capability** - Undo actions if they fail
3. **Rate limiting** - Limit actions per time period
4. **Approval workflow** - Request approval for risky actions
5. **Action scheduling** - Schedule actions for maintenance windows
6. **Multi-step actions** - Chain multiple actions
7. **Conditional actions** - Execute based on conditions

## Success Criteria

✅ **CrashLoopBackOff auto-fixed** - Pod restarted automatically  
✅ **ImagePullBackOff auto-fixed** - Pod deleted and recreated  
✅ **Safety enforced** - Only safe actions in allowed namespaces  
✅ **Logging complete** - All actions logged  
✅ **Error handling** - System continues on failures  

🎉 **Guardian now automatically fixes Kubernetes issues!**
