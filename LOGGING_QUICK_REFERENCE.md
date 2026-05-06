# 📖 Guardian Logging - Quick Reference

## 🚀 Quick Start

### Import Logger
```python
from backend.app.core.logger import get_monitor_logger

logger = get_monitor_logger()
```

### Log Messages
```python
logger.info("Normal operation message")
logger.warning("Warning message")
logger.error("Error message", exc_info=True)
logger.debug("Debug message")
```

---

## 📁 Log Files

| File | Content | Location |
|------|---------|----------|
| **guardian.log** | All logs from all services | `logs/guardian.log` |
| **errors.log** | ERROR level and above only | `logs/errors.log` |
| **monitoring.log** | Monitoring services | `logs/monitoring.log` |
| **ai.log** | AI service | `logs/ai.log` |
| **actions.log** | Remediation actions | `logs/actions.log` |

---

## 🔧 Available Loggers

```python
from backend.app.core.logger import (
    get_monitor_logger,      # MonitorService
    get_ai_logger,           # AIService
    get_prometheus_logger,   # PrometheusService
    get_k8s_logger,          # K8sService
    get_action_logger,       # ActionExecutor (OpenClaw)
    get_safety_logger        # SafetyRules
)
```

---

## 📊 Log Levels

| Level | When to Use | Example |
|-------|-------------|---------|
| **DEBUG** | Detailed diagnostic info | `logger.debug("Query: SELECT * FROM...")` |
| **INFO** | Normal operations | `logger.info("Issue detected")` |
| **WARNING** | Potential issues | `logger.warning("Retry limit reached")` |
| **ERROR** | Errors with stack traces | `logger.error("Failed", exc_info=True)` |

---

## 💡 Common Patterns

### Pattern 1: Info Logging
```python
logger.info(f"Issue detected: {pod_name} in {namespace}")
```

### Pattern 2: Warning Logging
```python
logger.warning(f"Failed to fetch metrics: {error}")
```

### Pattern 3: Error Logging with Stack Trace
```python
try:
    risky_operation()
except Exception as e:
    logger.error(f"Operation failed: {e}", exc_info=True)
```

### Pattern 4: Debug Logging
```python
logger.debug(f"Executing query: {query}")
```

---

## 🔍 View Logs

### View All Logs
```bash
tail -f logs/guardian.log
```

### View Errors Only
```bash
tail -f logs/errors.log
```

### View Monitoring Activity
```bash
tail -f logs/monitoring.log
```

### View AI Activity
```bash
tail -f logs/ai.log
```

### View Actions
```bash
tail -f logs/actions.log
```

### List All Log Files
```bash
ls -lh logs/
```

---

## ⚙️ Configuration

### Change Log Level
Edit `backend/app/core/logger.py`:
```python
LOG_LEVEL = logging.DEBUG    # More verbose
LOG_LEVEL = logging.INFO     # Default
LOG_LEVEL = logging.WARNING  # Less verbose
```

### Change Log File Size
Edit `backend/app/core/logger.py`:
```python
def create_rotating_handler(log_file, max_bytes=10*1024*1024, backup_count=10):
    # 10MB max, 10 backups
```

---

## ✅ Best Practices

### ✅ DO
- Use appropriate log levels
- Include context in messages
- Use `exc_info=True` for exceptions
- Log important events
- Use structured format

### ❌ DON'T
- Log sensitive data (passwords, tokens)
- Log in tight loops (use DEBUG level)
- Use print() statements
- Log without context
- Ignore exceptions

---

## 🧪 Test Logging

```bash
python test_logging_system.py
```

**Expected Output**:
```
✅ Root logger initialized
✅ Logs directory exists
✅ All service loggers working
✅ Error logging working
✅ All log files created
```

---

## 📖 Example Usage

### MonitorService
```python
from backend.app.core.logger import get_monitor_logger

logger = get_monitor_logger()

logger.info(f"Issue detected: {incident_message}")
logger.info("Prometheus metrics attached to AI context")
logger.info("AI diagnosis completed")
logger.info(f"Incident created: {incident.id}")
logger.warning(f"Failed to fetch metrics: {error}")
logger.error(f"Monitoring error: {e}", exc_info=True)
```

### AIService
```python
from backend.app.core.logger import get_ai_logger

logger = get_ai_logger()

logger.info(f"Requesting AI diagnosis for: {log_msg}")
logger.info(f"AI response received ({len(response)} chars)")
logger.info(f"Cause: {diagnosis['cause'][:80]}")
logger.error(f"Error in AI diagnosis: {e}", exc_info=True)
```

### ActionExecutor
```python
from backend.app.core.logger import get_action_logger

logger = get_action_logger()

logger.info(f"Executing action: restart pod {pod_name}")
logger.info(f"Restart successful: {pod_name}")
logger.warning(f"Restart failed: {error_msg}")
```

---

## 🎯 Quick Commands

```bash
# Start Guardian
cd backend && python -m app.main

# Test logging
python test_logging_system.py

# View all logs
tail -f logs/guardian.log

# View errors
tail -f logs/errors.log

# Check log sizes
ls -lh logs/

# Clear logs (if needed)
rm logs/*.log
```

---

## 📚 More Information

- **Full Documentation**: `PHASE13_LOGGING_COMPLETE.md`
- **Implementation Details**: `LOGGING_SYSTEM_COMPLETE.md`
- **Logger Module**: `backend/app/core/logger.py`
- **Test Script**: `test_logging_system.py`
