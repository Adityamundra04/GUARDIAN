# 📖 Guardian Database - Quick Reference

## 🚀 Quick Start

### Install SQLAlchemy
```bash
pip install sqlalchemy
```

### Start Guardian
```bash
cd backend
python -m app.main
```

**Database auto-created at**: `data/guardian.db`

---

## 📁 Database Files

| File | Purpose | Location |
|------|---------|----------|
| **guardian.db** | SQLite database | `data/guardian.db` |
| **database.py** | Configuration | `backend/app/core/database.py` |
| **incident_db.py** | ORM model | `backend/app/models/incident_db.py` |

---

## 🔧 Database Functions

### Initialize Database
```python
from backend.app.core.database import init_database

init_database()  # Creates database and tables
```

### Get Database Session (FastAPI)
```python
from backend.app.core.database import get_db
from fastapi import Depends

@router.get("/")
async def endpoint(db: Session = Depends(get_db)):
    # Use db here
    pass
```

### Get Database Session (Manual)
```python
from backend.app.core.database import get_db_session

db = get_db_session()
try:
    # Use db here
    db.commit()
finally:
    db.close()
```

---

## 📊 Database Schema

### Incidents Table

| Column | Type | Description |
|--------|------|-------------|
| `id` | String (PK) | UUID |
| `issue` | String | Incident description |
| `status` | String | Current status |
| `cause` | String | Root cause |
| `solution` | String | Proposed solution |
| `action_taken` | String | Remediation action |
| `action_status` | String | Action status |
| `created_at` | DateTime | Timestamp |

---

## 💡 Common Operations

### Create Incident
```python
from backend.app.models.incident_db import IncidentDB

db_incident = IncidentDB(
    issue="[default] crash-test → CrashLoopBackOff",
    status="detected",
    cause="Container crashes on startup",
    solution="Check logs and restart pod"
)

db.add(db_incident)
db.commit()
db.refresh(db_incident)
```

### Query All Incidents
```python
incidents = db.query(IncidentDB).all()
```

### Query by ID
```python
incident = db.query(IncidentDB).filter(IncidentDB.id == incident_id).first()
```

### Query by Status
```python
incidents = db.query(IncidentDB).filter(IncidentDB.status == "detected").all()
```

### Update Incident
```python
incident = db.query(IncidentDB).filter(IncidentDB.id == incident_id).first()
incident.status = "resolved"
db.commit()
```

### Order by Created Date
```python
incidents = db.query(IncidentDB).order_by(IncidentDB.created_at.desc()).all()
```

---

## 🔍 API Endpoints

### Create Incident
```bash
curl -X POST http://localhost:8000/incidents \
  -H "Content-Type: application/json" \
  -d '{
    "issue": "[default] test-pod → CrashLoopBackOff",
    "status": "detected",
    "cause": "Container crashes",
    "solution": "Restart pod"
  }'
```

### Get All Incidents
```bash
curl http://localhost:8000/incidents
```

### Get Specific Incident
```bash
curl http://localhost:8000/incidents/{incident_id}
```

---

## ⚙️ Configuration

### Change Database Location
Edit `backend/app/core/database.py`:
```python
DB_DIR = Path("data")  # Change directory
DATABASE_FILE = DB_DIR / "guardian.db"  # Change filename
```

### Enable SQL Query Logging
Edit `backend/app/core/database.py`:
```python
engine = create_engine(
    DATABASE_URL,
    echo=True  # Shows SQL queries in logs
)
```

---

## 🧪 Testing

### Run Database Test
```bash
python test_database.py
```

**Expected Output**:
```
✅ Database initialized
✅ Database file exists
✅ Incident created
✅ Retrieved incidents
✅ Found incident by ID
✅ Incident updated
```

---

## ✅ Best Practices

### ✅ DO
- Always close database sessions
- Use dependency injection in FastAPI
- Handle database errors gracefully
- Use transactions for multiple operations
- Log database operations

### ❌ DON'T
- Leave sessions open
- Ignore database errors
- Use raw SQL (use ORM)
- Store sensitive data unencrypted
- Skip error handling

---

## 🔧 Common Patterns

### Pattern 1: FastAPI Endpoint with Database
```python
@router.get("/incidents")
async def get_incidents(db: Session = Depends(get_db)):
    try:
        incidents = db.query(IncidentDB).all()
        return [db_to_pydantic(i) for i in incidents]
    except Exception as e:
        logger.error(f"Database error: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail="Database error")
```

### Pattern 2: Manual Session Management
```python
db = get_db_session()
try:
    incident = IncidentDB(issue="Test")
    db.add(incident)
    db.commit()
    db.refresh(incident)
    logger.info(f"Incident saved: {incident.id}")
except Exception as e:
    logger.error(f"Failed to save: {e}", exc_info=True)
    db.rollback()
finally:
    db.close()
```

### Pattern 3: Transaction with Multiple Operations
```python
db = get_db_session()
try:
    incident1 = IncidentDB(issue="Issue 1")
    incident2 = IncidentDB(issue="Issue 2")
    db.add(incident1)
    db.add(incident2)
    db.commit()  # Both saved or neither
except Exception as e:
    db.rollback()  # Rollback on error
    logger.error(f"Transaction failed: {e}")
finally:
    db.close()
```

---

## 📖 Example Queries

### Get Recent Incidents
```python
recent = db.query(IncidentDB)\
    .order_by(IncidentDB.created_at.desc())\
    .limit(10)\
    .all()
```

### Count Incidents by Status
```python
count = db.query(IncidentDB)\
    .filter(IncidentDB.status == "detected")\
    .count()
```

### Get Incidents with Actions
```python
with_actions = db.query(IncidentDB)\
    .filter(IncidentDB.action_taken.isnot(None))\
    .all()
```

### Get Incidents from Today
```python
from datetime import datetime, timedelta

today = datetime.now() - timedelta(days=1)
incidents = db.query(IncidentDB)\
    .filter(IncidentDB.created_at >= today)\
    .all()
```

---

## 🎯 Quick Commands

```bash
# Install SQLAlchemy
pip install sqlalchemy

# Test database
python test_database.py

# Start Guardian
cd backend && python -m app.main

# Check database file
ls -lh data/guardian.db

# Query incidents via API
curl http://localhost:8000/incidents

# Create test incident
curl -X POST http://localhost:8000/incidents \
  -H "Content-Type: application/json" \
  -d '{"issue": "Test incident"}'

# View database logs
tail -f logs/guardian.log | grep Database

# SQLite CLI (if installed)
sqlite3 data/guardian.db "SELECT * FROM incidents;"
```

---

## 🔍 Troubleshooting

### Database File Not Created
- Check `data/` directory exists
- Check file permissions
- Check logs for errors: `tail -f logs/guardian.log | grep Database`

### Database Locked Error
- Close all open sessions
- Check for long-running transactions
- Restart Guardian

### Incidents Not Persisting
- Check database initialization logs
- Verify `init_database()` called on startup
- Check for database errors in logs

### Session Errors
- Always close sessions in `finally` block
- Use dependency injection in FastAPI
- Don't reuse closed sessions

---

## 📚 More Information

- **Full Documentation**: `PHASE14_DATABASE_COMPLETE.md`
- **Database Config**: `backend/app/core/database.py`
- **ORM Model**: `backend/app/models/incident_db.py`
- **API Endpoints**: `backend/app/api/incidents.py`
- **Test Script**: `test_database.py`
