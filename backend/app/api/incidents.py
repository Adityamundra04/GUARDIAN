"""
Incident API endpoints for Guardian system.
Handles CRUD operations for Kubernetes incidents.
"""
from fastapi import APIRouter, HTTPException
from typing import List
from backend.app.models.incident import Incident, IncidentCreate

# Create API router
router = APIRouter(prefix="/incidents", tags=["incidents"])

# In-memory database (simple list)
incidents_db: List[Incident] = []


@router.post("/", response_model=Incident, status_code=201)
async def create_incident(incident_data: IncidentCreate) -> Incident:
    """
    Create a new incident.
    
    Args:
        incident_data: Incident creation data (issue, status, cause, solution)
    
    Returns:
        Created incident with auto-generated ID
    """
    # Create incident with auto-generated UUID
    incident = Incident(
        issue=incident_data.issue,
        status=incident_data.status,
        cause=incident_data.cause,
        solution=incident_data.solution
    )
    
    # Store in memory
    incidents_db.append(incident)
    
    return incident


@router.get("/", response_model=List[Incident])
async def get_all_incidents() -> List[Incident]:
    """
    Retrieve all incidents.
    
    Returns:
        List of all incidents in the system
    """
    return incidents_db


@router.get("/{incident_id}", response_model=Incident)
async def get_incident(incident_id: str) -> Incident:
    """
    Retrieve a specific incident by ID.
    
    Args:
        incident_id: UUID of the incident
    
    Returns:
        Incident object if found
    
    Raises:
        HTTPException: 404 if incident not found
    """
    # Search for incident by ID
    for incident in incidents_db:
        if incident.id == incident_id:
            return incident
    
    # Not found
    raise HTTPException(
        status_code=404,
        detail=f"Incident with id '{incident_id}' not found"
    )
