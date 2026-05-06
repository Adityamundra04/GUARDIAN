"""
Test script to verify Guardian database functionality.
Tests SQLite database creation, incident storage, and retrieval.
"""
import sys
import os
from pathlib import Path

# Add backend to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'backend'))

from backend.app.core.database import init_database, get_db_session, DATABASE_FILE
from backend.app.models.incident_db import IncidentDB
from backend.app.models.incident import Incident


def test_database():
    """Test the database functionality."""
    print("=" * 60)
    print("Guardian Database Test")
    print("=" * 60)
    
    # Initialize database
    print("\n1. Initializing database...")
    try:
        init_database()
        print(f"✅ Database initialized: {DATABASE_FILE}")
    except Exception as e:
        print(f"❌ Failed to initialize database: {e}")
        return
    
    # Check database file exists
    print("\n2. Checking database file...")
    if DATABASE_FILE.exists():
        size = DATABASE_FILE.stat().st_size
        print(f"✅ Database file exists: {DATABASE_FILE.absolute()} ({size} bytes)")
    else:
        print(f"❌ Database file not found: {DATABASE_FILE.absolute()}")
        return
    
    # Test creating an incident
    print("\n3. Testing incident creation...")
    db = get_db_session()
    try:
        test_incident = IncidentDB(
            issue="[default] test-pod → CrashLoopBackOff",
            status="detected",
            cause="Test cause",
            solution="Test solution",
            action_taken="restart_pod",
            action_status="success"
        )
        
        db.add(test_incident)
        db.commit()
        db.refresh(test_incident)
        
        print(f"✅ Incident created: {test_incident.id}")
        print(f"   Issue: {test_incident.issue}")
        print(f"   Status: {test_incident.status}")
        print(f"   Created: {test_incident.created_at}")
        
    except Exception as e:
        print(f"❌ Failed to create incident: {e}")
        db.rollback()
        return
    finally:
        db.close()
    
    # Test retrieving incidents
    print("\n4. Testing incident retrieval...")
    db = get_db_session()
    try:
        incidents = db.query(IncidentDB).all()
        print(f"✅ Retrieved {len(incidents)} incident(s) from database")
        
        for incident in incidents:
            print(f"   - {incident.id}: {incident.issue[:50]}...")
        
    except Exception as e:
        print(f"❌ Failed to retrieve incidents: {e}")
        return
    finally:
        db.close()
    
    # Test querying by ID
    print("\n5. Testing incident query by ID...")
    db = get_db_session()
    try:
        incident = db.query(IncidentDB).filter(IncidentDB.id == test_incident.id).first()
        
        if incident:
            print(f"✅ Found incident: {incident.id}")
            print(f"   Issue: {incident.issue}")
            print(f"   Cause: {incident.cause}")
            print(f"   Solution: {incident.solution}")
        else:
            print(f"❌ Incident not found: {test_incident.id}")
        
    except Exception as e:
        print(f"❌ Failed to query incident: {e}")
        return
    finally:
        db.close()
    
    # Test updating an incident
    print("\n6. Testing incident update...")
    db = get_db_session()
    try:
        incident = db.query(IncidentDB).filter(IncidentDB.id == test_incident.id).first()
        
        if incident:
            incident.status = "resolved"
            incident.action_status = "completed"
            db.commit()
            
            print(f"✅ Incident updated: {incident.id}")
            print(f"   New status: {incident.status}")
            print(f"   New action status: {incident.action_status}")
        else:
            print(f"❌ Incident not found for update")
        
    except Exception as e:
        print(f"❌ Failed to update incident: {e}")
        db.rollback()
        return
    finally:
        db.close()
    
    print("\n" + "=" * 60)
    print("Database Test Complete!")
    print("=" * 60)
    print("\nNext steps:")
    print("1. Install SQLAlchemy: pip install sqlalchemy")
    print("2. Start Guardian: cd backend && python -m app.main")
    print("3. Check database: ls -lh data/guardian.db")
    print("4. Query incidents: GET http://localhost:8000/incidents")


if __name__ == "__main__":
    test_database()
