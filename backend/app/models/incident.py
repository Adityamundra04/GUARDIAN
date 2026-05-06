"""
Incident data model for Guardian system.
Represents a Kubernetes incident with tracking information.
"""
from pydantic import BaseModel, Field
from typing import Optional
import uuid


class Incident(BaseModel):
    """
    Incident model representing a Kubernetes issue.
    
    Attributes:
        id: Unique identifier (auto-generated UUID)
        issue: Description of the incident (required)
        status: Current status (default: "detected")
        cause: Root cause analysis (optional)
        solution: Proposed or applied solution (optional)
        action_taken: Action executed for remediation (optional)
        action_status: Status of the action (optional)
    """
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    issue: str
    status: str = "detected"
    cause: Optional[str] = None
    solution: Optional[str] = None
    action_taken: Optional[str] = None
    action_status: Optional[str] = None


class IncidentCreate(BaseModel):
    """
    Schema for creating a new incident.
    Excludes auto-generated fields like id.
    """
    issue: str
    status: Optional[str] = "detected"
    cause: Optional[str] = None
    solution: Optional[str] = None
    action_taken: Optional[str] = None
    action_status: Optional[str] = None
