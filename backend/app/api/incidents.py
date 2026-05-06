"""
Incident API endpoints for Guardian system.
Handles CRUD operations for Kubernetes incidents.
"""
from fastapi import APIRouter, HTTPException, Depends
from typing import List
from sqlalchemy.orm import Session
from backend.app.models.incident import Incident, IncidentCreate
from backend.app.models.incident_db import IncidentDB
from backend.app.core.database import get_db
from backend.app.core.logger import get_logger

# Initialize logger
logger = get_logger("IncidentAPI")

# Create API router
router = APIRouter(prefix="/incidents", tags=["incidents"])


def db_to_pydantic(db_incident: IncidentDB) -> Incident:
    """
    Convert SQLAlchemy model to Pydantic model.
    
    Args:
        db_incident: SQLAlchemy incident object
    
    Returns:
        Pydantic incident object
    """
    return Incident(
        id=db_incident.id,
        issue=db_incident.issue,
        status=db_incident.status,
        cause=db_incident.cause,
        solution=db_incident.solution,
        action_taken=db_incident.action_taken,
        action_status=db_incident.action_status
    )


@router.post("/", response_model=Incident, status_code=201)
async def create_incident(incident_data: IncidentCreate, db: Session = Depends(get_db)) -> Incident:
    """
    Create a new incident.
    
    Args:
        incident_data: Incident creation data (issue, status, cause, solution)
        db: Database session
    
    Returns:
        Created incident with auto-generated ID
    """
    try:
        # Create SQLAlchemy model
        db_incident = IncidentDB(
            issue=incident_data.issue,
            status=incident_data.status,
            cause=incident_data.cause,
            solution=incident_data.solution,
            action_taken=incident_data.action_taken,
            action_status=incident_data.action_status
        )
        
        # Save to database
        db.add(db_incident)
        db.commit()
        db.refresh(db_incident)
        
        logger.info(f"Incident saved to database: {db_incident.id}")
        
        # Convert to Pydantic model for response
        return db_to_pydantic(db_incident)
    
    except Exception as e:
        logger.error(f"Failed to create incident: {e}", exc_info=True)
        db.rollback()
        raise HTTPException(status_code=500, detail="Failed to create incident")


@router.get("/", response_model=List[Incident])
async def get_all_incidents(db: Session = Depends(get_db)) -> List[Incident]:
    """
    Retrieve all incidents.
    
    Args:
        db: Database session
    
    Returns:
        List of all incidents in the system
    """
    try:
        # Query all incidents from database
        db_incidents = db.query(IncidentDB).order_by(IncidentDB.created_at.desc()).all()
        
        logger.info(f"Retrieved {len(db_incidents)} incidents from database")
        
        # Convert to Pydantic models
        return [db_to_pydantic(incident) for incident in db_incidents]
    
    except Exception as e:
        logger.error(f"Failed to retrieve incidents: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail="Failed to retrieve incidents")


@router.get("/{incident_id}", response_model=Incident)
async def get_incident(incident_id: str, db: Session = Depends(get_db)) -> Incident:
    """
    Retrieve a specific incident by ID.
    
    Args:
        incident_id: UUID of the incident
        db: Database session
    
    Returns:
        Incident object if found
    
    Raises:
        HTTPException: 404 if incident not found
    """
    try:
        # Query incident by ID
        db_incident = db.query(IncidentDB).filter(IncidentDB.id == incident_id).first()
        
        if not db_incident:
            logger.warning(f"Incident not found: {incident_id}")
            raise HTTPException(
                status_code=404,
                detail=f"Incident with id '{incident_id}' not found"
            )
        
        logger.info(f"Retrieved incident: {incident_id}")
        
        # Convert to Pydantic model
        return db_to_pydantic(db_incident)
    
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Failed to retrieve incident {incident_id}: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail="Failed to retrieve incident")
